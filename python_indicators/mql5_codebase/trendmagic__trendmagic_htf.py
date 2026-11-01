"""trendmagic — converted from MQL5: MQL5 Indicators/TrendMagic_HTF/trendmagic.mq5

Copyright: Copyright © 2014, Sergey Gritsai; Link: sergey1294@list.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Sergey Gritsai', 'link': 'sergey1294@list.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [32768, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'TrendMagic'}, 'levels': [], 'description': [], 'name': 'trendmagic', 'source': 'MQL5 Indicators/TrendMagic_HTF/trendmagic.mq5', 'folder': 'TrendMagic_HTF', 'inputs': [{'mql': 'CCI_Period', 'py': 'CCI_Period', 'param': 'CCI_Period', 'type': 'uint', 'default': 50, 'label': 'CCI period', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 5, 'label': 'CCI price', 'sinput': False}, {'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'uint', 'default': 5, 'label': 'ATR period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CCI_Period = _input('CCI_Period', 50)  # CCI period
CCIPrice = _input('CCIPrice', PRICE_MEDIAN)  # CCI price
ATR_Period = _input('ATR_Period', 5)  # ATR period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0
CCI_Handle = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, CCI_Handle, dPriceShift, min_rates_total
    min_rates_total = _int(MathMax(CCI_Period, ATR_Period))
    CCI_Handle = iCCI(None, 0, CCI_Period, CCIPrice)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iCCI indicator')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get the iATR indicator handle')
        return INIT_FAILED
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'TrendMagic(', CCI_Period, ', ', ATR_Period, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(CCI_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    CCI = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(CCI, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if CCI[bar] >= 0.0:
            IndBuffer[bar] = low[bar] - ATR[bar] + PriceShift
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                IndBuffer[bar] = IndBuffer[bar + 1]
            ColorIndBuffer[bar] = 0.0
        elif CCI[bar] < 0.0:
            IndBuffer[bar] = high[bar] + ATR[bar] + PriceShift
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                IndBuffer[bar] = IndBuffer[bar + 1]
            ColorIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendmagic(_MQL5Indicator):
    name = 'trendmagic'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CCI_Period': 50,  # CCI period
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # CCI price
        'ATR_Period': 5,  # ATR period
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

