#!/usr/bin/python2
from __future__ import print_function, division
import sys
from rdkit.Chem import MolFromSmiles, AddHs, RemoveHs
from rdkit.Chem.AllChem import EmbedMolecule

if __name__ == "__main__":
    for line in sys.stdin.readlines():
	s = line.strip()
	print(s)
        m = MolFromSmiles(s)
        m2 = AddHs(m)
        EmbedMolecule(m2, randomSeed=2020)
