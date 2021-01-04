Para la ejecuccion  del codigo se debe de realizar el siguiente proceso
Desde una  consola  que pertenezca a un host:
iperf  -c 10.0.0.5 -u -p 200
Desde una consola que pertenezca a un servidor:
iperf -s -u -p 200
ó 
Desde una consola que pertenezca a un host:
iperf -c 10.0.0.6 -p 80
y desde una consola que pertenezca a un servidor
iperf -s -p 80
