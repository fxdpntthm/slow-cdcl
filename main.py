from IO import read_input
import sys

# maps atoms to clauses and vice-versa
def create_skel_map(formula):
    atoms = formula.get_atoms()
    atom_map = {}
    atom_rev = {}
    i = 1
    for atom in atoms:
        atom_map[atom] = i
        atom_rev[i] = atom
        i += 1

    return (atom_map,atom_rev)

# another skel method, just iterates over the top level args tuple and calls skel_helper2 for each arg
# so at the end you get a 2D list that is a conjunction, and each of the 1D lists inside is a disjunction 
def skel2(formula,atom_map):
    res = []
    for arg in formula.args():
        r2 = []
        skel_helper2(arg,atom_map,r2)
        res.append(r2)
    return res

# turns atoms into clauses and stores them in a 1D list since they're all disjunctions so can be flattened
# an atom can be a clause on its own, so handles that case too
def skel_helper2(formula, atom_map,res):
    if len(formula.args()):
        for arg in formula.args():
            if arg in atom_map:
                res.append(atom_map[arg])
            elif arg.is_not():
                res.append(-1 * atom_map[arg.arg(0)])
            else:
                skel_helper2(arg,atom_map,res)
    else:
        if formula in atom_map:
            res.append(atom_map[formula])
        else:
            print("Something weird going on...")
            print(formula)
            print(atom_map)



# original skel and skel_helper methods written during the Apr 15 meeting (just normal recursion)
def skel(formula,atom_map):
    res = skel_helper(formula,atom_map)
    r2 = []
    for r in res:
        if type(r) == int:
            r2.append([r])
        else:
            r2.append(r)
    return r2


def skel_helper(formula, atom_map):
    res = []
    for arg in formula.args():
        if arg in atom_map:
            res.append(atom_map[arg])
        elif arg.is_not():
            res.append(-1 * atom_map[arg.arg(0)])
        else:
            r2 = skel_helper(arg,atom_map)
            res.append(r2)

    return res


# alternative skeleton method, that just collects atoms
# doesnt account for negations
def skel_atoms(formula, atom_map):
    res = []
    for arg in formula.args():
        atoms = arg.get_atoms()
        r2 = []
        for a in atoms:
            r2.append(atom_map[a])
        res.append(r2)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("no input file passed")
        sys.exit()
    else:
        formula = read_input(sys.argv[1])
        skel_map,rev_map = create_skel_map(formula)
        skeleton = skel2(formula,skel_map)

        print("Clauses: " + str(formula))
        print("Atoms: " + str(formula.get_atoms()))
        print("Atom map: " + str(skel_map))
        print("Boolean skeleton: " + str(skeleton))
