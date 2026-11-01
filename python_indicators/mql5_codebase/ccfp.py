"""CCFp — converted from MQL5: MQL5 Indicators/CCFp (Complex Common Frames percent)/CCFp.mq5

The indicator can be started ONLY on these timeframes:
                                           M1
                                           M5
                                           M15
                                           M30
                                           H1
                                           H4
                                           D1
                                           W1
                                           MN1
Copyright: SemSemFX@rambler.ru; Link: http://onix-trade.net/forum/index.php?showtopic=107; Version: 1.002

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'SemSemFX@rambler.ru', 'link': 'http://onix-trade.net/forum/index.php?showtopic=107', 'version': '1.002', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [32768], 2: [9109504], 3: [255], 4: [1993170], 5: [128], 6: [36095], 7: [8388736], 8: [8421376]}, 'widths': {}, 'styles': {}, 'labels': {1: 'USD', 2: 'EUR', 3: 'GBP', 4: 'CHF', 5: 'JPY', 6: 'AUD', 7: 'CAD', 8: 'NZD'}, 'levels': [], 'description': ['The indicator can be started ONLY on these timeframes:', '                                           M1', '                                           M5', '                                           M15', '                                           M30', '                                           H1', '                                           H4', '                                           D1', '                                           W1', '                                           MN1'], 'name': 'CCFp', 'source': 'MQL5 Indicators/CCFp (Complex Common Frames percent)/CCFp.mq5', 'folder': 'CCFp (Complex Common Frames percent)', 'inputs': [{'mql': 'InpFast_ma_period', 'py': 'InpFast_ma_period', 'param': 'InpFast_ma_period', 'type': 'int', 'default': 3, 'label': 'Fast MA: averaging period', 'sinput': False}, {'mql': 'InpSlow_ma_period', 'py': 'InpSlow_ma_period', 'param': 'InpSlow_ma_period', 'type': 'int', 'default': 5, 'label': 'Slow MA: averaging period', 'sinput': False}, {'mql': 'Inp_ma_method', 'py': 'Inp_ma_method', 'param': 'Inp_ma_method', 'type': 'int', 'default': 0, 'label': "Fast and Slow MA's: smoothing type", 'sinput': False}, {'mql': 'Inp_applied_price', 'py': 'Inp_applied_price', 'param': 'Inp_applied_price', 'type': 'int', 'default': 1, 'label': "Fast and Slow MA's: type of price", 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFast_ma_period = _input('InpFast_ma_period', 3)  # Fast MA: averaging period
InpSlow_ma_period = _input('InpSlow_ma_period', 5)  # Slow MA: averaging period
Inp_ma_method = _input('Inp_ma_method', MODE_SMA)  # Fast and Slow MA's: smoothing type
Inp_applied_price = _input('Inp_applied_price', PRICE_CLOSE)  # Fast and Slow MA's: type of price
ExtUSDBuffer = Arr(0, 0.0)
ExtEURBuffer = Arr(0, 0.0)
ExtGBPBuffer = Arr(0, 0.0)
ExtCHFBuffer = Arr(0, 0.0)
ExtJPYBuffer = Arr(0, 0.0)
ExtAUDBuffer = Arr(0, 0.0)
ExtCADBuffer = Arr(0, 0.0)
ExtNZDBuffer = Arr(0, 0.0)
array_symbols = Arr.of(['EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY'], fill="", dyn=False, size=7)
array_coef = Arr.of([1, 5, 3, 2, 2, 4, 6, 4], fill=0, dyn=False, size=8)
coefficient = 1
handles_Fast_EURUSD = Arr(0, 0)
handles_Fast_GBPUSD = Arr(0, 0)
handles_Fast_AUDUSD = Arr(0, 0)
handles_Fast_NZDUSD = Arr(0, 0)
handles_Fast_USDCAD = Arr(0, 0)
handles_Fast_USDCHF = Arr(0, 0)
handles_Fast_USDJPY = Arr(0, 0)
handles_Slow_EURUSD = Arr(0, 0)
handles_Slow_GBPUSD = Arr(0, 0)
handles_Slow_AUDUSD = Arr(0, 0)
handles_Slow_NZDUSD = Arr(0, 0)
handles_Slow_USDCAD = Arr(0, 0)
handles_Slow_USDCHF = Arr(0, 0)
handles_Slow_USDJPY = Arr(0, 0)

def OnInit():
    global coefficient
    if (((((((Period() != PERIOD_M1 and Period() != PERIOD_M5) and Period() != PERIOD_M15) and Period() != PERIOD_M30) and Period() != PERIOD_H1) and Period() != PERIOD_H4) and Period() != PERIOD_D1) and Period() != PERIOD_W1) and Period() != PERIOD_MN1:
        Alert('The indicator can be started ONLY on these timeframes: M1, M5, M15, M30, H1, H4, D1, W1, MN1')
        return INIT_FAILED
    total_symbols = ArraySize(array_symbols)
    total_coef = ArraySize(array_coef)
    start_coef = 1
    _sw1 = Period()
    if _sw1 == PERIOD_M1:
        start_coef = 0
    elif _sw1 == PERIOD_M5:
        start_coef = 1
    elif _sw1 == PERIOD_M15:
        start_coef = 2
    elif _sw1 == PERIOD_M30:
        start_coef = 3
    elif _sw1 == PERIOD_H1:
        start_coef = 4
    elif _sw1 == PERIOD_H4:
        start_coef = 5
    elif _sw1 == PERIOD_D1:
        start_coef = 6
    for i in range(0, total_symbols):
        for j in range(start_coef, total_coef):
            coefficient = (1 if (j == start_coef) else (coefficient * array_coef[j]))
            Fast_handle = Box(0)
            if not CreateMA(array_symbols[i], Period(), InpFast_ma_period * coefficient, 0, Inp_ma_method, Inp_applied_price, Fast_handle):
                return INIT_FAILED
            Slow_handle = Box(0)
            if not CreateMA(array_symbols[i], Period(), InpSlow_ma_period * coefficient, 0, Inp_ma_method, Inp_applied_price, Slow_handle):
                return INIT_FAILED
            size = -1
            _sw2 = i
            if _sw2 == 0:
                size = ArraySize(handles_Fast_EURUSD)
                ArrayResize(handles_Fast_EURUSD, size + 1)
                handles_Fast_EURUSD[size] = Fast_handle.v
                size = ArraySize(handles_Slow_EURUSD)
                ArrayResize(handles_Slow_EURUSD, size + 1)
                handles_Slow_EURUSD[size] = Slow_handle.v
            elif _sw2 == 1:
                size = ArraySize(handles_Fast_GBPUSD)
                ArrayResize(handles_Fast_GBPUSD, size + 1)
                handles_Fast_GBPUSD[size] = Fast_handle.v
                size = ArraySize(handles_Slow_GBPUSD)
                ArrayResize(handles_Slow_GBPUSD, size + 1)
                handles_Slow_GBPUSD[size] = Slow_handle.v
            elif _sw2 == 2:
                size = ArraySize(handles_Fast_AUDUSD)
                ArrayResize(handles_Fast_AUDUSD, size + 1)
                handles_Fast_AUDUSD[size] = Fast_handle.v
                size = ArraySize(handles_Slow_AUDUSD)
                ArrayResize(handles_Slow_AUDUSD, size + 1)
                handles_Slow_AUDUSD[size] = Slow_handle.v
            elif _sw2 == 3:
                size = ArraySize(handles_Fast_NZDUSD)
                ArrayResize(handles_Fast_NZDUSD, size + 1)
                handles_Fast_NZDUSD[size] = Fast_handle.v
                size = ArraySize(handles_Slow_NZDUSD)
                ArrayResize(handles_Slow_NZDUSD, size + 1)
                handles_Slow_NZDUSD[size] = Slow_handle.v
            elif _sw2 == 4:
                size = ArraySize(handles_Fast_USDCAD)
                ArrayResize(handles_Fast_USDCAD, size + 1)
                handles_Fast_USDCAD[size] = Fast_handle.v
                size = ArraySize(handles_Slow_USDCAD)
                ArrayResize(handles_Slow_USDCAD, size + 1)
                handles_Slow_USDCAD[size] = Slow_handle.v
            elif _sw2 == 5:
                size = ArraySize(handles_Fast_USDCHF)
                ArrayResize(handles_Fast_USDCHF, size + 1)
                handles_Fast_USDCHF[size] = Fast_handle.v
                size = ArraySize(handles_Slow_USDCHF)
                ArrayResize(handles_Slow_USDCHF, size + 1)
                handles_Slow_USDCHF[size] = Slow_handle.v
            elif _sw2 == 6:
                size = ArraySize(handles_Fast_USDJPY)
                ArrayResize(handles_Fast_USDJPY, size + 1)
                handles_Fast_USDJPY[size] = Fast_handle.v
                size = ArraySize(handles_Slow_USDJPY)
                ArrayResize(handles_Slow_USDJPY, size + 1)
                handles_Slow_USDJPY[size] = Slow_handle.v
    size = ArraySize(handles_Fast_EURUSD)
    if (((((((((((((((size != ArraySize(handles_Slow_EURUSD) or size != ArraySize(handles_Fast_GBPUSD)) or size != ArraySize(handles_Slow_GBPUSD)) or size != ArraySize(handles_Fast_AUDUSD)) or size != ArraySize(handles_Slow_AUDUSD)) or size != ArraySize(handles_Fast_NZDUSD)) or size != ArraySize(handles_Slow_NZDUSD)) or size != ArraySize(handles_Fast_USDCAD)) or size != ArraySize(handles_Slow_USDCAD)) or size != ArraySize(handles_Fast_USDCHF)) or size != ArraySize(handles_Slow_USDCHF)) or size != ArraySize(handles_Fast_USDJPY)) or size != ArraySize(handles_Slow_USDJPY)) or size != ArraySize(handles_Fast_GBPUSD)) or size != ArraySize(handles_Slow_GBPUSD)) or size != ArraySize(handles_Fast_GBPUSD)) or size != ArraySize(handles_Slow_GBPUSD):
        Alert('ArraySize !=')
        return INIT_FAILED
    array_EURUSD = Arr(0, 0.0)
    array_GBPUSD = Arr(0, 0.0)
    array_AUDUSD = Arr(0, 0.0)
    array_NZDUSD = Arr(0, 0.0)
    array_USDCAD = Arr(0, 0.0)
    array_USDCHF = Arr(0, 0.0)
    array_USDJPY = Arr(0, 0.0)
    CopyClose('EURUSD', Period(), 0, 1000, array_EURUSD)
    CopyClose('GBPUSD', Period(), 0, 1000, array_GBPUSD)
    CopyClose('AUDUSD', Period(), 0, 1000, array_AUDUSD)
    CopyClose('NZDUSD', Period(), 0, 1000, array_NZDUSD)
    CopyClose('USDCAD', Period(), 0, 1000, array_USDCAD)
    CopyClose('USDCHF', Period(), 0, 1000, array_USDCHF)
    CopyClose('USDJPY', Period(), 0, 1000, array_USDJPY)
    SetIndexBuffer(0, ExtUSDBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtEURBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtGBPBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCHFBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtJPYBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtAUDBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtCADBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ExtNZDBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(ExtUSDBuffer, True)
    ArraySetAsSeries(ExtEURBuffer, True)
    ArraySetAsSeries(ExtGBPBuffer, True)
    ArraySetAsSeries(ExtCHFBuffer, True)
    ArraySetAsSeries(ExtJPYBuffer, True)
    ArraySetAsSeries(ExtAUDBuffer, True)
    ArraySetAsSeries(ExtCADBuffer, True)
    ArraySetAsSeries(ExtNZDBuffer, True)
    ArrayInitialize(ExtUSDBuffer, 0.0)
    ArrayInitialize(ExtEURBuffer, 0.0)
    ArrayInitialize(ExtGBPBuffer, 0.0)
    ArrayInitialize(ExtCHFBuffer, 0.0)
    ArrayInitialize(ExtJPYBuffer, 0.0)
    ArrayInitialize(ExtAUDBuffer, 0.0)
    ArrayInitialize(ExtCADBuffer, 0.0)
    ArrayInitialize(ExtNZDBuffer, 0.0)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    bars_EURUSD = Bars('EURUSD', Period())
    bars_GBPUSD = Bars('GBPUSD', Period())
    bars_AUDUSD = Bars('AUDUSD', Period())
    bars_NZDUSD = Bars('NZDUSD', Period())
    bars_USDCAD = Bars('USDCAD', Period())
    bars_USDCHF = Bars('USDCHF', Period())
    bars_USDJPY = Bars('USDJPY', Period())
    if (((((bars_EURUSD == 0 or bars_GBPUSD == 0) or bars_AUDUSD == 0) or bars_NZDUSD == 0) or bars_USDCAD == 0) or bars_USDCHF == 0) or bars_USDJPY == 0:
        return 0
    size = ArraySize(handles_Fast_EURUSD)
    for i in range(0, size):
        if BarsCalculated(handles_Fast_EURUSD[i]) != bars_EURUSD:
            return 0
        if BarsCalculated(handles_Fast_GBPUSD[i]) != bars_GBPUSD:
            return 0
        if BarsCalculated(handles_Fast_AUDUSD[i]) != bars_AUDUSD:
            return 0
        if BarsCalculated(handles_Fast_NZDUSD[i]) != bars_NZDUSD:
            return 0
        if BarsCalculated(handles_Fast_USDCAD[i]) != bars_USDCAD:
            return 0
        if BarsCalculated(handles_Fast_USDCHF[i]) != bars_USDCHF:
            return 0
        if BarsCalculated(handles_Fast_USDJPY[i]) != bars_USDJPY:
            return 0
        if BarsCalculated(handles_Slow_EURUSD[i]) != bars_EURUSD:
            return 0
        if BarsCalculated(handles_Slow_GBPUSD[i]) != bars_GBPUSD:
            return 0
        if BarsCalculated(handles_Slow_AUDUSD[i]) != bars_AUDUSD:
            return 0
        if BarsCalculated(handles_Slow_NZDUSD[i]) != bars_NZDUSD:
            return 0
        if BarsCalculated(handles_Slow_USDCAD[i]) != bars_USDCAD:
            return 0
        if BarsCalculated(handles_Slow_USDCHF[i]) != bars_USDCHF:
            return 0
        if BarsCalculated(handles_Slow_USDJPY[i]) != bars_USDJPY:
            return 0
    array_bars = Arr(7, 0, dyn=False)
    array_bars[0] = bars_EURUSD
    array_bars[1] = bars_GBPUSD
    array_bars[2] = bars_AUDUSD
    array_bars[3] = bars_NZDUSD
    array_bars[4] = bars_USDCAD
    array_bars[5] = bars_USDCHF
    array_bars[6] = bars_USDJPY
    limit = INT_MAX
    if prev_calculated == 0:
        size = ArraySize(array_bars)
        for i in range(0, size):
            if limit > array_bars[i]:
                limit = array_bars[i]
        index = coefficient * _int(MathMax(float(InpFast_ma_period), float(InpSlow_ma_period)))
        limit = MathMin(index, limit)
    else:
        limit = rates_total - prev_calculated + 1
    size = ArraySize(handles_Fast_EURUSD)
    ma_Fast = 0.0
    ma_Slow = 0.0
    ma = 0.0
    for i in range(limit, 0 - 1, -1):
        ma_Fast = 0.0
        ma_Slow = 0.0
        for j in range(0, size):
            ma = iMAGet(handles_Fast_EURUSD[j], i)
            if ma == 0.0:
                return 0
            ma_Fast += ma
            ma = iMAGet(handles_Slow_EURUSD[j], i)
            if ma == 0.0:
                return 0
            ma_Slow += ma
        if ma_Slow == 0.0 or ma_Fast == 0.0:
            return 0
        EURUSD = _fdiv(ma_Slow, ma_Fast)
        if EURUSD == 0.0:
            return 0
        ma_Fast = 0.0
        ma_Slow = 0.0
        for j in range(0, size):
            ma = iMAGet(handles_Fast_GBPUSD[j], i)
            if ma == 0.0:
                return 0
            ma_Fast += ma
            ma = iMAGet(handles_Slow_GBPUSD[j], i)
            if ma == 0.0:
                return 0
            ma_Slow += ma
        if ma_Slow == 0.0 or ma_Fast == 0.0:
            return 0
        GBPUSD = _fdiv(ma_Slow, ma_Fast)
        if GBPUSD == 0.0:
            return 0
        ma_Fast = 0.0
        ma_Slow = 0.0
        for j in range(0, size):
            ma = iMAGet(handles_Fast_AUDUSD[j], i)
            if ma == 0.0:
                return 0
            ma_Fast += ma
            ma = iMAGet(handles_Slow_AUDUSD[j], i)
            if ma == 0.0:
                return 0
            ma_Slow += ma
        if ma_Slow == 0.0 or ma_Fast == 0.0:
            return 0
        AUDUSD = _fdiv(ma_Slow, ma_Fast)
        if AUDUSD == 0.0:
            return 0
        ma_Fast = 0.0
        ma_Slow = 0.0
        for j in range(0, size):
            ma = iMAGet(handles_Fast_NZDUSD[j], i)
            if ma == 0.0:
                return 0
            ma_Fast += ma
            ma = iMAGet(handles_Slow_NZDUSD[j], i)
            if ma == 0.0:
                return 0
            ma_Slow += ma
        if ma_Slow == 0.0 or ma_Fast == 0.0:
            return 0
        NZDUSD = _fdiv(ma_Slow, ma_Fast)
        if NZDUSD == 0.0:
            return 0
        ma_Fast = 0.0
        ma_Slow = 0.0
        for j in range(0, size):
            ma = iMAGet(handles_Fast_USDCAD[j], i)
            if ma == 0.0:
                return 0
            ma_Fast += ma
            ma = iMAGet(handles_Slow_USDCAD[j], i)
            if ma == 0.0:
                return 0
            ma_Slow += ma
        if ma_Slow == 0.0 or ma_Fast == 0.0:
            return 0
        CADUSD = _fdiv(ma_Fast, ma_Slow)
        if CADUSD == 0.0:
            return 0
        ma_Fast = 0.0
        ma_Slow = 0.0
        for j in range(0, size):
            ma = iMAGet(handles_Fast_USDCHF[j], i)
            if ma == 0.0:
                return 0
            ma_Fast += ma
            ma = iMAGet(handles_Slow_USDCHF[j], i)
            if ma == 0.0:
                return 0
            ma_Slow += ma
        if ma_Slow == 0.0 or ma_Fast == 0.0:
            return 0
        CHFUSD = _fdiv(ma_Fast, ma_Slow)
        if CHFUSD == 0.0:
            return 0
        ma_Fast = 0.0
        ma_Slow = 0.0
        for j in range(0, size):
            ma = iMAGet(handles_Fast_USDJPY[j], i)
            if ma == 0.0:
                return 0
            ma_Fast += ma
            ma = iMAGet(handles_Slow_USDJPY[j], i)
            if ma == 0.0:
                return 0
            ma_Slow += ma
        if ma_Slow == 0.0 or ma_Fast == 0.0:
            return 0
        JPYUSD = _fdiv(ma_Fast, ma_Slow)
        if JPYUSD == 0.0:
            return 0
        sum_ = EURUSD + GBPUSD + AUDUSD + NZDUSD + CHFUSD + CADUSD + JPYUSD
        ExtUSDBuffer[i] = sum_ - 7.0
        ExtEURBuffer[i] = _fdiv(sum_ - EURUSD + 1.0, EURUSD) - 7.0
        ExtGBPBuffer[i] = _fdiv(sum_ - GBPUSD + 1.0, GBPUSD) - 7.0
        ExtAUDBuffer[i] = _fdiv(sum_ - AUDUSD + 1.0, AUDUSD) - 7.0
        ExtNZDBuffer[i] = _fdiv(sum_ - NZDUSD + 1.0, NZDUSD) - 7.0
        ExtCADBuffer[i] = _fdiv(sum_ - CADUSD + 1.0, CADUSD) - 7.0
        ExtCHFBuffer[i] = _fdiv(sum_ - CHFUSD + 1.0, CHFUSD) - 7.0
        ExtJPYBuffer[i] = _fdiv(sum_ - JPYUSD + 1.0, JPYUSD) - 7.0
    return rates_total

def CreateMA(symbol, period, ma_period, ma_shift, ma_method, applied_price, handle_iMA):
    ResetLastError()
    handle_iMA.v = iMA(symbol, period, ma_period, ma_shift, ma_method, applied_price)
    if handle_iMA.v == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s,%s, av. period %d, shift %d, smoothing %s, price %s,error code %d', symbol, EnumToString(period, 'ENUM_TIMEFRAMES'), ma_period, ma_shift, EnumToString(ma_method, 'ENUM_MA_METHOD'), EnumToString(applied_price, 'ENUM_APPLIED_PRICE'), GetLastError())
        return False
    return True

def iMAGet(handle_iMA, index):
    MA = Arr(1, 0.0, dyn=False)
    ResetLastError()
    if CopyBuffer(handle_iMA, 0, index, 1, MA) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return 0.0
    return MA[0]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCFp(_MQL5Indicator):
    name = 'CCFp'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFast_ma_period': 3,  # Fast MA: averaging period
        'InpSlow_ma_period': 5,  # Slow MA: averaging period
        'Inp_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Fast and Slow MA's: smoothing type
        'Inp_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Fast and Slow MA's: type of price
    }

