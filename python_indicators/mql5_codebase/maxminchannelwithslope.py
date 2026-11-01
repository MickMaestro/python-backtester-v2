"""maxminchannelwithslope — converted from MQL5: MQL5 Indicators/MaxminChannelWithSlope/maxminchannelwithslope.mq5

simple max - min channel with ema slope
Copyright: Copyright © 2016, fajuzi; Link: fajuzi@yahoo.it 2015; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, fajuzi', 'link': 'fajuzi@yahoo.it 2015', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [15658671]}, 'widths': {}, 'styles': {}, 'labels': {1: 'MaxminChannelWithSlope'}, 'levels': [], 'description': ['simple max - min channel with ema slope'], 'name': 'maxminchannelwithslope', 'source': 'MQL5 Indicators/MaxminChannelWithSlope/maxminchannelwithslope.mq5', 'folder': 'MaxminChannelWithSlope', 'inputs': [{'mql': 'barre', 'py': 'barre', 'param': 'barre', 'type': 'uint', 'default': 20, 'label': 'Bars for calculation min max', 'sinput': False}, {'mql': 'ratio', 'py': 'ratio', 'param': 'ratio', 'type': 'double', 'default': 4.0, 'label': 'Ratio EMA period / bars', 'sinput': False}, {'mql': 'xslope', 'py': 'xslope', 'param': 'xslope', 'type': 'double', 'default': 1.0, 'label': 'Slope adjustment', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
barre = _input('barre', 20)  # Bars for calculation min max
ratio = _input('ratio', 4.0)  # Ratio EMA period / bars
xslope = _input('xslope', 1.0)  # Slope adjustment
min_rates_total = 0
cosemap = 0.0
emap = 0.0
xslp = 0.0
pendenzaxslp = 0.0
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)

def OnInit():
    global cosemap, emap, min_rates_total, xslp
    min_rates_total = 3
    xslp = xslope * 0.5
    emap = barre * ratio
    cosemap = (emap + 1.0) / 2.0
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'MaxminChannelWithSlope(', barre, ', ', DoubleToString(ratio, 2), ', ', xslope, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_pendenza_prev, pendenzaxslp
    if rates_total < min_rates_total:
        return 0
    pendenza = 0.0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_pendenza_prev = 0.0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    for bar in range(limit, 0 - 1, -1):
        pendenza = _s_OnCalculate_pendenza_prev + _fdiv(High[bar] + Low[bar] - High[bar + 1] - Low[bar + 1] - _s_OnCalculate_pendenza_prev, cosemap)
        pendenzaxslp = pendenza * xslp
        _sw1 = bar + 1 - ArrayMaximum(High, bar, barre)
        if _sw1 == 0:
            UpBuffer[bar + 1] = High[bar + 1]
        else:
            UpBuffer[bar + 1] = UpBuffer[bar + 2] + pendenzaxslp
        _sw2 = bar + 1 - ArrayMinimum(Low, bar, barre)
        if _sw2 == 0:
            DnBuffer[bar + 1] = Low[bar + 1]
        else:
            DnBuffer[bar + 1] = DnBuffer[bar + 2] + pendenzaxslp
        if bar:
            _s_OnCalculate_pendenza_prev = pendenza
    UpBuffer[0] = UpBuffer[1] + pendenzaxslp
    DnBuffer[0] = DnBuffer[1] + pendenzaxslp
    return rates_total

# ---- static local variables
_s_OnCalculate_pendenza_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Maxminchannelwithslope(_MQL5Indicator):
    name = 'maxminchannelwithslope'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'barre': 20,  # Bars for calculation min max
        'ratio': 4.0,  # Ratio EMA period / bars
        'xslope': 1.0,  # Slope adjustment
    }

