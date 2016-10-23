import pycosat

class Gate:
    def __init__(self,gate,inputs,output):
        self.gate=gate
        self.inputs = inputs
        self.output = output
        
gates = []
gates.append(Gate("nand",[6,7],1))
gates.append(Gate("nor",[7,8],2))
gates.append(Gate("not",[1],3))
gates.append(Gate("or",[1,2],4))
gates.append(Gate("and",[3,4],5))
output=5


#Gerar CNF

phi=[[output]]


for gate in gates:
    
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

    elif gate=="xor":
        phi.append([-gate.inputs[0] , -gate.inputs[1] ,-gate.output])
        phi.append([gate.inputs[0] , gate.inputs[1] ,-gate.output])
        phi.append([gate.inputs[0] , -gate.inputs[1] ,gate.output])
        phi.append([-gate.inputs[0] , gate.inputs[1] ,gate.output])

    elif gate=="xnor":
        phi.append([-gate.inputs[0] , -gate.inputs[1] ,gate.output])
        phi.append([gate.inputs[0] , gate.inputs[1] ,gate.output])
        phi.append([gate.inputs[0] , -gate.inputs[1] ,-gate.output])
        phi.append([-gate.inputs[0] , gate.inputs[1] ,-gate.output])

#print(phi)

#RESOLVER SAT
print(pycosat.solve(phi))
