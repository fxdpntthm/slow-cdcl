from pysmt.smtlib.parser import SmtLibParser
from pysmt.rewritings import CNFizer

# reads an SMT_LIB 2 script, and returns it in CNF form
def read_input(fname): 
    script = SmtLibParser().get_script_fname(fname)
    formula = script.get_last_formula()
    cnf = CNFizer()
    return (cnf.convert_as_formula(formula), formula.get_free_variables())
