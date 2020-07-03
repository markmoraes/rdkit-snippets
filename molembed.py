#!/usr/bin/python2
# Little harness for timing how long it takes to embed a molecule
# which seems extremely variable on one machine,
from __future__ import print_function, division
import sys, time, os
from rdkit.Chem import MolFromSmiles, AddHs, RemoveHs
from rdkit.Chem.AllChem import EmbedMolecule

if __name__ == "__main__":
    dotimestamp = int(os.getenv('MOLEMBED_TIME', '0'))
    doaddh = int(os.getenv('MOLEMBED_ADDH', '0'))
    rseed = int(os.getenv('MOLEMBED_SEED', '0'))
    t0 = time.time()
    for line in sys.stdin.readlines():
        s = line.strip()
        if dotimestamp:
            t1 = time.time()
            dt = (t1-t0)*1e3
            print('%.3f' % dt, s)
            t0 = t1
        else:
            print(s)
        m = MolFromSmiles(s)
        if doaddh:
            m2 = AddHs(m)
        else:
            m2 = m
        EmbedMolecule(m2, randomSeed=rseed)
