"""mba_channel — converted from MQL5: MQL5 Indicators/Momentum-based Adaptive Channel/mba_channel.mq5

Copyright: Copyright 2021, Yossy Nakata; Link: https://yossy-nakata.hateblo.jp; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, Yossy Nakata', 'link': 'https://yossy-nakata.hateblo.jp', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16748574]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'upper', 2: 'lower'}, 'levels': [], 'description': [], 'name': 'mba_channel', 'source': 'MQL5 Indicators/Momentum-based Adaptive Channel/mba_channel.mq5', 'folder': 'Momentum-based Adaptive Channel', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 20, 'label': 'Channel Period', 'sinput': False}, {'mql': 'InpVFactor', 'py': 'InpVFactor', 'param': 'InpVFactor', 'type': 'double', 'default': 0.5, 'label': 'Volatility Factor', 'sinput': False}, {'mql': 'InpVEmaPeriod', 'py': 'InpVEmaPeriod', 'param': 'InpVEmaPeriod', 'type': 'int', 'default': 200, 'label': 'Volatility Smoothing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FAST = 3  # Minimum Channel Period;
InpPeriod = _input('InpPeriod', 20)  # Channel Period
InpVFactor = _input('InpVFactor', 0.5)  # Volatility Factor
InpVEmaPeriod = _input('InpVEmaPeriod', 200)  # Volatility Smoothing
g_high = Arr(0, 0.0)
g_low = Arr(0, 0.0)
g_upper = Arr(0, 0.0)
g_lower = Arr(0, 0.0)
g_upper_i = Arr(0, 0.0)
g_lower_i = Arr(0, 0.0)
g_volat = Arr(0, 0.0)
g_start_time = 0

class MsVolatItem(MqlObject):
    _q_fields = ('main', 'adf', 'df3', 'df4', 'df5', 'df6', 'df8', 'df10', 'df13')
    def __init__(self, *args):
        self.main = 0.0
        self.adf = 0.0
        self.df3 = 0.0
        self.df4 = 0.0
        self.df5 = 0.0
        self.df6 = 0.0
        self.df8 = 0.0
        self.df10 = 0.0
        self.df13 = 0.0

class MsVolat(MqlObject):
    _q_fields = ('_begin_plot', '_alpha', '_sq3', '_sq4', '_sq5', '_sq6', '_sq8', '_sq10', '_sq13', '_buf', '_buf_size')
    def __init__(self):
        self._begin_plot = 0
        self._alpha = 0.0
        self._sq3 = 0.0
        self._sq4 = 0.0
        self._sq5 = 0.0
        self._sq6 = 0.0
        self._sq8 = 0.0
        self._sq10 = 0.0
        self._sq13 = 0.0
        self._buf = Arr(0, 0, factory=MsVolatItem)
        self._buf_size = 0
        self._begin_plot = 0
        self._alpha = 0.0
        self._sq3 = sqrt(3)
        self._sq4 = sqrt(4)
        self._sq5 = sqrt(5)
        self._sq6 = sqrt(6)
        self._sq8 = sqrt(8)
        self._sq10 = sqrt(10)
        self._sq13 = sqrt(13)
        return
    def _q_dtor(self):
        return
    def init(self, period):
        self._begin_plot = period + 1 + 13
        self._alpha = _fdiv(2.0, period + 1.0)
    def diff(self, lag, w, value, i):
        return _fdiv(MathAbs(value[i - lag] - value[i]), w)
    def calculate(self, value, i, bars, rslt):
        if self._buf_size < bars:
            self._buf_size = ArrayResize(self._buf, bars + 500, 2000)
        if self._buf_size == -1:
            return False
        if i <= 13:
            self._buf[i].main = EMPTY_VALUE
            return False
        self._buf[i].df3 = MsVolat.diff(self, 3, self._sq3, value, i)
        self._buf[i].df4 = MsVolat.diff(self, 4, self._sq4, value, i)
        self._buf[i].df5 = MsVolat.diff(self, 5, self._sq5, value, i)
        self._buf[i].df6 = MsVolat.diff(self, 6, self._sq6, value, i)
        self._buf[i].df8 = MsVolat.diff(self, 8, self._sq8, value, i)
        self._buf[i].df10 = MsVolat.diff(self, 10, self._sq10, value, i)
        self._buf[i].df13 = MsVolat.diff(self, 13, self._sq13, value, i)
        self._buf[i].adf = (self._buf[i].df3 + self._buf[i].df4 + self._buf[i].df5 + self._buf[i].df6 + self._buf[i].df8 + self._buf[i].df10 + self._buf[i].df13) / 7.0
        if i <= 14:
            self._buf[i].main = self._buf[i].adf
            return False
        self._buf[i].main = (self._alpha * self._buf[i].adf) + ((1.0 - self._alpha) * self._buf[i - 1].main)
        rslt.v = self._buf[i].main
        return True

def OnInit():
    global g_start_time
    SetIndexBuffer(0, g_upper, INDICATOR_DATA)
    SetIndexBuffer(1, g_lower, INDICATOR_DATA)
    SetIndexBuffer(2, g_high, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, g_low, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, g_volat, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, g_upper_i, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, g_lower_i, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArrayInitialize(g_upper, EMPTY_VALUE)
    ArrayInitialize(g_lower, EMPTY_VALUE)
    ArrayInitialize(g_upper_i, EMPTY_VALUE)
    ArrayInitialize(g_lower_i, EMPTY_VALUE)
    ArrayInitialize(g_high, EMPTY_VALUE)
    ArrayInitialize(g_low, EMPTY_VALUE)
    ArrayInitialize(g_volat, EMPTY_VALUE)
    m_msv.init(InpVEmaPeriod)
    g_start_time = 0
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global g_start_time
    i = 0
    pos = 0
    ArraySetAsSeries(time, False)
    ArraySetAsSeries(high, False)
    ArraySetAsSeries(low, False)
    ArraySetAsSeries(g_upper, False)
    ArraySetAsSeries(g_lower, False)
    ArraySetAsSeries(g_upper_i, False)
    ArraySetAsSeries(g_lower_i, False)
    ArraySetAsSeries(g_high, False)
    ArraySetAsSeries(g_low, False)
    ArraySetAsSeries(g_volat, False)
    pos = MathMax(prev_calculated - 1, 0)
    if prev_calculated == 0 or (rates_total > 0 and g_start_time != time[0]):
        ArrayInitialize(g_upper, EMPTY_VALUE)
        ArrayInitialize(g_lower, EMPTY_VALUE)
        ArrayInitialize(g_upper_i, EMPTY_VALUE)
        ArrayInitialize(g_lower_i, EMPTY_VALUE)
        ArrayInitialize(g_high, EMPTY_VALUE)
        ArrayInitialize(g_low, EMPTY_VALUE)
        ArrayInitialize(g_volat, EMPTY_VALUE)
        g_start_time = time[0]
        pos = 0
    v = Box(0.0)
    i = pos
    for i in range(i, rates_total):
        if not m_msv.calculate(close, i, rates_total, v):
            continue
        g_volat[i] = v.v
        if i < (InpPeriod + 3):
            g_high[i] = high[i]
            g_low[i] = low[i]
            g_upper[i] = high[i]
            g_lower[i] = low[i]
            g_upper_i[i] = i
            g_lower_i[i] = i
            continue
        g_high[i] = (high[i] if (g_high[i - 1] <= high[i]) else high[ArrayMaximum(high, i - (FAST - 1), FAST)])
        g_low[i] = (low[i] if (g_low[i - 1] >= low[i]) else low[ArrayMinimum(low, i - (FAST - 1), FAST)])
        width = g_volat[i] * InpVFactor
        if g_upper[i - 1] <= high[i]:
            g_upper[i] = high[i]
            g_upper_i[i] = i
        else:
            h_pos = _int(g_upper_i[i - 1])
            lookback = 1 + i - h_pos
            dist = distance(width, h_pos, i, g_high[h_pos], g_high[i])
            if (InpPeriod * width) < dist:
                len_ = MathMax(1, lookback - 1)
                max_i = ArrayMaximum(high, i - (len_ - 1), len_)
                g_upper[i] = high[max_i]
                g_upper_i[i] = max_i
            else:
                g_upper[i] = g_upper[i - 1]
                g_upper_i[i] = g_upper_i[i - 1]
        if g_lower[i - 1] >= low[i]:
            g_lower[i] = low[i]
            g_lower_i[i] = i
        else:
            l_pos = _int(g_lower_i[i - 1])
            lookback = 1 + i - l_pos
            dist = distance(width, l_pos, i, g_low[l_pos], g_low[i])
            if (InpPeriod * width) < dist:
                len_ = MathMax(1, lookback - 1)
                min_i = ArrayMinimum(low, i - (len_ - 1), len_)
                g_lower[i] = low[min_i]
                g_lower_i[i] = min_i
            else:
                g_lower[i] = g_lower[i - 1]
                g_lower_i[i] = g_lower_i[i - 1]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def distance(v, x1, x2, y1, y2):
    return MathSqrt(MathPow(v * (x2 - x1), 2) + MathPow(y2 - y1, 2))

# ---- global variables initialised from expressions
m_msv = _alloc(MsVolat)
m_msv.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MbaChannel(_MQL5Indicator):
    name = 'mba_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Channel Period
        'InpVFactor': 0.5,  # Volatility Factor
        'InpVEmaPeriod': 200,  # Volatility Smoothing
    }

