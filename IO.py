from pysmt.smtlib.parser import SmtLibParser
from pysmt.rewritings import CNFizer

def read_input(fname): 
    script = SmtLibParser().get_script_fname(fname)
    formula = script.get_last_formula()
    cnf = CNFizer()
    return cnf.convert_as_formula(formula)
