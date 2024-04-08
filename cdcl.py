import sys
import cvc5

def read_input(fname): 
    solver = cvc5.Solver()

    #guessing we don't need this?
    #solver.setOption("produce-models", "true")

    #### Initialize symbol manager
    symbol_manager = cvc5.SymbolManager(solver)

    #### Initialize parser
    parser = cvc5.InputParser(solver, symbol_manager)
    parser.setFileInput(cvc5.InputLanguage.SMT_LIB_2_6, fname)

    while not(parser.done()):
        command = parser.nextCommand()
        
        # it seems to always have a null command at the end which throws an error
        if str(command) != "null":
            command.invoke(solver,symbol_manager)

    return (parser,symbol_manager,solver)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("no input file passed")
        sys.exit()
    else:
        parser,sym,solver = read_input(sys.argv[1])
        clause_set = solver.getAssertions()
        print("Clauses: " + str(clause_set))
        
      