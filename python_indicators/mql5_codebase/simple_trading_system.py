"""simple_trading_system — converted from MQL5: MQL5 Indicators/Simple Trading System/simple_trading_system.mq5

Copyright: Copyright 2014, Vitalie Postolache; Link: http://www.mql4.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014, Vitalie Postolache', 'link': 'http://www.mql4.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [9639167], 2: [11186720]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'simple_trading_system Sell', 2: 'simple_trading_system Buy'}, 'levels': [], 'description': [], 'name': 'simple_trading_system', 'source': 'MQL5 Indicators/Simple Trading System/simple_trading_system.mq5', 'folder': 'Simple Trading System', 'inputs': [{'mql': 'MAShift', 'py': 'MAShift', 'param': 'MAShift', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAShift = _input('MAShift', 4)
MAPeriod = _input('MAPeriod', 2)
MAType = _input('MAType', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
MA_Handle = 0
ATR_Handle = 0
min_rates_total = 0
Count = Arr(0, 0)
MAShift_ = 0
SumPeriod = 0
Ma = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global ATR_Handle, MAShift_, MA_Handle, SumPeriod, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(MathMax(ATR_Period, MAPeriod + MAShift))
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    MA_Handle = iMA(None, 0, MAPeriod, 0, MAType, MAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    MAShift_ = _int(MAShift + 1)
    SumPeriod = _int(MAPeriod + MAShift)
    ArrayResize(Count, MAShift_)
    ArrayResize(Ma, MAShift_)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Ma, 0.0)
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'simple_trading_system'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_sign1
    if (BarsCalculated(MA_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    sign0 = 0
    MA = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    ma0 = 0.0
    ma1 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_sign1 = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(MA, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    sign0 = _s_OnCalculate_sign1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        Ma[Count[0]] = MA[bar]
        ma0 = MA[bar]
        ma1 = Ma[Count[MAShift]]
        if (((sign0 < 1 and ma0 <= ma1) and close[bar] >= close[bar + MAShift]) and close[bar] <= close[bar + SumPeriod]) and close[bar] < open[bar]:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            sign0 = 1
        if (((sign0 > -1 and ma0 >= ma1) and close[bar] <= close[bar + MAShift]) and close[bar] >= close[bar + SumPeriod]) and close[bar] > open[bar]:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
            sign0 = -1
        if bar:
            Recount_ArrayZeroPos(Count, MAShift_)
            _s_OnCalculate_sign1 = sign0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_sign1 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SimpleTradingSystem(_MQL5Indicator):
    name = 'simple_trading_system'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAShift': 4,
        'MAPeriod': 2,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

