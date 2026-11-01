"""DMH — converted from MQL5: MQL5 Indicators/DMH/DMH.mq5

Directional Movement using Hann windowing
Based on work published by John Ehlers
Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16760576, 5275647]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'DMH'}, 'levels': [], 'description': ['Directional Movement using Hann windowing', 'Based on work published by John Ehlers'], 'name': 'DMH', 'source': 'MQL5 Indicators/DMH/DMH.mq5', 'folder': 'DMH', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'DMH period', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 0, 'label': 'Color change mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorOn
col_onSlope = 0
col_onZero = 1
col_noChange = 2
_enum('enColorOn', {0: 'col_onSlope', 1: 'col_onZero', 2: 'col_noChange'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # DMH period
inpColorOn = _input('inpColorOn', col_onSlope)  # Color change mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('period', 'alpha', 'coeffs', 'coeffsSum')
    def __init__(self, *args):
        self.period = 0
        self.alpha = 0.0
        self.coeffs = Arr(0, 0.0)
        self.coeffsSum = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('ema',)
    def __init__(self, *args):
        self.ema = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    global_.period = MathMax(inpPeriod, 1)
    global_.alpha = _fdiv(1.0, float(global_.period))
    global_.coeffsSum = 0.0
    ArrayResize(global_.coeffs, global_.period)
    for i in range(0, global_.period):
        _coeff = 1.0 - MathCos(_fdiv(2 * M_PI * (i + 1), global_.period + 1.0))
        global_.coeffs[i] = _coeff
        global_.coeffsSum += _coeff
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('DMH (%i)', global_.period))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    _limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(_limit, rates_total):
        upperMove = ((high[i] - high[i - 1]) if (i > 0) else 0)
        lowerMove = ((low[i - 1] - low[i]) if (i > 0) else 0)
        plusDM = (upperMove if (upperMove > lowerMove and upperMove > 0) else 0)
        minusDM = (lowerMove if (lowerMove > upperMove and lowerMove > 0) else 0)
        _s_OnCalculate_m_work[i].ema = ((_s_OnCalculate_m_work[i - 1].ema + (global_.alpha * (plusDM - minusDM - _s_OnCalculate_m_work[i - 1].ema))) if (i > 0) else (plusDM - minusDM))
        dSum = 0.0
        k = 0
        while k < global_.period and i >= k:
            dSum += _s_OnCalculate_m_work[i - k].ema * global_.coeffs[k]
            k += 1
        val[i] = (_fdiv(dSum, global_.coeffsSum) if (global_.coeffsSum != 0) else 0)
        _sw1 = inpColorOn
        if _sw1 == col_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw1 == col_onZero:
            valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else valc[i - 1] if (i > 0) else 0)
        else:
            valc[i] = 0.0
    return rates_total

# ---- global variables initialised from expressions
global_ = _alloc(sGlobalStruct)
global_.__init__()

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DMH(_MQL5Indicator):
    name = 'DMH'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # DMH period
        'inpColorOn': _Choice({0: 'Change color on slope change', 1: 'Change color on zero cross', 2: 'No color change'}, default=0),  # Color change mode
    }

