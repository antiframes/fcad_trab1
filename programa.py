import pycosat

class Gate:
    def __init__(self,gate,inputs,output):
        self.gate=gate
        self.inputs = inputs
        self.output = output
        
gates = []
cnf=[]

gates.append(Gate("nand2",[6,7],1))
gates.append(Gate("nor2",[7,8],2))
gates.append(Gate("not1",[1],3))
gates.append(Gate("or2",[1,2],4))
gates.append(Gate("and2",[3,4],5))

