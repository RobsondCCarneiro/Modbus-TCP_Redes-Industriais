from pyModbusTCP.client import ModbusClient
import time

#TCP auto connect on first Modbus Request
c = ModbusClient(host="localhost", port=502, auto_open=True)

#TCP auto connect on Modbus Request, close after it
c = ModbusClient(host="127.0.0.1", auto_open=True, auto_close=True)
c = ModbusClient()
c.host("localhost")
c.port(502)

#O contador serve para saber o nivel do tanque
cont = 0

#setando registradores para serem usados no ScadaBR
LED = c.write_single_register(1,0)
tanque = c.write_single_register(2,0)
valvula = c.write_single_register(3,0)
alarme = c.write_single_register(4,0)

while True:
	# gerenciando sessoes TCP com chamadas para c.open()/c.close()
	c.open()
	led = c.read_holding_registers(1)
	tanque_valor = c.read_holding_registers(2)
	valvula = c.read_holding_registers(3)
	alarme = c.read_holding_registers(4)

	#verificando se o LED esta ligado e a valvula fechada para encher o tanque
	if(valvula[0] == 0 and led[0] == 1):
		cont=cont+1 #subindo o nivel do tanque
	c.write_single_register(2,cont) 
	tanque_valor = c.read_holding_registers(2)

	#verificando se o tanque igual ou maior que o nivel 8 para soar o alarme
	if tanque_valor[0] >= 8:
		c.write_single_register(4,1)
	else:
		c.write_single_register(4,0)

	#verificando se o valor do tanque chegou ao limite
	if tanque_valor[0]==10:
		c.write_single_register(1,0) #desligou o LED
		c.write_single_register(3,1) #abriu a valvula

	if (led[0] == 0 and valvula[0] == 1):
		cont=cont-1
		c.write_single_register(2,cont)
		tanque_valor = c.read_holding_registers(2) #lendo o valor do tanque
		if tanque_valor[0]==0:
			c.write_single_register(3,0) #fechou a valvula



	if led:
		print("valor do LED: ")
		print(led)
		print("valor do tanque: ")
		print(tanque_valor)
		print("valor da valvula")
		print(valvula)
		print("valor do alarme")
		print(alarme)
	else:
		print("read error")
	time.sleep(2)