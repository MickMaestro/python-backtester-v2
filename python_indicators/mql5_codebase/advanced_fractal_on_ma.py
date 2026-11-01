"""Advanced_Fractal_On_MA — converted from MQL5: MQL5 Indicators/Advanced_Fractal_On_MA/Advanced_Fractal_On_MA.mq5

Advanced fractal on MA indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [32768], 2: [255], 3: [32768], 4: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Lower Fractal', 2: 'Upper Fractal', 3: 'Bullish signal', 4: 'Bearish signal'}, 'levels': [], 'description': ['Advanced fractal on MA indicator'], 'name': 'Advanced_Fractal_On_MA', 'source': 'MQL5 Indicators/Advanced_Fractal_On_MA/Advanced_Fractal_On_MA.mq5', 'folder': 'Advanced_Fractal_On_MA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}, {'mql': 'InpAppliedPriceUP', 'py': 'InpAppliedPriceUP', 'param': 'InpAppliedPriceUP', 'type': 'int', 'default': 3, 'label': 'Upper applied price', 'sinput': False}, {'mql': 'InpAppliedPriceDN', 'py': 'InpAppliedPriceDN', 'param': 'InpAppliedPriceDN', 'type': 'int', 'default': 4, 'label': 'Lower applied price', 'sinput': False}, {'mql': 'InpFrames', 'py': 'InpFrames', 'param': 'InpFrames', 'type': 'uint', 'default': 5, 'label': 'Frames', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # MA period
InpMethod = _input('InpMethod', MODE_SMA)  # MA method
InpAppliedPriceUP = _input('InpAppliedPriceUP', PRICE_HIGH)  # Upper applied price
InpAppliedPriceDN = _input('InpAppliedPriceDN', PRICE_LOW)  # Lower applied price
InpFrames = _input('InpFrames', 5)  # Frames
BufferUPFR = Arr(0, 0.0)
BufferDNFR = Arr(0, 0.0)
BufferUPSig = Arr(0, 0.0)
BufferDNSig = Arr(0, 0.0)
BufferMAUP = Arr(0, 0.0)
BufferMADN = Arr(0, 0.0)
period = 0
frames = 0
shift = 0
shift2 = 0
handle_maup = 0
handle_madn = 0

def OnInit():
    global frames, handle_madn, handle_maup, period, shift, shift2
    period = (1 if (InpPeriod < 1) else InpPeriod)
    frames = (3 if (InpFrames < 3) else InpFrames)
    shift = _int(floor(_idiv(frames - 1, 2)))
    shift2 = 2 * shift
    SetIndexBuffer(0, BufferDNFR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUPFR, INDICATOR_DATA)
    SetIndexBuffer(2, BufferUPSig, INDICATOR_DATA)
    SetIndexBuffer(3, BufferDNSig, INDICATOR_DATA)
    SetIndexBuffer(4, BufferMAUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMADN, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW, 233)
    PlotIndexSetInteger(3, PLOT_ARROW, 234)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Advanced fractal on MA (' + _str(period) + ',' + _str(frames) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUPFR, True)
    ArraySetAsSeries(BufferDNFR, True)
    ArraySetAsSeries(BufferUPSig, True)
    ArraySetAsSeries(BufferDNSig, True)
    ArraySetAsSeries(BufferMAUP, True)
    ArraySetAsSeries(BufferMADN, True)
    ResetLastError()
    handle_maup = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, InpAppliedPriceUP)
    if handle_maup == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by ', EnumToString(InpAppliedPriceUP, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_madn = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, InpAppliedPriceDN)
    if handle_madn == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by ', EnumToString(InpAppliedPriceDN, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - shift2 - 1
        ArrayInitialize(BufferUPFR, EMPTY_VALUE)
        ArrayInitialize(BufferDNFR, EMPTY_VALUE)
        ArrayInitialize(BufferUPSig, EMPTY_VALUE)
        ArrayInitialize(BufferDNSig, EMPTY_VALUE)
        ArrayInitialize(BufferMAUP, 0)
        ArrayInitialize(BufferMADN, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_maup, 0, 0, count, BufferMAUP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_madn, 0, 0, count, BufferMADN)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if IsUpFractal(i + shift):
            BufferUPFR[i + shift] = high[i + shift]
            BufferDNSig[i] = open[i]
        else:
            BufferUPFR[i + shift] = EMPTY_VALUE
            BufferDNSig[i] = EMPTY_VALUE
        if IsDnFractal(i + shift):
            BufferDNFR[i + shift] = low[i + shift]
            BufferUPSig[i] = open[i]
        else:
            BufferDNFR[i + shift] = EMPTY_VALUE
            BufferUPSig[i] = EMPTY_VALUE
    return rates_total

def IsUpFractal(index):
    find = True
    for i in range(1, shift + 1):
        if BufferMAUP[index] <= BufferMAUP[index + i] or BufferMAUP[index] <= BufferMAUP[index - i]:
            find = False
    return find

def IsDnFractal(index):
    find = True
    for i in range(1, shift + 1):
        if BufferMADN[index] >= BufferMADN[index + i] or BufferMADN[index] >= BufferMADN[index - i]:
            find = False
    return find


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdvancedFractalOnMA(_MQL5Indicator):
    name = 'Advanced_Fractal_On_MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriod': 20,  # MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
        'InpAppliedPriceUP': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=3),  # Upper applied price
        'InpAppliedPriceDN': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=4),  # Lower applied price
        'InpFrames': 5,  # Frames
    }

