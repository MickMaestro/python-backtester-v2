"""matonysignal — converted from MQL5: MQL5 Indicators/MATonySignal/matonysignal.mq5

Indicator of the maximal trend
Copyright: Copyright © 2008, Jpkfox; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, Jpkfox', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [17919, 8388736, 8421504, 13434880, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'MATonySignal'}, 'levels': [], 'description': ['Indicator of the maximal trend'], 'name': 'matonysignal', 'source': 'MQL5 Indicators/MATonySignal/matonysignal.mq5', 'folder': 'MATonySignal', 'inputs': [{'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 1, 'label': 'Smoothing MA method', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 34, 'label': 'MA period', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'uint', 'default': 1, 'label': 'Period for the difference', 'sinput': False}, {'mql': 'MA_Level', 'py': 'MA_Level', 'param': 'MA_Level', 'type': 'uint', 'default': 30, 'label': 'minimal price difference in points for the start', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_SMethod = _input('MA_SMethod', MODE_EMA)  # Smoothing MA method
MA_Length = _input('MA_Length', 34)  # MA period
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # Applied price
MomPeriod = _input('MomPeriod', 1)  # Period for the difference
MA_Level = _input('MA_Level', 30)  # minimal price difference in points for the start
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
dLevel = 0.0
min_rates_total = 0
MA_Handle = 0

def OnInit():
    global MA_Handle, dLevel, min_rates_total
    min_rates_total = _int(MA_Length + MomPeriod)
    dLevel = Point() * MA_Level
    MA_Handle = iMA(None, 0, MA_Length, 0, MA_SMethod, AppliedPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
        return 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'MATonySignal(', MA_Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 1.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -1.0)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(MA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    dma = 0.0
    MA = Arr(0, 0.0)
    to_copy = 0
    limit = 0
    ArraySetAsSeries(MA, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = _int(limit + 1 + MomPeriod)
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    for bar in range(limit, 0 - 1, -1):
        dma = MA[bar] - MA[bar + MomPeriod]
        IndBuffer[bar] = 0.0
        ColorIndBuffer[bar] = 2.0
        if dma > 0:
            if dma > dLevel:
                IndBuffer[bar] = 2.0
                ColorIndBuffer[bar] = 4.0
            else:
                IndBuffer[bar] = 1.0
                ColorIndBuffer[bar] = 3.0
        if dma < 0:
            if dma < (-dLevel):
                IndBuffer[bar] = -2.0
                ColorIndBuffer[bar] = 0.0
            else:
                IndBuffer[bar] = -1.0
                ColorIndBuffer[bar] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Matonysignal(_MQL5Indicator):
    name = 'matonysignal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_SMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Smoothing MA method
        'MA_Length': 34,  # MA period
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'MomPeriod': 1,  # Period for the difference
        'MA_Level': 30,  # minimal price difference in points for the start
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

