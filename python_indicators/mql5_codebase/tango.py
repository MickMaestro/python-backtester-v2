"""tango — converted from MQL5: MQL5 Indicators/TANGO/tango.mq5

TANGO
Copyright: Copyright © 2009, MetaQL; Link: mrexpertforex@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, MetaQL', 'link': 'mrexpertforex@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 5}, 'colors': {1: [55295], 2: [16711680], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {}, 'labels': {1: 'TANGO Att', 2: 'TANGO Buy', 3: 'TANGO Sell'}, 'levels': [], 'description': ['TANGO'], 'name': 'tango', 'source': 'MQL5 Indicators/TANGO/tango.mq5', 'folder': 'TANGO', 'inputs': [{'mql': 'PeriodRSI', 'py': 'PeriodRSI', 'param': 'PeriodRSI', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'Level', 'py': 'Level', 'param': 'Level', 'type': 'double', 'default': 20.0, 'label': '', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PeriodRSI = _input('PeriodRSI', 20)
Level = _input('Level', 20.0)
Length = _input('Length', 100)
AttBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
RSI_Handle = 0
min_rates_total = 0

def OnInit():
    global RSI_Handle, min_rates_total
    min_rates_total = _int(PeriodRSI + Length + 1)
    RSI_Handle = iRSI(None, 0, PeriodRSI, PRICE_CLOSE)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the RSI indicator')
    SetIndexBuffer(0, AttBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 111)
    ArraySetAsSeries(AttBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'TANGO'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(RSI_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    RSI = Arr(0, 0.0)
    RSI_1 = 0.0
    HI_RSI = 0.0
    LO_RSI = 0.0
    RSI_2 = 0.0
    UP = 0.0
    DOWN = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = _int(limit + 1 + Length)
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        AttBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        RSI_1 = RSI[bar]
        HI_RSI = RSI_1
        LO_RSI = RSI_1
        for kkk in range(0, _int(Length)):
            RSI_2 = RSI[bar + kkk]
            if RSI_2 > HI_RSI:
                HI_RSI = RSI_2
            if RSI_2 < LO_RSI:
                LO_RSI = RSI_2
            if (close[bar + kkk] < close[bar] and RSI_2 >= RSI_1) or (close[bar + kkk] >= close[bar] and RSI_2 < RSI_1):
                UP = HI_RSI - (((HI_RSI - LO_RSI) / 100) * Level)
                if RSI_2 >= UP:
                    BuyBuffer[bar] = low[bar]
                DOWN = LO_RSI + (((HI_RSI - LO_RSI) / 100) * Level)
                if RSI_2 <= DOWN:
                    SellBuffer[bar] = high[bar]
                if RSI_2 > DOWN and RSI_2 < UP:
                    AttBuffer[bar] = close[bar]
                break
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Tango(_MQL5Indicator):
    name = 'tango'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodRSI': 20,
        'Level': 20.0,
        'Length': 100,
    }

