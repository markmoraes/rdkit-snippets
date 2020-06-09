#!/usr/bin/python2

from __future__ import print_function, division
import os, sys, time, logging, contextlib, urllib2
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Descriptors import MolWt, TPSA, MolLogP, NumRotatableBonds, \
    NumHDonors, NumHAcceptors
from rdkit.Chem.Draw.MolDrawing import Font

# experiment with annotating canvas ourselves, since
# /usr/lib/python2.7/dist-packages/rdkit/Chem/Draw/__init__.py
# has a 0.94 hardwired factor for positioning legend

def drawmol(s):
    bsize=200
    tsize=80
    size = (bsize,bsize+tsize)
    m = Chem.MolFromSmiles(s)
    #print("wt", MolWt(m))
    img, canvas, drawer = Draw.MolToImage(m, size=size, returnCanvas=True)
#                        centerIt=False, drawingTrans=(bsize/2+1,bsize/2+tsize))
    font=Font(face='sans',size=12)
    pos = bsize/2,bsize,0
    canvas.addCanvasText('%s\r\nMolWt: %g\tTPSA: %g' % (s, MolWt(m), TPSA(m)),
                         pos,font)
        
    with open('xx'+s+'.png', 'w') as f:
        canvas.flush()
        img.save(f)

if __name__ == '__main__':
    drawmol('CN1CCC[C@H]1c2cccnc2')
    drawmol('CC(=O)OC1=CC=CC=C1C(=O)O')
    drawmol('O1C=C[C@H]([C@H]1O2)c3c2cc(OC)c4c3OC(=O)C5=C4CCC(=O)5')
    sys.exit(0)

    # sample code to use new drawing API (older rdkit do not have DrawString)
    from rdkit.Chem.AllChem import EmbedMolecule
    assert EmbedMolecule(m) >= 0
    x = Draw.rdMolDraw2D.MolDraw2DSVG(200,250)
    x.DrawMolecule(m)
    x.DrawString('Test String', 20, 200)
    x.FinishDrawing()
    print(x.GetDrawingText())

    # sample code to generate a legend
    legstr = ''
    if molname:
        legstr += molname + '\n'
    legstr += '%s\nWt=%g LogP=%g TPSA=%g\nHBA=%d HBD=%d RotBond=%d\n' % \
        (smiles, MolWt(mol), MolLogP(mol), TPSA(mol),
         NumHAcceptors(mol), NumHDonors(mol), NumRotatableBonds(mol))
