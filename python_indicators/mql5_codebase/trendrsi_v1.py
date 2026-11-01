"""trendrsi_v1 — converted from MQL5: MQL5 Indicators/TrendRSI_v1/trendrsi_v1.mq5

Copyright: Copyright © 2005, TrendLaboratory Ltd.; Link: E-mail: igorad2004@list.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TrendLaboratory Ltd.', 'link': 'E-mail: igorad2004@list.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [32768]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'RSI', 2: 'MARSI fast', 3: 'MARSI slow'}, 'levels': [70.0, 50.0, 30.0], 'description': [''], 'name': 'trendrsi_v1', 'source': 'MQL5 Indicators/TrendRSI_v1/trendrsi_v1.mq5', 'folder': 'TrendRSI_v1', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FastMAPeriod', 'py': 'FastMAPeriod', 'param': 'FastMAPeriod', 'type': 'uint', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'FastMAType', 'py': 'FastMAType', 'param': 'FastMAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'SlowMAPeriod', 'py': 'SlowMAPeriod', 'param': 'SlowMAPeriod', 'type': 'uint', 'default': 45, 'label': '', 'sinput': False}, {'mql': 'SlowMAType', 'py': 'SlowMAType', 'param': 'SlowMAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RSIPeriod = _input('RSIPeriod', 14)
RSIPrice = _input('RSIPrice', PRICE_CLOSE)
FastMAPeriod = _input('FastMAPeriod', 9)
FastMAType = _input('FastMAType', MODE_EMA)
SlowMAPeriod = _input('SlowMAPeriod', 45)
SlowMAType = _input('SlowMAType', MODE_EMA)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
min_rates_total = 0
RSI_Handle = 0
FsMA_Handle = 0
SlMA_Handle = 0

def OnInit():
    global FsMA_Handle, RSI_Handle, SlMA_Handle, min_rates_total
    min_rates_total = _int(MathMax(FastMAPeriod, SlowMAPeriod) + RSIPeriod)
    RSI_Handle = iRSI(None, 0, RSIPeriod, RSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the iRSI indicator')
        return INIT_FAILED
    FsMA_Handle = iMA(Symbol(), PERIOD_CURRENT, FastMAPeriod, 0, FastMAType, RSI_Handle)
    if FsMA_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the Fast iMA indicator')
        return INIT_FAILED
    SlMA_Handle = iMA(Symbol(), PERIOD_CURRENT, SlowMAPeriod, 0, SlowMAType, RSI_Handle)
    if SlMA_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the Slow iMA indicator')
        return INIT_FAILED
    SetIndexBuffer(0, Ind1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind1Buffer, True)
    SetIndexBuffer(1, Ind2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind2Buffer, True)
    SetIndexBuffer(2, Ind3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind3Buffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrendRSI_v1')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(RSI_Handle) < rates_total or BarsCalculated(FsMA_Handle) < rates_total) or BarsCalculated(SlMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total - min_rates_total
    else:
        to_copy = rates_total - prev_calculated + 1
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, Ind1Buffer) <= 0:
        return 0
    if CopyBuffer(FsMA_Handle, 0, 0, to_copy, Ind2Buffer) <= 0:
        return 0
    if CopyBuffer(SlMA_Handle, 0, 0, to_copy, Ind3Buffer) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendrsiV1(_MQL5Indicator):
    name = 'trendrsi_v1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod': 14,
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'FastMAPeriod': 9,
        'FastMAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'SlowMAPeriod': 45,
        'SlowMAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

