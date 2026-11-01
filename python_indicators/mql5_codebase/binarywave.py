"""binarywave — converted from MQL5: MQL5 Indicators/BinaryWave_HTF/binarywave.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'BinaryWave'}, 'levels': [0.0], 'description': [], 'name': 'binarywave', 'source': 'MQL5 Indicators/BinaryWave_HTF/binarywave.mq5', 'folder': 'BinaryWave_HTF', 'inputs': [{'mql': 'WeightMA', 'py': 'WeightMA', 'param': 'WeightMA', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightMACD', 'py': 'WeightMACD', 'param': 'WeightMACD', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightOsMA', 'py': 'WeightOsMA', 'param': 'WeightOsMA', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightCCI', 'py': 'WeightCCI', 'param': 'WeightCCI', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightMOM', 'py': 'WeightMOM', 'param': 'WeightMOM', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightRSI', 'py': 'WeightRSI', 'param': 'WeightRSI', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WeightADX', 'py': 'WeightADX', 'param': 'WeightADX', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FastMACD', 'py': 'FastMACD', 'param': 'FastMACD', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowMACD', 'py': 'SlowMACD', 'param': 'SlowMACD', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'SignalMACD', 'py': 'SignalMACD', 'param': 'SignalMACD', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'PriceMACD', 'py': 'PriceMACD', 'param': 'PriceMACD', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'SignalPeriod', 'py': 'SignalPeriod', 'param': 'SignalPeriod', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'OsMAPrice', 'py': 'OsMAPrice', 'param': 'OsMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'MOMPeriod', 'py': 'MOMPeriod', 'param': 'MOMPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MOMPrice', 'py': 'MOMPrice', 'param': 'MOMPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ADXPeriod', 'py': 'ADXPeriod', 'param': 'ADXPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'bMA_Method', 'py': 'bMA_Method', 'param': 'bMA_Method', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'bLength', 'py': 'bLength', 'param': 'bLength', 'type': 'int', 'default': 5, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'bPhase', 'py': 'bPhase', 'param': 'bPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
WeightMA = _input('WeightMA', 1.0)
WeightMACD = _input('WeightMACD', 1.0)
WeightOsMA = _input('WeightOsMA', 1.0)
WeightCCI = _input('WeightCCI', 1.0)
WeightMOM = _input('WeightMOM', 1.0)
WeightRSI = _input('WeightRSI', 1.0)
WeightADX = _input('WeightADX', 1.0)
MAPeriod = _input('MAPeriod', 13)
MAType = _input('MAType', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
FastMACD = _input('FastMACD', 12)
SlowMACD = _input('SlowMACD', 26)
SignalMACD = _input('SignalMACD', 9)
PriceMACD = _input('PriceMACD', PRICE_CLOSE)
FastPeriod = _input('FastPeriod', 12)
SlowPeriod = _input('SlowPeriod', 26)
SignalPeriod = _input('SignalPeriod', 9)
OsMAPrice = _input('OsMAPrice', PRICE_CLOSE)
CCIPeriod = _input('CCIPeriod', 14)
CCIPrice = _input('CCIPrice', PRICE_MEDIAN)
MOMPeriod = _input('MOMPeriod', 14)
MOMPrice = _input('MOMPrice', PRICE_CLOSE)
RSIPeriod = _input('RSIPeriod', 14)
RSIPrice = _input('RSIPrice', PRICE_CLOSE)
ADXPeriod = _input('ADXPeriod', 14)
bMA_Method = _input('bMA_Method', MODE_JJMA)  # Метод усреднения
bLength = _input('bLength', 5)  # Глубина сглаживания
bPhase = _input('bPhase', 100)  # Параметр сглаживания
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_total_1 = 0
MA_Handle = 0
MACD_Handle = 0
OsMA_Handle = 0
CCI_Handle = 0
MOM_Handle = 0
RSI_Handle = 0
ADX_Handle = 0

def MAClose(bar, MaArray, Close):
    if WeightMA > 0:
        if (Close[bar] - MaArray[bar]) > 0:
            return WeightMA
        if (Close[bar] - MaArray[bar]) < 0:
            return -WeightMA
    return 0.0

def MACD(bar, MacdArray):
    if WeightMACD > 0:
        if (MacdArray[bar] - MacdArray[bar + 1]) > 0:
            return WeightMACD
        if (MacdArray[bar] - MacdArray[bar + 1]) < 0:
            return -WeightMACD
    return 0.0

def OsMA(bar, OsMAArray):
    if WeightOsMA > 0:
        if OsMAArray[bar] > 0:
            return WeightOsMA
        if OsMAArray[bar] < 0:
            return -WeightOsMA
    return 0.0

def CCI(bar, CCIArray):
    if WeightCCI > 0:
        if CCIArray[bar] > 0:
            return WeightCCI
        if CCIArray[bar] < 0:
            return -WeightCCI
    return 0.0

def MOM(bar, MOMArray):
    if WeightMOM > 0:
        if MOMArray[bar] > 100:
            return WeightMOM
        if MOMArray[bar] < 100:
            return -WeightMOM
    return 0.0

def RSI(bar, RSIArray):
    if WeightRSI > 0:
        if RSIArray[bar] > 50:
            return WeightRSI
        if RSIArray[bar] < 50:
            return -WeightRSI
    return 0.0

def ADX(bar, DMIPArray, DMIMArray):
    if WeightADX > 0:
        if DMIPArray[bar] > DMIMArray[bar]:
            return WeightADX
        if DMIPArray[bar] < DMIMArray[bar]:
            return -WeightADX
    return 0.0

def OnInit():
    global ADX_Handle, CCI_Handle, MACD_Handle, MA_Handle, MOM_Handle, OsMA_Handle, RSI_Handle, min_rates_total, min_rates_total_1
    min_rates_total_1 = MathMax(MAPeriod, MathMax(SlowPeriod, MathMax(CCIPeriod, MathMax(SlowMACD, MOMPeriod)))) + 1
    min_rates_total = min_rates_total_1 + XMA1.GetStartBars(bMA_Method, bLength, bPhase)
    XMA1.XMALengthCheck('bLength', bLength)
    XMA1.XMAPhaseCheck('bPhase', bPhase, bMA_Method)
    MA_Handle = iMA(None, 0, MAPeriod, 0, MAType, MAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    MACD_Handle = iMACD(None, 0, FastMACD, SlowMACD, SignalMACD, PriceMACD)
    if MACD_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMACD')
        return INIT_FAILED
    OsMA_Handle = iOsMA(None, 0, FastPeriod, SlowPeriod, SignalPeriod, OsMAPrice)
    if OsMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iOsMA')
        return INIT_FAILED
    CCI_Handle = iCCI(None, 0, CCIPeriod, CCIPrice)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI')
        return INIT_FAILED
    MOM_Handle = iMomentum(None, 0, MOMPeriod, MOMPrice)
    if MOM_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMomentum')
        return INIT_FAILED
    RSI_Handle = iRSI(None, 0, RSIPeriod, RSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    ADX_Handle = iADX(None, 0, ADXPeriod)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iADX')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(bMA_Method)
    StringConcatenate(shortname, 'BinaryWave(', bLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((((BarsCalculated(MA_Handle) < rates_total or BarsCalculated(MACD_Handle) < rates_total) or BarsCalculated(OsMA_Handle) < rates_total) or BarsCalculated(CCI_Handle) < rates_total) or BarsCalculated(MOM_Handle) < rates_total) or BarsCalculated(RSI_Handle) < rates_total) or BarsCalculated(ADX_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    tmp = 0.0
    MA_ = Arr(0, 0.0)
    MACD_ = Arr(0, 0.0)
    OsMA_ = Arr(0, 0.0)
    CCI_ = Arr(0, 0.0)
    MOM_ = Arr(0, 0.0)
    RSI_ = Arr(0, 0.0)
    DMIP_ = Arr(0, 0.0)
    DMIM_ = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - 2
    else:
        to_copy = rates_total - prev_calculated + 1
        limit = rates_total - prev_calculated
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA_) <= 0:
        return 0
    if CopyBuffer(MACD_Handle, 0, 0, to_copy + 1, MACD_) <= 0:
        return 0
    if CopyBuffer(OsMA_Handle, 0, 0, to_copy, OsMA_) <= 0:
        return 0
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI_) <= 0:
        return 0
    if CopyBuffer(MOM_Handle, 0, 0, to_copy, MOM_) <= 0:
        return 0
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI_) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 1, 0, to_copy, DMIP_) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 2, 0, to_copy, DMIM_) <= 0:
        return 0
    ArraySetAsSeries(MA_, True)
    ArraySetAsSeries(MACD_, True)
    ArraySetAsSeries(OsMA_, True)
    ArraySetAsSeries(CCI_, True)
    ArraySetAsSeries(MOM_, True)
    ArraySetAsSeries(RSI_, True)
    ArraySetAsSeries(DMIP_, True)
    ArraySetAsSeries(DMIM_, True)
    ArraySetAsSeries(close, True)
    maxbar = rates_total - min_rates_total_1 - 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        tmp = MAClose(bar, MA_, close) + MACD(bar, MACD_) + OsMA(bar, OsMA_) + CCI(bar, CCI_) + MOM(bar, MOM_) + RSI(bar, RSI_) + ADX(bar, DMIP_, DMIM_)
        IndBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, bMA_Method, bPhase, bLength, tmp, bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Binarywave(_MQL5Indicator):
    name = 'binarywave'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WeightMA': 1.0,
        'WeightMACD': 1.0,
        'WeightOsMA': 1.0,
        'WeightCCI': 1.0,
        'WeightMOM': 1.0,
        'WeightRSI': 1.0,
        'WeightADX': 1.0,
        'MAPeriod': 13,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'FastMACD': 12,
        'SlowMACD': 26,
        'SignalMACD': 9,
        'PriceMACD': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'FastPeriod': 12,
        'SlowPeriod': 26,
        'SignalPeriod': 9,
        'OsMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'CCIPeriod': 14,
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),
        'MOMPeriod': 14,
        'MOMPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSIPeriod': 14,
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'ADXPeriod': 14,
        'bMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'bLength': 5,  # Глубина сглаживания
        'bPhase': 100,  # Параметр сглаживания
    }

