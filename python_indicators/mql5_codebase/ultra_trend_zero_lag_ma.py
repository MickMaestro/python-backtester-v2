"""Ultra trend - zero lag ma — converted from MQL5: MQL5 Indicators/Ultra Trend - Zero Lag MA/Ultra trend - zero lag ma.mq5

Zero lag MA ultra trend
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 8}, 'colors': {1: [9498256, 11788021], 2: [11119017, 3329330, 42495], 3: [11119017, 3329330, 42495]}, 'widths': {2: 3, 3: 1}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Ultra trend +', 3: 'Ultra trend -'}, 'levels': [], 'description': ['Zero lag MA ultra trend'], 'name': 'Ultra trend - zero lag ma', 'source': 'MQL5 Indicators/Ultra Trend - Zero Lag MA/Ultra trend - zero lag ma.mq5', 'folder': 'Ultra Trend - Zero Lag MA', 'inputs': [{'mql': 'inpUtrPeriod', 'py': 'inpUtrPeriod', 'param': 'inpUtrPeriod', 'type': 'int', 'default': 3, 'label': 'Start period', 'sinput': False}, {'mql': 'inpProgression', 'py': 'inpProgression', 'param': 'inpProgression', 'type': 'int', 'default': 5, 'label': 'Step', 'sinput': False}, {'mql': 'inpInstances', 'py': 'inpInstances', 'param': 'inpInstances', 'type': 'int', 'default': 30, 'label': 'Instances', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'int', 'default': 5, 'label': 'Ultra trend smoothing period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpUtrPeriod = _input('inpUtrPeriod', 3)  # Start period
inpProgression = _input('inpProgression', 5)  # Step
inpInstances = _input('inpInstances', 30)  # Instances
inpSmooth = _input('inpSmooth', 5)  # Ultra trend smoothing period
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
valp = Arr(0, 0.0)
valpc = Arr(0, 0.0)
valm = Arr(0, 0.0)
valmc = Arr(0, 0.0)

class CZeroLagMa(MqlObject):
    _q_fields = ('m_size', 'm_wrk')
    def __init__(self):
        self.m_size = 0
        self.m_wrk = Arr(0, 0.0, dims=(2,))
        self.m_size = 0
        return
    def _q_dtor(self):
        return
    def CalculateValue(self, price, length, r, bars):
        if ArrayRange(self.m_wrk, 0) != bars:
            ArrayResize(self.m_wrk, bars)
        self.m_wrk[r][0] = price
        per = _int((length - 1.0) / 2.0)
        if r < (per + 1) or length <= 1:
            self.m_wrk[r][1] = price
        else:
            median = 0.0
            alpha = _fdiv(2.0, 1.0 + length)
            if _imod(_int(length), 2) == 0:
                median = (self.m_wrk[r - per][0] + self.m_wrk[r - per - 1][0]) / 2.0
            else:
                median = self.m_wrk[r - per][0]
            self.m_wrk[r][1] = self.m_wrk[r - 1][1] + (alpha * ((2.0 * price) - median - self.m_wrk[r - 1][1]))
        return self.m_wrk[r][1]

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, valp, INDICATOR_DATA)
    SetIndexBuffer(3, valpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, valm, INDICATOR_DATA)
    SetIndexBuffer(5, valmc, INDICATOR_COLOR_INDEX)
    ArrayResize(_iSmooth, inpInstances + 3)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Zero lag MA ultra trend  (' + _str(inpUtrPeriod) + ',' + _str(inpProgression) + ',' + _str(inpInstances) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    endLength = inpUtrPeriod + (inpProgression * inpInstances)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        valueUp = 0.0
        valueDn = 0.0
        k = inpUtrPeriod
        instance = 2
        while k <= endLength and i > 0:
            if _iSmooth[instance].CalculateValue(close[i - 1], k, i - 1, rates_total) < _iSmooth[instance].CalculateValue(close[i], k, i, rates_total):
                valueUp += 1
            else:
                valueDn += 1
            k += inpProgression
            instance += 1
        valp[i] = _iSmooth[0].CalculateValue(valueUp, inpSmooth, i, rates_total)
        valm[i] = _iSmooth[1].CalculateValue(valueDn, inpSmooth, i, rates_total)
        valpc[i] = (1 if (valp[i] > valm[i]) else 2)
        valmc[i] = valpc[i]
        fillu[i] = valp[i]
        filld[i] = valm[i]
        i += 1
    return i

# ---- global variables initialised from expressions
_iSmooth = Arr(0, 0, factory=CZeroLagMa)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UltraTrendZeroLagMa(_MQL5Indicator):
    name = 'Ultra trend - zero lag ma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpUtrPeriod': 3,  # Start period
        'inpProgression': 5,  # Step
        'inpInstances': 30,  # Instances
        'inpSmooth': 5,  # Ultra trend smoothing period
    }

