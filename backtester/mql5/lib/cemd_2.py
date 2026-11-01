"""CEMD_2.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.object import *  # Object.mqh
from backtester.mql5.lib.stdliberr import *  # StdLibErr.mqh


class CEMD(CObject):
    _q_fields = ('N', 'nIMF', 'Mean', 'MaxIMF', 'MaxIter', 'Eps', 'Trs', 'Retr', 'IMFResult', 'X', 'Imf', 'XMax', 'YMax', 'XMin', 'YMin', 'EnvUpp', 'EnvLow')
    def __init__(self):
        CObject.__init__(self)
        self.N = 0
        self.nIMF = 0
        self.Mean = 0.0
        self.MaxIMF = 0
        self.MaxIter = 0
        self.Eps = 0.0
        self.Trs = 0.0
        self.Retr = 0.0
        self.IMFResult = Arr(0, 0.0)
        self.X = Arr(0, 0.0)
        self.Imf = Arr(0, 0.0)
        self.XMax = Arr(0, 0.0)
        self.YMax = Arr(0, 0.0)
        self.XMin = Arr(0, 0.0)
        self.YMin = Arr(0, 0.0)
        self.EnvUpp = Arr(0, 0.0)
        self.EnvLow = Arr(0, 0.0)
        self.MaxIMF = 16
        self.MaxIter = 1000
        self.Eps = 8 * DBL_EPSILON
        self.Trs = 4 * DBL_EPSILON
        self.Retr = 7.0
    def CEMD(self):
        pass
    def Decomp(self, y):
        i = 0
        j = 0
        iter_ = 0
        nmax = Box(0)
        nmin = Box(0)
        nzer = Box(0)
        pmin = 0
        pmax = 0
        pzer = 0
        count = 0
        valid = 0
        a = 0.0
        self.N = ArraySize(y)
        if self.N < 6:
            Print('CEMD::Decomp', ': Error! Insufficient length of the input data.')
            return -1
        i = self.arrayprepare()
        if i < 0:
            Print('CEMD::Decomp', ': Error! ArrayResize() error.')
            return -2
        i = 0
        for i in range(i, self.N):
            self.X[i] = i
        else:
            i = _range_end(i, self.N, 1)
        self.Mean = 0.0
        i = 0
        for i in range(i, self.N):
            self.Mean += _fdiv(y[i] - self.Mean, i + 1.0)
        else:
            i = _range_end(i, self.N, 1)
        i = 0
        for i in range(i, self.N):
            a = y[i] - self.Mean
            self.Imf[i] = a
            self.IMFResult[i] = a
        else:
            i = _range_end(i, self.N, 1)
        self.nIMF = 0
        while _incattr(self, 'nIMF', 1, True) < self.MaxIMF:
            j = self.extrcounter(self.Imf)
            if j < 2:
                break
            iter_ = 0
            count = 0
            pmin = INT_MAX
            pmax = INT_MAX
            pzer = INT_MAX
            while ((iter_ := iter_ + 1) - 1) < self.MaxIter:
                valid = self.extrema(self.Imf, nmax, self.XMax, self.YMax, nmin, self.XMin, self.YMin, nzer)
                if ((nmax.v == pmax and nmin.v == pmin) and nzer.v == pzer) and valid == 1:
                    count += 1
                else:
                    pmax = nmax.v
                    pmin = nmin.v
                    pzer = nzer.v
                    count = 0
                if count >= self.Retr:
                    break
                if nmax.v < 2:
                    i = 0
                    for i in range(i, self.N):
                        self.EnvUpp[i] = self.Imf[i]
                    else:
                        i = _range_end(i, self.N, 1)
                else:
                    self.SplineInterp(self.XMax, self.YMax, nmax.v, self.X, self.EnvUpp)
                if nmin.v < 2:
                    i = 0
                    for i in range(i, self.N):
                        self.EnvLow[i] = self.Imf[i]
                    else:
                        i = _range_end(i, self.N, 1)
                else:
                    self.SplineInterp(self.XMin, self.YMin, nmin.v, self.X, self.EnvLow)
                i = 0
                for i in range(i, self.N):
                    self.Imf[i] -= self.EnvUpp[i] + ((self.EnvLow[i] - self.EnvUpp[i]) * 0.5)
                else:
                    i = _range_end(i, self.N, 1)
            if iter_ >= self.MaxIter:
                Print('CEMD::Decomp', ': Warning! Reached the maximum number of iterations.')
            j = self.extrcounter(self.Imf)
            if j < 1:
                break
            if ArrayResize(self.IMFResult, self.N * (self.nIMF + 1)) != (self.N * (self.nIMF + 1)):
                Print('CEMD::Decomp', ': Error! ArrayResize() error.')
                return -2
            i = 0
            for i in range(i, self.N):
                self.IMFResult[i + (self.N * self.nIMF)] = self.Imf[i]
                a = self.IMFResult[i] - self.Imf[i]
                self.IMFResult[i] = a
                self.Imf[i] = a
            else:
                i = _range_end(i, self.N, 1)
        if ArrayResize(self.IMFResult, self.N * (self.nIMF + 1)) != (self.N * (self.nIMF + 1)):
            Print('CEMD::Decomp' + ': Error! ArrayResize() error.')
            return -2
        i = 0
        for i in range(i, self.N):
            self.IMFResult[i + (self.N * self.nIMF)] = self.IMFResult[i]
            self.IMFResult[i] = y[i] - self.Mean
        else:
            i = _range_end(i, self.N, 1)
        if self.nIMF >= self.MaxIMF:
            Print('CEMD::Decomp', ': Warning! Reached the maximum number of IMF.')
        return 0
    def GetIMF(self, x, nn):
        i = 0
        k = 0
        k = ArraySize(x)
        if k > self.N:
            k = self.N
        if (nn < 0 or nn > self.nIMF) or self.nIMF == 0:
            i = 0
            for i in range(i, k):
                x[i] = 0.0
            else:
                i = _range_end(i, k, 1)
        else:
            i = 0
            for i in range(i, k):
                x[i] = self.IMFResult[i + (self.N * nn)]
            else:
                i = _range_end(i, k, 1)
    def arrayprepare(self):
        if ArrayResize(self.IMFResult, self.N) != self.N:
            return -1
        if ArrayResize(self.X, self.N) != self.N:
            return -1
        if ArrayResize(self.Imf, self.N) != self.N:
            return -1
        if ArrayResize(self.XMax, self.N + 4) != (self.N + 4):
            return -1
        if ArrayResize(self.YMax, self.N + 4) != (self.N + 4):
            return -1
        if ArrayResize(self.XMin, self.N + 4) != (self.N + 4):
            return -1
        if ArrayResize(self.YMin, self.N + 4) != (self.N + 4):
            return -1
        if ArrayResize(self.EnvUpp, self.N) != self.N:
            return -1
        if ArrayResize(self.EnvLow, self.N) != self.N:
            return -1
        return 0
    def extrcounter(self, y):
        i = 0
        j = 0
        a = 0.0
        b = 0.0
        c = 0.0
        a = y[0]
        b = y[1]
        j = 0
        i = 1
        for i in range(i, self.N - 1):
            c = y[i + 1]
            if MathAbs(b - c) > (DBL_MIN + (self.Eps * MathMax(MathAbs(b), MathAbs(c)))):
                if (b > c and b > a) or (b < c and b < a):
                    j += 1
                a = b
                b = c
        else:
            i = _range_end(i, self.N - 1, 1)
        return j
    def extrema(self, y, nmax, xmax, ymax, nmin, xmin, ymin, nzer):
        i = 0
        k = 0
        nb = 0
        sig = 0
        ret = 0
        a = 0.0
        b = 0.0
        c = 0.0
        d = 0.0
        sig = 0
        nzer.v = 0
        i = 0
        for i in range(i, self.N):
            if y[i] > self.Trs and sig < 1:
                if sig == -1:
                    nzer.v += 1
                sig = 1
            if y[i] < (-self.Trs) and sig > -1:
                if sig == 1:
                    nzer.v += 1
                sig = -1
        else:
            i = _range_end(i, self.N, 1)
        nmax.v = 0
        nmin.v = 0
        ret = 1
        a = y[0]
        b = y[1]
        k = 1
        i = 1
        for i in range(i, self.N - 1):
            c = y[i + 1]
            if MathAbs(b - c) > (DBL_MIN + (self.Eps * MathMax(MathAbs(b), MathAbs(c)))):
                if b > c and b > a:
                    xmax[nmax.v + 2] = 0.5 * (k + i)
                    d = 0.5 * (y[k] + y[i])
                    ymax[2 + _incbox(nmax, 1, True)] = d
                    if d < 0:
                        ret = 0
                elif b < c and b < a:
                    xmin[nmin.v + 2] = 0.5 * (k + i)
                    d = 0.5 * (y[k] + y[i])
                    ymin[2 + _incbox(nmin, 1, True)] = d
                    if d > 0:
                        ret = 0
                a = b
                b = c
                k = i + 1
        else:
            i = _range_end(i, self.N - 1, 1)
        if ret == 1:
            k = nzer.v - nmax.v - nmin.v
            if k > 1 and k < -1:
                ret = 0
        nb = 2
        while nmin.v < (nb + 1) and nmax.v < (nb + 1):
            nb -= 1
        if nb < 2:
            i = 0
            for i in range(i, nmin.v):
                xmin[i + nb] = xmin[i + 2]
                ymin[i + nb] = ymin[i + 2]
            else:
                i = _range_end(i, nmin.v, 1)
            i = 0
            for i in range(i, nmax.v):
                xmax[i + nb] = xmax[i + 2]
                ymax[i + nb] = ymax[i + 2]
            else:
                i = _range_end(i, nmax.v, 1)
        if nb < 1:
            return ret
        if xmax[nb] < xmin[nb]:
            if y[0] > ymin[nb]:
                if ((2 * xmax[nb]) - xmin[(2 * nb) - 1]) > 0:
                    i = 0
                    for i in range(i, nb):
                        xmax[i] = -xmax[(2 * nb) - 1 - i]
                        ymax[i] = ymax[(2 * nb) - 1 - i]
                        xmin[i] = -xmin[(2 * nb) - 1 - i]
                        ymin[i] = ymin[(2 * nb) - 1 - i]
                    else:
                        i = _range_end(i, nb, 1)
                else:
                    i = 0
                    for i in range(i, nb):
                        xmax[i] = (2 * xmax[nb]) - xmax[(2 * nb) - i]
                        ymax[i] = ymax[(2 * nb) - i]
                        xmin[i] = (2 * xmax[nb]) - xmin[(2 * nb) - 1 - i]
                        ymin[i] = ymin[(2 * nb) - 1 - i]
                    else:
                        i = _range_end(i, nb, 1)
            else:
                i = 0
                for i in range(i, nb):
                    xmax[i] = -xmax[(2 * nb) - 1 - i]
                    ymax[i] = ymax[(2 * nb) - 1 - i]
                else:
                    i = _range_end(i, nb, 1)
                i = 0
                for i in range(i, nb - 1):
                    xmin[i] = -xmin[(2 * nb) - 2 - i]
                    ymin[i] = ymin[(2 * nb) - 2 - i]
                else:
                    i = _range_end(i, nb - 1, 1)
                xmin[nb - 1] = 0.0
                ymin[nb - 1] = y[0]
        else:
            if y[0] < ymax[nb]:
                if ((2 * xmin[nb]) - xmax[(2 * nb) - 1]) > 0:
                    i = 0
                    for i in range(i, nb):
                        xmax[i] = -xmax[(2 * nb) - 1 - i]
                        ymax[i] = ymax[(2 * nb) - 1 - i]
                        xmin[i] = -xmin[(2 * nb) - 1 - i]
                        ymin[i] = ymin[(2 * nb) - 1 - i]
                    else:
                        i = _range_end(i, nb, 1)
                else:
                    i = 0
                    for i in range(i, nb):
                        xmax[i] = (2 * xmin[nb]) - xmax[(2 * nb) - 1 - i]
                        ymax[i] = ymax[(2 * nb) - 1 - i]
                        xmin[i] = (2 * xmin[nb]) - xmin[(2 * nb) - i]
                        ymin[i] = ymin[(2 * nb) - i]
                    else:
                        i = _range_end(i, nb, 1)
            else:
                i = 0
                for i in range(i, nb):
                    xmin[i] = -xmin[(2 * nb) - 1 - i]
                    ymin[i] = ymin[(2 * nb) - 1 - i]
                else:
                    i = _range_end(i, nb, 1)
                i = 0
                for i in range(i, nb - 1):
                    xmax[i] = -xmax[(2 * nb) - 2 - i]
                    ymax[i] = ymax[(2 * nb) - 2 - i]
                else:
                    i = _range_end(i, nb - 1, 1)
                xmax[nb - 1] = 0.0
                ymax[nb - 1] = y[0]
        nmin.v += nb - 1
        nmax.v += nb - 1
        if xmax[nmax.v] < xmin[nmin.v]:
            if y[self.N - 1] < ymax[nmax.v]:
                if ((2 * xmin[nmin.v]) - xmax[nmax.v - nb + 1]) < (self.N - 1):
                    i = 0
                    for i in range(i, nb):
                        xmax[nmax.v + 1 + i] = (2 * (self.N - 1)) - xmax[nmax.v - i]
                        ymax[nmax.v + 1 + i] = ymax[nmax.v - i]
                        xmin[nmin.v + 1 + i] = (2 * (self.N - 1)) - xmin[nmin.v - i]
                        ymin[nmin.v + 1 + i] = ymin[nmin.v - i]
                    else:
                        i = _range_end(i, nb, 1)
                else:
                    i = 0
                    for i in range(i, nb):
                        xmax[nmax.v + 1 + i] = (2 * xmin[nmin.v]) - xmax[nmax.v - i]
                        ymax[nmax.v + 1 + i] = ymax[nmax.v - i]
                        xmin[nmin.v + 1 + i] = (2 * xmin[nmin.v]) - xmin[nmin.v - 1 - i]
                        ymin[nmin.v + 1 + i] = ymin[nmin.v - 1 - i]
                    else:
                        i = _range_end(i, nb, 1)
            else:
                i = 0
                for i in range(i, nb):
                    xmin[nmin.v + 1 + i] = (2 * (self.N - 1)) - xmin[nmin.v - i]
                    ymin[nmin.v + 1 + i] = ymin[nmin.v - i]
                else:
                    i = _range_end(i, nb, 1)
                i = 0
                for i in range(i, nb - 1):
                    xmax[nmax.v + 2 + i] = (2 * (self.N - 1)) - xmax[nmax.v - i]
                    ymax[nmax.v + 2 + i] = ymax[nmax.v - i]
                else:
                    i = _range_end(i, nb - 1, 1)
                xmax[nmax.v + 1] = self.N - 1
                ymax[nmax.v + 1] = y[self.N - 1]
        else:
            if y[self.N - 1] > ymin[nmin.v]:
                if ((2 * xmax[nmax.v]) - xmin[nmin.v - nb + 1]) < (self.N - 1):
                    i = 0
                    for i in range(i, nb):
                        xmax[nmax.v + 1 + i] = (2 * (self.N - 1)) - xmax[nmax.v - i]
                        ymax[nmax.v + 1 + i] = ymax[nmax.v - i]
                        xmin[nmin.v + 1 + i] = (2 * (self.N - 1)) - xmin[nmin.v - i]
                        ymin[nmin.v + 1 + i] = ymin[nmin.v - i]
                    else:
                        i = _range_end(i, nb, 1)
                else:
                    i = 0
                    for i in range(i, nb):
                        xmax[nmax.v + 1 + i] = (2 * xmax[nmax.v]) - xmax[nmax.v - 1 - i]
                        ymax[nmax.v + 1 + i] = ymax[nmax.v - 1 - i]
                        xmin[nmin.v + 1 + i] = (2 * xmax[nmax.v]) - xmin[nmin.v - i]
                        ymin[nmin.v + 1 + i] = ymin[nmin.v - i]
                    else:
                        i = _range_end(i, nb, 1)
            else:
                i = 0
                for i in range(i, nb):
                    xmax[nmax.v + 1 + i] = (2 * (self.N - 1)) - xmax[nmax.v - i]
                    ymax[nmax.v + 1 + i] = ymax[nmax.v - i]
                else:
                    i = _range_end(i, nb, 1)
                i = 0
                for i in range(i, nb - 1):
                    xmin[nmin.v + 2 + i] = (2 * (self.N - 1)) - xmin[nmin.v - i]
                    ymin[nmin.v + 2 + i] = ymin[nmin.v - i]
                else:
                    i = _range_end(i, nb - 1, 1)
                xmin[nmin.v + 1] = self.N - 1
                ymin[nmin.v + 1] = y[self.N - 1]
        nmin.v = nmin.v + nb + 1
        nmax.v = nmax.v + nb + 1
        return ret
    def SplineInterp(self, x, y, n, x2, y2, btype=0):
        i = 0
        n2 = 0
        intervalindex = 0
        pointindex = 0
        havetoadvance = False
        c0 = 0.0
        c1 = 0.0
        c2 = 0.0
        c3 = 0.0
        a = 0.0
        bb = 0.0
        w = 0.0
        w2 = 0.0
        w3 = 0.0
        fa = 0.0
        fb = 0.0
        da = 0.0
        db = 0.0
        t = 0.0
        a1 = Arr(0, 0.0)
        a2 = Arr(0, 0.0)
        a3 = Arr(0, 0.0)
        b = Arr(0, 0.0)
        d = Arr(0, 0.0)
        n2 = ArraySize(x2)
        if (((n > ArraySize(x) or n > ArraySize(y)) or n2 > ArraySize(y2)) or n < 2) or n2 < 1:
            Print('CEMD::SplineInterp', ': Error! Arguments has wrong size.')
            return -1
        ArrayInitialize(y2, 0)
        if ArrayResize(a1, n) != n:
            Print('CEMD::SplineInterp', ': Error! ArrayResize() error.')
            return -2
        if ArrayResize(a2, n) != n:
            Print('CEMD::SplineInterp', ': Error! ArrayResize() error.')
            return -2
        if ArrayResize(a3, n) != n:
            Print('CEMD::SplineInterp', ': Error! ArrayResize() error.')
            return -2
        if ArrayResize(b, n) != n:
            Print('CEMD::SplineInterp', ': Error! ArrayResize() error.')
            return -2
        if ArrayResize(d, n) != n:
            Print('CEMD::SplineInterp', ': Error! ArrayResize() error.')
            return -2
        i = 1
        for i in range(i, n - 2 + 1):
            a1[i] = x[i + 1] - x[i]
            a2[i] = 2 * (x[i + 1] - x[i - 1])
            a3[i] = x[i] - x[i - 1]
            b[i] = (_fdiv(3 * (y[i] - y[i - 1]), x[i] - x[i - 1]) * (x[i + 1] - x[i])) + (_fdiv(3 * (y[i + 1] - y[i]), x[i + 1] - x[i]) * (x[i] - x[i - 1]))
        else:
            i = _range_end(i, n - 2 + 1, 1)
        if btype == 1 and n == 2:
            d[0] = _fdiv(y[1] - y[0], x[1] - x[0])
            d[1] = d[0]
        else:
            if btype == 1:
                a1[0] = 0.0
                a2[0] = 1.0
                a3[0] = 1.0
                b[0] = _fdiv(2 * (y[1] - y[0]), x[1] - x[0])
                a1[n - 1] = 1.0
                a2[n - 1] = 1.0
                a3[n - 1] = 0.0
                b[n - 1] = _fdiv(2 * (y[n - 1] - y[n - 2]), x[n - 1] - x[n - 2])
            else:
                a1[0] = 0.0
                a2[0] = 2.0
                a3[0] = 1.0
                b[0] = _fdiv(3 * (y[1] - y[0]), x[1] - x[0])
                a1[n - 1] = 1.0
                a2[n - 1] = 2.0
                a3[n - 1] = 0.0
                b[n - 1] = _fdiv(3 * (y[n - 1] - y[n - 2]), x[n - 1] - x[n - 2])
            i = 1
            for i in range(i, n - 1 + 1):
                t = _fdiv(a1[i], a2[i - 1])
                a2[i] = a2[i] - (t * a3[i - 1])
                b[i] = b[i] - (t * b[i - 1])
            else:
                i = _range_end(i, n - 1 + 1, 1)
            d[n - 1] = _fdiv(b[n - 1], a2[n - 1])
            i = n - 2
            for i in range(i, 0 - 1, -1):
                d[i] = _fdiv(b[i] - (a3[i] * d[i + 1]), a2[i])
            else:
                i = _range_end(i, 0 - 1, -1)
        c0 = 0.0
        c1 = 0.0
        c2 = 0.0
        c3 = 0.0
        a = 0.0
        bb = 0.0
        intervalindex = -1
        pointindex = 0
        while True:
            if pointindex >= n2:
                break
            t = x2[pointindex]
            havetoadvance = False
            if intervalindex == -1:
                havetoadvance = True
            elif intervalindex < (n - 2):
                havetoadvance = t >= bb
            if havetoadvance:
                intervalindex = intervalindex + 1
                a = x[intervalindex]
                bb = x[intervalindex + 1]
                w = bb - a
                w2 = w * w
                w3 = w * w2
                fa = y[intervalindex]
                fb = y[intervalindex + 1]
                da = d[intervalindex]
                db = d[intervalindex + 1]
                c0 = fa
                c1 = da
                c2 = _fdiv((3 * (fb - fa)) - (2 * da * w) - (db * w), w2)
                c3 = _fdiv((2 * (fa - fb)) + (da * w) + (db * w), w3)
                continue
            t = t - a
            y2[pointindex] = c0 + (t * (c1 + (t * (c2 + (t * c3)))))
            pointindex = pointindex + 1
        return 0

__all__ = ['CEMD']
