"""Moving slope rate of change - extended — converted from MQL5: MQL5 Indicators/Moving slope rate of change - Extended/Moving slope rate of change - extended.mq5

Moving slope rate of change - extended
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [14870490, 14278143], 2: [11119017, 16748574, 3937500]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'msrc filling', 2: 'msrc value'}, 'levels': [], 'description': ['Moving slope rate of change - extended'], 'name': 'Moving slope rate of change - extended', 'source': 'MQL5 Indicators/Moving slope rate of change - Extended/Moving slope rate of change - extended.mq5', 'folder': 'Moving slope rate of change - Extended', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Calculation period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLevLookBack', 'py': 'inpLevLookBack', 'param': 'inpLevLookBack', 'type': 'int', 'default': 25, 'label': 'Floating level period (<=0 no floating level)', 'sinput': False}, {'mql': 'inpLevLevelUp', 'py': 'inpLevLevelUp', 'param': 'inpLevLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating level up %', 'sinput': False}, {'mql': 'inpLevLevelDown', 'py': 'inpLevLevelDown', 'param': 'inpLevLevelDown', 'type': 'double', 'default': 10.0, 'label': 'Floating level down %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Calculation period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpLevLookBack = _input('inpLevLookBack', 25)  # Floating level period (<=0 no floating level)
inpLevLevelUp = _input('inpLevLevelUp', 90.0)  # Floating level up %
inpLevLevelDown = _input('inpLevLevelDown', 10.0)  # Floating level down %
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Moving slope rate of change (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        sum_xy = 0.0
        sum_x = 0.0
        sum_y = 0.0
        sum_xx = 0.0
        j = 0
        while j < inpPeriod and (i - j) >= 0:
            y = getPrice(inpPrice, open, close, high, low, i - j, rates_total)
            x = inpPeriod - j
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_xx += x * x
            j += 1
        numerator = (inpPeriod * sum_xy) - (sum_x * sum_y)
        denominator = (inpPeriod * sum_xx) - (sum_x * sum_x)
        val[i] = (_fdiv(numerator, denominator) if (denominator != 0) else 0)
        fillu[i] = val[i]
        if inpLevLookBack > 0:
            start = MathMax(i - inpLevLookBack + 1, 0)
            min_ = val[ArrayMinimum(val, start, inpLevLookBack)]
            max_ = val[ArrayMaximum(val, start, inpLevLookBack)]
            range_ = max_ - min_
            levu = min_ + ((inpLevLevelUp * range_) / 100.0)
            levd = min_ + ((inpLevLevelDown * range_) / 100.0)
            filld[i] = (levu if (val[i] > levu) else levd if (val[i] < levd) else val[i])
            valc[i] = (1 if (val[i] > levu) else 2 if (val[i] < levd) else 0)
        else:
            filld[i] = 0.0
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def getPrice(tprice, open, close, high, low, i, _bars):
    _sw1 = tprice
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MovingSlopeRateOfChangeExtended(_MQL5Indicator):
    name = 'Moving slope rate of change - extended'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Calculation period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLevLookBack': 25,  # Floating level period (<=0 no floating level)
        'inpLevLevelUp': 90.0,  # Floating level up %
        'inpLevLevelDown': 10.0,  # Floating level down %
    }

