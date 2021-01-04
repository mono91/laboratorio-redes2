import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSBridge
from mininet.nodelib import LinuxBridge
from sys import argv

#En la ejecuccion del script se debe agregar un parametro adicional: count
script, count = argv
class CustomTopo(Topo):
	def __init__(self,**opts):
		Topo.__init__(self, **opts)
		switches = []
       		hosts = []
       		for i in range(0,int(count)):
        	       	switch=self.addSwitch('S%d'%i,cls=OVSBridge,stp=True)
               		switches.append(switch)
               		host=self.addHost('h%d'%i)
               		hosts.append(host)
			self.addLink(switches[i],hosts[i])
		for j in range(0, int(count)):
			if j != int(count): #Ya que no hay ningun enlace pendiente
				for k in range(j+1,int(count)):
					self.addLink(switches[j],switches[k])

def runNet():
	topo=CustomTopo()
	net = Mininet(topo)
	net.start()
	net.pingAll()
	time.sleep(30)
	net.pingAll()
	time.sleep(30)
	net.pingAll()
	return topo

if __name__ == '__main__':
	setLogLevel('info')
	runNet()
