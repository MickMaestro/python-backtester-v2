"""MA_Signal — converted from MQL5: MQL5 Indicators/MA_Signal/MA_Signal.mq5

MA signal indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [3329330], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bullish signal', 2: 'Bearish signal'}, 'levels': [], 'description': ['MA signal indicator'], 'name': 'MA_Signal', 'source': 'MQL5 Indicators/MA_Signal/MA_Signal.mq5', 'folder': 'MA_Signal', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 10, 'label': 'First MA period', 'sinput': False}, {'mql': 'InpAppliedPrice1', 'py': 'InpAppliedPrice1', 'param': 'InpAppliedPrice1', 'type': 'int', 'default': 1, 'label': 'First MA applied price', 'sinput': False}, {'mql': 'InpMethod1', 'py': 'InpMethod1', 'param': 'InpMethod1', 'type': 'int', 'default': 1, 'label': 'First MA method', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 50, 'label': 'Second MA period', 'sinput': False}, {'mql': 'InpAppliedPrice2', 'py': 'InpAppliedPrice2', 'param': 'InpAppliedPrice2', 'type': 'int', 'default': 1, 'label': 'Second MA applied price', 'sinput': False}, {'mql': 'InpMethod2', 'py': 'InpMethod2', 'param': 'InpMethod2', 'type': 'int', 'default': 1, 'label': 'Second MA method', 'sinput': False}, {'mql': 'InpPeriod3', 'py': 'InpPeriod3', 'param': 'InpPeriod3', 'type': 'uint', 'default': 20, 'label': 'Third MA period', 'sinput': False}, {'mql': 'InpAppliedPrice3', 'py': 'InpAppliedPrice3', 'param': 'InpAppliedPrice3', 'type': 'int', 'default': 1, 'label': 'Third MA applied price', 'sinput': False}, {'mql': 'InpMethod3', 'py': 'InpMethod3', 'param': 'InpMethod3', 'type': 'int', 'default': 0, 'label': 'Third MA method', 'sinput': False}, {'mql': 'InpPeriod4', 'py': 'InpPeriod4', 'param': 'InpPeriod4', 'type': 'uint', 'default': 40, 'label': 'Fourth MA period', 'sinput': False}, {'mql': 'InpAppliedPrice4', 'py': 'InpAppliedPrice4', 'param': 'InpAppliedPrice4', 'type': 'int', 'default': 1, 'label': 'Fourth MA applied price', 'sinput': False}, {'mql': 'InpMethod4', 'py': 'InpMethod4', 'param': 'InpMethod4', 'type': 'int', 'default': 0, 'label': 'Fourth MA method', 'sinput': False}, {'mql': 'InpUseSwing', 'py': 'InpUseSwing', 'param': 'InpUseSwing', 'type': 'int', 'default': 1, 'label': 'Use swing signals', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color1 = 3329330  # #property indicator_color1

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 10)  # First MA period
InpAppliedPrice1 = _input('InpAppliedPrice1', PRICE_CLOSE)  # First MA applied price
InpMethod1 = _input('InpMethod1', MODE_EMA)  # First MA method
InpPeriod2 = _input('InpPeriod2', 50)  # Second MA period
InpAppliedPrice2 = _input('InpAppliedPrice2', PRICE_CLOSE)  # Second MA applied price
InpMethod2 = _input('InpMethod2', MODE_EMA)  # Second MA method
InpPeriod3 = _input('InpPeriod3', 20)  # Third MA period
InpAppliedPrice3 = _input('InpAppliedPrice3', PRICE_CLOSE)  # Third MA applied price
InpMethod3 = _input('InpMethod3', MODE_SMA)  # Third MA method
InpPeriod4 = _input('InpPeriod4', 40)  # Fourth MA period
InpAppliedPrice4 = _input('InpAppliedPrice4', PRICE_CLOSE)  # Fourth MA applied price
InpMethod4 = _input('InpMethod4', MODE_SMA)  # Fourth MA method
InpUseSwing = _input('InpUseSwing', INPUT_YES)  # Use swing signals
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferMA3 = Arr(0, 0.0)
BufferMA4 = Arr(0, 0.0)
BufferLast = Arr(0, 0.0)
ma_func = None
period_1 = 0
period_2 = 0
period_3 = 0
period_4 = 0
period_max = 0
handle_ma1 = 0
handle_ma2 = 0
handle_ma3 = 0
handle_ma4 = 0

def OnInit():
    global handle_ma1, handle_ma2, handle_ma3, handle_ma4, ma_func, period_1, period_2, period_3, period_4, period_max
    period_1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period_2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    period_3 = (1 if (InpPeriod3 < 1) else InpPeriod3)
    period_4 = (1 if (InpPeriod4 < 1) else InpPeriod4)
    period_max = fmax(period_1, fmax(period_2, fmax(period_3, period_4)))
    array = Arr.of([0, 0], fill=0, dyn=False, size=4, dims=(2,))
    array[0][0] = period_1
    array[0][1] = 1
    array[1][0] = period_2
    array[1][1] = 2
    array[2][0] = period_3
    array[2][1] = 3
    array[3][0] = period_4
    array[3][1] = 4
    ArraySort(array)
    max_period = array[3][1]
    _sw1 = max_period
    if _sw1 == 1:
        ma_func = MA1
    elif _sw1 == 2:
        ma_func = MA2
    elif _sw1 == 3:
        ma_func = MA3
    else:
        ma_func = MA4
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMA4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferLast, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, (indicator_color1 if (not InpUseSwing) else clrGreen))
    PlotIndexSetInteger(0, PLOT_ARROW, (233 if InpUseSwing else 158))
    PlotIndexSetInteger(1, PLOT_ARROW, (234 if InpUseSwing else 158))
    IndicatorSetString(INDICATOR_SHORTNAME, 'MA signal (' + MethodToString(InpMethod1) + '(' + _str(period_1) + '),' + MethodToString(InpMethod2) + '(' + _str(period_2) + '),' + MethodToString(InpMethod3) + '(' + _str(period_3) + '),' + MethodToString(InpMethod4) + '(' + _str(period_4) + '))')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferMA3, True)
    ArraySetAsSeries(BufferMA4, True)
    ArraySetAsSeries(BufferLast, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, period_1, 0, InpMethod1, InpAppliedPrice1)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(', _str(period_1), ') by ', EnumToString(InpAppliedPrice1, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(None, PERIOD_CURRENT, period_2, 0, InpMethod2, InpAppliedPrice2)
    if handle_ma2 == INVALID_HANDLE:
        Print('The iMA(', _str(period_2), ') by ', EnumToString(InpAppliedPrice2, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma3 = iMA(None, PERIOD_CURRENT, period_3, 0, InpMethod3, InpAppliedPrice3)
    if handle_ma3 == INVALID_HANDLE:
        Print('The iMA(', _str(period_3), ') by ', EnumToString(InpAppliedPrice3, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma4 = iMA(None, PERIOD_CURRENT, period_4, 0, InpMethod4, InpAppliedPrice4)
    if handle_ma4 == INVALID_HANDLE:
        Print('The iMA(', _str(period_4), ') by ', EnumToString(InpAppliedPrice4, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
        ArrayInitialize(BufferMA3, 0)
        ArrayInitialize(BufferMA4, 0)
        ArrayInitialize(BufferLast, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count, BufferMA2)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma3, 0, 0, count, BufferMA3)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma4, 0, 0, count, BufferMA4)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferDN[i] = EMPTY_VALUE
        BufferUP[i] = BufferDN[i]
        MA1_ = BufferMA1[i]
        MA2_ = BufferMA2[i]
        MA3_ = BufferMA3[i]
        MA4_ = BufferMA4[i]
        BufferLast[i] = BufferLast[i + 1]
        if (MA1_ > MA2_ and MA3_ > MA4_) and (BufferLast[i + 1] != 1 or (not InpUseSwing)):
            BufferUP[i] = (open[i] if InpUseSwing else ma_func(i))
            BufferLast[i] = 1.0
        if (MA1_ < MA2_ and MA3_ < MA4_) and (BufferLast[i + 1] != -1 or (not InpUseSwing)):
            BufferDN[i] = (open[i] if InpUseSwing else ma_func(i))
            BufferLast[i] = -1.0
    return rates_total

def MethodToString(method):
    return StringSubstr(EnumToString(method, 'ENUM_MA_METHOD'), 5)

def MA1(index):
    return BufferMA1[index]

def MA2(index):
    return BufferMA2[index]

def MA3(index):
    return BufferMA3[index]

def MA4(index):
    return BufferMA4[index]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MASignal(_MQL5Indicator):
    name = 'MA_Signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 10,  # First MA period
        'InpAppliedPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # First MA applied price
        'InpMethod1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # First MA method
        'InpPeriod2': 50,  # Second MA period
        'InpAppliedPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Second MA applied price
        'InpMethod2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Second MA method
        'InpPeriod3': 20,  # Third MA period
        'InpAppliedPrice3': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Third MA applied price
        'InpMethod3': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Third MA method
        'InpPeriod4': 40,  # Fourth MA period
        'InpAppliedPrice4': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Fourth MA applied price
        'InpMethod4': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Fourth MA method
        'InpUseSwing': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use swing signals
    }

