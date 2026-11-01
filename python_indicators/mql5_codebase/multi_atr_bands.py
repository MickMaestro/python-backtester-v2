"""Multi_ATR_Bands — converted from MQL5: MQL5 Indicators/Multi_ATR_Bands/Multi_ATR_Bands.mq5

Three ATR Bands with multiple selection
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 15, 'indicator_plots': 9}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, 'colors': {1: [255], 2: [255], 3: [255], 4: [32768], 5: [32768], 6: [32768], 7: [16711680], 8: [16711680], 9: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'labels': {1: 'Top Band 1', 2: 'Middle Band 1', 3: 'Bottom Band 1', 4: 'Top Band 2', 5: 'Middle Band 2', 6: 'Bottom Band 2', 7: 'Top Band 3', 8: 'Middle Band 3', 9: 'Bottom Band 3'}, 'levels': [], 'description': ['Three ATR Bands with multiple selection'], 'name': 'Multi_ATR_Bands', 'source': 'MQL5 Indicators/Multi_ATR_Bands/Multi_ATR_Bands.mq5', 'folder': 'Multi_ATR_Bands', 'inputs': [{'mql': 'InpShowMiddle', 'py': 'InpShowMiddle', 'param': 'InpShowMiddle', 'type': 'int', 'default': 0, 'label': 'Show middle lines', 'sinput': False}, {'mql': 'InpShowBands1', 'py': 'InpShowBands1', 'param': 'InpShowBands1', 'type': 'int', 'default': 1, 'label': 'Show first ATR Bands', 'sinput': False}, {'mql': 'InpPeriodATR1', 'py': 'InpPeriodATR1', 'param': 'InpPeriodATR1', 'type': 'uint', 'default': 14, 'label': 'First ATR period', 'sinput': False}, {'mql': 'InpPeriodMA1', 'py': 'InpPeriodMA1', 'param': 'InpPeriodMA1', 'type': 'uint', 'default': 14, 'label': 'First MA period', 'sinput': False}, {'mql': 'InpMethod1', 'py': 'InpMethod1', 'param': 'InpMethod1', 'type': 'int', 'default': 1, 'label': 'First MA type', 'sinput': False}, {'mql': 'InpAppliedPrice1', 'py': 'InpAppliedPrice1', 'param': 'InpAppliedPrice1', 'type': 'int', 'default': 1, 'label': 'First applied price', 'sinput': False}, {'mql': 'InpPercent1', 'py': 'InpPercent1', 'param': 'InpPercent1', 'type': 'double', 'default': 2.0, 'label': 'First bands multiplier', 'sinput': False}, {'mql': 'InpShowBands2', 'py': 'InpShowBands2', 'param': 'InpShowBands2', 'type': 'int', 'default': 1, 'label': 'Show second ATR Bands', 'sinput': False}, {'mql': 'InpPeriodATR2', 'py': 'InpPeriodATR2', 'param': 'InpPeriodATR2', 'type': 'uint', 'default': 18, 'label': 'Second ATR period', 'sinput': False}, {'mql': 'InpPeriodMA2', 'py': 'InpPeriodMA2', 'param': 'InpPeriodMA2', 'type': 'uint', 'default': 50, 'label': 'Second MA period', 'sinput': False}, {'mql': 'InpMethod2', 'py': 'InpMethod2', 'param': 'InpMethod2', 'type': 'int', 'default': 2, 'label': 'Second MA type', 'sinput': False}, {'mql': 'InpAppliedPrice2', 'py': 'InpAppliedPrice2', 'param': 'InpAppliedPrice2', 'type': 'int', 'default': 1, 'label': 'Second applied price', 'sinput': False}, {'mql': 'InpPercent2', 'py': 'InpPercent2', 'param': 'InpPercent2', 'type': 'double', 'default': 2.0, 'label': 'Second bands multiplier', 'sinput': False}, {'mql': 'InpShowBands3', 'py': 'InpShowBands3', 'param': 'InpShowBands3', 'type': 'int', 'default': 1, 'label': 'Show third ATR Bands', 'sinput': False}, {'mql': 'InpPeriodATR3', 'py': 'InpPeriodATR3', 'param': 'InpPeriodATR3', 'type': 'uint', 'default': 15, 'label': 'Third ATR period', 'sinput': False}, {'mql': 'InpPeriodMA3', 'py': 'InpPeriodMA3', 'param': 'InpPeriodMA3', 'type': 'uint', 'default': 100, 'label': 'Third MA period', 'sinput': False}, {'mql': 'InpMethod3', 'py': 'InpMethod3', 'param': 'InpMethod3', 'type': 'int', 'default': 8, 'label': 'Third MA type', 'sinput': False}, {'mql': 'InpAppliedPrice3', 'py': 'InpAppliedPrice3', 'param': 'InpAppliedPrice3', 'type': 'int', 'default': 1, 'label': 'Third applied price', 'sinput': False}, {'mql': 'InpPercent3', 'py': 'InpPercent3', 'param': 'InpPercent3', 'type': 'double', 'default': 2.0, 'label': 'Third bands multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MA_MODE
METHOD_SMA = 0
METHOD_EMA = 1
METHOD_SMMA = 2
METHOD_LWMA = 3
METHOD_WILDER_EMA = 4
METHOD_SINE_WMA = 5
METHOD_TRI_MA = 6
METHOD_LSMA = 7
METHOD_HMA = 8
METHOD_ZL_EMA = 9
METHOD_ITREND_MA = 10
METHOD_MOVING_MEDIAN = 11
METHOD_GEO_MEAN = 12
METHOD_REMA = 13
METHOD_ILRS = 14
METHOD_IE_2 = 15
METHOD_TRI_MA_GEN = 16
METHOD_VWMA = 17
_enum('ENUM_MA_MODE', {0: 'METHOD_SMA', 1: 'METHOD_EMA', 2: 'METHOD_SMMA', 3: 'METHOD_LWMA', 4: 'METHOD_WILDER_EMA', 5: 'METHOD_SINE_WMA', 6: 'METHOD_TRI_MA', 7: 'METHOD_LSMA', 8: 'METHOD_HMA', 9: 'METHOD_ZL_EMA', 10: 'METHOD_ITREND_MA', 11: 'METHOD_MOVING_MEDIAN', 12: 'METHOD_GEO_MEAN', 13: 'METHOD_REMA', 14: 'METHOD_ILRS', 15: 'METHOD_IE_2', 16: 'METHOD_TRI_MA_GEN', 17: 'METHOD_VWMA'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpShowMiddle = _input('InpShowMiddle', INPUT_NO)  # Show middle lines
InpShowBands1 = _input('InpShowBands1', INPUT_YES)  # Show first ATR Bands
InpPeriodATR1 = _input('InpPeriodATR1', 14)  # First ATR period
InpPeriodMA1 = _input('InpPeriodMA1', 14)  # First MA period
InpMethod1 = _input('InpMethod1', METHOD_EMA)  # First MA type
InpAppliedPrice1 = _input('InpAppliedPrice1', PRICE_CLOSE)  # First applied price
InpPercent1 = _input('InpPercent1', 2.0)  # First bands multiplier
InpShowBands2 = _input('InpShowBands2', INPUT_YES)  # Show second ATR Bands
InpPeriodATR2 = _input('InpPeriodATR2', 18)  # Second ATR period
InpPeriodMA2 = _input('InpPeriodMA2', 50)  # Second MA period
InpMethod2 = _input('InpMethod2', METHOD_SMMA)  # Second MA type
InpAppliedPrice2 = _input('InpAppliedPrice2', PRICE_CLOSE)  # Second applied price
InpPercent2 = _input('InpPercent2', 2.0)  # Second bands multiplier
InpShowBands3 = _input('InpShowBands3', INPUT_YES)  # Show third ATR Bands
InpPeriodATR3 = _input('InpPeriodATR3', 15)  # Third ATR period
InpPeriodMA3 = _input('InpPeriodMA3', 100)  # Third MA period
InpMethod3 = _input('InpMethod3', METHOD_HMA)  # Third MA type
InpAppliedPrice3 = _input('InpAppliedPrice3', PRICE_CLOSE)  # Third applied price
InpPercent3 = _input('InpPercent3', 2.0)  # Third bands multiplier
BufferTop1 = Arr(0, 0.0)
BufferMiddle1 = Arr(0, 0.0)
BufferBottom1 = Arr(0, 0.0)
BufferTop2 = Arr(0, 0.0)
BufferMiddle2 = Arr(0, 0.0)
BufferBottom2 = Arr(0, 0.0)
BufferTop3 = Arr(0, 0.0)
BufferMiddle3 = Arr(0, 0.0)
BufferBottom3 = Arr(0, 0.0)
BufferATR1 = Arr(0, 0.0)
BufferATR2 = Arr(0, 0.0)
BufferATR3 = Arr(0, 0.0)
BufferPrice1 = Arr(0, 0.0)
BufferPrice2 = Arr(0, 0.0)
BufferPrice3 = Arr(0, 0.0)
percent1 = 0.0
percent2 = 0.0
percent3 = 0.0
period_ma1 = 0
period_ma2 = 0
period_ma3 = 0
period_atr1 = 0
period_atr2 = 0
period_atr3 = 0
period_max = 0
handle_ma1 = 0
handle_ma2 = 0
handle_ma3 = 0
handle_atr1 = 0
handle_atr2 = 0
handle_atr3 = 0

def OnInit():
    global handle_atr1, handle_atr2, handle_atr3, handle_ma1, handle_ma2, handle_ma3, percent1, percent2, percent3, period_atr1, period_atr2, period_atr3, period_ma1, period_ma2, period_ma3, period_max
    percent1 = InpPercent1
    percent2 = InpPercent2
    percent3 = InpPercent3
    period_ma1 = (2 if (InpPeriodMA1 < 2) else InpPeriodMA1)
    period_ma2 = (2 if (InpPeriodMA2 < 2) else InpPeriodMA2)
    period_ma3 = (2 if (InpPeriodMA3 < 2) else InpPeriodMA3)
    period_atr1 = (1 if (InpPeriodATR1 < 1) else InpPeriodATR1)
    period_atr2 = (1 if (InpPeriodATR2 < 1) else InpPeriodATR2)
    period_atr3 = (1 if (InpPeriodATR3 < 1) else InpPeriodATR3)
    period_max = fmax(period_ma1, fmax(period_ma2, period_ma3))
    SetIndexBuffer(0, BufferTop1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMiddle1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom1, INDICATOR_DATA)
    SetIndexBuffer(3, BufferTop2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferMiddle2, INDICATOR_DATA)
    SetIndexBuffer(5, BufferBottom2, INDICATOR_DATA)
    SetIndexBuffer(6, BufferTop3, INDICATOR_DATA)
    SetIndexBuffer(7, BufferMiddle3, INDICATOR_DATA)
    SetIndexBuffer(8, BufferBottom3, INDICATOR_DATA)
    SetIndexBuffer(9, BufferATR1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferATR2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferATR3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferPrice1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferPrice2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, BufferPrice3, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MTF ATR Bands')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, InpShowBands1)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, (InpShowMiddle if InpShowBands1 else 0))
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, InpShowBands1)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, InpShowBands2)
    PlotIndexSetInteger(4, PLOT_DRAW_TYPE, (InpShowMiddle if InpShowBands2 else 0))
    PlotIndexSetInteger(5, PLOT_DRAW_TYPE, InpShowBands2)
    PlotIndexSetInteger(6, PLOT_DRAW_TYPE, InpShowBands3)
    PlotIndexSetInteger(7, PLOT_DRAW_TYPE, (InpShowMiddle if InpShowBands3 else 0))
    PlotIndexSetInteger(8, PLOT_DRAW_TYPE, InpShowBands3)
    ArraySetAsSeries(BufferTop1, True)
    ArraySetAsSeries(BufferMiddle1, True)
    ArraySetAsSeries(BufferBottom1, True)
    ArraySetAsSeries(BufferTop2, True)
    ArraySetAsSeries(BufferMiddle2, True)
    ArraySetAsSeries(BufferBottom2, True)
    ArraySetAsSeries(BufferTop3, True)
    ArraySetAsSeries(BufferMiddle3, True)
    ArraySetAsSeries(BufferBottom3, True)
    ArraySetAsSeries(BufferATR1, True)
    ArraySetAsSeries(BufferATR2, True)
    ArraySetAsSeries(BufferATR3, True)
    ArraySetAsSeries(BufferPrice1, True)
    ArraySetAsSeries(BufferPrice2, True)
    ArraySetAsSeries(BufferPrice3, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice1)
    if handle_ma1 == INVALID_HANDLE:
        Print(217, ': The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice2)
    if handle_ma2 == INVALID_HANDLE:
        Print(223, ': The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma3 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice3)
    if handle_ma3 == INVALID_HANDLE:
        Print(229, ': The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_atr1 = iATR(None, PERIOD_CURRENT, period_atr1)
    if handle_atr1 == INVALID_HANDLE:
        Print(235, ': The iATR(', _str(period_atr1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_atr2 = iATR(None, PERIOD_CURRENT, period_atr2)
    if handle_atr2 == INVALID_HANDLE:
        Print(241, ': The iATR(', _str(period_atr2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_atr3 = iATR(None, PERIOD_CURRENT, period_atr3)
    if handle_atr3 == INVALID_HANDLE:
        Print(247, ': The iATR(', _str(period_atr3), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 1
        ArrayInitialize(BufferTop1, EMPTY_VALUE)
        ArrayInitialize(BufferMiddle1, 0)
        ArrayInitialize(BufferBottom1, EMPTY_VALUE)
        ArrayInitialize(BufferTop2, EMPTY_VALUE)
        ArrayInitialize(BufferMiddle2, 0)
        ArrayInitialize(BufferBottom2, EMPTY_VALUE)
        ArrayInitialize(BufferTop3, EMPTY_VALUE)
        ArrayInitialize(BufferMiddle3, 0)
        ArrayInitialize(BufferBottom3, EMPTY_VALUE)
        ArrayInitialize(BufferATR1, 0)
        ArrayInitialize(BufferATR2, 0)
        ArrayInitialize(BufferATR3, 0)
        ArrayInitialize(BufferPrice1, 0)
        ArrayInitialize(BufferPrice2, 0)
        ArrayInitialize(BufferPrice3, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferPrice1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count, BufferPrice2)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma3, 0, 0, count, BufferPrice3)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr1, 0, 0, count, BufferATR1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr2, 0, 0, count, BufferATR2)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr3, 0, 0, count, BufferATR3)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        GetMA(rates_total, InpMethod1, period_ma1, i, BufferPrice1, BufferMiddle1, tick_volume)
        BufferTop1[i] = BufferMiddle1[i] + (BufferATR1[i] * percent1)
        BufferBottom1[i] = BufferMiddle1[i] - (BufferATR1[i] * percent1)
        GetMA(rates_total, InpMethod2, period_ma2, i, BufferPrice2, BufferMiddle2, tick_volume)
        BufferTop2[i] = BufferMiddle2[i] + (BufferATR2[i] * percent2)
        BufferBottom2[i] = BufferMiddle2[i] - (BufferATR2[i] * percent2)
        GetMA(rates_total, InpMethod3, period_ma3, i, BufferPrice3, BufferMiddle3, tick_volume)
        BufferTop3[i] = BufferMiddle3[i] + (BufferATR3[i] * percent1)
        BufferBottom3[i] = BufferMiddle3[i] - (BufferATR3[i] * percent1)
    return rates_total

def GetMA(rates_total, method, period, shift, price, ma, tick_volume):
    _sw1 = method
    if _sw1 == METHOD_EMA:
        ma[shift] = EMA(rates_total, price[shift], ma[shift + 1], period, shift)
    elif _sw1 == METHOD_SMMA:
        ma[shift] = SMMA(rates_total, price, ma[shift + 1], period, shift)
    elif _sw1 == METHOD_LWMA:
        ma[shift] = LWMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_WILDER_EMA:
        ma[shift] = Wilder(rates_total, price[shift], ma[shift + 1], period, shift)
    elif _sw1 == METHOD_SINE_WMA:
        ma[shift] = SineWMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_TRI_MA:
        ma[shift] = TriMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_LSMA:
        ma[shift] = LSMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_HMA:
        ma[shift] = HMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_ZL_EMA:
        ma[shift] = ZeroLagEMA(rates_total, price, ma[shift + 1], period, shift)
    elif _sw1 == METHOD_ITREND_MA:
        ma[shift] = ITrend(rates_total, price, ma, period, shift)
    elif _sw1 == METHOD_MOVING_MEDIAN:
        ma[shift] = Median(rates_total, price, period, shift)
    elif _sw1 == METHOD_GEO_MEAN:
        ma[shift] = GeoMean(rates_total, price, period, shift)
    elif _sw1 == METHOD_REMA:
        ma[shift] = REMA(rates_total, price[shift], ma, period, 0.5, shift)
    elif _sw1 == METHOD_ILRS:
        ma[shift] = ILRS(rates_total, price, period, shift)
    elif _sw1 == METHOD_IE_2:
        ma[shift] = IE2(rates_total, price, period, shift)
    elif _sw1 == METHOD_TRI_MA_GEN:
        ma[shift] = TriMAgen(rates_total, price, period, shift)
    elif _sw1 == METHOD_VWMA:
        ma[shift] = VWMA(rates_total, price, tick_volume, period, shift)
    else:
        ma[shift] = SMA(rates_total, price, period, shift)

def SMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return array_src[shift]
    sum_ = 0.0
    for i in range(0, period):
        sum_ += array_src[shift + i]
    return _fdiv(sum_, period)

def EMA(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + (_fdiv(2.0, 1 + period) * (price - prev))))

def Wilder(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + _fdiv(price - prev, period)))

def LWMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += period - i
        sum_ += array_src[shift + i] * (period - i)
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

def SineWMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += sin(_fdiv(M_PI * (i + 1), period + 1))
        sum_ += array_src[shift + i] * sin(_fdiv(M_PI * (i + 1), period + 1))
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

def TriMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sma = 0.0
    len_ = _int(ceil((period + 1) * 0.5))
    sum_ = 0.0
    for i in range(0, len_):
        sma = SMA(rates_total, array_src, len_, shift + i)
        sum_ += sma
    return _fdiv(sum_, len_)

def LSMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    for i in range(period, 1 - 1, -1):
        sum_ += (i - ((period + 1) / 3.0)) * array_src[shift + period - i]
    return _fdiv(sum_ * 6.0, period * (period + 1))

def SMMA(rates_total, array_src, prev, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    smma = 0.0
    if shift == (rates_total - period - 1):
        smma = SMA(rates_total, array_src, period, shift)
    elif shift < (rates_total - period - 1):
        sum_ = 0.0
        for i in range(0, period):
            sum_ += array_src[shift + i + 1]
        smma = _fdiv(sum_ - prev + array_src[shift], period)
    return smma

def HMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    tmp1 = Arr(0, 0.0)
    hma = 0.0
    len_ = _int(sqrt(period))
    ArrayResize(tmp1, len_)
    if shift == (rates_total - period - 1):
        hma = array_src[shift]
    elif shift < (rates_total - period - 1):
        for i in range(0, len_):
            tmp1[i] = (2.0 * LWMA(rates_total, array_src, _idiv(period, 2), shift + i)) - LWMA(rates_total, array_src, period, shift + i)
        hma = LWMA(rates_total, tmp1, len_, 0)
    return hma

def ZeroLagEMA(rates_total, array_src, prev, period, shift):
    alfa = _fdiv(2.0, 1 + period)
    lag = _int(0.5 * (period - 1))
    return (array_src[shift] if (shift >= (rates_total - lag)) else ((alfa * ((2.0 * array_src[shift]) - array_src[shift + lag])) + ((1 - alfa) * prev)))

def ITrend(rates_total, array_src, array, period, shift):
    alfa = _fdiv(2.0, period + 1)
    return ((((alfa - (0.25 * alfa * alfa)) * array_src[shift]) + (0.5 * alfa * alfa * array_src[shift + 1]) - ((alfa - (0.75 * alfa * alfa)) * array_src[shift + 2]) + (2 * (1 - alfa) * array[shift + 1]) - ((1 - alfa) * (1 - alfa) * array[shift + 2])) if (shift < (rates_total - 7)) else ((array_src[shift] + (2 * array_src[shift + 1]) + array_src[shift + 2]) / 4.0))

def Median(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    array = Arr(0, 0.0)
    ArrayResize(array, period)
    for i in range(0, period):
        array[i] = array_src[shift + i]
    ArraySort(array)
    num = _int(round(_idiv(period - 1, 2)))
    return (array_src[num] if (fmod(period, 2) > 0) else (0.5 * (array_src[num] + array[num + 1])))

def GeoMean(rates_total, array_src, period, shift):
    gmean = 0.0
    if shift < (rates_total - period):
        gmean = pow(array_src[shift], _fdiv(1.0, period))
        for i in range(1, period):
            gmean *= pow(array_src[shift + i], _fdiv(1.0, period))
    return gmean

def REMA(rates_total, price, array, period, lambda_, shift):
    alpha = _fdiv(2.0, period + 1)
    return (price if (shift >= (rates_total - 3)) else _fdiv((array[shift + 1] * (1 + (2 * lambda_))) + (alpha * (price - array[shift + 1])) - (lambda_ * array[shift + 2]), 1 + lambda_))

def ILRS(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = period * (period - 1) * 0.5
    sum2 = ((period - 1) * period * ((2 * period) - 1)) / 6.0
    sum1 = 0.0
    sumy = 0.0
    for i in range(0, period):
        sum1 += i * array_src[shift + i]
        sumy += array_src[shift + i]
    num1 = (period * sum1) - (sum_ * sumy)
    num2 = (sum_ * sum_) - (period * sum2)
    slope = (_fdiv(num1, num2) if (num2 != 0) else 0)
    return slope + SMA(rates_total, array_src, period, shift)

def IE2(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    return 0.5 * (ILRS(rates_total, array_src, period, shift) + LSMA(rates_total, array_src, period, shift))

def TriMAgen(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    len1 = _int(floor((period + 1) * 0.5))
    len2 = _int(ceil((period + 1) * 0.5))
    sum_ = 0.0
    for i in range(0, len2):
        sum_ += SMA(rates_total, array_src, len1, shift + i)
    return _fdiv(sum_, len2)

def VWMA(rates_total, array_src, volume, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += float(volume[shift + i])
        sum_ += array_src[shift + i] * volume[shift + i]
    return (_fdiv(sum_, weight) if (weight > 0) else 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultiATRBands(_MQL5Indicator):
    name = 'Multi_ATR_Bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpShowMiddle': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show middle lines
        'InpShowBands1': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show first ATR Bands
        'InpPeriodATR1': 14,  # First ATR period
        'InpPeriodMA1': 14,  # First MA period
        'InpMethod1': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'Linear-Weighted', 4: 'Wilder Exponential', 5: 'Sine-Weighted', 6: 'Triangular', 7: 'Least Square', 8: 'Hull MA by Alan Hull', 9: 'Zero-Lag Exponential', 10: 'Instantaneous Trendline by J.Ehlers', 11: 'Moving Median', 12: 'Geometric Mean', 13: 'Regularized EMA by Chris Satchwell', 14: 'Integral of Linear Regression Slope', 15: 'Combination of LSMA and ILRS', 16: 'Triangular MA generalized by J.Ehlers', 17: 'Volume-Weighted'}, default=1),  # First MA type
        'InpAppliedPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # First applied price
        'InpPercent1': 2.0,  # First bands multiplier
        'InpShowBands2': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show second ATR Bands
        'InpPeriodATR2': 18,  # Second ATR period
        'InpPeriodMA2': 50,  # Second MA period
        'InpMethod2': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'Linear-Weighted', 4: 'Wilder Exponential', 5: 'Sine-Weighted', 6: 'Triangular', 7: 'Least Square', 8: 'Hull MA by Alan Hull', 9: 'Zero-Lag Exponential', 10: 'Instantaneous Trendline by J.Ehlers', 11: 'Moving Median', 12: 'Geometric Mean', 13: 'Regularized EMA by Chris Satchwell', 14: 'Integral of Linear Regression Slope', 15: 'Combination of LSMA and ILRS', 16: 'Triangular MA generalized by J.Ehlers', 17: 'Volume-Weighted'}, default=2),  # Second MA type
        'InpAppliedPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Second applied price
        'InpPercent2': 2.0,  # Second bands multiplier
        'InpShowBands3': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show third ATR Bands
        'InpPeriodATR3': 15,  # Third ATR period
        'InpPeriodMA3': 100,  # Third MA period
        'InpMethod3': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'Linear-Weighted', 4: 'Wilder Exponential', 5: 'Sine-Weighted', 6: 'Triangular', 7: 'Least Square', 8: 'Hull MA by Alan Hull', 9: 'Zero-Lag Exponential', 10: 'Instantaneous Trendline by J.Ehlers', 11: 'Moving Median', 12: 'Geometric Mean', 13: 'Regularized EMA by Chris Satchwell', 14: 'Integral of Linear Regression Slope', 15: 'Combination of LSMA and ILRS', 16: 'Triangular MA generalized by J.Ehlers', 17: 'Volume-Weighted'}, default=8),  # Third MA type
        'InpAppliedPrice3': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Third applied price
        'InpPercent3': 2.0,  # Third bands multiplier
    }

