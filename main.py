from IO import read_input
import sys


def build_skeleton_map(formula):
    """
    Builds map to represent each literal.
    eg.     {1 -> x + y >= 0, 2 -> B, 3 -> D, 4 -> y <=0 , 5 -> C}
            and also its inverse map
            {x + y >= 0 -> 1, B -> 2, D -> 3, y <=0 -> 4, C -5}
    """
    atoms = formula.get_atoms()
    atom_map = {}
    atom_rev = {}
    i = 1
    for atom in atoms:
        atom_map[atom] = i
        atom_rev[i] = atom
        i += 1
    return (atom_map,atom_rev)

def build_skeleton(formula, atom_map):
    """
    The input formula is in CNF form and may contain theory literals,
       eg. !(x + y >= 0) \/ B /\ -D /\ y <= 0 \/ C
    Computes the boolean skeleton of the formula:
       [[-1, 2], [-3] ,[4, 5]]

    the skel_map contains the mappings for atoms to numbers
    {1 -> x + y >= 0, 2 -> B, 3 -> D, 4 -> y <=0 , 5 -> C}
    """
    formula_skeleton = []
    for clause in formula.args():
        clause_skeleton = []
        if len(clause.args()) == 0:
            # this is a singleton clause so just append its lookup
            clause_skeleton.append(atom_map[clause])
        else:
            for literal in clause.args():
                if literal.is_not():
                    clause_skeleton.append(-1 * atom_map[literal.arg(0)])
                else: clause_skeleton.append(atom_map[literal])
        clause_skeleton.sort
        res.append(clause_skeleton)
    return formula_skeleton


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("no input file passed")
        sys.exit()
    else:
        formula = read_input(sys.argv[1])
        skel_map,rev_map = create_skeleton_map(formula)
        skeleton = build_skeleton(formula, skel_map)

        print("Clauses: " + str(formula))
        print("Atoms: " + str(formula.get_atoms()))
        print("Atom map: " + str(skel_map))
        print("Boolean skeleton: " + str(skeleton))
