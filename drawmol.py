#!/usr/bin/python2
"""
Use the RDKit to generate SVG (or other image type) for
specified molecules SMILES from stdin (each followed by
optional filename) and store .png under the specified OUTDIR argument
Use DRAWMOL_IMGTYPE environment variable to specify other image
types like png pdf or ps (jpg if rdkit uses agg rather than cairo)
"""

from __future__ import print_function, division
import os, sys, time
from rdkit.Chem import Draw, MolFromSmiles

def drawmol(mol, odir, obasename, otype):
    if not os.path.exists(odir):
        os.mkdir(odir)
    tsuff = "_tmp_" + str(time.time()) + "_" + str(os.getpid())
    imgfile = os.path.join(odir, obasename+"."+otype)
    if not os.path.exists(imgfile):
        timgfile = imgfile + tsuff
        Draw.MolToFile(mol, timgfile, imageType=otype)
        os.rename(timgfile, imgfile)
    return imgfile

def draw_to_outdir(odir, otype):
    for s in sys.stdin.readlines():
        s = s.strip()
        if not s or s.startswith('#'):
            continue
        v = s.split()
        smiles = v[0]
        if len(v) > 1:
            obasename = v[1]
        else:
            obasename = v[0]
        drawmol(MolFromSmiles(smiles), odir, obasename, otype)
    return 0

if __name__=='__main__':
    tdir = None
    try:
        otype = os.environ.get('DRAWMOL_IMGTYPE', 'svg')
        if len(sys.argv) != 2:
            sys.exit("Usage: "+sys.argv[0]+" OUTDIR")
        else:
            sys.exit(draw_to_outdir(sys.argv[1], otype))
    except KeyboardInterrupt:
        sys.exit(1)
