"""forexprofitboost_2nb — converted from MQL5: MQL5 Indicators/ForexProfitBoost_2nb/forexprofitboost_2nb.mq5

Copyright: Copyright © 2015, TradeLikeaPro.ru; Link: http://tradelikeapro.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, TradeLikeaPro.ru', 'link': 'http://tradelikeapro.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 4, 2: 4, 3: 4}, 'colors': {1: [42495], 2: [9639167], 3: [16711680]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'ForexProfitBoost_2nb 1', 2: 'ForexProfitBoost_2nb 2', 3: 'ForexProfitBoost_2nb 3'}, 'levels': [], 'description': [], 'name': 'forexprofitboost_2nb', 'source': 'MQL5 Indicators/ForexProfitBoost_2nb/forexprofitboost_2nb.mq5', 'folder': 'ForexProfitBoost_2nb', 'inputs': [{'mql': 'MAPeriod1', 'py': 'MAPeriod1', 'param': 'MAPeriod1', 'type': 'uint', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'MAType1', 'py': 'MAType1', 'param': 'MAType1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice1', 'py': 'MAPrice1', 'param': 'MAPrice1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPeriod2', 'py': 'MAPeriod2', 'param': 'MAPeriod2', 'type': 'uint', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'MAType2', 'py': 'MAType2', 'param': 'MAType2', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MAPrice2', 'py': 'MAPrice2', 'param': 'MAPrice2', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'BBDeviation', 'py': 'BBDeviation', 'param': 'BBDeviation', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'BBShift', 'py': 'BBShift', 'param': 'BBShift', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod1 = _input('MAPeriod1', 7)
MAType1 = _input('MAType1', MODE_EMA)
MAPrice1 = _input('MAPrice1', PRICE_CLOSE)
MAPeriod2 = _input('MAPeriod2', 21)
MAType2 = _input('MAType2', MODE_SMA)
MAPrice2 = _input('MAPrice2', PRICE_CLOSE)
BBPeriod = _input('BBPeriod', 15)
BBDeviation = _input('BBDeviation', 1.0)
BBShift = _input('BBShift', 1)
min_rates_total = 0
upmax = Arr(0, 0.0)
upmin = Arr(0, 0.0)
dnmax = Arr(0, 0.0)
dnmin = Arr(0, 0.0)
max_ = Arr(0, 0.0)
min_ = Arr(0, 0.0)
MA1_Handle = 0
MA2_Handle = 0
BB_Handle = 0

def OnInit():
    global BB_Handle, MA1_Handle, MA2_Handle, min_rates_total
    min_rates_total = _int(MathMax(BBPeriod, MathMax(MAPeriod1, MAPeriod2)))
    MA1_Handle = iMA(None, 0, MAPeriod1, 0, MAType1, MAPrice1)
    if MA1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA 1')
        return INIT_FAILED
    MA2_Handle = iMA(None, 0, MAPeriod2, 0, MAType2, MAPrice2)
    if MA2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA 2')
        return INIT_FAILED
    MA2_Handle = iMA(None, 0, MAPeriod2, 0, MAType2, MAPrice2)
    if MA2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA 2')
        return INIT_FAILED
    BB_Handle = iBands(None, 0, BBPeriod, BBShift, BBDeviation, PRICE_CLOSE)
    if BB_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBands')
        return INIT_FAILED
    SetIndexBuffer(0, max_, INDICATOR_DATA)
    SetIndexBuffer(1, min_, INDICATOR_DATA)
    SetIndexBuffer(2, dnmax, INDICATOR_DATA)
    SetIndexBuffer(3, dnmin, INDICATOR_DATA)
    SetIndexBuffer(4, upmax, INDICATOR_DATA)
    SetIndexBuffer(5, upmin, INDICATOR_DATA)
    ArraySetAsSeries(upmax, True)
    ArraySetAsSeries(upmin, True)
    ArraySetAsSeries(dnmax, True)
    ArraySetAsSeries(dnmin, True)
    ArraySetAsSeries(max_, True)
    ArraySetAsSeries(min_, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'ForexProfitBoost_2nb'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if ((BarsCalculated(BB_Handle) < rates_total or BarsCalculated(MA1_Handle) < rates_total) or BarsCalculated(MA2_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    MA1 = Arr(0, 0.0)
    MA2 = Arr(0, 0.0)
    UpBB = Arr(0, 0.0)
    DnBB = Arr(0, 0.0)
    limit = 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(MA1, True)
    ArraySetAsSeries(MA2, True)
    ArraySetAsSeries(UpBB, True)
    ArraySetAsSeries(DnBB, True)
    to_copy = limit + 1
    if CopyBuffer(MA1_Handle, 0, 0, to_copy, MA1) <= 0:
        return 0
    if CopyBuffer(MA2_Handle, 0, 0, to_copy, MA2) <= 0:
        return 0
    if CopyBuffer(BB_Handle, UPPER_BAND, 0, to_copy, UpBB) <= 0:
        return 0
    if CopyBuffer(BB_Handle, LOWER_BAND, 0, to_copy, DnBB) <= 0:
        return 0
    for bar in range(limit, 0 - 1, -1):
        max_[bar] = MathMax(UpBB[bar], MathMax(MA1[bar], MA2[bar]))
        min_[bar] = MathMin(DnBB[bar], MathMin(MA1[bar], MA2[bar]))
        if MA1[bar] > MA2[bar]:
            upmax[bar] = MathMax(MA1[bar], MA2[bar])
            upmin[bar] = MathMin(DnBB[bar], MathMin(MA1[bar], MA2[bar]))
            dnmax[bar] = EMPTY_VALUE
            dnmin[bar] = EMPTY_VALUE
        else:
            dnmax[bar] = MathMax(UpBB[bar], MathMax(MA1[bar], MA2[bar]))
            dnmin[bar] = MathMin(MA1[bar], MA2[bar])
            upmax[bar] = EMPTY_VALUE
            upmin[bar] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Forexprofitboost2nb(_MQL5Indicator):
    name = 'forexprofitboost_2nb'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod1': 7,
        'MAType1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'MAPeriod2': 21,
        'MAType2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'MAPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'BBPeriod': 15,
        'BBDeviation': 1.0,
        'BBShift': 1,
    }

