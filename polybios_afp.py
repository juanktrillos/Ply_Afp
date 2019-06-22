import sys
import getopt
import time
import os

start_time = time.time()

#VARIABLES DEL ANALISIS DE FRECUENCIA
var = '▅' # CARACTER PARA CREAR LAS BARRAS DE LAS GRAFICAS DE FRECUENCIA
frequency = '' # STRING PARA ALMACENAR Y CONCATENAR EL CONFUNTO DE FRECUENCIAS ANALIZADAS SEGUN N_GRAMA
graph = '' # STRING PARA ALMACENAR Y CONCATENAR LAS GRAFICAS DE FRECUENCIA
totalwords = 0 # VARIABLE PARA CONOCER LA CANTIDAD DE CARACTERES ANALIZADOS
folder = [] # ARRAY PARA ALMACENAR LAS CARPETAS QUE SE DESEAN ANALIZAR
n_grama = 0 # LA CANTIDAD DE GRAMAS QUE SE DESEA ANALIZAR PARA CONOCER LA REDUNDANCIA DE LOS LENGUAJES

#VARIABLES DEL CIFRADO DE POLYBIOS
_type = '' # VARIABLE GLOBAL PARA IDENTIFICAR SI SE QUIERE CIFRAR O DESCIFRAR
plyFile = '' # VARIABLE PARA EXTRAER EL NOMBRE BASE DEL ARCHIVO QUE SE DESEA ANALIZAR ex: (quijote, MobyDick)
# MATRIZ nxn QUE FUNCIONA COMO LA LLAVE PARA CIFRAR Y DESCIFRAR CON POLYBIOS
key = [['A', 'B', 'C', 'D', 'E', 'F', 'G'],['H', 'I', 'J', 'K', 'L', 'M', 'N'],['Ñ', 'O', 'P', 'Q', 'R', 'S', 'T'],
['U', 'V', 'W', 'X', 'Y', 'Z', 'Ü'],['«', 'Ï', ']', 'À', '%', 'Ù', '\n'],['_', '[', '0', '1', '2', '3', '4'],
['5', '6', '7', '8', '9', '{', '}']]

def main(args):

	# SE INICIALIZAN LOS PARAMETROS BASE
	flags = 'hv:g:f:c:d:k:'
	global n_grama
	global _type
	global plyFile
	global key
	message = ''
	_plyType = 0
	
	# SE VALIDAN LAS FLAGS	
	try:
		opts,arg = getopt.getopt(args,flags,[])
	except getopt.GetoptError:
		Docs (args)
		sys.exit()

	# DEPENDIENDO DE LAS FLAGS EJECUTADAS, SE EJECUTAN DIFERENTES COMANDOS
	for opt,arg in opts:
		if opt=='-g':
			n_grama = int(arg) # almacena la cantidad de gramas que se desea analizar
		if opt=='-h':
			Docs(args) # metodo para pedir la guia de ejecucion del programa
		if opt=='-f':
			SearchFiles(arg) # metodo para buscar archivos y subdirectorios en el directorio general seleccionado
		if opt=='-c':
			# se definen las variables para CIFRAR por POLYBIOS, se lee el archivo de texto plano y se almacena su contenido
			_plyType = 1
			plyFile = arg
			file = open(arg,'r',encoding='ISO-8859-1')
			message = file.read()
			file.close()
		if opt=='-d':
			# se definen las variables para DESCIFRAR por POLYBIOS, se lee el archivo de texto cifrado y se almacena
			_plyType = 2
			plyFile = arg
			file = open(arg,'r',encoding='ISO-8859-1')
			message = file.read()
			file.close()

	if _type=='afp' and len(folder)>0 and n_grama>0:
		# Metodo general para empezar el analisis de frecuencias
		AnalisysFP()
	elif _type == 'ply':
		# Metodo general para empezar el cifrado de polybios
		CifradoPly(message,_plyType)
	else:
		# Si se encuentran errores, se despliega la ayuda
		Docs(args)

# --------------------------------------------- METODOS DE ANÁLISIS DE FRECUENCIA ------------------------------------------

