"""MA plus — converted from MQL5: MQL5 Indicators/MA plus/MA plus.mq5

Copyright: Alexandr Sokolov; Link: https://www.mql5.com/en/users/asokolov7; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Alexandr Sokolov', 'link': 'https://www.mql5.com/en/users/asokolov7', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 18, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [65280, 255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'MA plus', 'source': 'MQL5 Indicators/MA plus/MA plus.mq5', 'folder': 'MA plus', 'inputs': [{'mql': 'ma_period', 'py': 'ma_period', 'param': 'ma_period', 'type': 'uint', 'default': 25, 'label': 'Period', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}, {'mql': 'ma_ap', 'py': 'ma_ap', 'param': 'ma_ap', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'ma_hm', 'py': 'ma_hm', 'param': 'ma_hm', 'type': 'int', 'default': 0, 'label': 'Hull method', 'sinput': False}, {'mql': 'ma_shift', 'py': 'ma_shift', 'param': 'ma_shift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'vb', 'py': 'vb', 'param': 'vb', 'type': 'int', 'default': 1, 'label': 'Virtual bars', 'sinput': False}, {'mql': 'vb_period', 'py': 'vb_period', 'param': 'vb_period', 'type': 'uint', 'default': 3, 'label': 'Period of virtual bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum METHODS
MODE_SIMPLE = 0
MODE_EXPONENTIAL = 1
MODE_DOUBLE_EXPONENTIAL = 2
MODE_TRIPLE_EXPONENTIAL = 3
MODE_SMOOTHED = 4
MODE_LINEAR_WEIGHTED = 5
_enum('METHODS', {0: 'MODE_SIMPLE', 1: 'MODE_EXPONENTIAL', 2: 'MODE_DOUBLE_EXPONENTIAL', 3: 'MODE_TRIPLE_EXPONENTIAL', 4: 'MODE_SMOOTHED', 5: 'MODE_LINEAR_WEIGHTED'})

# enum UNU
u = 0
nu = 1
_enum('UNU', {0: 'u', 1: 'nu'})

# ---- inputs and global variables
MA = Arr(0, 0.0)  # Main array
MA_color = Arr(0, 0.0)  # Array to store color index
v_open = Arr(0, 0.0)  # Array to store virtual price open
v_high = Arr(0, 0.0)  # Array to store virtual price high
v_low = Arr(0, 0.0)  # Array to store virtual price low
Price = Arr(0, 0.0)  # Array to store prices
OEMA = Arr(0, 0.0)  # auxiliary arrays ...
DEMA = Arr(0, 0.0)
TEMA = Arr(0, 0.0)
H_FV = Arr(0, 0.0)
H_DV = Arr(0, 0.0)
Hull_Value = Arr(0, 0.0)
H_OEMA = Arr(0, 0.0)
H_DEMA = Arr(0, 0.0)
H_TEMA = Arr(0, 0.0)
H_OEMA2 = Arr(0, 0.0)
H_DEMA2 = Arr(0, 0.0)
H_TEMA2 = Arr(0, 0.0)
calculation = None  # Calculation type
ma_period = _input('ma_period', 25)  # Period
ma_method = _input('ma_method', MODE_EXPONENTIAL)  # Method
ma_ap = _input('ma_ap', PRICE_CLOSE)  # Applied price
ma_hm = _input('ma_hm', u)  # Hull method
ma_shift = _input('ma_shift', 0)  # Shift
vb = _input('vb', nu)  # Virtual bars
vb_period = _input('vb_period', 3)  # Period of virtual bars

def OnInit():
    global calculation
    if ma_period == 0:
        Print('Period error - it must be greater than 0')
        return INIT_FAILED
    if vb == u and vb_period < 2:
        Print('Virtual bars are not formed - their period must be greater than 1')
    if ma_hm == u:
        calculation = Hull
    else:
        calculation = Simple
    label = ('Hull MA ' if (ma_hm == u) else 'MA ')
    _sw1 = ma_method
    if _sw1 == MODE_SIMPLE:
        label += 'Si'
    elif _sw1 == MODE_EXPONENTIAL:
        label += 'E'
    elif _sw1 == MODE_DOUBLE_EXPONENTIAL:
        label += 'DE'
    elif _sw1 == MODE_TRIPLE_EXPONENTIAL:
        label += 'TE'
    elif _sw1 == MODE_SMOOTHED:
        label += 'Sm'
    else:
        label += 'LW'
    label += ' P' + _str(ma_period) + ' AP'
    _sw2 = ma_ap
    if _sw2 == PRICE_CLOSE:
        label += 'C'
    elif _sw2 == PRICE_HIGH:
        label += 'H'
    elif _sw2 == PRICE_LOW:
        label += 'L'
    elif _sw2 == PRICE_OPEN:
        label += 'O'
    elif _sw2 == PRICE_MEDIAN:
        label += 'M'
    elif _sw2 == PRICE_TYPICAL:
        label += 'T'
    else:
        label += 'W'
    label += ' Sh' + _str(ma_shift)
    if vb == u:
        label += ' PoVB' + _str(vb_period)
    PlotIndexSetInteger(0, PLOT_SHIFT, ma_shift)
    PlotIndexSetString(0, PLOT_LABEL, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, MA, INDICATOR_DATA)
    SetIndexBuffer(1, MA_color, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, v_open, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, v_high, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, v_low, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, Price, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, OEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, DEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, TEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, H_FV, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, H_DV, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, Hull_Value, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, H_OEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, H_DEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, H_TEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, H_OEMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, H_DEMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(17, H_TEMA2, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(MA, True)
    ArraySetAsSeries(MA_color, True)
    ArraySetAsSeries(v_open, True)
    ArraySetAsSeries(v_high, True)
    ArraySetAsSeries(v_low, True)
    ArraySetAsSeries(Price, True)
    ArraySetAsSeries(OEMA, True)
    ArraySetAsSeries(DEMA, True)
    ArraySetAsSeries(TEMA, True)
    ArraySetAsSeries(H_FV, True)
    ArraySetAsSeries(H_DV, True)
    ArraySetAsSeries(Hull_Value, True)
    ArraySetAsSeries(H_OEMA, True)
    ArraySetAsSeries(H_DEMA, True)
    ArraySetAsSeries(H_TEMA, True)
    ArraySetAsSeries(H_OEMA2, True)
    ArraySetAsSeries(H_DEMA2, True)
    ArraySetAsSeries(H_TEMA2, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if prev_calculated == 0:
        ArrayInitialize(MA, EMPTY_VALUE)
        ArrayInitialize(MA_color, EMPTY_VALUE)
        ArrayInitialize(v_open, EMPTY_VALUE)
        ArrayInitialize(v_high, EMPTY_VALUE)
        ArrayInitialize(v_low, EMPTY_VALUE)
        ArrayInitialize(Price, EMPTY_VALUE)
        ArrayInitialize(OEMA, EMPTY_VALUE)
        ArrayInitialize(DEMA, EMPTY_VALUE)
        ArrayInitialize(TEMA, EMPTY_VALUE)
        ArrayInitialize(H_FV, EMPTY_VALUE)
        ArrayInitialize(H_DV, EMPTY_VALUE)
        ArrayInitialize(Hull_Value, EMPTY_VALUE)
        ArrayInitialize(H_OEMA, EMPTY_VALUE)
        ArrayInitialize(H_DEMA, EMPTY_VALUE)
        ArrayInitialize(H_TEMA, EMPTY_VALUE)
        ArrayInitialize(H_OEMA2, EMPTY_VALUE)
        ArrayInitialize(H_DEMA2, EMPTY_VALUE)
        ArrayInitialize(H_TEMA2, EMPTY_VALUE)
    if (vb == u and vb_period > 1) and vb_period <= _uint(rates_total):
        limit = rates_total - prev_calculated - _int(vb_period)
        if limit < 0:
            limit = 0
        for a in range(limit, 0 - 1, -1):
            v_open[a] = open[a + _int(vb_period) - 1]
            v_high[a] = low[a]
            v_low[a] = high[a]
            for b in range(a + _int(vb_period) - 1, a - 1, -1):
                if high[b] > v_high[a]:
                    v_high[a] = high[b]
                if low[b] < v_low[a]:
                    v_low[a] = low[b]
    elif vb == u and vb_period > _uint(rates_total):
        PrintFormat('Period of virtual bars exceeds the number of available bars - %u (Current period of virtual bars - %u)', rates_total, vb_period)
        return 0
    limit = rates_total - prev_calculated - 1
    if vb == u and vb_period > 1:
        limit -= _int(vb_period) + 1
    if limit < 0:
        limit = 0
    for i in range(limit, 0 - 1, -1):
        if vb == u and vb_period > 1:
            Price[i] = GetPrice(i, v_open, v_high, v_low, close)
        else:
            Price[i] = GetPrice(i, open, high, low, close)
    result = False
    if vb == u and vb_period > 1:
        result = _bool(calculation(rates_total, prev_calculated))
    else:
        result = _bool(calculation(rates_total, prev_calculated))
    return (rates_total if result else 0)

def GetPrice(index, open, high, low, close):
    _sw3 = ma_ap
    if _sw3 == PRICE_OPEN:
        return open[index]
    elif _sw3 == PRICE_HIGH:
        return high[index]
    elif _sw3 == PRICE_LOW:
        return low[index]
    elif _sw3 == PRICE_MEDIAN:
        return (high[index] + low[index]) / 2.0
    elif _sw3 == PRICE_TYPICAL:
        return (high[index] + low[index] + close[index]) / 3.0
    elif _sw3 == PRICE_WEIGHTED:
        return (high[index] + low[index] + close[index] + close[index]) / 4.0
    return close[index]

def Simple(rates_total, prev_calculated):
    limit = rates_total - prev_calculated - 1
    _sw4 = ma_method
    if _sw4 == MODE_DOUBLE_EXPONENTIAL:
        limit -= (_int(ma_period) * 2) - 2
    elif _sw4 == MODE_TRIPLE_EXPONENTIAL:
        limit -= (_int(ma_period) * 4) - 4
    else:
        limit -= _int(ma_period) - 1
    if vb == u and vb_period > 1:
        limit -= _int(vb_period) - 1
    if prev_calculated == 0 and limit < 0:
        Print('The current averaging period does not allow the indicator to be calculated due to an insufficient number of bars')
        return False
    if limit < 0:
        limit = 0
    for i in range(limit, 0 - 1, -1):
        Averaging(i, ma_method, ma_period, Price, MA, OEMA, DEMA, TEMA)
        MA_color[i] = (0 if (MA[i + 1] == EMPTY_VALUE) else 0 if (MA[i] >= MA[i + 1]) else 1)
    return True

def Hull(rates_total, prev_calculated):
    limit = rates_total - prev_calculated - 1
    _sw5 = ma_method
    if _sw5 == MODE_DOUBLE_EXPONENTIAL:
        limit -= (_int(ma_period) * 2) - 2
    elif _sw5 == MODE_TRIPLE_EXPONENTIAL:
        limit -= (_int(ma_period) * 4) - 4
    else:
        limit -= _int(ma_period) - 1
    if vb == u and vb_period > 1:
        limit -= _int(vb_period) - 1
    if prev_calculated == 0 and limit < 0:
        Print('The current averaging period does not allow the indicator to be calculated due to an insufficient number of bars')
        return False
    if limit < 0:
        limit = 0
    period_d = _int(MathFloor((ma_period if (ma_period > 1) else 1.0) / 2.0))
    period_r = _int(MathFloor(MathSqrt((ma_period if (ma_period > 1) else 1.0))))
    if period_d < 1:
        period_d = 1
    if period_r < 1:
        period_r = 1
    hull_limit = limit
    _sw6 = ma_method
    if _sw6 == MODE_DOUBLE_EXPONENTIAL:
        hull_limit -= (period_r * 2) - 2
    elif _sw6 == MODE_TRIPLE_EXPONENTIAL:
        hull_limit -= (period_r * 4) - 4
    else:
        hull_limit -= period_r - 1
    if prev_calculated == 0 and hull_limit < 0:
        Print('The current averaging period does not allow the indicator to be calculated due to an insufficient number of bars')
        return False
    if hull_limit < 0:
        hull_limit = 0
    for i in range(limit, 0 - 1, -1):
        Averaging(i, ma_method, ma_period, Price, H_FV, OEMA, DEMA, TEMA)
        Averaging(i, ma_method, period_d, Price, H_DV, H_OEMA, H_DEMA, H_TEMA)
        Hull_Value[i] = (2.0 * H_DV[i]) - H_FV[i]
        if i <= hull_limit:
            if period_r > 1:
                Averaging(i, ma_method, period_r, Hull_Value, MA, H_OEMA2, H_DEMA2, H_TEMA2)
            else:
                MA[i] = Hull_Value[i]
            MA_color[i] = (0 if (MA[i + 1] == EMPTY_VALUE) else 0 if (MA[i] >= MA[i + 1]) else 1)
    return True

def Averaging(index, method, period, values_from, value_to, oe, de, te):
    sum_ = 0.0
    coef = 0.0
    limit = 0
    lw_period = period
    lw_sum = 0
    if method == MODE_SIMPLE:
        limit = index + period
        for i in range(index, limit):
            sum_ += values_from[i]
        value_to[index] = _fdiv(sum_, float(period))
    elif method == MODE_EXPONENTIAL:
        if value_to[index + 1] == EMPTY_VALUE:
            Averaging(index, MODE_SIMPLE, period, values_from, value_to, oe, de, te)
            return
        coef = _fdiv(2.0, float(period + 1))
        value_to[index] = (coef * values_from[index]) + ((1.0 - coef) * value_to[index + 1])
    elif method == MODE_DOUBLE_EXPONENTIAL:
        if oe[index + 1] == EMPTY_VALUE:
            limit = index + period
            for i in range(limit - 1, index - 1, -1):
                Averaging(i, MODE_EXPONENTIAL, period, values_from, oe, oe, de, te)
        else:
            Averaging(index, MODE_EXPONENTIAL, period, values_from, oe, oe, de, te)
        Averaging(index, MODE_EXPONENTIAL, period, oe, de, oe, de, te)
        value_to[index] = (2.0 * oe[index]) - de[index]
    elif method == MODE_TRIPLE_EXPONENTIAL:
        o_start = index + (period * 2) - 2
        if oe[o_start + 1] == EMPTY_VALUE:
            limit = o_start + period - 1
            for i in range(limit, index - 1, -1):
                Averaging(i, MODE_EXPONENTIAL, period, values_from, oe, oe, de, te)
        else:
            Averaging(index, MODE_EXPONENTIAL, period, values_from, oe, oe, de, te)
        d_start = index + period - 1
        if de[d_start + 1] == EMPTY_VALUE:
            limit = d_start + period - 1
            for i in range(limit, index - 1, -1):
                Averaging(i, MODE_EXPONENTIAL, period, oe, de, oe, de, te)
        else:
            Averaging(index, MODE_EXPONENTIAL, period, oe, de, oe, de, te)
        Averaging(index, MODE_EXPONENTIAL, period, de, te, oe, de, te)
        value_to[index] = (3.0 * oe[index]) - (3.0 * de[index]) + te[index]
    elif method == MODE_SMOOTHED:
        if value_to[index + 1] == EMPTY_VALUE:
            Averaging(index, MODE_SIMPLE, period, values_from, value_to, oe, de, te)
            return
        elif value_to[index + 1] != EMPTY_VALUE and value_to[index + 2] == EMPTY_VALUE:
            limit = index + period
            for i in range(index, limit):
                sum_ += values_from[i]
            value_to[index] = _fdiv(sum_ - value_to[index + 1] + values_from[index], float(period))
            return
        sum_ = value_to[index + 1] * float(period)
        value_to[index] = _fdiv(sum_ - value_to[index + 1] + values_from[index], float(period))
    else:
        limit = index + period
        for i in range(index, limit):
            sum_ += values_from[i] * float(lw_period)
            lw_sum += lw_period
            lw_period -= 1
        value_to[index] = _fdiv(sum_, float(lw_sum))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAPlus(_MQL5Indicator):
    name = 'MA plus'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ma_period': 25,  # Period
        'ma_method': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Double Exponential', 3: 'Triple Exponential', 4: 'Smoothed', 5: 'Linear Weighted'}, default=1),  # Method
        'ma_ap': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'ma_hm': _Choice({0: 'Use', 1: 'Not use'}, default=0),  # Hull method
        'ma_shift': 0,  # Shift
        'vb': _Choice({0: 'Use', 1: 'Not use'}, default=1),  # Virtual bars
        'vb_period': 3,  # Period of virtual bars
    }

