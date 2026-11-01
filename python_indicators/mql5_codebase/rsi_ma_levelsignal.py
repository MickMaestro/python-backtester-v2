"""rsi_ma_levelsignal — converted from MQL5: MQL5 Indicators/RSI_MA_LevelSignal/rsi_ma_levelsignal.mq5

Copyright: Copyright © 2009, Helen_Iv; Link: http://helenclubfinance.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Helen_Iv', 'link': 'http://helenclubfinance.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'RSI_MA_LevelSignal Sell', 2: 'RSI_MA_LevelSignal Buy'}, 'levels': [], 'description': [], 'name': 'rsi_ma_levelsignal', 'source': 'MQL5 Indicators/RSI_MA_LevelSignal/rsi_ma_levelsignal.mq5', 'folder': 'RSI_MA_LevelSignal', 'inputs': [{'mql': 'RsiPeriod', 'py': 'RsiPeriod', 'param': 'RsiPeriod', 'type': 'uint', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'Ma1Period', 'py': 'Ma1Period', 'param': 'Ma1Period', 'type': 'uint', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'Ma2Period', 'py': 'Ma2Period', 'param': 'Ma2Period', 'type': 'uint', 'default': 150, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RsiPeriod = _input('RsiPeriod', 7)
Ma1Period = _input('Ma1Period', 50)
Ma2Period = _input('Ma2Period', 150)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
Rsi_Handle = 0
Ma1_Handle = 0
Ma2_Handle = 0

def OnInit():
    global Ma1_Handle, Ma2_Handle, Rsi_Handle, min_rates_total
    min_rates_total = _int(MathMax(RsiPeriod + 1, MathMax(Ma1Period, Ma2Period)))
    Rsi_Handle = iRSI(None, 0, RsiPeriod, PRICE_CLOSE)
    if Rsi_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI indicator')
    Ma1_Handle = iMA(None, 0, Ma1Period, 0, MODE_EMA, PRICE_CLOSE)
    if Ma1_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA1 indicator')
    Ma2_Handle = iMA(None, 0, Ma2Period, 0, MODE_EMA, PRICE_CLOSE)
    if Ma2_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA2 indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'RSI_MA_LevelSignal Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'RSI_MA_LevelSignal Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'RSI_MA_LevelSignal'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(Rsi_Handle) < rates_total or BarsCalculated(Ma1_Handle) < rates_total) or BarsCalculated(Ma2_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    range_ = 0.0
    Rsi = Arr(0, 0.0)
    Ma1 = Arr(0, 0.0)
    Ma2 = Arr(0, 0.0)
    ArraySetAsSeries(Rsi, True)
    ArraySetAsSeries(Ma1, True)
    ArraySetAsSeries(Ma2, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ma1_Handle, 0, 0, to_copy, Ma1) <= 0:
        return 0
    if CopyBuffer(Ma2_Handle, 0, 0, to_copy, Ma2) <= 0:
        return 0
    to_copy += 1
    if CopyBuffer(Rsi_Handle, 0, 0, to_copy, Rsi) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        range_ = 0.0
        kkk = bar + 9
        while kkk <= bar:
            range_ += MathAbs(high[kkk] - low[kkk])
            kkk -= 1
        range_ *= 0.2 / 10.0
        if ((Rsi[bar] > 30.0 and Rsi[bar + 1] < 30.0) and Rsi[bar] > Rsi[bar + 1]) and Ma1[bar] > Ma2[bar]:
            BuyBuffer[bar] = low[bar] - range_
        if ((Rsi[bar] < 70.0 and Rsi[bar + 1] > 70.0) and Rsi[bar] < Rsi[bar + 1]) and Ma1[bar] < Ma2[bar]:
            SellBuffer[bar] = high[bar] + range_
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsiMaLevelsignal(_MQL5Indicator):
    name = 'rsi_ma_levelsignal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RsiPeriod': 7,
        'Ma1Period': 50,
        'Ma2Period': 150,
    }

