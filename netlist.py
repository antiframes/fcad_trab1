import re
import sys
class Netlist:
	def __init__(self, file):
		self.lembrete = " "
		self.vetEntSai = {}
		self.vetEntSai['\\'] = -1
		self.id = ''
		self.inputs = []
		self.outputs = []
		self.gates = []
		self.generate(file)
	
	def generate(self, file):
		for line in file:
			self.parse(line[0:line.find('#')].lower().split())
	
	
	def parse(self, list):
		if list:
			type = list[0][(list[0].find('.')+1):]
			if type == 'model':
				self.id = list[1]
			elif type == 'inputs':
				r = self.getIdES(list[1:],"i")
				self.inputs = self.inputs+r
			elif type == 'outputs':
				r = self.getIdES(list[1:],"o")
				self.outputs = self.outputs+r
			elif type == 'gate':
				r = self.getGate(list[1:])
				self.gates.append(r)
			elif type == 'end':
				return True
			else :
				if self.lembrete.find("m") != -1:
					if self.lembrete.find("i")!= -1:
						self.lembrete=""
						r = self.getIdES(list,"i")
						self.inputs = self.inputs+r
					if self.lembrete.find("o")!= -1:
						self.lembrete=""
						r = self.getIdES(list,"o")
						self.outputs = self.outputs+r

	def getIdES(self, var, lem):
		ret = []
		for n in var:
			if n.find("\\") != -1:
				self.lembrete = "m"+lem
			else:
				if n not in self.vetEntSai.keys():
					self.vetEntSai[n] = len(self.vetEntSai)
				ret.append(self.vetEntSai[n])
		return ret

	def getGate(self, var):
		gate = var[0][:-1]
		ret = []
		tmp = int
		tmp2 = []
		n_in = int(var[0][-1])
		for x in range(n_in+1):
			v_in = re.search("=(.*)", var[x+1])
			v_in = v_in.group(1)
			if v_in not in self.vetEntSai.keys():
					self.vetEntSai[v_in] = len(self.vetEntSai)
			tmp= self.vetEntSai[v_in]
			tmp2.append(int(tmp))
		tmp2.pop(n_in)
		return (gate, tmp2, int(tmp))

		
