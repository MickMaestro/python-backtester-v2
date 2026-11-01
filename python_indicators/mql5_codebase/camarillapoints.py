"""Camarillapoints — converted from MQL5: MQL5 Indicators/Camarilla Points/Camarillapoints.mq5

Telegram Channel: https://t.me/fxstill\\n
Camarillapoints: Slawomir Bobrowski \\"Stocks & Commodities V. 31:3 (10-15)\\"
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 10}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1}, 'colors': {1: [2237106], 2: [2237106], 3: [255], 4: [255], 5: [13353215], 6: [8388608], 7: [8388608], 8: [16711680], 9: [16711680], 10: [15453831]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 2, 5: 1, 6: 1, 7: 1, 8: 2, 9: 2, 10: 1}, 'styles': {1: 1, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1, 7: 0, 8: 0, 9: 0, 10: 0}, 'labels': {1: 'S1 Buffer', 2: 'S2 Buffer', 3: 'S3 Buffer', 4: 'S4 Buffer', 5: 'S5 Buffer', 6: 'R1 Buffer', 7: 'R2 Buffer', 8: 'R3 Buffer', 9: 'R4 Buffer', 10: 'R5 Buffer'}, 'levels': [], 'description': ['Telegram Channel: https://t.me/fxstill\\n', 'Camarillapoints: Slawomir Bobrowski \\"Stocks & Commodities V. 31:3 (10-15)\\"'], 'name': 'Camarillapoints', 'source': 'MQL5 Indicators/Camarilla Points/Camarillapoints.mq5', 'folder': 'Camarilla Points', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
s1 = Arr(0, 0.0)
s2 = Arr(0, 0.0)
s3 = Arr(0, 0.0)
s4 = Arr(0, 0.0)
s5 = Arr(0, 0.0)
r1 = Arr(0, 0.0)
r2 = Arr(0, 0.0)
r3 = Arr(0, 0.0)
r4 = Arr(0, 0.0)
r5 = Arr(0, 0.0)
MINBAR = 5

class CPivotData(MqlObject):
    _q_fields = ('m_curCount', 'm_s1', 'm_s2', 'm_s3', 'm_s4', 'm_s5', 'm_r1', 'm_r2', 'm_r3', 'm_r4', 'm_r5', 'k1', 'k2', 'k3', 'k4')
    def __init__(self, *args):
        self.m_curCount = 0
        self.m_s1 = 0.0
        self.m_s2 = 0.0
        self.m_s3 = 0.0
        self.m_s4 = 0.0
        self.m_s5 = 0.0
        self.m_r1 = 0.0
        self.m_r2 = 0.0
        self.m_r3 = 0.0
        self.m_r4 = 0.0
        self.m_r5 = 0.0
        self.k1 = 0.0
        self.k2 = 0.0
        self.k3 = 0.0
        self.k4 = 0.0
    def CPivotData(self):
        self.m_curCount = _idiv(DAYINSEC, PeriodSeconds())
        if self.m_curCount <= 1:
            Print('The indicator works on a timeframe below the D1')
        self.k1 = 1.1 / 2
        self.k2 = 1.1 / 4
        self.k3 = 1.1 / 6
        self.k4 = 1.1 / 12
    def InitResult(self):
        return (INIT_SUCCEEDED if (self.m_curCount > 1) else INIT_PARAMETERS_INCORRECT)
    def SetLasRates(self, r):
        rg = r.high - r.low
        self.m_r5 = _fdiv(r.high, r.low) * r.close
        self.m_r4 = r.close + (rg * self.k1)
        self.m_r3 = r.close + (rg * self.k2)
        self.m_r2 = r.close + (rg * self.k3)
        self.m_r1 = r.close + (rg * self.k4)
        self.m_s1 = r.close - (rg * self.k4)
        self.m_s2 = r.close - (rg * self.k3)
        self.m_s3 = r.close - (rg * self.k2)
        self.m_s4 = r.close - (rg * self.k1)
        self.m_s5 = r.close - (self.m_r5 - r.close)
    def FillBuffers(self, shift):
        s1[shift] = self.m_s1
        s2[shift] = self.m_s2
        s3[shift] = self.m_s3
        s4[shift] = self.m_s4
        s5[shift] = self.m_s5
        r1[shift] = self.m_r1
        r2[shift] = self.m_r2
        r3[shift] = self.m_r3
        r4[shift] = self.m_r4
        r5[shift] = self.m_r5

def OnInit():
    SetIndexBuffer(0, s1, INDICATOR_DATA)
    SetIndexBuffer(1, s2, INDICATOR_DATA)
    SetIndexBuffer(2, s3, INDICATOR_DATA)
    SetIndexBuffer(3, s4, INDICATOR_DATA)
    SetIndexBuffer(4, s5, INDICATOR_DATA)
    SetIndexBuffer(5, r1, INDICATOR_DATA)
    SetIndexBuffer(6, r2, INDICATOR_DATA)
    SetIndexBuffer(7, r3, INDICATOR_DATA)
    SetIndexBuffer(8, r4, INDICATOR_DATA)
    SetIndexBuffer(9, r5, INDICATOR_DATA)
    ArraySetAsSeries(s1, True)
    ArraySetAsSeries(s2, True)
    ArraySetAsSeries(s3, True)
    ArraySetAsSeries(s4, True)
    ArraySetAsSeries(s5, True)
    ArraySetAsSeries(r1, True)
    ArraySetAsSeries(r2, True)
    ArraySetAsSeries(r3, True)
    ArraySetAsSeries(r4, True)
    ArraySetAsSeries(r5, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Camarillapoints')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def GetValue(h, l, c, t, shift):
    if isNewDay(t[shift], t[shift + 1]):
        d = iBarShift(Symbol(), PERIOD_D1, t[shift])
        GetDay(d + 1)
    cPivot.FillBuffers(shift)

def GetDay(shift):
    mrt = Arr(1, 0, dyn=False, factory=MqlRates)
    if CopyRates(Symbol(), PERIOD_D1, shift, 1, mrt) != 1:
        Print(' Error in CopyRates: ', GetLastError(), ' for day: ', shift)
        return False
    cPivot.SetLasRates(mrt[0])
    return True

def isNewDay(now, prv):
    global _s_isNewDay_tmp
    if _s_isNewDay_tmp == now:
        return False
    _s_isNewDay_tmp = now
    dn = _idiv(now, DAYINSEC)
    dp = _idiv(prv, DAYINSEC)
    return dn != dp

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < MINBAR:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        pass
    elif limit == 1:
        GetValue(high, low, close, time, 1)
        return rates_total
    elif limit > 1:
        if not GetDay(1):
            return 0
        ArrayInitialize(s1, EMPTY_VALUE)
        ArrayInitialize(s2, EMPTY_VALUE)
        ArrayInitialize(s3, EMPTY_VALUE)
        ArrayInitialize(s4, EMPTY_VALUE)
        ArrayInitialize(s5, EMPTY_VALUE)
        ArrayInitialize(r1, EMPTY_VALUE)
        ArrayInitialize(r2, EMPTY_VALUE)
        ArrayInitialize(r3, EMPTY_VALUE)
        ArrayInitialize(r4, EMPTY_VALUE)
        ArrayInitialize(r5, EMPTY_VALUE)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(high, low, close, time, i)
        return rates_total
    GetValue(high, low, close, time, 0)
    return rates_total

# ---- global variables initialised from expressions
DAYINSEC = PeriodSeconds(PERIOD_D1)  # 86400;
cPivot = _alloc(CPivotData)
cPivot.__init__()

# ---- static local variables
_s_isNewDay_tmp = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Camarillapoints(_MQL5Indicator):
    name = 'Camarillapoints'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

