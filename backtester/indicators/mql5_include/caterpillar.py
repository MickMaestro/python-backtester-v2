"""``SSA/CCaterpillar.mqh`` (Roman Korotchenko, 2016) — SSA ("caterpillar")
trend extraction — port.

The source builds the lag-``L`` trajectory matrix, decomposes it with
ALGLIB's ``CSingValueDecompose::RMatrixSVD`` and rebuilds the trend from the
eigen-triples ``ModeNUM1..ModeNUM2`` by diagonal averaging. The SVD here is
:func:`numpy.linalg.svd` (LAPACK), which returns the same singular values and
the same products ``u_k · s_k · v_kᵀ`` (singular vectors are only defined up
to sign, and the reconstruction does not depend on it). Everything else is
transcribed line by line.

Usage, as in the indicators::

    cat = CCaterpillar()
    cat.TrendSize(segment, lag)
    cat.DoAnalyse(data, segment, lag, eig_min, eig_max)
    trend = cat.Trend[:segment]
"""

from __future__ import annotations

import numpy as np

SERIA_DFLT_LENGTH = 32768


class CCaterpillar:
    def __init__(self):
        self.datCoeff = 1.0
        self.convMode = 1
        self.MASHEPSILON = 1e-15
        self.SignalEigNoiseLimit = 0
        self.EigNoiseValue = 2.0
        self.EIF_NUM_MAX = 400
        self.uneeded = 1
        self.vtneeded = 1
        self.addmem = 2
        self.m_serlen = 1024
        self.m_Lag = 0
        self.m_series = [0.0] * self.m_serlen
        self.m_convData = [0.0] * self.m_serlen
        self.vR = [0.0] * self.m_serlen
        self.Trend = [0.0] * self.m_serlen
        self.ModeNUM1 = 1
        self.ModeNUM2 = 10
        self.mTrajRow = 0
        self.mTrajCol = 0
        self.mTraj = np.zeros((0, 0))
        self.mU = np.zeros((0, 0))
        self.mV = np.zeros((0, 0))
        self.mS = np.zeros((0, 0))
        self.LV = np.zeros(0)
        self.EigenValues: list = []
        self.mEigVectorCount = 0
        self.mEigValueCount = 0
        self.mEigValueCtrl = 0
        self.firstValue = self.lastValue = self.AmplValue = 0.0

    @staticmethod
    def _grow(arr: list, size: int) -> None:
        if len(arr) < size:
            arr.extend([0.0] * (size - len(arr)))

    def TrendSize(self, segment: int, lag: int) -> None:
        self.m_serlen = segment
        self.m_Lag = lag
        for arr in (self.m_series, self.m_convData, self.vR, self.Trend):
            del arr[segment:]
            self._grow(arr, segment)

    def SetNoiseRegime(self, flag: int, PercentValue: float) -> None:
        self.SignalEigNoiseLimit = flag
        self.EigNoiseValue = PercentValue

    def TrajectoryMatrixFill(self, ser, serlen: int, lag: int) -> int:
        self.m_Lag = lag
        if len(ser) < 2 or serlen < 2:
            return 0
        N, L = serlen, lag
        K = N - L + 1
        self.mTrajRow, self.mTrajCol = L, K
        s = np.asarray(ser[: N], dtype=float)
        self.mTraj = np.array([s[j: j + K] for j in range(L)])
        return K

    def SVD(self, weightEigenValuesInPercent: float) -> int:
        U, S, VT = np.linalg.svd(self.mTraj[: self.mTrajRow, : self.mTrajCol], full_matrices=False)
        self.mU, self.LV, self.mV = U, S, VT
        NMax = min(self.mTrajRow, self.mTrajCol)
        sumVal = 0.0
        self.mEigVectorCount = 0
        for i in range(NMax):
            if abs(self.LV[i]) > self.MASHEPSILON:
                self.mEigVectorCount += 1
                sumVal += self.LV[i]
        if weightEigenValuesInPercent < self.MASHEPSILON:
            return self.mEigVectorCount
        minLevel = weightEigenValuesInPercent * 0.01
        self.mEigValueCount = self.mEigVectorCount
        cum = 0.0
        for i in range(self.mEigVectorCount):
            if self.SignalEigNoiseLimit == 1 and self.LV[i] / sumVal < minLevel:
                self.mEigValueCount = i
                break
            if self.SignalEigNoiseLimit == 2:
                cum = cum + self.LV[i]
                curLevel = cum / sumVal
                if (1 - curLevel) < minLevel:
                    self.mEigValueCount = i
                    break
        return self.mEigValueCount

    def Grouping(self, eigN0: int, eigN1: int | None = None) -> None:
        if eigN1 is None:                       # Grouping(int eigNum)
            eigN0, eigN1 = 0, eigN0 - 1
        eigMax = self.mEigVectorCount
        if eigN1 > eigMax - 1:
            eigN1 = eigMax - 1
        S = np.zeros((self.mTrajRow, self.mTrajCol))
        for k in range(eigN0, eigN1 + 1):
            S += np.outer(self.mU[:, k], self.mV[k, :]) * self.LV[k]
        self.mS = S

    def SkewDiagAvr(self) -> int:
        nrow, ncol = self.mTrajRow, self.mTrajCol
        L, K = nrow, ncol
        N = nrow + ncol - 1
        flagTransp = 0
        if nrow > ncol:
            flagTransp = 1
            L, K = ncol, nrow
        if len(self.vR) < N:
            self._grow(self.vR, 2 * N)
        mS = self.mS
        for k in range(1, L + 1):
            s = 0.0
            for j in range(1, k + 1):
                s += mS[j - 1][k - j] if not flagTransp else mS[k - j][j - 1]
            self.vR[k - 1] = s / k
        for k in range(L + 1, K):
            s = 0.0
            for j in range(1, L + 1):
                s += mS[j - 1][k - j] if not flagTransp else mS[k - j][j - 1]
            self.vR[k - 1] = s / L
        for k in range(K, N + 1):
            s = 0.0
            for j in range(k - K + 1, L + 1):
                s += mS[j - 1][k - j] if not flagTransp else mS[k - j][j - 1]
            self.vR[k - 1] = s / (N - k + 1)
        return N

    def RestoreTrend(self) -> int:
        self.Grouping(self.ModeNUM1 - 1, self.ModeNUM2 - 1)
        return self.SkewDiagAvr()

    def ForwardDataConversion(self, seria, serLength: int, convData: list, Mode: int) -> None:
        if len(convData) < serLength:
            self._grow(convData, 2 * serLength)
        self.lastValue = seria[serLength - 1]
        if Mode == 0:
            for i in range(serLength):
                convData[i] = self.datCoeff * seria[i]
        elif Mode == 1:
            self.AmplValue = seria[0]
            for i in range(1, serLength):
                self.AmplValue = max(self.AmplValue, seria[i])
            self.firstValue = seria[0] / self.AmplValue
            for i in range(serLength):
                convData[i] = seria[i] / self.AmplValue - self.firstValue

    def BackwardDataConversion(self, data, datlen: int, result: list, Mode: int) -> None:
        if len(result) < datlen:
            self._grow(result, 2 * datlen)
        if Mode == 0:
            for i in range(datlen):
                result[i] = data[i] / self.datCoeff
        elif Mode == 1:
            for i in range(datlen):
                result[i] = (self.firstValue + data[i]) * self.AmplValue

    def DoAnalyse(self, segmData, segmlen: int, lag: int, eigMin: int, eigMax: int) -> int:
        self.ModeNUM1 = eigMin
        self.ModeNUM2 = eigMax
        self.ForwardDataConversion(segmData, segmlen, self.m_convData, self.convMode)
        self.TrajectoryMatrixFill(self.m_convData, segmlen, lag)
        evLimPercent = self.EigNoiseValue if self.SignalEigNoiseLimit else 0.0
        self.mEigValueCtrl = self.SVD(evLimPercent)
        if self.mEigValueCtrl >= self.EIF_NUM_MAX:
            self.mEigValueCtrl = self.EIF_NUM_MAX
        if self.ModeNUM2 >= self.mEigValueCtrl:
            self.ModeNUM2 = self.mEigValueCtrl
        self.EigenValues = [float(v) for v in self.LV[: self.mEigValueCtrl]]
        self.RestoreTrend()
        self.BackwardDataConversion(self.vR, segmlen, self.Trend, self.convMode)
        return 1
