"""Simple wrapper for reporting time and progress in python scripts (should
work in both py2 and py3)

Mark Moraes, 20200609
"""
from __future__ import print_function, division
import time

class Timer:
    def __init__(self, opname, overheadms = 0., tmax = 1., ncheck = 500, secsreport = 2.5):
        self.opname = opname
        self.overheadms = overheadms
        self.ncheck = ncheck
        self.secsreport = secsreport
        self.tmax = tmax
        self.t = time.time()
        self.n = 0
        self.lastreport = self.t
    def incr(self):
        self.n += 1
        if (self.ncheck > 0 and self.n % self.ncheck) == 0:
            t = time.time()
            if t - self.t > self.tmax:
                return 1
            if t - self.lastreport > self.secsreport:
                self.report("...")
                self.lastreport = t
        return 0
    def report(self, *args):
        dtsec = time.time() - self.t
        if self.n == 0:
            msop = 0.
        else:
            msop = dtsec*1e3/self.n
        print("%.3g ms/%s ( %.3g ms/%s tot, %d in %.3g secs) %s" %
                (msop - self.overheadms, self.opname, msop, self.opname,
                 self.n, dtsec, ' '.join([str(i) for i in args])))
        return (msop, dtsec, self.n)

