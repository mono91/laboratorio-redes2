#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementación sencilla de Dijkstra en POX
Utilizando la aplicación discovery se abstrae la topología
y se construye
"""


from pox.core import core  
import pox.openflow.libopenflow_01 as of  
from pox.lib.revent import *  
from pox.lib.recoco import Timer  
from collections import defaultdict, namedtuple  
from pox.openflow.discovery import Discovery
from pox.forwarding.topo_proactive import TopoSwitch  
from pox.lib.util import dpid_to_str  
import time
from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import random
import pox.openflow.discovery
import pox.openflow.spanning_tree
from pox.lib.packet.arp import arp
from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.packet_base import packet_base
from pox.lib.packet.packet_utils import *
import pox.lib.packet as pkt
from pox.lib.recoco import Timer


 

log = core.getLogger()





def dijkstra (neighbor, node, N):
    costs = {}
    min_dist = 9999999
    pred={}
    paths={}
    vis_nodes = []
    
   
    
    for i in range(1,N+1):
        if i in neighbor[node]:
            costs[i] = neighbor[node][i]
        else:
            costs[i] = 9999
            

    vis_nodes = list(neighbor.keys())
    vis_nodes.remove(node)
    
    
    for i in neighbor.keys():
        if not neighbor[i]:
            vis_nodes.remove(i)
    
    
    del costs[node]

    
    for i in vis_nodes:
        paths[i]=[i]
        pred[i] = i
        p = []

    while vis_nodes:
        for item in vis_nodes:

            if costs[item] < min_dist:
                min_dist = costs[item]
                closest_node = item 
                
                
        for item in vis_nodes:
            if item in neighbor[closest_node]:
                if neighbor[closest_node][item] + costs[closest_node] < costs[item]:
                    cn = []
                    costs[item] = neighbor[closest_node][item] + costs[closest_node]
                    pred[item] = closest_node
                    cn.append(closest_node)
                    p = p + cn
                    paths[item]=cn+paths[item]
        vis_nodes.remove(closest_node)
        min_dist = 99999   
        
    for key in pred:
        if pred[key] == key:
            paths[key] = []
            paths[key].append(pred[key])
        else:
            paths[key] = []
            n2 = key
            paths[key].append(key)
            while n2 != pred[n2]:
                n2 = pred[n2]
                paths[key].insert(0,n2)


    return paths



class topoDiscovery(EventMixin):

    
    def __init__(self):
        def startup():
            core.openflow.addListeners(self, priority = 0)
            core.openflow_discovery.addListeners(self)
        core.call_when_ready(startup, ('openflow','openflow_discovery'))
        print ('init over')
        self.graph = {} 
        self.neigh = {}
        self.edges = []
        self.edges2 = []
        self.sw = []
        self.tree = []
        self.neigh_cost = {}
        self.rules = {}
        self.tree_org = []
        self.sw_con = []
        self.paths = {}

        
    def _handle_LinkEvent(self, event):
        l = event.link
        sw1 = l.dpid1
        sw2 = l.dpid2
        pt1 = l.port1
        pt2 = l.port2
        e = [sw1,sw2]
        e2 = [sw2,sw1]
        link = (sw2,pt1)
	log.debug(str(sw1))
	log.debug(str(sw2))
        dpid = '00-00-00-00-00-0'+str(sw1)
        self.sw_con.append(event)

     
        
        if event.added == True:
            self.edges.append(e)
            for i in range(len(self.edges)):
                self.edges[i] = sorted(self.edges[i])

            
            for num in self.edges: 
                if num not in self.edges2: 
                    self.edges2.append(num)
            
            
            link = (sw2,pt1)
            if sw1 in self.graph.keys():
                
                self.graph[sw1].append(link)
    
            else:
                self.graph[sw1]=[]
                self.graph[sw1].append(link)
            
            for key in self.graph:
                self.neigh[key] = []
                for i in range(len(self.graph[key])):
                    self.neigh[key].append(self.graph[key][i][0]) #Cada llave de este dict son los vecinos en una lista

    
                
        elif event.removed == True:
            print('LINK_DOWN')
            if e in self.edges:
                self.edges.remove(e)
            elif e2 in self.edges:
                self.edges.remove(e2)
                
            if e in self.edges2:
                self.edges2.remove(e)
            elif e2 in self.edges2:
                self.edges2.remove(e2)
            self.graph[sw1].remove(link)
            
            if sw1 in self.neigh[sw2]:
                self.neigh[sw2].remove(sw1)
                
            
            if sw2 in self.neigh[sw1]:
                self.neigh[sw1].remove(sw2)
                
                
        self.neigh_cost_pre = {1: {2: 10, 4: 1, 6: 100}, 2: {1: 10, 3: 10}, 
                           3: {2: 10, 6: 10}, 4: {1: 1, 5: 1}, 5: {4: 1, 6: 1}, 
                           6: {1: 100, 3: 10, 5: 1}}
        
        for key in self.neigh:
            self.neigh_cost[key] = {}
            for i in range(0,len(self.neigh[key])):
                self.neigh_cost[key][self.neigh[key][i]] = self.neigh_cost_pre[key][self.neigh[key][i]]

        
        for key in self.graph:
            print ('-----switch%d se conecta con:----- ' %key)
            for i in range(len(self.graph[key])):
                print ('switch%d en el puerto%d ' %(self.graph[key][i][0], self.graph[key][i][1]))


        if not list(self.neigh.keys()):
            NN = 1
            N = 1
        else:
            NN = list(self.neigh.keys())
            N = max(NN)

        for node in NN:
            
            self.paths[node] = []
            if node in self.neigh_cost.keys() and N > 1:
                if not self.neigh_cost[node]:
                    print('El SW%d no tiene vecinos' %node)
                else:
                    self.paths[node] = dijkstra(self.neigh_cost,node,N)

            else:
                print('El SW%d no ha enviado su estado o ha sido aislado' %node)
        
        if not self.paths:
            print('Sin rutas')
        else:
	    log.debug(self.paths)
	    for paths, ps in self.paths.iteritems():
		print('Switch: ',paths)
		print('Caminos: ',ps)
		for path, p in ps.iteritems():
		    print('Camino de ',paths,'a ',path,': ',p)
		    actual = paths
		    for ssalto in p:
			log.debug(ssalto)
			#i=1
			for connection in core.openflow.connections:
			    if '00-00-00-00-00-0'+str(actual) == dpidToStr(connection.dpid):
				for grafo,g in self.graph.iteritems():
				    if grafo == actual:
	       			       for t in g:
					   if t[0] == ssalto:
					      outport = t[1]
					      actual = ssalto	 
			   	              mensaje = of.ofp_flow_mod()
					      coincidencia = of.ofp_match()
					      coincidencia.dl_src = EthAddr('00:00:00:00:00:0'+str(paths))
				              coincidencia.dl_dst = EthAddr('00:00:00:00:00:0'+str(path))
					      mensaje.match = coincidencia
				  	      accion = of.ofp_action_output(port = outport)
					      mensaje.actions.append(accion)
					      connection.send(mensaje)		
	    
	    i = 1	
	    for connection in core.openflow.connections:
		 mensaje = of.ofp_flow_mod()
                 coincidencia = of.ofp_match()
                 coincidencia.dl_dst = EthAddr('00:00:00:00:00:0'+str(i))
                 mensaje.match = coincidencia
                 accion = of.ofp_action_output(port = 1)
                 mensaje.actions.append(accion)
                 connection.send(mensaje)
		 i=i+1

		
	
            '''
		Se sugiere crear una estructura donde se guarden las reglas al
		recorrer el archivo de paths '''
            for connection in core.openflow.connections:
		log.debug(connection)
        


        if not self.rules:
            print('Sin reglas')
        else:
            '''Adicione su lógica para crear los mensajes acá'''

            


def launch():  
    core.registerNew(topoDiscovery)

 


