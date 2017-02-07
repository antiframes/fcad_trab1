import re
import sys

lembrete = ""

def getId(var, lem):
	global lembrete
	ret = []
	for n in var:
		# Lembrete usado para os finais de linha com \
		if n.find("\\") != -1:
			lembrete = "m"+lem
		else:
			n= n.split("_")
			ret.append(int(n[1]))
	return ret

def getId2(var):
	v_in = re.search("=(.*)", var)
	v_in = v_in.group(1)
#usado para inputs
	if v_in.find("_") != -1:
		n= v_in.split("_")
		return str(n[1])
#usado para outputs
	if v_in.find("[") != -1:
		n= v_in.split("[")
		n= n[1].split("]")
		return n[0]
#usado para outputs
	return str(v_in)

def getGate(var):
	gate = var[0][:-1]
	ret = []
	tmp = int
	tmp2 = []
	n_in = int(var[0][-1])
	for x in range(n_in+1):
		tmp= getId2(var[x+1])
		tmp2.append(int(tmp))
	tmp2.pop(n_in)
	return (gate, tmp2, int(tmp))


#c2.add_gate(Gate("nand",[6,7],9))

class Netlist:
	global lembrete
	def __init__(self, file):
		self.id = ''
		self.inputs = []
		self.outputs = []
		self.gates = []
 		self.generate(file)

	def generate(self, file):
		for line in file:
			self.parse(line[0:line.find('#')].lower().split())
	
	def parse(self, list):
		global lembrete
		if list:
			type = list[0][(list[0].find('.')+1):]
			if type == 'model':
				self.id = list[1]
			elif type == 'inputs':
				r = getId(list[1:],"i")
				self.inputs = self.inputs+r
			elif type == 'outputs':
				r = getId(list[1:],"o")
				self.outputs = self.outputs+r
			elif type == 'gate':
				r = getGate(list[1:])
				self.gates.append(r)
			elif type == 'end':
				return True
			else :
				if lembrete.find("m") != -1:
					if lembrete.find("i")!= -1:
						lembrete=""
						r = getId(list[1:],"i")
						self.inputs = self.inputs+r
					if lembrete.find("o")!= -1:
						lembrete=""
						r = getId(list[1:],"o")
						self.outputs = self.outputs+r
			

		
