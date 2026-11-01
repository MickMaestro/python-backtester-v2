"""CCaterpillar.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class CCaterpillar(MqlObject):
    _q_fields = ('MASHEPSILON', 'Shift0', 'SignalEigNoiseLimit', 'EigNoiseValue', 'EIF_NUM_MAX', 'm_series', 'm_serlen', 'm_Lag', 'mTraj', 'mU', 'mV', 'LV', 'mTrajRow', 'mTrajCol', 'mEigVectorCount', 'mEigValueCount', 'mEigValueCtrl', 'mS', 'vR', 'EigenValues', 'uneeded', 'vtneeded', 'addmem', 'datCoeff', 'firstValue', 'lastValue', 'AmplValue', 'm_convData', 'convMode', 'ModeNUM1', 'ModeNUM2', 'Trend')
    def __init__(self):
        self.MASHEPSILON = 0.0
        self.Shift0 = 0.0
        self.SignalEigNoiseLimit = 0
        self.EigNoiseValue = 0.0
        self.EIF_NUM_MAX = 0
        self.m_series = Arr(0, 0.0)
        self.m_serlen = 0
        self.m_Lag = 0
        self.mTraj = CMatrixDouble()
        self.mU = CMatrixDouble()
        self.mV = CMatrixDouble()
        self.LV = Arr(0, 0.0)
        self.mTrajRow = 0
        self.mTrajCol = 0
        self.mEigVectorCount = 0
        self.mEigValueCount = 0
        self.mEigValueCtrl = 0
        self.mS = CMatrixDouble()
        self.vR = Arr(0, 0.0)
        self.EigenValues = Arr(0, 0.0)
        self.uneeded = 0
        self.vtneeded = 0
        self.addmem = 0
        self.datCoeff = 0.0
        self.firstValue = 0.0
        self.lastValue = 0.0
        self.AmplValue = 0.0
        self.m_convData = Arr(0, 0.0)
        self.convMode = 0
        self.ModeNUM1 = 0
        self.ModeNUM2 = 0
        self.Trend = Arr(0, 0.0)
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
        ArrayResize(self.m_series, self.m_serlen, 32768)
        ArrayResize(self.m_convData, self.m_serlen, 32768)
        ArrayResize(self.vR, self.m_serlen, 32768)
        ArrayResize(self.Trend, self.m_serlen, 32768)
        self.ModeNUM1 = 1
        self.ModeNUM2 = 10
        self.mTrajRow = 0
        self.mTrajCol = 0
    def _q_dtor(self):
        ArrayFree(self.m_series)
        ArrayFree(self.m_convData)
        ArrayFree(self.vR)
        ArrayFree(self.Trend)
    def TrajectoryMatrixFill(self, ser, serlen, lag):
        self.m_Lag = lag
        if ArraySize(ser) < 2 or serlen < 2:
            return 0
        N = serlen
        L = lag
        K = N - L + 1
        if self.mTrajRow < L or self.mTrajCol < K:
            self.mTraj.Resize(L, K)
        self.mTrajRow = L
        self.mTrajCol = K
        for j in range(0, L):
            for k in range(0, K):
                self.mTraj[j].Set(k, ser[k + j])
        return K
    def SVD(self, weightEigenValuesInPercent):
        if self.mU.Size() < self.mTrajRow or self.mU[0].Size() < self.mTrajCol:
            self.mU.Resize(self.mTrajRow, self.mTrajCol)
        if self.mV.Size() < self.mTrajCol or self.mU[0].Size() < self.mTrajRow:
            self.mV.Resize(self.mTrajCol, self.mTrajRow)
        CSingValueDecompose.RMatrixSVD(self.mTraj, self.mTrajRow, self.mTrajCol, self.uneeded, self.vtneeded, self.addmem, self.LV, self.mU, self.mV)
        NMax = MathMin(self.mTrajRow, self.mTrajCol)
        sumVal = 0.0
        self.mEigVectorCount = 0
        for i in range(0, NMax):
            if fabs(self.LV[i]) > self.MASHEPSILON:
                self.mEigVectorCount += 1
                sumVal += self.LV[i]
        if weightEigenValuesInPercent < self.MASHEPSILON:
            return self.mEigVectorCount
        minLevel = weightEigenValuesInPercent * 0.01
        curLevel = 0.0
        cum = 0.0
        self.mEigValueCount = self.mEigVectorCount
        cum = 0.0
        for i in range(0, self.mEigVectorCount):
            if self.SignalEigNoiseLimit == 1 and _fdiv(self.LV[i], sumVal) < minLevel:
                self.mEigValueCount = i
                break
            if self.SignalEigNoiseLimit == 2:
                cum = cum + self.LV[i]
                curLevel = _fdiv(cum, sumVal)
                if (1 - curLevel) < minLevel:
                    self.mEigValueCount = i
                    break
        return self.mEigValueCount
    def Grouping_2(self, eigN0, eigN1):
        eigMax = self.mEigVectorCount
        Unrow = self.mTrajRow
        Vnrow = self.mTrajCol
        if eigN1 > (eigMax - 1):
            eigN1 = eigMax - 1
        if self.mS.Size() < self.mTrajRow or self.mS[0].Size() < self.mTrajCol:
            self.mS.Resize(Unrow, Vnrow)
        sum_ = 0.0
        for m in range(0, Unrow):
            for n in range(0, Vnrow):
                sum_ = 0.0
                for k in range(eigN0, eigN1 + 1):
                    sum_ = sum_ + (self.mU[m][k] * self.mV[k][n] * self.LV[k])
                self.mS[m].Set(n, sum_)
    def Grouping_1(self, eigNum):
        self.Grouping_2(0, eigNum - 1)
    def SkewDiagAvr(self):
        nrow = self.mTrajRow
        ncol = self.mTrajCol
        L = nrow
        K = ncol
        N = nrow + ncol - 1
        k = 0
        j = 0
        flagTransp = 0
        s = 0.0
        if nrow > ncol:
            flagTransp = 1
            L = ncol
            K = nrow
        if ArraySize(self.vR) < N:
            ArrayResize(self.vR, 2 * N, 32768)
        k = 1
        for k in range(k, L + 1):
            s = 0.0
            j = 1
            for j in range(j, k + 1):
                if not flagTransp:
                    s += self.mS[j - 1][k - j]
                else:
                    s += self.mS[k - j][j - 1]
            else:
                j = _range_end(j, k + 1, 1)
            s = _fdiv(s, k)
            self.vR[k - 1] = s
        else:
            k = _range_end(k, L + 1, 1)
        k = L + 1
        for k in range(k, K):
            s = 0.0
            j = 1
            for j in range(j, L + 1):
                if not flagTransp:
                    s += self.mS[j - 1][k - j]
                else:
                    s += self.mS[k - j][j - 1]
            else:
                j = _range_end(j, L + 1, 1)
            s = _fdiv(s, L)
            self.vR[k - 1] = s
        else:
            k = _range_end(k, K, 1)
        k = K
        for k in range(k, N + 1):
            s = 0.0
            j = k - K + 1
            for j in range(j, L + 1):
                if not flagTransp:
                    s += self.mS[j - 1][k - j]
                else:
                    s += self.mS[k - j][j - 1]
            else:
                j = _range_end(j, L + 1, 1)
            s = _fdiv(s, N - k + 1)
            self.vR[k - 1] = s
        else:
            k = _range_end(k, N + 1, 1)
        return N
    def RestoreTrend(self):
        efMin = 0
        efMax = 0
        N = 0
        efMin = self.ModeNUM1 - 1
        efMax = self.ModeNUM2 - 1
        self.Grouping_2(efMin, efMax)
        N = self.SkewDiagAvr()
        return N
    def ForwardDataConversion(self, seria, serLength, convData, Mode):
        i = 0
        if ArraySize(convData) < serLength:
            ArrayResize(convData, 2 * serLength, 32768)
        self.lastValue = seria[serLength - 1]
        _sw1 = Mode
        if _sw1 == 0:
            i = 0
            for i in range(i, serLength):
                convData[i] = self.datCoeff * seria[i]
            else:
                i = _range_end(i, serLength, 1)
        elif _sw1 == 1:
            self.AmplValue = seria[0]
            i = 1
            for i in range(i, serLength):
                self.AmplValue = MathMax(self.AmplValue, seria[i])
            else:
                i = _range_end(i, serLength, 1)
            self.firstValue = _fdiv(seria[0], self.AmplValue)
            i = 0
            for i in range(i, serLength):
                convData[i] = _fdiv(seria[i], self.AmplValue) - self.firstValue
            else:
                i = _range_end(i, serLength, 1)
    def BackwardDataConversion(self, data, datlen, result, Mode):
        i = 0
        if ArraySize(result) < datlen:
            ArrayResize(result, 2 * datlen, 32768)
        _sw2 = Mode
        if _sw2 == 0:
            i = 0
            for i in range(i, datlen):
                result[i] = _fdiv(data[i], self.datCoeff)
            else:
                i = _range_end(i, datlen, 1)
        elif _sw2 == 1:
            i = 0
            for i in range(i, datlen):
                result[i] = (self.firstValue + data[i]) * self.AmplValue
            else:
                i = _range_end(i, datlen, 1)
    def TrendSize(self, segment, lag):
        self.m_serlen = segment
        self.m_Lag = lag
        ArrayResize(self.m_series, self.m_serlen, 32768)
        ArrayResize(self.m_convData, self.m_serlen, 32768)
        ArrayResize(self.vR, self.m_serlen, 32768)
        ArrayResize(self.Trend, self.m_serlen, 32768)
    def SetNoiseRegime(self, flag, PercentValue):
        self.SignalEigNoiseLimit = flag
        self.EigNoiseValue = PercentValue
    def DoAnalyse(self, segmData, segmlen, lag, eigMin, eigMax):
        evLimPercent = 0.0
        self.ModeNUM1 = eigMin
        self.ModeNUM2 = eigMax
        self.ForwardDataConversion(segmData, segmlen, self.m_convData, self.convMode)
        self.TrajectoryMatrixFill(self.m_convData, segmlen, lag)
        evLimPercent = (self.EigNoiseValue if self.SignalEigNoiseLimit else 0.0)
        self.mEigValueCtrl = self.SVD(evLimPercent)
        if self.mEigValueCtrl >= self.EIF_NUM_MAX:
            self.mEigValueCtrl = self.EIF_NUM_MAX
        if self.ModeNUM2 >= self.mEigValueCtrl:
            self.ModeNUM2 = self.mEigValueCtrl
        if ArraySize(self.EigenValues) < self.mEigValueCtrl:
            ArrayResize(self.EigenValues, 2 * self.mEigValueCtrl, self.EIF_NUM_MAX)
        for k in range(0, self.mEigValueCtrl):
            self.EigenValues[k] = self.LV[k]
        self.RestoreTrend()
        self.BackwardDataConversion(self.vR, segmlen, self.Trend, self.convMode)
        return 1

__all__ = ['CCaterpillar']
