import sys
import getopt
import time
import os

start_time = time.time()
var = '▅'
frequency = ''
graph = ''
message = ''
totalwords = 0
folder = []

def main(args):
	flags = 'hv:t:g:f:'
	n_grama = 0
	
	try:
		opts,arg = getopt.getopt(args,flags,[])
	except getopt.GetoptError:
		Docs (args)
		sys.exit()

	for opt,arg in opts:
		if opt=='-t':
			try:
				file = open(arg,'r')
				message = file.read()
				file.close();
			except :
				message = arg
		if opt=='-g':
			n_grama = int(arg)
		if opt=='-h':
			Docs(args)
		if opt=='-f':
			SearchFiles(arg)

	if len(folder)>0 and n_grama>0:
		global frequency
		global graph
		global totalwords
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
	else:
		Docs(args)


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


def Docs(flags):
	#print(flags)
	_title_ = 'ANALISIS POR FRECUENCIAS'

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
		__doc__ = """
			"""+_title_+"""

	Sintaxis: python3 """+sys.argv[0]+""" <algoritmo>

	<algoritmo>:
		afp:	Análisis de frecuencia polialfabética
		pb:		Cifrado de Polybios"""+_authors

	elif (((len(flags)<2) and (flags[0]=='afp')) or (flags[0] in ('-a','-p','-t','-h'))):
		__doc__ = """
				"""+_title_+"""

	Sintaxis: python3 """+sys.argv[0]+""" afp -t <texto> -g <n-grama>

	<texto>:	Texto o archivo del texto que se desea analizar por frecuencias
	<n-grama>:	Tamaño n-grama que se desea buscar en el texto

	Ejemplo: 	python3 """+sys.argv[0]+""" aft -t texto.txt -g 5"""+_authors

	elif (((len(flags)<2) and (flags[0]=='pb')) or (flags[0] in ('d'))):
		__doc__ = """
				"""+_title_+"""

	Sintaxis: python3 """+sys.argv[0]+""" pb

	<texto>:	Texto o archivo del texto que se desea analizar por frecuencias
	<n-grama>:	Tamaño n-grama que se desea buscar en el texto

	Ejemplo: 	python3 """+sys.argv[0]+""" pb """+_authors
	try:
		sys.exit (__doc__)
	except Exception:
		exit(__doc__)

if __name__ == '__main__':
	Docs(sys.argv[1:]);
	main(sys.argv[2:]);
