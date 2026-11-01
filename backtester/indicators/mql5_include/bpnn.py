"""``BPNN_MQL.mqh`` + ``BPNN_MQL_IMPL.mqh`` — a back-propagation neural network
trained with RPROP (resilient propagation) — line-by-line port.

``BPNN_MQL.mqh`` declares the ``Train``/``Test`` API (normally ``#import``\\ ed
from ``BPNN_MQL.ex5``); ``BPNN_MQL_IMPL.mqh`` is the implementation, embedded
when ``BPNN_LIBRARY`` is defined. Both map to this module.

Arrays are flat lists in the source's layout: ``inpTrain[i*nin + j]``,
``outTarget[i*nout + j]``; weights are listed layer by layer, neuron by
neuron, bias last. Activation functions (``AFT``): 0 = logistic sigmoid,
1 = tanh, 2 = x/(1+|x|). ``OAF`` = 1 applies it to the output layer too.

Randomness: the source seeds C ``rand()`` with ``GetTickCount()``, so in MT5
every training run starts from different weights. Here the initial weights
come from :mod:`random` with an optional ``seed`` (``None`` = unseeded, like
MT5); they are drawn as ``0.6*(rand()/32767 - 0.5)`` from the same 0…32767
integer range. Pass ``UEW = 1`` with ``extInitWt`` for reproducible runs.

``ValidationSet(Percent, MseRatio, BadEpochCountPercent)`` sets the early-
stopping globals, as the exported MQL5 function does.
"""

from __future__ import annotations

import math
import random

from .mql_runtime import idiv

NN_STATE_ABORTED = -1
NN_STATE_UNDEFINED = 0
NN_STATE_TRAINED_BY_VALIDATION = 1
NN_STATE_TRAINED_BY_ACCURACY = 2
NN_STATE_TRAINED_BY_EPOCH_LIMIT = 3

ValidationPercent = 0
TrainValidationMseRatio = 0
EpochPercent = 1


class NNStatus:
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __repr__(self):
        return f"NNStatus({self.code}, {self.message!r})"


def ValidationSet(Percent: int, MseRatio: int, BadEpochCountPercent: int) -> None:
    global ValidationPercent, TrainValidationMseRatio, EpochPercent
    ValidationPercent = int(Percent)
    TrainValidationMseRatio = int(MseRatio)
    EpochPercent = int(BadEpochCountPercent)


def _sign(val: float) -> int:
    if val < 0.0:
        return -1
    if val == 0.0:
        return 0
    return 1


