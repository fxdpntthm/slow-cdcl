from pysmt.smtlib.parser import SmtLibParser
from pysmt.rewritings import CNFizer

# reads an SMT_LIB 2 script, and returns it in CNF form
def read_input(fname): 
    script = SmtLibParser().get_script_fname(fname)
    formula = script.get_last_formula()
    cnfizer = CNFizer()
    cnf_formula = cnfizer.convert_as_formula(formula)
    simp_cnf_formula = cnf_formula.simplify() # get rid of all the boolean constants
    return (simp_cnf_formula, formula.get_free_variables())
