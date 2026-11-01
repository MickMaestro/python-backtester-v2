"""STPMT — converted from MQL5: MQL5 Indicators/STPMT/STPMT.mq5

Medium Term Weighted Stochastics oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [32768], 2: [255], 3: [12632256], 4: [12632256], 5: [12632256], 6: [12632256]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'STPMT', 2: 'Signal', 3: 'Stochastic 1', 4: 'Stochastic 2', 5: 'Stochastic 3', 6: 'Stochastic 4'}, 'levels': [], 'description': ['Medium Term Weighted Stochastics oscillator'], 'name': 'STPMT', 'source': 'MQL5 Indicators/STPMT/STPMT.mq5', 'folder': 'STPMT', 'inputs': [{'mql': 'InpPeriodK1', 'py': 'InpPeriodK1', 'param': 'InpPeriodK1', 'type': 'uint', 'default': 5, 'label': 'Stochastic 1 %K period', 'sinput': False}, {'mql': 'InpPeriodD1', 'py': 'InpPeriodD1', 'param': 'InpPeriodD1', 'type': 'uint', 'default': 3, 'label': 'Stochastic 1 %D period', 'sinput': False}, {'mql': 'InpSlowing1', 'py': 'InpSlowing1', 'param': 'InpSlowing1', 'type': 'uint', 'default': 3, 'label': 'Stochastic 1 Slowing', 'sinput': False}, {'mql': 'InpMethod1', 'py': 'InpMethod1', 'param': 'InpMethod1', 'type': 'int', 'default': 0, 'label': 'Stochastic 1 Method', 'sinput': False}, {'mql': 'InpPriceField1', 'py': 'InpPriceField1', 'param': 'InpPriceField1', 'type': 'int', 'default': 0, 'label': 'Stochastic 1 Price field', 'sinput': False}, {'mql': 'InpWeight1', 'py': 'InpWeight1', 'param': 'InpWeight1', 'type': 'double', 'default': 4.1, 'label': 'Stochastic 1 Weight', 'sinput': False}, {'mql': 'InpPeriodK2', 'py': 'InpPeriodK2', 'param': 'InpPeriodK2', 'type': 'uint', 'default': 14, 'label': 'Stochastic 2 %K period', 'sinput': False}, {'mql': 'InpPeriodD2', 'py': 'InpPeriodD2', 'param': 'InpPeriodD2', 'type': 'uint', 'default': 3, 'label': 'Stochastic 2 %D period', 'sinput': False}, {'mql': 'InpSlowing2', 'py': 'InpSlowing2', 'param': 'InpSlowing2', 'type': 'uint', 'default': 3, 'label': 'Stochastic 2 Slowing', 'sinput': False}, {'mql': 'InpMethod2', 'py': 'InpMethod2', 'param': 'InpMethod2', 'type': 'int', 'default': 0, 'label': 'Stochastic 2 Method', 'sinput': False}, {'mql': 'InpPriceField2', 'py': 'InpPriceField2', 'param': 'InpPriceField2', 'type': 'int', 'default': 0, 'label': 'Stochastic 2 Price field', 'sinput': False}, {'mql': 'InpWeight2', 'py': 'InpWeight2', 'param': 'InpWeight2', 'type': 'double', 'default': 2.5, 'label': 'Stochastic 2 Weight', 'sinput': False}, {'mql': 'InpPeriodK3', 'py': 'InpPeriodK3', 'param': 'InpPeriodK3', 'type': 'uint', 'default': 45, 'label': 'Stochastic 3 %K period', 'sinput': False}, {'mql': 'InpPeriodD3', 'py': 'InpPeriodD3', 'param': 'InpPeriodD3', 'type': 'uint', 'default': 14, 'label': 'Stochastic 3 %D period', 'sinput': False}, {'mql': 'InpSlowing3', 'py': 'InpSlowing3', 'param': 'InpSlowing3', 'type': 'uint', 'default': 3, 'label': 'Stochastic 3 Slowing', 'sinput': False}, {'mql': 'InpMethod3', 'py': 'InpMethod3', 'param': 'InpMethod3', 'type': 'int', 'default': 0, 'label': 'Stochastic 3 Method', 'sinput': False}, {'mql': 'InpPriceField3', 'py': 'InpPriceField3', 'param': 'InpPriceField3', 'type': 'int', 'default': 0, 'label': 'Stochastic 3 Price field', 'sinput': False}, {'mql': 'InpWeight3', 'py': 'InpWeight3', 'param': 'InpWeight3', 'type': 'double', 'default': 1.0, 'label': 'Stochastic 3 Weight', 'sinput': False}, {'mql': 'InpPeriodK4', 'py': 'InpPeriodK4', 'param': 'InpPeriodK4', 'type': 'uint', 'default': 75, 'label': 'Stochastic 4 %K period', 'sinput': False}, {'mql': 'InpPeriodD4', 'py': 'InpPeriodD4', 'param': 'InpPeriodD4', 'type': 'uint', 'default': 20, 'label': 'Stochastic 4 %D period', 'sinput': False}, {'mql': 'InpSlowing4', 'py': 'InpSlowing4', 'param': 'InpSlowing4', 'type': 'uint', 'default': 3, 'label': 'Stochastic 4 Slowing', 'sinput': False}, {'mql': 'InpMethod4', 'py': 'InpMethod4', 'param': 'InpMethod4', 'type': 'int', 'default': 0, 'label': 'Stochastic 4 Method', 'sinput': False}, {'mql': 'InpPriceField4', 'py': 'InpPriceField4', 'param': 'InpPriceField4', 'type': 'int', 'default': 0, 'label': 'Stochastic 4 Price field', 'sinput': False}, {'mql': 'InpWeight4', 'py': 'InpWeight4', 'param': 'InpWeight4', 'type': 'double', 'default': 4.0, 'label': 'Stochastic 4 Weight', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 9, 'label': 'Signal line period', 'sinput': False}, {'mql': 'InpShowComponents', 'py': 'InpShowComponents', 'param': 'InpShowComponents', 'type': 'int', 'default': 1, 'label': 'Show components', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodK1 = _input('InpPeriodK1', 5)  # Stochastic 1 %K period
InpPeriodD1 = _input('InpPeriodD1', 3)  # Stochastic 1 %D period
InpSlowing1 = _input('InpSlowing1', 3)  # Stochastic 1 Slowing
InpMethod1 = _input('InpMethod1', MODE_SMA)  # Stochastic 1 Method
InpPriceField1 = _input('InpPriceField1', STO_LOWHIGH)  # Stochastic 1 Price field
InpWeight1 = _input('InpWeight1', 4.1)  # Stochastic 1 Weight
InpPeriodK2 = _input('InpPeriodK2', 14)  # Stochastic 2 %K period
InpPeriodD2 = _input('InpPeriodD2', 3)  # Stochastic 2 %D period
InpSlowing2 = _input('InpSlowing2', 3)  # Stochastic 2 Slowing
InpMethod2 = _input('InpMethod2', MODE_SMA)  # Stochastic 2 Method
InpPriceField2 = _input('InpPriceField2', STO_LOWHIGH)  # Stochastic 2 Price field
InpWeight2 = _input('InpWeight2', 2.5)  # Stochastic 2 Weight
InpPeriodK3 = _input('InpPeriodK3', 45)  # Stochastic 3 %K period
InpPeriodD3 = _input('InpPeriodD3', 14)  # Stochastic 3 %D period
InpSlowing3 = _input('InpSlowing3', 3)  # Stochastic 3 Slowing
InpMethod3 = _input('InpMethod3', MODE_SMA)  # Stochastic 3 Method
InpPriceField3 = _input('InpPriceField3', STO_LOWHIGH)  # Stochastic 3 Price field
InpWeight3 = _input('InpWeight3', 1.0)  # Stochastic 3 Weight
InpPeriodK4 = _input('InpPeriodK4', 75)  # Stochastic 4 %K period
InpPeriodD4 = _input('InpPeriodD4', 20)  # Stochastic 4 %D period
InpSlowing4 = _input('InpSlowing4', 3)  # Stochastic 4 Slowing
InpMethod4 = _input('InpMethod4', MODE_SMA)  # Stochastic 4 Method
InpPriceField4 = _input('InpPriceField4', STO_LOWHIGH)  # Stochastic 4 Price field
InpWeight4 = _input('InpWeight4', 4.0)  # Stochastic 4 Weight
InpPeriodSig = _input('InpPeriodSig', 9)  # Signal line period
InpShowComponents = _input('InpShowComponents', INPUT_YES)  # Show components
BufferSTPMT = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
weights = 0.0
period_sig = 0
period_max = 0
total = 0

class SDataStoch(MqlObject):
    _q_fields = ('buffer', 'weight', 'method', 'price', 'period_k', 'period_d', 'slowing', 'handle')
    def __init__(self, *args):
        self.buffer = Arr(0, 0.0)
        self.weight = 0.0
        self.method = 0
        self.price = 0
        self.period_k = 0
        self.period_d = 0
        self.slowing = 0
        self.handle = 0

def OnInit():
    global period_max, period_sig, total, weights
    period_sig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    total = ArraySize(stoch)
    period_max = 0
    weights = period_max
    i = 0
    while i < total:
        SetIndexBuffer(i + 2, stoch[i].buffer, INDICATOR_DATA)
        ArraySetAsSeries(stoch[i].buffer, True)
        PlotIndexSetInteger(i + 2, PLOT_DRAW_TYPE, InpShowComponents)
        PlotIndexSetInteger(i + 2, PLOT_SHOW_DATA, False)
        SetParams(i, _AttrRef(stoch[i], 'period_k'), _AttrRef(stoch[i], 'period_d'), _AttrRef(stoch[i], 'slowing'), _AttrRef(stoch[i], 'weight'), _AttrRef(stoch[i], 'method'), _AttrRef(stoch[i], 'price'))
        stoch[i].handle = iStochastic(None, PERIOD_CURRENT, stoch[i].period_k, stoch[i].period_d, stoch[i].slowing, stoch[i].method, stoch[i].price)
        if stoch[i].handle == INVALID_HANDLE:
            Print('The iStochastic', i + 1, ' (', _str(stoch[i].period_k), ',', _str(stoch[i].period_d), ',', _str(stoch[i].slowing), ') object was not created: Error ', GetLastError())
            return INIT_FAILED
        weights += stoch[i].weight
        period = fmax(stoch[i].period_k, stoch[i].period_d)
        if period > period_max:
            period_max = period
        i += 1
    SetIndexBuffer(0, BufferSTPMT, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Medium Term Weighted Stochastics')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, period_max)
    ArraySetAsSeries(BufferSTPMT, True)
    ArraySetAsSeries(BufferSignal, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferSTPMT, 0)
        ArrayInitialize(BufferSignal, 0)
        for i in range(0, total):
            ArrayInitialize(stoch[i].buffer, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    for i in range(0, total):
        copied = CopyBuffer(stoch[i].handle, MAIN_LINE, 0, count, stoch[i].buffer)
        if copied != count:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferSTPMT[i] = _fdiv((stoch[0].weight * stoch[0].buffer[i]) + (stoch[1].weight * stoch[1].buffer[i]) + (stoch[2].weight * stoch[2].buffer[i]) + (stoch[3].weight * stoch[3].buffer[i]), weights)
        BufferSignal[i] = GetSMA(rates_total, i, period_sig, BufferSTPMT)
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)

def SetParams(index, period_k, period_d, slowihg, weight, method, price):
    _sw1 = index
    if _sw1 == 1:
        period_k.v = (1 if (InpPeriodK2 < 1) else InpPeriodK2)
        period_d.v = (1 if (InpPeriodD2 < 1) else InpPeriodD2)
        slowihg.v = (1 if (InpSlowing2 < 1) else InpSlowing2)
        price.v = InpPriceField2
        method.v = InpMethod2
        weight.v = InpWeight2
    elif _sw1 == 2:
        period_k.v = (1 if (InpPeriodK3 < 1) else InpPeriodK3)
        period_d.v = (1 if (InpPeriodD3 < 1) else InpPeriodD3)
        slowihg.v = (1 if (InpSlowing3 < 1) else InpSlowing3)
        price.v = InpPriceField3
        method.v = InpMethod3
        weight.v = InpWeight3
    elif _sw1 == 3:
        period_k.v = (1 if (InpPeriodK4 < 1) else InpPeriodK4)
        period_d.v = (1 if (InpPeriodD4 < 1) else InpPeriodD4)
        slowihg.v = (1 if (InpSlowing4 < 1) else InpSlowing4)
        price.v = InpPriceField4
        method.v = InpMethod4
        weight.v = InpWeight4
    else:
        period_k.v = (1 if (InpPeriodK1 < 1) else InpPeriodK1)
        period_d.v = (1 if (InpPeriodD1 < 1) else InpPeriodD1)
        slowihg.v = (1 if (InpSlowing1 < 1) else InpSlowing1)
        price.v = InpPriceField1
        method.v = InpMethod1
        weight.v = InpWeight1

# ---- global variables initialised from expressions
stoch = Arr(4, 0, dyn=False, factory=SDataStoch)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class STPMT(_MQL5Indicator):
    name = 'STPMT'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodK1': 5,  # Stochastic 1 %K period
        'InpPeriodD1': 3,  # Stochastic 1 %D period
        'InpSlowing1': 3,  # Stochastic 1 Slowing
        'InpMethod1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stochastic 1 Method
        'InpPriceField1': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic 1 Price field
        'InpWeight1': 4.1,  # Stochastic 1 Weight
        'InpPeriodK2': 14,  # Stochastic 2 %K period
        'InpPeriodD2': 3,  # Stochastic 2 %D period
        'InpSlowing2': 3,  # Stochastic 2 Slowing
        'InpMethod2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stochastic 2 Method
        'InpPriceField2': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic 2 Price field
        'InpWeight2': 2.5,  # Stochastic 2 Weight
        'InpPeriodK3': 45,  # Stochastic 3 %K period
        'InpPeriodD3': 14,  # Stochastic 3 %D period
        'InpSlowing3': 3,  # Stochastic 3 Slowing
        'InpMethod3': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stochastic 3 Method
        'InpPriceField3': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic 3 Price field
        'InpWeight3': 1.0,  # Stochastic 3 Weight
        'InpPeriodK4': 75,  # Stochastic 4 %K period
        'InpPeriodD4': 20,  # Stochastic 4 %D period
        'InpSlowing4': 3,  # Stochastic 4 Slowing
        'InpMethod4': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stochastic 4 Method
        'InpPriceField4': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic 4 Price field
        'InpWeight4': 4.0,  # Stochastic 4 Weight
        'InpPeriodSig': 9,  # Signal line period
        'InpShowComponents': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show components
    }

