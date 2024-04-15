from IO import read_input
import sys

def create_skeleton(formula):
    atoms = formula.get_atoms()
    atom_map = {}
    atom_rev = {}
    i = 1
    for atom in atoms:
        atom_map[atom] = i
        atom_rev[i] = atom
        i += 1

    return (atom_map,atom_rev)


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

def skel(formula,atom_map):
    res = skel_helper(formula,atom_map)
    r2 = []
    for r in res:
        if type(r) == int:
            r2.append([r])
        else:
            r2.append(r)
    return r2


#alternative skeleton method
def skel2(formula, atom_map):
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
        skel_map,rev_map = create_skeleton(formula)
        skeleton = skel(formula,skel_map)

        print("Clauses: " + str(formula))
        print("Atoms: " + str(formula.get_atoms()))
        print("Atom map: " + str(skel_map))
        print("Boolean skeleton: " + str(skeleton))
