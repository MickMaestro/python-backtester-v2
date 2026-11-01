"""gann_hi_lo_activator_ssl — converted from MQL5: MQL5 Indicators/Gann Hi-Lo Activator SSL/gann_hi_lo_activator_ssl.mq5

Author: Kalenzo
Link: https://login.mql5.com/en/users/avoitenko; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '', 'link': 'https://login.mql5.com/en/users/avoitenko', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16748574, 17919]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'GHL (13, SMMA)'}, 'levels': [], 'description': ['Author: Kalenzo'], 'name': 'gann_hi_lo_activator_ssl', 'source': 'MQL5 Indicators/Gann Hi-Lo Activator SSL/gann_hi_lo_activator_ssl.mq5', 'folder': 'Gann Hi-Lo Activator SSL', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 13, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 2, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 13)  # Period
InpMethod = _input('InpMethod', MODE_SMMA)  # Method
GannBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
MaHighBuffer = Arr(0, 0.0)
MaLowBuffer = Arr(0, 0.0)
TrendBuffer = Arr(0, 0.0)
ma_high_handle = 0
ma_low_handle = 0
period = 0

def OnInit():
    global ma_high_handle, ma_low_handle, period
    period = _int(fmax(InpPeriod, 2))
    SetIndexBuffer(0, GannBuffer)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, MaHighBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, MaLowBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, TrendBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(GannBuffer, True)
    ArraySetAsSeries(ColorBuffer, True)
    ArraySetAsSeries(MaHighBuffer, True)
    ArraySetAsSeries(MaLowBuffer, True)
    ArraySetAsSeries(TrendBuffer, True)
    ma_high_handle = iMA(None, 0, period, 0, InpMethod, PRICE_HIGH)
    ma_low_handle = iMA(None, 0, period, 0, InpMethod, PRICE_LOW)
    if ma_high_handle == INVALID_HANDLE or ma_low_handle == INVALID_HANDLE:
        Print('Unable to create handle for iMA')
        return INIT_FAILED
    short_name = StringFormat('Gann High-Low Activator SSL (%u, %s)', period, StringSubstr(EnumToString(InpMethod, 'ENUM_MA_METHOD'), 5))
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = StringFormat('GHL (%u, %s)', period, StringSubstr(EnumToString(InpMethod, 'ENUM_MA_METHOD'), 5))
    PlotIndexSetString(0, PLOT_LABEL, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (period + 1):
        return 0
    ArraySetAsSeries(close, True)
    limit = 0
    if rates_total < prev_calculated or prev_calculated <= 0:
        limit = rates_total - period - 1
        ArrayInitialize(GannBuffer, EMPTY_VALUE)
        ArrayInitialize(ColorBuffer, 0)
        ArrayInitialize(MaHighBuffer, 0)
        ArrayInitialize(MaLowBuffer, 0)
        ArrayInitialize(TrendBuffer, 0)
    else:
        limit = rates_total - prev_calculated
    if CopyBuffer(ma_high_handle, 0, 0, limit + 1, MaHighBuffer) != (limit + 1):
        return 0
    if CopyBuffer(ma_low_handle, 0, 0, limit + 1, MaLowBuffer) != (limit + 1):
        return 0
    for i in range(limit, 0 - 1, -1):
        TrendBuffer[i] = TrendBuffer[i + 1]
        if NormalizeDouble(close[i], Digits()) > NormalizeDouble(MaHighBuffer[i + 1], Digits()):
            TrendBuffer[i] = 1.0
        if NormalizeDouble(close[i], Digits()) < NormalizeDouble(MaLowBuffer[i + 1], Digits()):
            TrendBuffer[i] = -1.0
        if TrendBuffer[i] < 0:
            GannBuffer[i] = MaHighBuffer[i]
            ColorBuffer[i] = 1.0
        if TrendBuffer[i] > 0:
            GannBuffer[i] = MaLowBuffer[i]
            ColorBuffer[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GannHiLoActivatorSsl(_MQL5Indicator):
    name = 'gann_hi_lo_activator_ssl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 13,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Method
    }