def AnalisysFP():
	# Se inicializan las variables globales que se van a utilizar
	global frequency
	global graph
	global totalwords
	global n_grama

	for _dir in folder: # si existen archivos de texto en el directorio proporcionado, se busca leer estos archivos
		message = ''
		msg1 = ("""
-------------------- ANÁLISIS DE FRECUENCIA EN DIRECTORIO '"""+_dir[0]+"""' INICIO ------------------------------ 
""")
		frequency += msg1
		graph += msg1
		print(msg1)

		files = _dir[1] # se lee el nombre del archivos que se encuentran en el directorio
		files_list = files.split('*') # si existen varios archivos, se dividen en un alista
		if len(files_list)>0: # se busca leer el texto de cada archivo y concatenarlo en una variable
			for file in files_list:
				_open = open(_dir[0]+'/'+file,'r',encoding='ISO-8859-1')
				message += _open.read()
				_open.close()

		if message!='': # Teniendo la variable con el texto a analizar, se empieza su ejecucion
			data = ''
			for x in range(1,n_grama+1): # se busca analizar desde el grama 1 al n_grama, dependiendo de la elecciòn del usuario
				msgList = ExtractList(message,x) # el mensaje en variable STRING es recorrido y pasado a una LISTA
				matriz = SearchFrequency(msgList) # la LISTA es recorrida y segun su frecuencia se almacenan los datos como una MATRIZ
				data = OrganizeData(matriz,x) # los datos de la MATRIZ son organizados de forma ascendente segun su frecuencia
				graph += data
			print(data)

		else:
			exit('DIRECTORIO VACIO: '+_dir[0])

		msg2 = ("""

-------------------- ANÁLISIS DE FRECUENCIA EN DIRECTORIO '"""+_dir[0]+"""' FIN --------------------------------- 
""")
		# SE IMPRIME EN CONSOLA Y SE ALMACENA EN LAS VARIABLES DE GRAFICOS Y FRECUENCIAS
		print(msg2)
		frequency += msg2
		graph += msg2
		totalwords += len(message)

	# SE CREA UN ARCHIVO PARA CADA VARIABLE: UNA PARA LOS GRAFICOS Y OTRA PARA UNA LISTA DE FRECUENCIAS
	file = open('frequencies_list.txt','w')
	file2 = open('frequencies_graph.txt','w')
	file.write(frequency+'\n')
	file2.write(graph+'\n')
	file.close()
	file2.close()

	final = """
Tiempo de Ejecución: """+str(time.time()-start_time)+""" seg.
Número de Palabras: """+str(totalwords)+"""
Análisis Terminado

-------------------------------- FIN EJECUCIÓN ------------------------------------

"""
	exit(final)

# El metodo obtiene el mensaje y crea una lista de caracteres de longitud n_grama
def ExtractList(message, n_grama):
	# formula: 
	msgList = []
	_list = list(message)
	_lLen = len(_list)

	for x in range(0, _lLen, n_grama):
		_temp = '' # se almacena cada caracter hasta que se cumpla la longitud de n_grama
		for y in range(n_grama):
			if (x+y)<_lLen:
				_temp += _list[x+y]# se lee y almacena el caracter acomulando en la variable _temp
			else:
				continue
		else:
			if(len(_temp)==n_grama): # Cuando la longitud es la ideal, se agregan los caracteres a la lista
				msgList.append(_temp)

	msgList.sort() # Organiza la lista de forma alfabetica para mejorar el rendimiento de los pasos a seguir
	return msgList

# Se buscan en la carpeta principal subcarpetas y archivos para identificar el origen de los archivos
def SearchFiles(nameDir):
	try:
		entries = os.scandir(nameDir)
		files = ''
		global folder
		for entry in entries:
			if os.path.isdir(entry):# Si existen subcarpetas, se itera el directorio para buscar dentro los archivos
				SearchFiles(nameDir+"/"+entry.name)
			if os.path.isfile(entry):
				if files != '':
					files += '*'# si existen mas de un archivo se concatenan sus nombres para unirlos al directorio
				files += entry.name

		if files != '':# se crea una matriz con el nombre del directorio y los archivos que contiene
			folder.append([nameDir,files])
	except Exception:
		exit('FOLDER NOT FOUND')

