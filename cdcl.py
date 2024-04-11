import sys
from IO import read_input

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("no input file passed")
        sys.exit()
    else:
        formula = read_input(sys.argv[1])
        print("Clauses: " + str(formula))
        print("Atoms: " + str(formula.get_atoms()))
        
      