import pycosat
class Circuit:
    def __init__(self):
        self.inputs=[]
        self.gates=[]
        self.outputs=[]
    def add_gate(self,gate):
        self.gates.append(gate)
    def add_input(self,inp):
        self.inputs.append(inp)
    def add_output(self,output):
        self.outputs.append(output)
    def refactor_num(self,num, is_odd):
        foo = num*2
        if is_odd:
            foo +=1
        return foo
    def refactor(self,is_odd):
        for gate in self.gates:
            for i in range(len(gate.inputs)):
                gate.inputs[i] = self.refactor_num(gate.inputs[i],is_odd)
            gate.output = self.refactor_num(gate.output,is_odd)
        for i in range((len(self.outputs))):
            self.outputs[i] = self.refactor_num(self.outputs[i],is_odd)
        for i in range((len(self.inputs))):
            self.inputs[i] = self.refactor_num(self.inputs[i],is_odd)
    def push_numbers(self,offset):
        for gate in self.gates:
            for i in range(len(gate.inputs)):
                gate.inputs[i] = gate.inputs[i]+offset
            gate.output =gate.output+offset
        for i in range((len(self.outputs))):
            self.outputs[i] =self.outputs[i]+offset;
        for i in range((len(self.inputs))):
            self.inputs[i] =self.inputs[i]+offset;
    def input_index(self,num):
        for i in range(len(self.inputs)):
            if self.inputs[i]==num:
                return i
        return -1
    def remap_inputs(self, other_inputs):
        for gate in self.gates:
            for i in range(len(gate.inputs)):
                j = self.input_index(gate.inputs[i])
                if j>-1:
                    gate.inputs[i] = other_inputs[j]
        

class Gate:
    def __init__(self,gate,inputs,output):
        self.gate=gate
        self.inputs = inputs
        self.output = output
c1 = Circuit()
c1.add_input(6)
c1.add_input(7)
c1.add_input(8)
c1.add_gate(Gate("nand",[6,7],1))
c1.add_gate(Gate("nor",[7,8],2))
c1.add_gate(Gate("not",[1],3))
c1.add_gate(Gate("or",[1,2],4))
c1.add_gate(Gate("and",[3,4],5))
c1.add_output(5)

c2 = Circuit()
c2.add_input(1)
c2.add_input(4)
c2.add_input(5)
c2.add_gate(Gate("not",[1],2))
c2.add_gate(Gate("and",[1,2],3))

c2.add_output(3)



#gera ids únicos para evitar repetição
c1.refactor(True)
c2.refactor(False)


#se número de saídas for diferente, encerra programa
if len(c1.inputs) != len(c2.inputs):
    print("Circuitos com número incompatível de entradas")
    quit()
    
#se número de saídas for diferente, encerra programa
if len(c1.outputs) != len(c2.outputs):
    print("Circuitos com número incompatível de saídas")
    quit()


#empurra os ids dos circuitos para dar espaço às portas adicionais
additional = len(c1.outputs)
if additional>1:
    additional+=1
c1.push_numbers(additional)
c2.push_numbers(additional)


#refatora um circuito para receber as mesmas entradas do primeiro
c2.remap_inputs(c1.inputs)


final_gates=[]#portas a serem verificadas no SAT
final_gate_inputs=[]#entradas para o OR da última porta
#adiciona XOR's
for i in range(len(c1.outputs)):
    final_gates.append(Gate("xor",[ c1.outputs[i], c2.outputs[i] ], i+1 ))
    final_gate_inputs.append(i+1)
if len(c1.outputs)>1:
    final_gates.append(Gate("or",final_gate_inputs,additional))

for gate in c1.gates:
    final_gates.append(gate)

    
for gate in c2.gates:
    final_gates.append(gate)

#Gerar CNF

phi=[[additional]]


for gate in final_gates:
    
    if gate.gate=="or":
        for i in range(len(gate.inputs)):
            phi.append([-gate.inputs[i] , gate.output])
        last = []
        for i in range(len(gate.inputs)):
            last.append(gate.inputs[i])
        last.append(-gate.output)
        phi.append(last)
        
    elif gate.gate=="not":
        phi.append([gate.inputs[0] , gate.output])
        phi.append([-gate.inputs[0] , -gate.output])
                   
    elif gate.gate=="and":
        for i in range(len(gate.inputs)):
            phi.append([gate.inputs[i] , -gate.output])
        last = []
        for i in range(len(gate.inputs)):
            last.append(-gate.inputs[i])
        last.append(gate.output)
        phi.append(last)

    elif gate.gate=="nor":
        for i in range(len(gate.inputs)):
            phi.append([-gate.inputs[i] , -gate.output])
        last = []
        for i in range(len(gate.inputs)):
            last.append(gate.inputs[i])
        last.append(gate.output)
        phi.append(last)

                    
    elif gate.gate=="nand":
        for i in range(len(gate.inputs)):
            phi.append([gate.inputs[i] , gate.output])
        last = []
        for i in range(len(gate.inputs)):
            last.append(-gate.inputs[i])
        last.append(-gate.output)
        phi.append(last)

    elif gate.gate=="xor":
        phi.append([-gate.inputs[0] , -gate.inputs[1] ,-gate.output])
        phi.append([gate.inputs[0] , gate.inputs[1] ,-gate.output])
        phi.append([gate.inputs[0] , -gate.inputs[1] ,gate.output])
        phi.append([-gate.inputs[0] , gate.inputs[1] ,gate.output])

    elif gate.gate=="xnor":
        phi.append([-gate.inputs[0] , -gate.inputs[1] ,gate.output])
        phi.append([gate.inputs[0] , gate.inputs[1] ,gate.output])
        phi.append([gate.inputs[0] , -gate.inputs[1] ,-gate.output])
        phi.append([-gate.inputs[0] , gate.inputs[1] ,-gate.output])

#for gate in final_gates:
    #print("gate",gate.inputs,gate.output);
#RESOLVER SAT
print(pycosat.solve(phi))