# Se leen los datos de la lista y se busca que tanto se repiten para unirlos en una matriz
def SearchFrequency(msgList):
	matriz = []

	posList = 0

	for x in range(len(msgList)):
		count = 0
		while msgList[x]==msgList[posList]:# mientras los datos recorridos sean iguales, se aumenta la frecuencia de este
			count += 1 # es la variable que lleva la cantidad de veces que se repite un mismo caracter
			posList += 1
			if posList>=len(msgList):
				posList = 0
		else:
			if count>0: # Si se confirma que el contador es mayor que cero, existe 1 o mas veces el caracter
				matriz.append([msgList[x],count]) # por lo tanto se agrega el caracter y su contador en una matriz
	return matriz # por ultimo se devuelve la matriz con todos los datos y sus frecuencias

# Se organiza la matriz de forma ascendente para organizar los datos y visualizarlos de forma mas sencilla
def OrganizeData(matriz,n_grama):
	text = """

Análisis de Frecuencia: Tamaño de n_grama = """+str(n_grama)+"""

"""
	data = ''
	global frequency
	frequency += text

	matriz.sort(key=lambda x: x[1])
	MAX = matriz[len(matriz)-1][1]

	for x in range(0,len(matriz)):
		if (x%5==0):# en grupos de 5 se almacenan en una variable para despues llevar a un archivo
			frequency += '\n'
		frequency += ''+str(matriz[x][0])+':	'+str(matriz[x][1])+'		'

		por = round(matriz[x][1]*100/MAX)
		if(por>=10):# se buscan las frecuencias mas altas al 10% omitir los valores menos importantes
			if (x%1==0):
				data += '\n '# se grafica segun el valor de la frecuencia y se almacena en una variable 
				data += '	'+str(matriz[x][0])+':	'+(var*por)+' 	'+str(matriz[x][1])
	frequency+='\n'
	return (text+data)# se retorna los graficos para imprimir en consola

# -------------------------------------------- METODOS DE CIFRADO DE POLYBIOS ------------------------------------------------

def CifradoPly(message,_plyType):
	global key
	if _plyType==1:
		if message != '' and key != '':
			print('''

-------------------------------- INICIANDO CIFRADO ----------------------------------------''')
			#key = createMatrixKey(_alft,message)
			crypt(message,key)
			final = """
Tiempo de Ejecución: """+str(time.time()-start_time)+""" seg.
Número de Palabras: """+str(len(message))+"""
Análisis Terminado

-------------------------------- FIN EJECUCIÓN ------------------------------------

"""
			exit(final)
	elif _plyType==2:
		if message != '' and key != '':
			print('''

-------------------------------- INICIANDO DESCIFRADO ----------------------------------------''')
			decrypt(message,key)
				
			final = """
Tiempo de Ejecución: """+str(time.time()-start_time)+""" seg.
Número de Palabras: """+str(len(message))+"""
Análisis Terminado

-------------------------------- FIN EJECUCIÓN ------------------------------------

"""
			exit(final)

'''Metodo para crear la llave matrix que se va a utilizar.
	Recibe el alfabeto a utilizar y el mensaje, este metodo no solo crea la matriz sino que tambien
	complementa el alfabeto antes de crearla con un analisis monoalfabetico realizado al mensaje'''
"""def createMatrixKey(alft,msg):
	m = msg
	global plyFile
	keyName = plyFile.split(".")[0]+".key";
	print('Creando llave: \"'+keyName+'\"')
	'''Analisis monoalfabetico, el cual complementa el alfabeto agregando 
		los caracteres nuevos encontrados en el analisis'''
	for i in m:
		if i not in alft:
			alft.append(i)
		else:
			continue
	'''else:
					continue'''
		#print(alft,int(round(len(alft)**0.5)),len(alft))
	s = int(round(len(alft)**0.5)) #Raiz del tamaño del arreglo redondeado para saber las dimensiones de la matriz
	#print(s)
	k = list() #Lista que va a almacenar la matrix.
	#Creación de la matriz
	for i in range(0,len(alft),s):
		ki = alft[i:i+s]
		#print(mi)
		k.append(ki)
	else:
		#print(m)
		#Almacenamiento de la matriz como una llave.
		key = open(keyName,"w")
		key.write(str(k))
		key.close()
		print('Llave Creada...')
		return k"""

