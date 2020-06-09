#!/usr/bin/python2
"""Timing rdkit operations, just to get a sense of relative costs

Mark Moraes, 20200609
"""

from __future__ import print_function, division
import os, sys, time, logging, contextlib, urllib2
from rdkit.Chem import Draw, MolFromSmiles, MolToSmiles, \
    AddHs, RemoveHs, MolToMolBlock
from rdkit.Chem.AllChem import EmbedMolecule
from rdkit.Chem.Descriptors import MolWt, TPSA, MolLogP, NumRotatableBonds, \
    NumHDonors, NumHAcceptors
from cStringIO import StringIO
from hashlib import sha256

from mmtimer import Timer

# various primitives to time.  The second element of the value indicates
# a dependent step whose timing will be subtracted
steps = {
    0:('readline',-1),
    1:('MolFromSmiles',0),
    2:('GetNumAtoms',1),
    3:('GetNumBonds',1),
    4:('MolToSmiles',1),
    5:('MolToMolBlock',1),
    6:('MolToMolBlockEmbed',1),
    7:('MolToImageSVG', 1),
    8:('MolToImagePNG', 1),
    9:('sha256',0),
    10:('filewrite',0),
    11:('fsync',10),
}
stepmax = max(steps.keys())+1

tmpname = '/tmp/tmol.'+sha256(repr((time.time(), os.getpid(), id(stepmax)))).hexdigest()

def processline(t, step, line):
    global lensum
    if t.incr():
        return 1
    if step == 0:
        lensum += len(line)
    elif step == 9:
        lensum += len(sha256(line).hexdigest())
    elif step in (10, 11):
	with open(tmpname, 'wb+') as f:
	    print(line, file=f)
	    if step == 11:
		os.fsync(f.fileno())
    else:
        m = MolFromSmiles(line)
        if step == 1:
            lensum += len(line)
        elif step == 2:
            lensum += m.GetNumAtoms()
        elif step == 3:
            lensum += m.GetNumBonds()
        elif step == 4:
            lensum += len(MolToSmiles(m))
        elif step == 5:
            lensum += len(MolToMolBlock(m))
        elif step == 6:
            m2 = AddHs(m)
            EmbedMolecule(m2, randomSeed=2020)
            m2 = RemoveHs(m2)
            m2.SetProp("_Name", "test")
            lensum += len(MolToMolBlock(m2))
        elif step == 7:
            sio = StringIO()
            Draw.MolToFile(m, sio, imageType='svg')
            lensum += sio.tell()
        elif step == 8:
            sio = StringIO()
            Draw.MolToFile(m, sio, imageType='png')
            lensum += sio.tell()
        else:
            raise ValueError("Not implemented step "+str(step))
                
    return 0


if __name__ == "__main__":
    import random
    # one iteration of step 0 (readline) to warm cache
    # then do all steps
    seed = int(os.getenv('TMOL_SEED', time.time()))
    randmax = int(os.getenv('TMOL_RANDMAX', '10'))
    tmax = float(os.getenv('TMOL_TMAX', '1.'))
    for nsteps in (1,1,stepmax):
	steptimes = {}
	for step in range(0, nsteps):
	    random.seed(seed)
	    lensum = 0
	    sys.stdin.seek(0)
	    dependson = steps[step][1]
	    if dependson >= 0:
		overhead = steptimes[dependson][0]
	    else:
		overhead = 0.
	    desc = steps[step][0]
	    if nsteps != 1 and step == 0:
		desc += "-rand%d" % randmax
	    t = Timer(desc, overheadms=overhead, tmax=tmax)
	    for line in sys.stdin.readlines():
		# In first two passes, i.e.nsteps == 1, just scan all lines
		# with step 0 to warm buffer cache.
		# In final pass, select approx 1 in randmax lines randomly
		# for all steps.
		if nsteps == 1 or random.randrange(randmax) == 0:
		    if processline(t, step, line):
			break
	    steptimes[step] = t.report(lensum)
    os.remove(tmpname)
    sys.exit(0)
