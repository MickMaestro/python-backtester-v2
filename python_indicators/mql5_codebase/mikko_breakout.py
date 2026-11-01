"""Mikko breakout — converted from MQL5: MQL5 Indicators/Mikko Breakout/Mikko breakout.mq5

mikko breakout
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 14, 'indicator_plots': 3}, 'types': {1: 16, 2: 17, 3: 8}, 'colors': {1: [11119017, 3329330, 6333684], 2: [11119017, 3329330, 6333684], 3: [11119017, 3329330, 6333684]}, 'widths': {3: 2}, 'styles': {}, 'labels': {1: 'Bars', 2: 'Candles', 3: 'Line'}, 'levels': [], 'description': ['mikko breakout'], 'name': 'Mikko breakout', 'source': 'MQL5 Indicators/Mikko Breakout/Mikko breakout.mq5', 'folder': 'Mikko Breakout', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Period / count', 'sinput': False}, {'mql': 'inpDisplayStyle', 'py': 'inpDisplayStyle', 'param': 'inpDisplayStyle', 'type': 'int', 'default': 0, 'label': 'Display style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDisplayStyle
dis_automatic = 0
dis_line = 1
dis_bars = 2
dis_candles = 3
_enum('enDisplayStyle', {0: 'dis_automatic', 1: 'dis_line', 2: 'dis_bars', 3: 'dis_candles'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Period / count
inpDisplayStyle = _input('inpDisplayStyle', dis_automatic)  # Display style
canh = Arr(0, 0.0)
canl = Arr(0, 0.0)
cano = Arr(0, 0.0)
canc = Arr(0, 0.0)
cancl = Arr(0, 0.0)
baro = Arr(0, 0.0)
barh = Arr(0, 0.0)
barl = Arr(0, 0.0)
barc = Arr(0, 0.0)
barcl = Arr(0, 0.0)
line = Arr(0, 0.0)
linecl = Arr(0, 0.0)
val = Arr(0, 0.0)
valcl = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, baro, INDICATOR_DATA)
    SetIndexBuffer(1, barh, INDICATOR_DATA)
    SetIndexBuffer(2, barl, INDICATOR_DATA)
    SetIndexBuffer(3, barc, INDICATOR_DATA)
    SetIndexBuffer(4, barcl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, cano, INDICATOR_DATA)
    SetIndexBuffer(6, canh, INDICATOR_DATA)
    SetIndexBuffer(7, canl, INDICATOR_DATA)
    SetIndexBuffer(8, canc, INDICATOR_DATA)
    SetIndexBuffer(9, cancl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(10, line, INDICATOR_DATA)
    SetIndexBuffer(11, linecl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(12, val, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, valcl, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Mikko breakout (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prevDisplayType
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    limit = prev_calculated - 1
    currDisplayType = -1
    _sw1 = inpDisplayStyle
    if _sw1 == dis_line:
        currDisplayType = CHART_LINE
    elif _sw1 == dis_bars:
        currDisplayType = CHART_BARS
    elif _sw1 == dis_candles:
        currDisplayType = CHART_CANDLES
    elif _sw1 == dis_automatic:
        currDisplayType = _int(ChartGetInteger(0, CHART_MODE))
    if currDisplayType != _s_OnCalculate_prevDisplayType:
        limit = 0
        _s_OnCalculate_prevDisplayType = currDisplayType
    i = MathMax(limit, 0)
    while i < rates_total:
        _start = MathMax(i - inpPeriod, 0)
        mmLow = low[ArrayMinimum(low, _start, inpPeriod)]
        mmHigh = high[ArrayMaximum(high, _start, inpPeriod)]
        trend = (1 if (high[i] > mmHigh) else -1 if (low[i] < mmLow) else 0)
        val[i] = ((high[i - 1] if (trend == 1) else low[i - 1] if (trend == -1) else ((high[i - 1] + low[i - 1]) / 2.0)) if (i > 0) else EMPTY_VALUE)
        valcl[i] = ((1 if (trend == 1) else 2 if (trend == -1) else valcl[i - 1]) if (i > 0) else 0)
        barc[i] = EMPTY_VALUE
        barl[i] = barc[i]
        barh[i] = barl[i]
        baro[i] = barh[i]
        canc[i] = EMPTY_VALUE
        canl[i] = canc[i]
        canh[i] = canl[i]
        cano[i] = canh[i]
        line[i] = EMPTY_VALUE
        if trend != 0:
            _sw2 = currDisplayType
            if _sw2 == CHART_BARS:
                barh[i] = high[i]
                barl[i] = low[i]
                barc[i] = close[i]
                baro[i] = open[i]
                barcl[i] = valcl[i]
            elif _sw2 == CHART_CANDLES:
                canh[i] = high[i]
                canl[i] = low[i]
                canc[i] = close[i]
                cano[i] = open[i]
                cancl[i] = valcl[i]
            elif _sw2 == CHART_LINE:
                line[i] = val[i]
                linecl[i] = valcl[i]
        i += 1
    return i

# ---- static local variables
_s_OnCalculate_prevDisplayType = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MikkoBreakout(_MQL5Indicator):
    name = 'Mikko breakout'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Period / count
        'inpDisplayStyle': _Choice({0: 'Automatic display style', 1: 'Display line', 2: 'Display bars', 3: 'Display candles'}, default=0),  # Display style
    }

