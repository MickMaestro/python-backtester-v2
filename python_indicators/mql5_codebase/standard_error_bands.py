"""Standard_Error_Bands — converted from MQL5: MQL5 Indicators/Standard_Error_Bands/Standard_Error_Bands.mq5

Standard Error Bands indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [16711680], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'StdErr Top', 2: 'StdErr Central', 3: 'StdErr Bottom'}, 'levels': [], 'description': ['Standard Error Bands indicator'], 'name': 'Standard_Error_Bands', 'source': 'MQL5 Indicators/Standard_Error_Bands/Standard_Error_Bands.mq5', 'folder': 'Standard_Error_Bands', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 21, 'label': 'Regression period', 'sinput': False}, {'mql': 'InpPeriodSM', 'py': 'InpPeriodSM', 'param': 'InpPeriodSM', 'type': 'uint', 'default': 3, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 2.0, 'label': 'Multiplier', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 21)  # Regression period
InpPeriodSM = _input('InpPeriodSM', 3)  # Smoothing period
InpMultiplier = _input('InpMultiplier', 2.0)  # Multiplier
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTop = Arr(0, 0.0)
BufferCentral = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferLreg = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
BufferMADevTmp = Arr(0, 0.0)
multiplier = 0.0
period_reg = 0
period_max = 0
period_sm = 0
handle_ma = 0

def OnInit():
    global handle_ma, multiplier, period_max, period_reg, period_sm
    multiplier = InpMultiplier
    period_reg = (2 if (InpPeriod < 2) else InpPeriod)
    period_sm = (2 if (InpPeriodSM < 2) else InpPeriodSM)
    period_max = fmax(period_reg, period_sm)
    SetIndexBuffer(0, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCentral, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(3, BufferLreg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferMADevTmp, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Standard Error Bands (' + _str(period_reg) + ',' + _str(period_sm) + ',' + DoubleToString(multiplier, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_max + 2)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, period_max + 2)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, period_max + 2)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferCentral, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferLreg, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferDev, True)
    ArraySetAsSeries(BufferMADevTmp, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 1
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferCentral, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferLreg, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferDev, 0)
        ArrayInitialize(BufferMADevTmp, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        x = 0.0
        y = 0.0
        xy = 0.0
        x2 = 0.0
        for j in range(0, period_reg):
            y += BufferMA[i + j]
            xy += BufferMA[i + j] * j
            x += j
            x2 += j * j
        Temp = (period_reg * x2) - (x * x)
        m = _fdiv((period_reg * xy) - (x * y), Temp)
        yint = _fdiv(y + (m * x), period_reg)
        BufferLreg[i] = yint - (m * period_reg)
    if StdDevOnArray(rates_total, prev_calculated, 0, period_sm, MODE_SMA, BufferMADevTmp, BufferLreg, BufferDev) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferCentral[i] = GetSMA(rates_total, i, period_sm, BufferLreg)
        deviation = BufferDev[i]
        dev = multiplier * deviation
        BufferTop[i] = BufferCentral[i] + dev
        BufferBottom[i] = BufferCentral[i] - dev
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)

def StdDevOnArray(rates_total, prev_calculated, begin, period, method, buffer_ma_tmp, src_array, dest_buffer):
    pos = 0
    if rates_total < period:
        return 0
    as_series_arr = ArrayGetAsSeries(src_array)
    as_series_dev = ArrayGetAsSeries(dest_buffer)
    as_series_ma = ArrayGetAsSeries(buffer_ma_tmp)
    if as_series_arr:
        ArraySetAsSeries(src_array, False)
    if as_series_dev:
        ArraySetAsSeries(dest_buffer, False)
    if as_series_ma:
        ArraySetAsSeries(buffer_ma_tmp, False)
    pos = prev_calculated - 1
    if pos < period:
        pos = period - 1
        ArrayInitialize(dest_buffer, 0.0)
        ArrayInitialize(buffer_ma_tmp, 0.0)
    _sw1 = method
    if _sw1 == MODE_EMA:
        for i in range(pos, rates_total):
            if i == (period - 1):
                buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            else:
                buffer_ma_tmp[i] = ExponentialMA(i, period, buffer_ma_tmp[i - 1], src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    elif _sw1 == MODE_SMMA:
        for i in range(pos, rates_total):
            if i == (period - 1):
                buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            else:
                buffer_ma_tmp[i] = SmoothedMA(i, period, buffer_ma_tmp[i - 1], src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    elif _sw1 == MODE_LWMA:
        for i in range(pos, rates_total):
            buffer_ma_tmp[i] = LinearWeightedMA(i, period, src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    else:
        for i in range(pos, rates_total):
            buffer_ma_tmp[i] = SimpleMA(i, period, src_array)
            dest_buffer[i] = StdDevFunc(src_array, buffer_ma_tmp, period, i)
    if as_series_arr:
        ArraySetAsSeries(src_array, True)
    if as_series_dev:
        ArraySetAsSeries(dest_buffer, True)
    if as_series_ma:
        ArraySetAsSeries(buffer_ma_tmp, True)
    return rates_total

def StdDevFunc(price, price_ma, period, position):
    dev = 0.0
    for i in range(0, period):
        dev += pow(price[position - i] - price_ma[position], 2)
    dev = sqrt(_fdiv(dev, period))
    return dev


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StandardErrorBands(_MQL5Indicator):
    name = 'Standard_Error_Bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 21,  # Regression period
        'InpPeriodSM': 3,  # Smoothing period
        'InpMultiplier': 2.0,  # Multiplier
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

