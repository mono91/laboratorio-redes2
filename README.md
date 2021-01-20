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
iperf  -c 10.0.0.5 -u -p 200
Desde una consola que pertenezca a un servidor:
iperf -s -u -p 200
ó 
Desde una consola que pertenezca a un host:
iperf -c 10.0.0.6 -p 80
Desde una consola que pertenezca a  un servidor:
iperf -s -p 80


....
Autor:
Jhonatan Marin
UdeA
