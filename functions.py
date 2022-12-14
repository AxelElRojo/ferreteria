import pandas, sqlalchemy, matplotlib
from db import db
from gui import gui
import matplotlib.pyplot as plt
def fn1():
	global db
	indice = 0
	dic = {}
	moda = db.execute("SELECT * FROM productopedido")['CodigoProducto'].mode().tolist()[0]
	producto = db.execute("SELECT YEAR(pedido.Fecha) AS año, COUNT(pedido.Codigo) AS cuenta FROM productopedido JOIN pedido ON productopedido.CodigoPedido = pedido.Codigo WHERE productopedido.CodigoProducto = {} GROUP BY YEAR(pedido.Fecha)".format(moda)).to_dict()
	for i in producto["año"].keys():
		indice += 1
		dic[producto["año"][i]]=producto["cuenta"][i]
		gui.listbox.insert(indice, "%s --- (%s)" % (producto["año"][i], producto["cuenta"][i]))
	plt.bar(dic.keys(), dic.values())
	plt.xlabel("Año")
	plt.ylabel("Ventas")
	plt.title("Gráfica Producto")
	plt.show()
def fn2():
	global db
	indice = 0
	dic = {}
	montos = db.execute("SELECT MONTHNAME(Fecha) AS mes, SUM(Monto) AS suma FROM pedido WHERE Fecha BETWEEN '2022-08-01' AND '2022-11-31'")
	for i in montos["mes"].keys():
		indice += 1
		dic[montos["mes"][i]] = montos["suma"][i]
		gui.listbox.insert(indice, "%s --- (%s)" % (montos["mes"][i], montos["suma"][i]))
	plt.bar(dic.keys(), dic.values())
	plt.xlabel("Mes")
	plt.ylabel("Monto")
	plt.title("Gráfica Montos")
	plt.show()
def fn3():
	global db, gui
	moda = db.execute("SELECT * FROM productopedido")['CodigoProducto'].mode().tolist()[0]
	clientes = db.execute("SELECT cliente.Nombre AS nombreCliente FROM productopedido JOIN pedido ON productopedido.CodigoPedido = pedido.Codigo JOIN cliente ON cliente.Codigo = pedido.CodigoCliente WHERE CodigoProducto={}".format(moda))['nombreCliente'].unique().tolist()
	for i in range(len(clientes)):
		gui.listbox.insert(i, clientes[i])
def fn4():
	global db
	indice = 0
	dic = {}
	empleados = db.execute("SELECT empleado.Nombre AS nombreEmpleado, COUNT(pedido.CodigoEmpleado) AS cuenta FROM pedido JOIN empleado ON pedido.CodigoEmpleado = empleado.Codigo GROUP BY CodigoEmpleado LIMIT 5").to_dict()
	for i in empleados["nombreEmpleado"].keys():
		indice += 1
		dic[empleados["nombreEmpleado"][i]] = empleados["cuenta"][i]
		gui.listbox.insert(indice, "%s --- (%s)" % (empleados["nombreEmpleado"][i], empleados["cuenta"][i]))
	plt.bar(dic.keys(), dic.values())
	plt.xlabel("Empleado")
	plt.xticks(rotation=20)
	plt.ylabel("Ventas")
	plt.title("Gráfica Empleados")
	plt.show()
def fn5():
	global db, gui
	clientes = db.execute("SELECT cliente.Nombre AS nombre, COUNT(productopedido.CodigoPedido) AS cuenta FROM productopedido JOIN pedido ON productopedido.CodigoPedido = pedido.Codigo JOIN cliente ON cliente.Codigo = pedido.CodigoCliente GROUP BY pedido.CodigoCliente LIMIT 5").to_dict()
	for i in clientes['nombre'].keys():
		gui.listbox.insert(i, "{} --- ({})".format(clientes['nombre'][i], clientes['cuenta'][i]))
	cnt = len(clientes['nombre'])
	productos = db.execute("SELECT productos.Nombre AS nombre, COUNT(productopedido.CodigoProducto) AS cuenta FROM productopedido JOIN productos ON productopedido.CodigoProducto = productos.Codigo GROUP BY productopedido.CodigoProducto LIMIT 5").to_dict()
	for i in productos['nombre'].keys():
		gui.listbox.insert(cnt+i, "{} --- ({})".format(productos['nombre'][i], productos['cuenta'][i]))
def fn6():
	global gui
	gui.limpiar()