import json
import numpy as np
from collections import defaultdict, Counter
from setup_atoms import Atoms, read_helper_data
from atomic_constants import *


def get_X(names, elmap):
    Eatomicnum = []
    rad = []
    elecneg = []
    rowlist = []
    collist = []
    Eionization = []

    for name in names:
        Eatomicnum.append(atomic_number[name])
        rad.append(radius[name])
        elecneg.append(pauling[name])
        rowlist.append(row[name])
        collist.append(col[name])
        Eionization.append(Eion[name])

    val = [np.mean(Eatomicnum),
           np.mean(rad), np.max(rad)-np.min(rad), np.std(rad),
           np.mean(elecneg), np.max(elecneg)-np.min(elecneg), np.std(elecneg),
           np.mean(rowlist), np.std(rowlist),
           np.mean(collist), np.max(collist)-np.min(collist), np.std(collist),
           np.mean(Eionization), np.max(Eionization)-np.min(Eionization), np.std(Eionization)]

    elval = [0,] * len(elmap)
    uniqueel = Counter(names) # get unqiue elements
    for k1, v1 in uniqueel.items(): # propotion of each elements in cell
        elval[elmap[k1]] = float(v1) / len(names) # pauling[k1] / nn gives exactly the same name

    return val + elval


def read_json(filename = "data.json", energytype="atomization"):
    d = json.load(open(filename, 'r'))
    formulas = []
    mset = []
    if filename.split("/")[0] == filename:
        prefix = "."
    else:
        prefix = filename.split("/")[0]
    Exptvol, cord, coulomb = read_helper_data(prefix)
    naelements = [name for name, value in pauling.items() if value is None]
    naelements = [name for name, value in col.items() if value in ["Lanthanide", "Actinide"]]

    for i, item in enumerate(d):
        atoms = Atoms(item, Exptvol, cord, coulomb, energytype)
        if atoms.Eref is None: continue
        found = False
        for el in naelements:
            if el in atoms.names: 
                found = True
                break
        if found : continue
#        if atoms.bandgap < 0.05 or atoms.bandgap > 6.: continue
#        if len(atoms.formula.split()) <=2 : continue
#        if "La" in atoms.names: continue
#        if "Y" in atoms.names: continue

        # ignore formula already in dataset
        formula = " ".join(sorted(atoms.formula.split()))
        atoms.formula = formula
#        formula = atoms.formula
        if formula not in formulas: 
            formulas.append(formula)
        else:
            continue

#        anions = ['F', 'Cl', 'O', 'S', 'Se', 'Br', 'P', 'N']
#        found = 0
#        for el in anions:
#            if el in atoms.names:
#                found += 1
#        if found >= 2: continue

        if "atommasses_amu" in item.keys():
            volerror = np.abs(atoms.calcvol - atoms.exptvol) / atoms.exptvol 
            if volerror > 0.2: continue

        mset.append(atoms)
    del d

    # rank the dataset by Eref
    Eref = attribute_tolist(mset, attr="Eref")
    index = np.argsort(Eref)
    msetnew = []
    for i in index:
        msetnew.append(mset[i])

    print "Size of dataset : ", len(msetnew)//5*5

    return msetnew # return set that is divisable by 5, since its 5 fold 

def attribute_tolist(mset, attr="Eref", unique=False):
    if not unique:
        attrlist = []
    else:
        attrlist = set()
    for atom in mset:
        if not unique:
            attrlist.append(getattr(atom, attr))
        else:
            attrlist.add(getattr(atom, attr))
        
    return attrlist

def get_unique_elements(mset):
    elements = defaultdict(int)
    for atoms in mset:
        tmp = set()
        for name in atoms.names:
            tmp.add(name)
        for name in tmp:
            elements[name] += 1
    return elements

def get_elements_map(mset):
    elements = get_unique_elements(mset)
    elmap = {}
    for i, el in enumerate(elements):
        elmap[el] = i
    return elmap

def get_nelements_per_cell(mset):
    nel = defaultdict(int)
    for i in mset:
        nel[len(i.formula.split())] += 1
    return nel

if __name__ == "__main__":
    mset = read_json("data.json")
    Eref = attribute_tolist(mset, attr="Eref", unique=False)
    elements = get_unique_elements(mset)

    print Eref
    print elements, len(elements)

    numel_performula = defaultdict(int)
    for atoms in mset:
        l = len(atoms.formula.split())
        numel_performula[l] += 1
    print numel_performula
    print atoms.formula, atoms.Eref
