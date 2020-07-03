#!/usr/bin/python2
"""Timing rdkit operations, just to get a sense of relative costs

Mark Moraes, 20200609
"""

from __future__ import print_function, division
import os, sys, time
from rdkit.Chem import Draw, MolFromSmiles, MolToSmiles, \
    AddHs, RemoveHs, MolToMolBlock
from rdkit.Chem.AllChem import EmbedMolecule
from rdkit.Chem.Descriptors import MolWt, TPSA, MolLogP, NumRotatableBonds, \
    NumHDonors, NumHAcceptors
from hashlib import sha256

from mmtimer import Timer

# various primitives to time.  The second element of the value indicates
# a dependent step whose timing will be subtracted
steps = {
    0:('readline',-1),
    100:('MolFromSmiles',0),
    105:('sha256',100),
    110:('filewrite',100),
    120:('fsync',110),
    210:('GetNumAtoms',100),
    220:('GetNumBonds',100),
    300:('MolToSmiles',100),
    400:('MolToMolBlock',100),
    420:('MolToMolBlockEmbed',100),
    600:('MolToImageSVG',100),
    610:('MolToImagePNG',100),
}

tmpname = '/tmp/tmol.'+sha256(repr((time.time(), os.getpid(), id(steps))).encode()).hexdigest()

def mol2file(m, t):
    tf = tmpname + '.' + t
    Draw.MolToFile(m, tf, imageType=t)
    return os.stat(tf).st_size

def processline(t, step, line):
    global lensum
    if t.incr():
        return 1
    if step == 0:
        lensum += len(line)
    else:
        m = MolFromSmiles(line)
        if step == 100:
            lensum += len(line)
        elif step == 105:
            lensum += len(sha256(line).hexdigest())
        elif step in (110, 120):
            with open(tmpname, 'wb+') as f:
                print(line, file=f)
                if step == 120:
                    os.fsync(f.fileno())
            lensum += os.stat(tmpname).st_size
        elif step == 210:
            lensum += m.GetNumAtoms()
        elif step == 220:
            lensum += m.GetNumBonds()
        elif step == 300:
            lensum += len(MolToSmiles(m))
        elif step == 400:
            lensum += len(MolToMolBlock(m))
        elif step == 420:
            m2 = AddHs(m)
            EmbedMolecule(m2, randomSeed=2020)
            m2 = RemoveHs(m2)
            m2.SetProp("_Name", "test")
            lensum += len(MolToMolBlock(m2))
        elif step == 600:
            lensum += mol2file(m, 'svg')
        elif step == 610:
            lensum += mol2file(m, 'png')
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
    for nsteps in (1,1,1000):
        steptimes = {}
        for step in sorted(steps.keys())[:nsteps]:
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