# Metodo de decifrado de polybios
def decrypt(message, key):
	#key = ast.literal_eval(key)
	num = message.split(" ")
	#decript = list()
	M = ""
	for nm in num:
		n = list(nm)
		#print(n, len(n))
		if len(n) > 1 and len(n) <= 2:
			i = int(n[0])
			j = int(n[1])
			ms = key[i-1][j-1]
			if len(ms) <= 2:
				#print (ms)
				#decript.append(ms[0])
				M += ms[0]
			else:
				#print (ms[random.randint(0,1)])
				M += ms[random.randint(0,1)]
				#decript.append(random.randint(0,1))
		else:
			#sys.exit()
			#print("ERROR")
			continue
	#Creación y alamacenamiento del archivo .dec
	f = open(plyFile.split(".")[0]+".dec",'w',encoding='ISO-8859-1')
	#f.write("".join(decript))
	f.write(M)
	f.close()	
	#print(M)
	#print ("".join(decript))

# Cifrado de polybios.
def crypt(message, key):
	C = ""
	for l in message:
		#print(l)
		for row in key:
			for r in row:
				if l in r:
					ci = ""
					ci += str(key.index(row) + 1)
					ci += str(row.index(r) + 1)
					ci += " "
					C += ci		
				else:
					continue
		else:
			continue
	else:
		#Creacion del archivo cifrado.
		f = open(plyFile.split(".")[0]+".cif", "wt")
		f.write(C)
		f.close()

#  --------------------------------------------------------	METODOS GENERALES --------------------------------------------------------

def Docs(flags):
	#print(flags)
	global _type
	if len(flags)>0:
		_type = flags[0]

	_authors = """

	__________________________________________________________________________________________________

	Autores:	Juan Camilo Trillos Velosa		juan.trillos@uao.edu.co
			Jesus Daniel Neira			jesus.neira@uao.edu.co
	__________________________________________________________________________________________________

	Universidad Autónoma de Occidente
	Especialización en Seguridad Infromática
	Certificados y Firmas Digitales
	Siler Amador Donado
	2019-I
"""
	if (len(flags)==0 or (flags[0] in ('-help','-h'))):
		_title_ = 'ALGORITMOS DE POLYBIOS Y ANÁLISIS DE FRECUENCIA POLIALFABÉTICA'
		__doc__ = """
			"""+_title_+"""

	Sintaxis: python3 """+sys.argv[0]+""" <algoritmo>

	<algoritmo>:
		afp:	Análisis de frecuencia polialfabética
		ply:	Cifrado de Polybios"""+_authors

	elif (((len(flags)<=2) and (flags[0]=='afp')) or (flags[0] in ('-f','-g','-h'))):
		_title_ = 'ANALISIS POR FRECUENCIA POLIALFABÉTICA'
		__doc__ = """
				"""+_title_+"""

	Sintaxis: python3 """+sys.argv[0]+""" afp -f <carpeta> -g <n-grama>

	<carpeta>:	Carpeta donde se encuentran los textos a analizar
	<n-grama>:	Tamaño n-grama que se desea buscar en el texto

	Ejemplo: 	python3 """+sys.argv[0]+""" afp -f Español/ -g 5"""+_authors

	elif (((len(flags)<=2) and (flags[0]=='ply')) or (flags[0] in ('-d'))):
		_title_ = 'CIFRADO DE POLYBIOS'
		__doc__ = """
				"""+_title_+"""

	Sintaxis: python3 """+sys.argv[0]+""" ply <algoritmo>

	<algoritmo>:
		-c:	Cifrar un archivo de texto plano.
				Sintaxis: python3 """+sys.argv[0]+""" ply -c <file.txt>

		-d: 	Descifrar un archivo de texto.
				Sintaxis: python3 """+sys.argv[0]+""" ply -d <file.cif>
	
	<file.txt>:	archivo en texto plano que se desea cifrar
	<file.cif>:	archivo cifrado que se desea descifrar

	Ejemplos: 	python3 """+sys.argv[0]+""" ply -c quijote.txt

		 	python3 """+sys.argv[0]+""" ply -d quijote.cif"""+_authors
	try:
		sys.exit (__doc__)
	except Exception:
		pass

if __name__ == '__main__':
	Docs(sys.argv[1:]);
	main(sys.argv[2:]);
