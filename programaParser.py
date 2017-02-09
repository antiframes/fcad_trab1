import sys
import netlist

def main(argv):
	c1 = open(argv[0], 'r')
	net1 = netlist.Netlist(c1)
	
	print "Inputs: ", net1.inputs
	print "Outputs: ",net1.outputs
	print "Gates: ",net1.gates
	print "Dicionario: "
	for n in net1.vetEntSai:
		print "\t" 
		print n ,":", net1.vetEntSai[n]


if __name__ == "__main__":	
	main(sys.argv[1:])
