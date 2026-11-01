"""breaktrend — converted from MQL5: MQL5 Indicators/BreakTrend/breaktrend.mq5

ATR ratio
Copyright: Copyright © 2014, Ramil Minniakhmetov; Link: https://www.mql5.com/ru/users/mechanic; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Ramil Minniakhmetov', 'link': 'https://www.mql5.com/ru/users/mechanic', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'BreakTrend Sell', 2: 'BreakTrend Buy'}, 'levels': [], 'description': ['ATR ratio'], 'name': 'breaktrend', 'source': 'MQL5 Indicators/BreakTrend/breaktrend.mq5', 'folder': 'BreakTrend', 'inputs': [{'mql': 'i_nPriceDistance', 'py': 'i_nPriceDistance', 'param': 'i_nPriceDistance', 'type': 'uint', 'default': 1000, 'label': 'Price difference', 'sinput': False}, {'mql': 'i_nNumberOfBars', 'py': 'i_nNumberOfBars', 'param': 'i_nNumberOfBars', 'type': 'uint', 'default': 18, 'label': 'Bars to analyse', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
i_nPriceDistance = _input('i_nPriceDistance', 1000)  # Price difference
i_nNumberOfBars = _input('i_nNumberOfBars', 18)  # Bars to analyse
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
dPriceDistance = 0.0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, dPriceDistance, min_rates_total
    dPriceDistance = Point() * i_nPriceDistance
    ATR_Period = 15
    min_rates_total = _int(MathMax(ATR_Period, i_nNumberOfBars)) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'BreakTrend'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy += 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HH = high[ArrayMaximum(high, bar, i_nNumberOfBars)]
        LL = low[ArrayMinimum(low, bar, i_nNumberOfBars)]
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if low[bar] <= (HH - dPriceDistance):
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if high[bar] >= (LL + dPriceDistance):
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Breaktrend(_MQL5Indicator):
    name = 'breaktrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'i_nPriceDistance': 1000,  # Price difference
        'i_nNumberOfBars': 18,  # Bars to analyse
    }

