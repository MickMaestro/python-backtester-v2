"""McGinley dynamic average (official) — converted from MQL5: MQL5 Indicators/McGinley dynamic (official)/McGinley dynamic average (official).mq5

McGinley dynamic average
Copyright: © mladen, 2020; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2020', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'McGinley dynamic average'}, 'levels': [], 'description': ['McGinley dynamic average'], 'name': 'McGinley dynamic average (official)', 'source': 'MQL5 Indicators/McGinley dynamic (official)/McGinley dynamic average (official).mq5', 'folder': 'McGinley dynamic (official)', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpType', 'py': 'inpType', 'param': 'inpType', 'type': 'int', 'default': 0, 'label': 'Calculation type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enMcgType
mcg_original = 0
mcg_faster = 1
_enum('enMcgType', {0: 'mcg_original', 1: 'mcg_faster'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpType = _input('inpType', mcg_original)  # Calculation type
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
mcgMultiplier = 0.0

def OnInit():
    global mcgMultiplier
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    mcgMultiplier = (1.0 if (inpType == mcg_original) else 0.6)
    IndicatorSetString(INDICATOR_SHORTNAME, 'McGinley dynamic (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = ((prev_calculated - 1) if prev_calculated else 0)
    for i in range(limit, rates_total):
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        if i > 0 and inpPeriod > 1:
            _pow = inpPeriod * mcgMultiplier * MathPow((_fdiv(_price, val[i - 1]) if (val[i - 1] != 0 and _price != 0) else 0), 4)
            val[i] = ((val[i - 1] + _fdiv(_price - val[i - 1], _pow)) if _pow else _price)
        else:
            val[i] = _price
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class McGinleyDynamicAverageOfficial(_MQL5Indicator):
    name = 'McGinley dynamic average (official)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpType': _Choice({0: 'Original formula', 1: '"Improved" formula'}, default=0),  # Calculation type
    }