class NN:
    def __init__(self, nl: int, sz, aft: int, oaf: int, uew: int, extWt, seed=None):
        self.AFT = aft
        self.OAF = oaf
        self.d0 = 0.02
        self.dmin = 0.0
        self.dmax = 50.0
        self.plus = 1.2
        self.minus = 0.8
        self.numl = nl
        self.lsize = [int(sz[i]) for i in range(nl)]
        L = self.lsize
        self.out = [[0.0] * L[i] for i in range(nl)]
        self.delta = [[0.0] * L[i] if i else [] for i in range(nl)]

        def cube(fill):
            return [[[fill] * (L[i - 1] + 1) for _ in range(L[i])] if i else [] for i in range(nl)]

        self.w = cube(0.0)
        self.d = cube(self.d0)
        self.g = cube(0.0)
        self.gSign = cube(0)
        rng = random.Random(seed)
        iw = 0
        for i in range(1, nl):
            for j in range(L[i]):
                for k in range(L[i - 1] + 1):
                    if uew == 0:
                        self.w[i][j][k] = 0.6 * (rng.randint(0, 32767) / 32767.0 - 0.5)
                    else:
                        self.w[i][j][k] = extWt[iw]
                        iw += 1

    def af(self, x: float) -> float:
        if self.AFT == 1:
            tmp = 2.0 * x
            if tmp >= 0:
                tmp = math.exp(-tmp)
                return (1.0 - tmp) / (1.0 + tmp)
            tmp = math.exp(tmp)
            return (tmp - 1.0) / (tmp + 1.0)
        if self.AFT == 2:
            return x / (1.0 + abs(x))
        if x >= 0:
            return 1.0 / (1.0 + math.exp(-x))
        tmp = math.exp(x)
        return tmp / (tmp + 1.0)

    def afDeriv(self, t: float) -> float:
        if self.AFT == 1:
            return 2 * (1 - t * t)
        if self.AFT == 2:
            return (1.0 - abs(t)) ** 2
        return t * (1.0 - t)

    def Out(self, j: int) -> float:
        return self.out[self.numl - 1][j]

    def Wt(self, i: int, j: int, k: int) -> float:
        return self.w[i][j][k]

    def ffwd(self, inp) -> None:
        L = self.lsize
        for j in range(L[0]):
            self.out[0][j] = inp[j]
        for i in range(1, self.numl):
            prev = self.out[i - 1]
            for j in range(L[i]):
                wij = self.w[i][j]
                s = 0.0
                for k in range(L[i - 1]):
                    s += prev[k] * wij[k]
                s += wij[L[i - 1]]
                if i == self.numl - 1 and self.OAF == 0:
                    self.out[i][j] = s
                else:
                    self.out[i][j] = self.af(s)

    def xprop(self, inp, tgt, ntr: int, nep: int, maxMSE: float) -> NNStatus:
        L, nl = self.lsize, self.numl
        MSE = 0.0
        prevMSE = 1.0e9
        MSEM = MSET = MSEMT = 0.0
        minMSETep = 0
        status = ""
        ntr_learn = idiv(ntr * (100 - ValidationPercent), 100)
        minMSET = 1000000.0
        ep = 0
        while ep < nep:
            MSE = 0.0
            MSEM = 0.0
            for s in range(ntr_learn):
                self.ffwd(inp[s])
                MSEs = 0.0
                for j in range(L[nl - 1]):
                    self.delta[nl - 1][j] = tgt[s][j] - self.out[nl - 1][j]
                    MSEs += self.delta[nl - 1][j] ** 2
                    if self.OAF == 1:
                        self.delta[nl - 1][j] *= self.afDeriv(self.out[nl - 1][j])
                MSEs = math.sqrt(MSEs)
                MSE += MSEs
                if MSEs > MSEM:
                    MSEM = MSEs
                for i in range(nl - 2, 0, -1):
                    for j in range(L[i]):
                        acc = 0.0
                        for k in range(L[i + 1]):
                            acc += self.delta[i + 1][k] * self.w[i + 1][k][j]
                        self.delta[i][j] = self.afDeriv(self.out[i][j]) * acc
                for i in range(1, nl):
                    for j in range(L[i]):
                        gij = self.g[i][j]
                        for k in range(L[i - 1] + 1):
                            if s == 0:
                                gij[k] = 0.0
                            if k == L[i - 1]:
                                gij[k] -= self.delta[i][j]
                            else:
                                gij[k] -= self.delta[i][j] * self.out[i - 1][k]
            MSE /= ntr_learn
            if ValidationPercent > 0:
                MSET = 0.0
                MSEMT = 0.0
                for s in range(ntr_learn, ntr):
                    self.ffwd(inp[s])
                    MSEsT = 0.0
                    for j in range(L[nl - 1]):
                        self.delta[nl - 1][j] = tgt[s][j] - self.out[nl - 1][j]
                        MSEsT += self.delta[nl - 1][j] ** 2
                        if self.OAF == 1:
                            self.delta[nl - 1][j] *= self.afDeriv(self.out[nl - 1][j])
                    MSEsT = math.sqrt(MSEsT)
                    MSET += MSEsT
                    if MSEsT > MSEMT:
                        MSEMT = MSEsT
                MSET /= (ntr - ntr_learn)
            else:
                MSET = MSE
                MSEMT = MSEM
            if MSET < minMSET:
                minMSET = MSET
                minMSETep = ep
            elif (ep - minMSETep > idiv(nep * EpochPercent, 100)
                  and (MSET > TrainValidationMseRatio * minMSET and TrainValidationMseRatio > 0)):
                return NNStatus(NN_STATE_TRAINED_BY_VALIDATION,
                                f"Validation stop after epoch [{ep + 1}]; max.err. {MSEM:E}, ave.err "
                                f"{MSE:E}, max.v.err. {MSEMT:E}, ave.v. MSE {MSET:E}")
            if MSET < maxMSE:
                return NNStatus(NN_STATE_TRAINED_BY_ACCURACY,
                                f"Network trained in [{ep + 1}] epochs with max.err. {MSEMT:E}, ave. MSE {MSET:E}")
            for i in range(1, nl):
                for j in range(L[i]):
                    gij, gs, dij, wij = self.g[i][j], self.gSign[i][j], self.d[i][j], self.w[i][j]
                    for k in range(L[i - 1] + 1):
                        prod = gij[k] * gs[k]
                        if prod > 0.0:
                            dij[k] = min(dij[k] * self.plus, self.dmax)
                            gs[k] = _sign(gij[k])
                            wij[k] -= dij[k] * gs[k]
                        elif prod < 0.0:
                            if MSE > prevMSE:
                                wij[k] += dij[k] * gs[k]
                            dij[k] = max(dij[k] * self.minus, self.dmin)
                            gs[k] = 0
                        else:
                            gs[k] = _sign(gij[k])
                            wij[k] -= dij[k] * gs[k]
            prevMSE = MSE
            status = f"Epoch {ep + 1}, max. {MSEM:E}, ave. {MSE:E}, max.t. {MSEMT:E}, ave.t. {MSET:E}"
            ep += 1
        if ep == nep:
            return NNStatus(NN_STATE_TRAINED_BY_EPOCH_LIMIT,
                            f"Reached the limit of [{nep}] epochs with max.err. {MSEM:E}, ave.err {MSE:E}, "
                            f"max.v.err. {MSEMT:E}, ave.v. MSE {MSET:E}")
        return NNStatus(NN_STATE_UNDEFINED, status)


