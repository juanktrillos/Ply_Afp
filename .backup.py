import sys
import getopt
import time
import os

start_time = time.time()
var = '▅'
frequency = ''
graph = ''
totalwords = 0
folder = []
n_grama = 0
_type = ''
plyFile = ''

_alft = list("abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ")

def main(args):
	flags = 'hv:g:f:c:d:k'
	global n_grama
	global _type
	global plyFile
	message = ''
	key = ''
	_plyType = 0
	
	try:
		opts,arg = getopt.getopt(args,flags,[])
	except getopt.GetoptError:
		Docs (args)
		sys.exit()

	for opt,arg in opts:
		if opt=='-g':
			n_grama = int(arg)
		if opt=='-h':
			Docs(args)
		if opt=='-f':
			SearchFiles(arg)
		if opt=='-c':
			_plyType = 1
			plyFile = arg
			file = open(arg,'r')
			message = file.read()
			file.close()
		if opt=='-d':
			_plyType = 2
			plyFile = arg
			file = open(arg,'r')
			message = file.read()
			file.close()
		if opt=='-k':
			file = open(arg,'r')
			key = file.read()
			file.close()

	if _type=='afp' and len(folder)>0 and n_grama>0:
		AnalisysFP()
	elif _type == 'ply':
		if _plyType==1:
			if message != '':
				key = createMatrixKey(_alft,message)
				crypt(message,key)
		elif _plyType==2:
			pass
	else:
		Docs(args)

# --------------------------------------------- METODOS DE ANÁLISIS DE FRECUENCIA ------------------------------------------

def AnalisysFP():
	global frequency
	global graph
	global totalwords
	global n_grama

	for _dir in folder:
		message = ''
		msg1 = ("""
-------------------- ANÁLISIS DE FRECUENCIA EN DIRECTORIO '"""+_dir[0]+"""' INICIO ------------------------------ 
""")
		frequency += msg1
		graph += msg1
		print(msg1)
		files = _dir[1]
		files_list = files.split('*')
		if len(files_list)>0:
			for file in files_list:
				_open = open(_dir[0]+'/'+file,'r')
				message += _open.read()
				_open.close()

		if message!='':
			data = ''
			for x in range(1,n_grama+1):
				msgList = ExtractList(message,x)
				matriz = SearchFrequency(msgList)
				data = OrganizeData(matriz,x)
				graph += data
			print(data)

		else:
			exit('DIRECTORIO VACIO: '+_dir[0])

		msg2 = ("""

-------------------- ANÁLISIS DE FRECUENCIA EN DIRECTORIO '"""+_dir[0]+"""' FIN --------------------------------- 
""")
		print(msg2)
		frequency += msg2
		graph += msg2
		totalwords += len(message)

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


def ExtractList(message, n_grama):
	# formula: 
	msgList = []
	_list = list(message)
	_lLen = len(_list)

	for x in range(0, _lLen, n_grama):
		_temp = ''
		for y in range(n_grama):
			if (x+y)<_lLen:
				_temp += _list[x+y]
			else:
				continue
		else:
			if(len(_temp)==n_grama):
				msgList.append(_temp)

	msgList.sort()
	return msgList

def SearchFiles(nameDir):
	try:
		entries = os.scandir(nameDir)
		files = ''
		global folder
		for entry in entries:
			if os.path.isdir(entry):
				SearchFiles(nameDir+"/"+entry.name)
			if os.path.isfile(entry):
				if files != '':
					files += '*'
				files += entry.name

		if files != '':
			folder.append([nameDir,files])
	except Exception as e:
		exit('FOLDER NOT FOUND')
	
def SearchFrequency(msgList):
	pass
	matriz = []

	posList = 0

	for x in range(len(msgList)):
		count = 0
		while msgList[x]==msgList[posList]:
			count += 1
			posList += 1
			if posList>=len(msgList):
				posList = 0
		else:
			if count>0:
				matriz.append([msgList[x],count])
	return matriz

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
		if (x%5==0):
			frequency += '\n'
		frequency += ''+str(matriz[x][0])+':	'+str(matriz[x][1])+'		'

		por = round(matriz[x][1]*100/MAX)
		if(por>=10):
			if (x%1==0):
				data += '\n '
				data += '	'+str(matriz[x][0])+':	'+(var*por)+' 	'+str(matriz[x][1])
	frequency+='\n'
	return (text+data)

# -------------------------------------------- METODOS DE CIFRADO DE POLYBIOS ------------------------------------------------

'''Metodo para crear la llave matrix que se va a utilizar.
	Recibe el alfabeto a utilizar y el mensaje, este metodo no solo crea la matriz sino que tambien
	complementa el alfabeto antes de crearla con un analisis monoalfabetico realizado al mensaje'''
def createMatrixKey(alft,msg):
	m = msg
	global plyFile
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
		key = open(plyFile.split(".")[0]+".key","w")
		key.write(str(k))
		key.close()
		return k

# Metodo de decifrado de polybios
def decrypt(message, key):
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
	f = open(plyFile.split(".")[0]+".dec", "w")
	#f.write("".join(decript))
	f.write(M)
	f.close()	
	#print(M)
	#print ("".join(decript))

# Cifrado de polybios.
def crypt(message, key):
	#m = "".join(message.split(" "))
	#mss = list(m.upper())
	#crypt = list()
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
					#print(ci,l)		
					C += ci		
					#crypt.append(c)
				else:
					continue
		else:
			continue
	else:
		#Creacion del archivo cifrado.
		f = open(plyFile.split(".")[0]+".cif", "wt")
		#f.write(" ".join(crypt))
		f.write(C)
		f.close()
		#print(mss)
		#print(C)	
		#print (" ".join(crypt))

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
		
				Sintaxis: python3 """+sys.argv[0]+""" ply -d <file.cif> -k <key.key>
	
	<file.txt>:	archivo en texto plano que se desea cifrar

	<file.cif>:	archivo cifrado que se desea descifrar

	<key.key>:		archivo con la matriz clave para descifrar el <file.cif>


	Ejemplos: 	python3 """+sys.argv[0]+""" ply -c quijote.txt

		 	python3 """+sys.argv[0]+""" ply -d quijote.cif -k key"""+_authors
	try:
		sys.exit (__doc__)
	except Exception:
		pass

if __name__ == '__main__':
	Docs(sys.argv[1:]);
	main(sys.argv[2:]);
