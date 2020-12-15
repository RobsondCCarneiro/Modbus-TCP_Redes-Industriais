from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep	
from random import uniform

#Criando uma instancia de ModbusServer
server = ModbusServer ("127.0.0.1", 502, no_block=True)

try:
	print("INICIANDO O SERVIDOR...")
	server.start()
	print("SERVIDOR ESTA ONLINE")
	while True:
		DataBank.set_words(0, [int(uniform(0,100))])
		sleep(0.5)

except:
	print("FECHANDO O SERVIDOR")
	server.stop()
	print("SERVIDOR ESTA OFFLINE")

