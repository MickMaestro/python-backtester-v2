"""iMA+ATR Bands — converted from MQL5: MQL5 Indicators/Baseline_ iMA + ATR Bands/iMA+ATR Bands.mq5

Baseline: iMA+ATR Bands
Combines a Moving Average with ATR-based upper and lower bands to act as a trend filter and volatility channel.
Copyright: Copyright © 2025, Marteo Cosme (simartspoako); Link: https://www.mql5.com/en/users/simartspoako/publications; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2025, Marteo Cosme (simartspoako)', 'link': 'https://www.mql5.com/en/users/simartspoako/publications', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [16711680]}, 'widths': {1: 2}, 'styles': {1: 0, 2: 1, 3: 1}, 'labels': {}, 'levels': [], 'description': ['Baseline: iMA+ATR Bands', 'Combines a Moving Average with ATR-based upper and lower bands to act as a trend filter and volatility channel.'], 'name': 'iMA+ATR Bands', 'source': 'MQL5 Indicators/Baseline_ iMA + ATR Bands/iMA+ATR Bands.mq5', 'folder': 'Baseline_ iMA + ATR Bands', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 6, 'label': 'iMA Period', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'uint', 'default': 0, 'label': 'iMA Shift', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'iMA Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 14, 'label': 'ATR Period', 'sinput': False}, {'mql': 'InpATRxPlier', 'py': 'InpATRxPlier', 'param': 'InpATRxPlier', 'type': 'double', 'default': 1.0, 'label': 'ATR Multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 6)  # iMA Period
InpShift = _input('InpShift', 0)  # iMA Shift
InpMethod = _input('InpMethod', MODE_SMA)  # iMA Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpPeriodATR = _input('InpPeriodATR', 14)  # ATR Period
InpATRxPlier = _input('InpATRxPlier', 1.0)  # ATR Multiplier
BufferMA = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
BufferMAline = Arr(0, 0.0)
BufferUpperATR = Arr(0, 0.0)
BufferLowerATR = Arr(0, 0.0)
period_MA = 0
handle_MA = 0
period_ATR = 0
handle_ATR = 0

def OnInit():
    global handle_ATR, handle_MA, period_ATR, period_MA
    period_MA = (1 if (InpPeriod < 1) else InpPeriod)
    period_ATR = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    SetIndexBuffer(0, BufferMAline, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUpperATR, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLowerATR, INDICATOR_DATA)
    SetIndexBuffer(3, BufferATR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, EnumToString(InpMethod, 'ENUM_MA_METHOD') + '(' + _str(period_MA) + ')')
    PlotIndexSetString(0, PLOT_LABEL, EnumToString(InpMethod, 'ENUM_MA_METHOD') + '(' + _str(period_MA) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'upperATR' + '(' + IntegerToString(InpPeriodATR) + ' x ' + DoubleToString(InpATRxPlier, 1) + ')')
    PlotIndexSetString(2, PLOT_LABEL, 'lowerATR' + '(' + IntegerToString(InpPeriodATR) + ' x ' + DoubleToString(InpATRxPlier, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMAline, True)
    ArraySetAsSeries(BufferUpperATR, True)
    ArraySetAsSeries(BufferLowerATR, True)
    ArraySetAsSeries(BufferATR, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_MA = iMA(None, PERIOD_CURRENT, InpPeriod, InpShift, InpMethod, InpAppliedPrice)
    if handle_MA == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ATR = iATR(None, PERIOD_CURRENT, period_ATR)
    if handle_ATR == INVALID_HANDLE:
        Print('The iATR(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_MA:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_MA - 1
        ArrayInitialize(BufferMA, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_MA, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ATR, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMAline[i] = BufferMA[i]
        BufferUpperATR[i] = BufferMA[i] + (BufferATR[i] * InpATRxPlier)
        BufferLowerATR[i] = BufferMA[i] - (BufferATR[i] * InpATRxPlier)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IMAATRBands(_MQL5Indicator):
    name = 'iMA+ATR Bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 6,  # iMA Period
        'InpShift': 0,  # iMA Shift
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # iMA Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpPeriodATR': 14,  # ATR Period
        'InpATRxPlier': 1.0,  # ATR Multiplier
    }

