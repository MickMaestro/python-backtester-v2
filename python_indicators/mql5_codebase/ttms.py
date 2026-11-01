"""TTMS — converted from MQL5: MQL5 Indicators/TTMS/TTMS.mq5

John Carter TTM Squeeze Indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 10, 2: 5, 3: 5}, 'colors': {1: [3329330, 255], 2: [16711680], 3: [12632256]}, 'widths': {1: 2, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'TTMS', 2: 'Signal', 3: 'No Signal'}, 'levels': [], 'description': ['John Carter TTM Squeeze Indicator'], 'name': 'TTMS', 'source': 'MQL5 Indicators/TTMS/TTMS.mq5', 'folder': 'TTMS', 'inputs': [{'mql': 'InpPeriodBB', 'py': 'InpPeriodBB', 'param': 'InpPeriodBB', 'type': 'uint', 'default': 20, 'label': 'BB period', 'sinput': False}, {'mql': 'InpDevBB', 'py': 'InpDevBB', 'param': 'InpDevBB', 'type': 'double', 'default': 2.0, 'label': 'BB deviation', 'sinput': False}, {'mql': 'InpPeriodKL', 'py': 'InpPeriodKL', 'param': 'InpPeriodKL', 'type': 'uint', 'default': 20, 'label': 'Keltner period', 'sinput': False}, {'mql': 'InpPeriodSmoothKL', 'py': 'InpPeriodSmoothKL', 'param': 'InpPeriodSmoothKL', 'type': 'uint', 'default': 20, 'label': 'Keltner smooth period', 'sinput': False}, {'mql': 'InpMethodKL', 'py': 'InpMethodKL', 'param': 'InpMethodKL', 'type': 'int', 'default': 0, 'label': 'Keltner smooth method', 'sinput': False}, {'mql': 'InpDevKL', 'py': 'InpDevKL', 'param': 'InpDevKL', 'type': 'double', 'default': 2.0, 'label': 'Keltner deviation', 'sinput': False}, {'mql': 'InpSizeSig', 'py': 'InpSizeSig', 'param': 'InpSizeSig', 'type': 'uchar', 'default': 1, 'label': 'Signal label size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodBB = _input('InpPeriodBB', 20)  # BB period
InpDevBB = _input('InpDevBB', 2.0)  # BB deviation
InpPeriodKL = _input('InpPeriodKL', 20)  # Keltner period
InpPeriodSmoothKL = _input('InpPeriodSmoothKL', 20)  # Keltner smooth period
InpMethodKL = _input('InpMethodKL', MODE_SMA)  # Keltner smooth method
InpDevKL = _input('InpDevKL', 2.0)  # Keltner deviation
InpSizeSig = _input('InpSizeSig', 1)  # Signal label size
BufferTTMS = Arr(0, 0.0)
BufferTTMSColors = Arr(0, 0.0)
BufferSig = Arr(0, 0.0)
BufferNoSig = Arr(0, 0.0)
BufferMABB = Arr(0, 0.0)
BufferMAKL = Arr(0, 0.0)
BufferDEV = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
dev_bb = 0.0
dev_kl = 0.0
period_bb = 0
period_kl = 0
period_sm = 0
size_sig = 0
handle_mabb = 0
handle_makl = 0
handle_dev = 0
handle_atr = 0

def OnInit():
    global dev_bb, dev_kl, handle_atr, handle_dev, handle_mabb, handle_makl, period_bb, period_kl, period_sm, size_sig
    period_bb = (1 if (InpPeriodBB < 1) else InpPeriodBB)
    period_kl = (1 if (InpPeriodKL < 1) else InpPeriodKL)
    period_sm = (1 if (InpPeriodSmoothKL < 1) else InpPeriodSmoothKL)
    dev_bb = (0.1 if (InpDevBB < 0.1) else InpDevBB)
    dev_kl = (0.1 if (InpDevKL < 0.1) else InpDevKL)
    size_sig = (1 if (InpSizeSig < 1) else InpSizeSig)
    SetIndexBuffer(0, BufferTTMS, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTTMSColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSig, INDICATOR_DATA)
    SetIndexBuffer(3, BufferNoSig, INDICATOR_DATA)
    SetIndexBuffer(4, BufferMABB, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMAKL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferDEV, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferATR, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    PlotIndexSetInteger(2, PLOT_ARROW, 119)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, size_sig)
    PlotIndexSetInteger(2, PLOT_LINE_WIDTH, size_sig)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'TTM Squeeze')
    ArraySetAsSeries(BufferTTMS, True)
    ArraySetAsSeries(BufferTTMSColors, True)
    ArraySetAsSeries(BufferSig, True)
    ArraySetAsSeries(BufferNoSig, True)
    ArraySetAsSeries(BufferMABB, True)
    ArraySetAsSeries(BufferMAKL, True)
    ArraySetAsSeries(BufferDEV, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_mabb = iMA(None, PERIOD_CURRENT, period_bb, 0, MODE_SMA, PRICE_CLOSE)
    if handle_mabb == INVALID_HANDLE:
        Print('The iMA(', _str(period_bb), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_makl = iMA(None, PERIOD_CURRENT, period_kl, 0, InpMethodKL, PRICE_CLOSE)
    if handle_makl == INVALID_HANDLE:
        Print('The iMA(', _str(period_kl), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_dev = iStdDev(None, PERIOD_CURRENT, period_bb, 0, MODE_SMA, PRICE_CLOSE)
    if handle_dev == INVALID_HANDLE:
        Print('The iStdDev(', _str(period_bb), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_sm)
    if handle_dev == INVALID_HANDLE:
        Print('The iATR(', _str(period_sm), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferTTMS, EMPTY_VALUE)
        ArrayInitialize(BufferTTMSColors, EMPTY_VALUE)
        ArrayInitialize(BufferSig, EMPTY_VALUE)
        ArrayInitialize(BufferNoSig, EMPTY_VALUE)
        ArrayInitialize(BufferMABB, EMPTY_VALUE)
        ArrayInitialize(BufferMAKL, EMPTY_VALUE)
        ArrayInitialize(BufferDEV, EMPTY_VALUE)
        ArrayInitialize(BufferATR, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_dev, 0, 0, count, BufferDEV)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mabb, 0, 0, count, BufferMABB)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_makl, 0, 0, count, BufferMAKL)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        H = BufferMAKL[i] + (BufferATR[i] * dev_kl)
        L = BufferMAKL[i] - (BufferATR[i] * dev_kl)
        D = BufferDEV[i]
        TL = BufferMABB[i] + (dev_bb * D)
        BL = BufferMABB[i] - (dev_bb * D)
        BufferTTMS[i] = ((_fdiv(H - L, TL - BL) - 1) if (TL != BL) else 0)
        BufferTTMSColors[i] = (0 if (BufferTTMS[i] > BufferTTMS[i + 1]) else 1)
        if TL < H and BL > L:
            BufferSig[i] = 0.0
            BufferNoSig[i] = EMPTY_VALUE
        else:
            BufferSig[i] = EMPTY_VALUE
            BufferNoSig[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TTMS(_MQL5Indicator):
    name = 'TTMS'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodBB': 20,  # BB period
        'InpDevBB': 2.0,  # BB deviation
        'InpPeriodKL': 20,  # Keltner period
        'InpPeriodSmoothKL': 20,  # Keltner smooth period
        'InpMethodKL': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Keltner smooth method
        'InpDevKL': 2.0,  # Keltner deviation
        'InpSizeSig': 1,  # Signal label size
    }

