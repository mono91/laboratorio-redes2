Lab 1
sudo python Skeleton-Lab-1.py 8

Lab 2
Ejecutar la aplicacion POX:
./pox/pox.py forwarding.l2_learning misc.Skeleton-Lab-2
Ejecutar la topologia:
sudo mn --topo single,8 --mac --switch ovsk --controller remote,port=6633

Lab 3
Ejecutar la aplicación POX:  
./pox/pox.py log.level --DEBUG misc.Skeleton-Lab3
Ejecutar la topología: 
sudo python Topo.py

Lab 4
Ejecutar la aplicacion POX:
./pox/pox.py log.level --DEBUG pox.openflow.discovery misc.Skeleton-Lab4
Ejecutar la topología:
sudo mn --custom Topo2.py --topo simpletopo --controller remote,port=6633 --link tc --arp



Para la ejecuccion  del Skeleton-Lab3.py seguir los siguientes pasos:
Desde una  consola  que pertenezca a un host:
iperf  -c 10.0.0.5 -u -p 200 -b 100MB 
Desde una consola que pertenezca a un servidor
iperf -s -u -p 200
ó 
Desde una consola que pertenezca a un host:
iperf -c 10.0.0.6 -p 80
Desde una consola que pertenezca a  un servidor:
iperf -s -p 80

NOTA: si se va a  ejecutar la v2 (version 2) de la practica 3 se debe de agregar net.staticArp()
 en la topologia  Topo.py despues de la linea 96 para que la topologia se inicie con las  resoluciones arp ya hechas, esta solucion se diferencia de la otra en que en esta se inicia la topologia con las tablas arp llenas, mientras que en la primera version esto no sucedia por lo tanto se debia resolver las macs de los servidores dentro del algoritmo

