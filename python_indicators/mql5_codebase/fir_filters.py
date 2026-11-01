"""Fir filters — converted from MQL5: MQL5 Indicators/Fir filters/Fir filters.mq5

Fir filters
Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16760576, 5275647]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Hann average'}, 'levels': [], 'description': ['Fir filters'], 'name': 'Fir filters', 'source': 'MQL5 Indicators/Fir filters/Fir filters.mq5', 'folder': 'Fir filters', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpFirType', 'py': 'inpFirType', 'param': 'inpFirType', 'type': 'int', 'default': 1, 'label': 'FIR type', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enFirType
fir_rect = 0
fir_hann = 1
fir_hamm = 2
fir_blck = 3
fir_blha = 4
fir_lwma = 5
fir_tma = 6
_enum('enFirType', {0: 'fir_rect', 1: 'fir_hann', 2: 'fir_hamm', 3: 'fir_blck', 4: 'fir_blha', 5: 'fir_lwma', 6: 'fir_tma'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpFirType = _input('inpFirType', fir_hann)  # FIR type
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('period', 'coeffs', 'coeffsSum')
    def __init__(self, *args):
        self.period = 0
        self.coeffs = Arr(0, 0.0)
        self.coeffsSum = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('price',)
    def __init__(self, *args):
        self.price = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    global_.period = MathMax(inpPeriod, 1)
    global_.coeffsSum = 0.0
    _div = global_.period + 1.0
    _coeff = 1.0
    ArrayResize(global_.coeffs, global_.period)
    for i in range(0, global_.period):
        _sw1 = inpFirType
        if _sw1 == fir_rect:
            _coeff = 1.0
        elif _sw1 == fir_hann:
            _coeff = 0.5 - (0.5 * MathCos(_fdiv(2.0 * M_PI * (i + 1), _div)))
        elif _sw1 == fir_hamm:
            _coeff = 0.54 - (0.46 * MathCos(_fdiv(2.0 * M_PI * (i + 1), _div)))
        elif _sw1 == fir_blck:
            _coeff = 0.42 - (0.5 * MathCos(_fdiv(2.0 * M_PI * (i + 1), _div))) + (0.08 * MathCos(_fdiv(4.0 * M_PI * i, _div)))
        elif _sw1 == fir_blha:
            _coeff = 0.35875 - (0.48829 * MathCos(_fdiv(2.0 * M_PI * (i + 1), _div))) + (0.14128 * MathCos(_fdiv(4.0 * M_PI * (i + 1), _div))) - (0.01168 * MathCos(_fdiv(6.0 * M_PI * (i + 1), _div)))
        elif _sw1 == fir_lwma:
            _coeff = global_.period - i
        elif _sw1 == fir_tma:
            _coeff = i + 1.0
            if _coeff > ((global_.period + 1.0) / 2.0):
                _coeff = global_.period - i
        global_.coeffs[i] = _coeff
        global_.coeffsSum += _coeff
    _names = Arr.of(['Rectangular/SMA', 'Hanning', 'Hamming', 'Blackman', 'Blackman/Harris', 'Linear weighted', 'Triangular'], fill="")
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('%s (%i)', _names[inpFirType], global_.period))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    _limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(_limit, rates_total):
        _s_OnCalculate_m_work[i].price = iGetPrice(inpPrice, open[i], high[i], low[i], close[i])
        dSum = 0.0
        k = 0
        while k < global_.period and i >= k:
            dSum += _s_OnCalculate_m_work[i - k].price * global_.coeffs[k]
            k += 1
        val[i] = (_fdiv(dSum, global_.coeffsSum) if (global_.coeffsSum != 0) else 0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

def iGetPrice(price, open, high, low, close):
    _sw2 = price
    if _sw2 == PRICE_CLOSE:
        return close
    elif _sw2 == PRICE_OPEN:
        return open
    elif _sw2 == PRICE_HIGH:
        return high
    elif _sw2 == PRICE_LOW:
        return low
    elif _sw2 == PRICE_MEDIAN:
        return (high + low) / 2.0
    elif _sw2 == PRICE_TYPICAL:
        return (high + low + close) / 3.0
    elif _sw2 == PRICE_WEIGHTED:
        return (high + low + close + close) / 4.0
    return 0.0

# ---- global variables initialised from expressions
global_ = _alloc(sGlobalStruct)
global_.__init__()

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FirFilters(_MQL5Indicator):
    name = 'Fir filters'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpFirType': _Choice({0: 'Rectangular - simple moving average', 1: 'Hannig', 2: 'Hammig', 3: 'Blackman', 4: 'Blackman/Harris', 5: 'Linear weighted', 6: 'Triangular'}, default=1),  # FIR type
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

