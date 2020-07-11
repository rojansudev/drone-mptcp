#!/usr/bin/python

"""MPTCP Demo"""

from mininet.log import setLogLevel, info
from mininet.node import Controller
from mininet.link import TCLink
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI_wifi


def topology():

    """
          *ap1 .     
         *      .    
    sta1*         h10
        *        .    
         *     .      
          *ap2        
    """
 

    "Create a network."
    net = Mininet_wifi(controller=Controller,link=TCLink)

    info("*** Creating nodes\n")
    sta1 = net.addStation(
        'sta1', wlans=2, ip='10.0.0.10/8',min_x=79,max_x=121,min_y=60,max_y=80,min_v=5,max_v=7)
    ap1 = net.addAccessPoint(
        'ap1', mac='00:00:00:00:00:01', equipmentModel='TLWR740N',
        protocols='OpenFlow10', ssid= 'ssid_ap2', mode= 'g',
        channel= '6', position='80,70,0',range=80 )
    ap2 = net.addAccessPoint(
        'ap2', mac='00:00:00:00:00:02', equipmentModel='TLWR740N',
        protocols='OpenFlow10', ssid= 'ssid_ap3', mode= 'n',
        channel= '1', position='120,70,0',range=80 )
    h10 = net.addHost( 'h10', mac='00:00:00:00:00:10', ip='10.0.0.254/8' )
    c11 = net.addController( 'c11')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.addLink(ap1, sta1)
    net.addLink(ap2, sta1)
    net.addLink(h10, ap1)
    net.addLink(h10, ap2)
    

    h10.cmd('ifconfig h10-eth1 192.168.0.254/24')

    sta1.cmd('ifconfig sta1-wlan0 10.0.0.10/8')
    sta1.cmd('ifconfig sta1-wlan1 192.168.0.10/24')

    
    sta1.cmd('ip rule add from 10.0.0.10 table 1')
    sta1.cmd('ip rule add from 192.168.0.10 table 2')

    sta1.cmd('ip route add 10.0.0.0/8 dev sta1-wlan0 scope link table 1')
    sta1.cmd('ip route add default via 10.0.0.254 dev sta1-wlan0 table 1')

    sta1.cmd('ip route add 192.168.0.0/24 dev sta1-wlan1 scope link table 2')
    sta1.cmd('ip route add default via 192.168.0.254 dev sta1-wlan1 table 2')

    sta1.cmd('ip route add default scope global nexthop via 10.0.0.254 dev sta1-wlan0')

    
    h10.cmd('sudo ip rule add from 10.0.0.254 table 1')
    h10.cmd('sudo ip rule add from 192.168.0.254 table 2')
    h10.cmd('sudo ip route add 10.0.0.0/8 dev h10-eth0 scope link table 1')
    h10.cmd('sudo ip route add default via 10.0.0.10 dev h10-eth0 table 1')
    h10.cmd('sudo ip route add 192.168.0.0/24 dev h10-eth1 scope link table 2')
    h10.cmd('sudo ip route add default via 192.168.0.10 dev h10-eth1 table 2')
    
        
    info("*** Starting network\n")
    
    #mobility model
    net.plotGraph(max_x=180, max_y=180 )
    net.startMobility(time=0, model='RandomDirection',AC='ssf')
    
   
    net.build()
    c11.start()
    ap1.start( [c11] )
    ap2.start( [c11] )

    CLI_wifi( net )

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
