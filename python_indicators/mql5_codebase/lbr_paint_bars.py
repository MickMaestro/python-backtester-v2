"""LBR_Paint_Bars — converted from MQL5: MQL5 Indicators/LBR_Paint_Bars/LBR_Paint_Bars.mq5

LBR Paint Bars indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 11, 'indicator_plots': 4}, 'types': {1: 11, 2: 17, 3: 1, 4: 1}, 'colors': {1: [7451452, 5275647, 11119017], 2: [32768, 255, 9157775, 12180223, 11119017], 3: [9419919], 4: [9221330]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 2, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Cloud edge1;Cloud edge2', 2: 'Open;High;Low;Close', 3: 'Line1', 4: 'Line2'}, 'levels': [], 'description': ['LBR Paint Bars indicator'], 'name': 'LBR_Paint_Bars', 'source': 'MQL5 Indicators/LBR_Paint_Bars/LBR_Paint_Bars.mq5', 'folder': 'LBR_Paint_Bars', 'inputs': [{'mql': 'InpFactor', 'py': 'InpFactor', 'param': 'InpFactor', 'type': 'double', 'default': 2.5, 'label': 'Factor', 'sinput': False}, {'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 9, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpPeriodHL', 'py': 'InpPeriodHL', 'param': 'InpPeriodHL', 'type': 'uint', 'default': 16, 'label': 'HL period', 'sinput': False}, {'mql': 'InpShowCandles', 'py': 'InpShowCandles', 'param': 'InpShowCandles', 'type': 'int', 'default': 1, 'label': 'Color Candles', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# enum ENUM_CANDLE_TYPE
CANDLE_TYPE_BULLISH = 0
CANDLE_TYPE_BEARISH = 1
CANDLE_TYPE_DOJI = 2
_enum('ENUM_CANDLE_TYPE', {0: 'CANDLE_TYPE_BULLISH', 1: 'CANDLE_TYPE_BEARISH', 2: 'CANDLE_TYPE_DOJI'})

# ---- inputs and global variables
InpFactor = _input('InpFactor', 2.5)  # Factor
InpPeriodATR = _input('InpPeriodATR', 9)  # ATR period
InpPeriodHL = _input('InpPeriodHL', 16)  # HL period
InpShowCandles = _input('InpShowCandles', INPUT_YES)  # Color Candles
BufferCloud1 = Arr(0, 0.0)
BufferCloud2 = Arr(0, 0.0)
BufferColorsCloud = Arr(0, 0.0)
BufferCandleOpen = Arr(0, 0.0)
BufferCandleHigh = Arr(0, 0.0)
BufferCandleLow = Arr(0, 0.0)
BufferCandleClose = Arr(0, 0.0)
BufferColorsCandle = Arr(0, 0.0)
BufferLine1 = Arr(0, 0.0)
BufferLine2 = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
factor = 0.0
period_atr = 0
period_hl = 0
handle_atr = 0

def OnInit():
    global factor, handle_atr, period_atr, period_hl
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    period_hl = (1 if (InpPeriodHL < 1) else InpPeriodHL)
    factor = fabs(InpFactor)
    SetIndexBuffer(0, BufferCloud1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCloud2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferColorsCloud, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, BufferCandleOpen, INDICATOR_DATA)
    SetIndexBuffer(4, BufferCandleHigh, INDICATOR_DATA)
    SetIndexBuffer(5, BufferCandleLow, INDICATOR_DATA)
    SetIndexBuffer(6, BufferCandleClose, INDICATOR_DATA)
    SetIndexBuffer(7, BufferColorsCandle, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, BufferLine1, INDICATOR_DATA)
    SetIndexBuffer(9, BufferLine2, INDICATOR_DATA)
    SetIndexBuffer(10, BufferATR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'LBR Paint Bars (' + DoubleToString(factor, 1) + ',' + _str(period_atr) + ',' + _str(period_hl) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferCloud1, True)
    ArraySetAsSeries(BufferCloud2, True)
    ArraySetAsSeries(BufferColorsCloud, True)
    ArraySetAsSeries(BufferCandleOpen, True)
    ArraySetAsSeries(BufferCandleHigh, True)
    ArraySetAsSeries(BufferCandleLow, True)
    ArraySetAsSeries(BufferCandleClose, True)
    ArraySetAsSeries(BufferColorsCandle, True)
    ArraySetAsSeries(BufferLine1, True)
    ArraySetAsSeries(BufferLine2, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_hl, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_hl - 1
        ArrayInitialize(BufferCloud1, EMPTY_VALUE)
        ArrayInitialize(BufferCloud2, EMPTY_VALUE)
        ArrayInitialize(BufferColorsCloud, 2)
        ArrayInitialize(BufferCandleOpen, EMPTY_VALUE)
        ArrayInitialize(BufferCandleHigh, EMPTY_VALUE)
        ArrayInitialize(BufferCandleLow, EMPTY_VALUE)
        ArrayInitialize(BufferCandleClose, EMPTY_VALUE)
        ArrayInitialize(BufferColorsCandle, 4)
        ArrayInitialize(BufferLine1, EMPTY_VALUE)
        ArrayInitialize(BufferLine2, EMPTY_VALUE)
        ArrayInitialize(BufferATR, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        ATR = BufferATR[i]
        delta = factor * ATR
        bl = Lowest(period_hl, i)
        bh = Highest(period_hl, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            return 0
        min_ = low[bl]
        max_ = high[bh]
        BufferCloud1[i] = min_ + delta
        BufferLine1[i] = BufferCloud1[i]
        BufferCloud2[i] = max_ - delta
        BufferLine2[i] = BufferCloud2[i]
        BufferColorsCloud[i] = (0 if (BufferCloud1[i] > BufferCloud2[i]) else 1 if (BufferCloud1[i] < BufferCloud2[i]) else 2)
        UpperVolatility = (True if (close[i] > BufferCloud1[i] and close[i] > BufferCloud2[i]) else False)
        LowerVolatility = (True if (close[i] < BufferCloud1[i] and close[i] < BufferCloud2[i]) else False)
        if InpShowCandles:
            type_ = CandleType(i, open, close)
            BufferCandleOpen[i] = open[i]
            BufferCandleHigh[i] = high[i]
            BufferCandleLow[i] = low[i]
            BufferCandleClose[i] = close[i]
            if UpperVolatility:
                BufferColorsCandle[i] = (0 if (type_ == CANDLE_TYPE_BULLISH) else 2 if (type_ == CANDLE_TYPE_BEARISH) else 4)
            else:
                if LowerVolatility:
                    BufferColorsCandle[i] = (1 if (type_ == CANDLE_TYPE_BEARISH) else 3 if (type_ == CANDLE_TYPE_BULLISH) else 4)
                else:
                    BufferColorsCandle[i] = 4.0
    return rates_total

def Highest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start, as_series=True):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, as_series)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def CandleType(index, open, close):
    return (CANDLE_TYPE_BULLISH if (close[index] > open[index]) else CANDLE_TYPE_BEARISH if (close[index] < open[index]) else CANDLE_TYPE_DOJI)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LBRPaintBars(_MQL5Indicator):
    name = 'LBR_Paint_Bars'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFactor': 2.5,  # Factor
        'InpPeriodATR': 9,  # ATR period
        'InpPeriodHL': 16,  # HL period
        'InpShowCandles': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Color Candles
    }