def Train(inpTrain, outTarget, outTrain, ntr, UEW, extInitWt, trainedWt, numLayers, lSz,
          AFT, OAF, nep, maxMSE, seed=None) -> NNStatus:
    """Train on ``ntr`` samples; fills ``outTrain`` (network outputs on the
    training set) and ``trainedWt`` (lists, resized as needed)."""
    nin = lSz[0]
    nout = lSz[numLayers - 1]
    trainData = [[inpTrain[i * nin + j] for j in range(nin)] for i in range(ntr)]
    targetData = [[outTarget[i * nout + j] for j in range(nout)] for i in range(ntr)]
    bp = NN(numLayers, lSz, AFT, OAF, UEW, extInitWt, seed=seed)
    result = bp.xprop(trainData, targetData, ntr, nep, maxMSE)
    need = ntr * nout
    if len(outTrain) < need:
        outTrain.extend([0.0] * (need - len(outTrain)))
    for i in range(ntr):
        bp.ffwd(trainData[i])
        for j in range(nout):
            outTrain[i * nout + j] = bp.Out(j)
    weights = [bp.Wt(i, j, k) for i in range(1, numLayers) for j in range(lSz[i])
               for k in range(lSz[i - 1] + 1)]
    if len(trainedWt) < len(weights):
        trainedWt.extend([0.0] * (len(weights) - len(trainedWt)))
    trainedWt[: len(weights)] = weights
    return result


def Test(inpTest, outTest, ntt, extInitWt, numLayers, lSz, AFT, OAF) -> None:
    """Run ``ntt`` samples through a network with weights ``extInitWt``."""
    nin = lSz[0]
    nout = lSz[numLayers - 1]
    bp = NN(numLayers, lSz, AFT, OAF, 1, extInitWt)
    need = ntt * nout
    if len(outTest) < need:
        outTest.extend([0.0] * (need - len(outTest)))
    for i in range(ntt):
        bp.ffwd([inpTest[i * nin + j] for j in range(nin)])
        for j in range(nout):
            outTest[i * nout + j] = bp.Out(j)
