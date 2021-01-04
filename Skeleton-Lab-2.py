from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import csv

log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Activando el firewall")

    def _handle_ConnectionUp (self, event):
	with open('firewall-policies.csv') as csvfile:
		reader = csv.DictReader(csvfile) # Se carga el archivo
		for row in reader: # Se instala regla para cada un de los pares de MAC
			MAC_origen_negar = EthAddr(row['mac_0'])
			MAC_destino_negar = EthAddr(row['mac_1'])	
			coincidencia = of.ofp_match()
			coincidencia.dl_src = MAC_origen_negar
			coincidencia.dl_dst = MAC_destino_negar
			mensaje = of.ofp_flow_mod()	
			mensaje.match = coincidencia
			accion = of.ofp_action_output(port = of.OFPP_NONE)
			mensaje.actions.append(accion) 
			event.connection.send(mensaje)	        
	log.debug("Reglas instaladas en %s", dpidToStr(event.dpid))

def launch ():

    core.registerNew(Firewall)
