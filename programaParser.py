import sys
import netlist

def main(argv):
	c1 = open(argv[0], 'r')
	net1 = netlist.Netlist(c1)
	
	c2 = open(argv[1], 'r')
	net2 = netlist.Netlist(c2)



if __name__ == "__main__":	
	main(sys.argv[1:])
