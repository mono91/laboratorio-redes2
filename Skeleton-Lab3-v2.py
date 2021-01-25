from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr

from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

import pox.lib.packet as pkt
import time

log = core.getLogger()

class CustomSlice (EventMixin):
	def __init__(self):
		self.listenTo(core.openflow)
		core.openflow_discovery.addListeners(self)

		# Adjacency map.  [sw1][sw2] -> port from sw1 to sw2
		self.adjacency = defaultdict(lambda:defaultdict(lambda:None))

		self.portmap = { 
                         ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:01'),EthAddr('00:00:00:00:00:05'),200): '00-00-00-00-00-04',
		         ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:01'),EthAddr('00:00:00:00:00:05'),200): '00-00-00-00-00-07',
			 
			 ('00-00-00-00-00-02', EthAddr('00:00:00:00:00:02'),EthAddr('00:00:00:00:00:05'),200): '00-00-00-00-00-01',
			 ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:02'),EthAddr('00:00:00:00:00:05'),200): '00-00-00-00-00-04',
			 ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:02'),EthAddr('00:00:00:00:00:05'),200): '00-00-00-00-00-07',

			 ('00-00-00-00-00-02', EthAddr('00:00:00:00:00:02'),EthAddr('00:00:00:00:00:06'), 80): '00-00-00-00-00-05',
		   	 ('00-00-00-00-00-05', EthAddr('00:00:00:00:00:02'),EthAddr('00:00:00:00:00:06'), 80): '00-00-00-00-00-07',

			 ('00-00-00-00-00-03', EthAddr('00:00:00:00:00:03'),EthAddr('00:00:00:00:00:06'), 80): '00-00-00-00-00-06',
			 ('00-00-00-00-00-06', EthAddr('00:00:00:00:00:03'),EthAddr('00:00:00:00:00:06'), 80): '00-00-00-00-00-07',
			 ('00-00-00-00-00-03', EthAddr('00:00:00:00:00:04'),EthAddr('00:00:00:00:00:06'), 80): '00-00-00-00-00-06',
			 ('00-00-00-00-00-06', EthAddr('00:00:00:00:00:04'),EthAddr('00:00:00:00:00:06'), 80): '00-00-00-00-00-07',

 		       	 ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:05'),EthAddr('00:00:00:00:00:01'),200): '00-00-00-00-00-01',
                         ('00-00-00-00-00-07', EthAddr('00:00:00:00:00:05'),EthAddr('00:00:00:00:00:01'),200): '00-00-00-00-00-04',

                         ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:05'),EthAddr('00:00:00:00:00:02'),200): '00-00-00-00-00-02',
                         ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:05'),EthAddr('00:00:00:00:00:02'),200): '00-00-00-00-00-01',
                         ('00-00-00-00-00-07', EthAddr('00:00:00:00:00:05'),EthAddr('00:00:00:00:00:02'),200): '00-00-00-00-00-04',

                         ('00-00-00-00-00-05', EthAddr('00:00:00:00:00:06'),EthAddr('00:00:00:00:00:02'), 80): '00-00-00-00-00-02',
                         ('00-00-00-00-00-07', EthAddr('00:00:00:00:00:06'),EthAddr('00:00:00:00:00:02'), 80): '00-00-00-00-00-05',

                         ('00-00-00-00-00-06', EthAddr('00:00:00:00:00:06'),EthAddr('00:00:00:00:00:03'), 80): '00-00-00-00-00-03',
                         ('00-00-00-00-00-07', EthAddr('00:00:00:00:00:06'),EthAddr('00:00:00:00:00:03'), 80): '00-00-00-00-00-06',
                         ('00-00-00-00-00-06', EthAddr('00:00:00:00:00:06'),EthAddr('00:00:00:00:00:04'), 80): '00-00-00-00-00-03',
                         ('00-00-00-00-00-07', EthAddr('00:00:00:00:00:06'),EthAddr('00:00:00:00:00:04'), 80): '00-00-00-00-00-06'
				}

	def _handle_ConnectionUp(self, event):
		dpid = dpidToStr(event.dpid)
		log.debug("Switch %s se ha conectado...", dpid)


		if dpid == '00-00-00-00-00-01':
                        mensaje = of.ofp_flow_mod()
                        mensaje.match = of.ofp_match()
                        mensaje.match.dl_dst = EthAddr('00:00:00:00:00:01')
                        accion = of.ofp_action_output(port = 1)
                        mensaje.actions.append(accion)
                        event.connection.send(mensaje)
                        log.debug('Se instalo regla para envio paquete de s1 a h1')

                elif dpid == '00-00-00-00-00-02':
                        mensaje = of.ofp_flow_mod()
                        mensaje.match = of.ofp_match()
                        mensaje.match.dl_dst = EthAddr('00:00:00:00:00:02')
                        accion = of.ofp_action_output(port = 2)
                        mensaje.actions.append(accion)
                        event.connection.send(mensaje)
                        log.debug('Se instalo regla para envio de paquete de s2 a h2')

                elif dpid == '00-00-00-00-00-03':
                        mensaje = of.ofp_flow_mod()
                        mensaje.match = of.ofp_match()
                        mensaje.match.dl_dst = EthAddr('00:00:00:00:00:03')
                        accion = of.ofp_action_output(port = 2)
                        mensaje.actions.append(accion)
                        event.connection.send(mensaje)
                        log.debug('Se instalo regla para envio de paquete de s3 a h3')
                        mensaje = of.ofp_flow_mod()
                        mensaje.match = of.ofp_match()
                        mensaje.match.dl_dst = EthAddr('00:00:00:00:00:04')
                        accion = of.ofp_action_output(port = 3)
                        mensaje.actions.append(accion)
                        event.connection.send(mensaje)
                        log.debug('Se instalo regla para envio de paquete de s3 a h4')

		elif dpid == '00-00-00-00-00-07':
                        mensaje = of.ofp_flow_mod()
                        mensaje.match = of.ofp_match()
                        mensaje.match.dl_dst = EthAddr('00:00:00:00:00:05')
                        accion = of.ofp_action_output(port = 4)
                        mensaje.actions.append(accion)
                        event.connection.send(mensaje)
                        log.debug('Se instalo regla para envio de paquete de s7 a serv1')
                        mensaje = of.ofp_flow_mod()
                        mensaje.match = of.ofp_match()
                        mensaje.match.dl_dst = EthAddr('00:00:00:00:00:06')
                        accion = of.ofp_action_output(port = 5)
                        mensaje.actions.append(accion)
                        event.connection.send(mensaje)
                        log.debug('Se instalo regla para envio de paquete de s7 a serv2')
			

	def _handle_LinkEvent (self, event):
		l = event.link
		sw1 = dpid_to_str(l.dpid1)
		sw2 = dpid_to_str(l.dpid2)
		log.debug ("link %s[%d] <-> %s[%d]",
			sw1, l.port1,
			sw2, l.port2)
		self.adjacency[sw1][sw2] = l.port1
		self.adjacency[sw2][sw1] = l.port2
              				

	def _handle_PacketIn (self, event):
		"""
		Handle packet in messages from the switch to implement above algorithm.
		"""
		packet = event.parsed
		#log.debug("Ha llegado un paquete de tipo %s al controlador.", pkt.ETHERNET.ethernet.getNameForType(packet.type))
		
		# flood, but don't install the rule
		def flood (message = None):
			""" Floods the packet """
			msg = of.ofp_packet_out()
			msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
			msg.data = event.ofp
			msg.in_port = event.port
			event.connection.send(msg)

		def install_fwdrule(event,packet,outport):
			msg = of.ofp_flow_mod()
			#msg.priority =  10
			#msg.idle_timeout = 10
			#msg.hard_timeout = 30
			msg.match.dl_src = EthAddr(packet.src)
			msg.match.dl_dst = EthAddr(packet.dst)
			#msg.match = of.ofp_match.from_packet(packet, event.port)
			msg.actions.append(of.ofp_action_output(port = outport))
			#msg.data = event.ofp
			#msg.in_port = event.port
			event.connection.send(msg)
			#print(msg)
			#log.debug("Se instalo regla")
			#time.sleep(15)

                  	
		def forward (message = None):
            		this_dpid = dpid_to_str(event.dpid)

            		if packet.dst.is_multicast:
                		flood()
                		return
           		else:
                		log.debug("Got unicast packet for %s at %s (input port %d):", packet.dst, dpid_to_str(event.dpid), event.port)

                	try:

				""" Adicione su logica aca"""
				#Se valida el puerto de destino
				if event.parsed.find('tcp'):
					port_dest = 80
				elif event.parsed.find('udp'):
					port_dest = 200
					
				#MAC's
				src_mac = EthAddr(packet.src)
				dst_mac = EthAddr(packet.dst)

				#log.debug(this_dpid)
				#log.debug(src_mac)
				#log.debug(dst_mac)
				#log.debug(event.parsed.find('tcp'))
				#log.debug(event.parsed.find('udp'))			

				#Se define un puerto cuando el paquete es un paquete de tipo ARP reply
				#if packet.type == packet.ARP_TYPE:
                		#	if dst_mac == EthAddr('00:00:00:00:00:01') : port_dest = 200
                        	#	elif src_mac == EthAddr('00:00:00:00:00:05') and dst_mac == EthAddr('00:00:00:00:00:02') : port_dest = 200
                        	#	elif src_mac == EthAddr('00:00:00:00:00:06') and dst_mac == EthAddr('00:00:00:00:00:02') : port_dest = 80
                        	#	elif dst_mac == EthAddr('00:00:00:00:00:03') or dst_mac == EthAddr('00:00:00:00:00:04'): port_dest = 80

				#print(pkt.ETHERNET.ethernet.getNameForType(packet.type),  this_dpid, src_mac, dst_mac, port_dest)
				#Acorde al dpid origen, mac origen, mac destino y puerto destino se valida el dpid del switch destino y el puerto de salida para llegar a ese switch destino.
                		if (this_dpid, src_mac, dst_mac, port_dest) in self.portmap:     	                	
					dpid2 = self.portmap[(this_dpid, src_mac, dst_mac, port_dest)]
                                	port_out = self.adjacency[this_dpid][dpid2]
					#log.debug("Se instalara regla en el switch %s  para enviar paquete a traves del puerto %s", dpid2, port_out)
                                	install_fwdrule(event,packet,port_out) 
				
                	except AttributeError:
                    		log.debug("packet type has no transport ports, flooding")

                    	# flood and install the flow table entry for the flood
                    	#install_fwdrule(event,packet,of.OFPP_FLOOD)

		forward()

def launch():
	# Ejecute spanning tree para evitar problemas con topologias con bucles
	pox.openflow.discovery.launch()
	pox.openflow.spanning_tree.launch()

	core.registerNew(CustomSlice)

