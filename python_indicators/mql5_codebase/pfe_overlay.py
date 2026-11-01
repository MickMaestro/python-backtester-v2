"""PFE_Overlay — converted from MQL5: MQL5 Indicators/PFE_Overlay/PFE_Overlay.mq5

Polarized Fractal Efficiency Overlay indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [8421376], 2: [255], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'PFE Overlay', 2: 'Top dev', 3: 'Bottom dev'}, 'levels': [], 'description': ['Polarized Fractal Efficiency Overlay indicator'], 'name': 'PFE_Overlay', 'source': 'MQL5 Indicators/PFE_Overlay/PFE_Overlay.mq5', 'folder': 'PFE_Overlay', 'inputs': [{'mql': 'InpPeriodFastROC', 'py': 'InpPeriodFastROC', 'param': 'InpPeriodFastROC', 'type': 'uint', 'default': 1, 'label': 'Fast ROC period', 'sinput': False}, {'mql': 'InpPeriodSlowROC', 'py': 'InpPeriodSlowROC', 'param': 'InpPeriodSlowROC', 'type': 'uint', 'default': 9, 'label': 'Slow ROC period', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 5, 'label': 'MA period', 'sinput': False}, {'mql': 'InpPDS', 'py': 'InpPDS', 'param': 'InpPDS', 'type': 'int', 'default': 10, 'label': 'PDS', 'sinput': False}, {'mql': 'InpPeriodAVG', 'py': 'InpPeriodAVG', 'param': 'InpPeriodAVG', 'type': 'uint', 'default': 20, 'label': 'Avg period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'InpShowDev', 'py': 'InpShowDev', 'param': 'InpShowDev', 'type': 'int', 'default': 1, 'label': 'Show deviations', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodFastROC = _input('InpPeriodFastROC', 1)  # Fast ROC period
InpPeriodSlowROC = _input('InpPeriodSlowROC', 9)  # Slow ROC period
InpPeriodMA = _input('InpPeriodMA', 5)  # MA period
InpPDS = _input('InpPDS', 10)  # PDS
InpPeriodAVG = _input('InpPeriodAVG', 20)  # Avg period
InpDeviation = _input('InpDeviation', 2.0)  # Deviation
InpShowDev = _input('InpShowDev', INPUT_YES)  # Show deviations
BufferPFE = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferTL = Arr(0, 0.0)
BufferBL = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferAvgRAW = Arr(0, 0.0)
deviation = 0.0
period_froc = 0
period_sroc = 0
period_ma = 0
period_avg = 0
period_max = 0
pds = 0
handle_ma = 0
handle_dev = 0

def OnInit():
    global deviation, handle_dev, handle_ma, pds, period_avg, period_froc, period_ma, period_max, period_sroc
    period_froc = (1 if (InpPeriodFastROC < 1) else InpPeriodFastROC)
    period_sroc = (1 if (InpPeriodSlowROC < 1) else InpPeriodSlowROC)
    period_ma = (2 if (InpPeriodMA < 2) else InpPeriodMA)
    period_avg = (1 if (InpPeriodAVG < 1) else InpPeriodAVG)
    period_max = fmax(period_froc, period_sroc)
    deviation = InpDeviation
    pds = InpPDS
    SetIndexBuffer(0, BufferPFE, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(3, BufferTL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferBL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferAvgRAW, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Polarized Fractal Efficiency Overlay (' + _str(period_froc) + ',' + _str(period_sroc) + ',' + _str(period_ma) + ',' + _str(pds) + ',' + _str(period_avg) + ',' + DoubleToString(deviation, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, InpShowDev)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, InpShowDev)
    ArraySetAsSeries(BufferPFE, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferTL, True)
    ArraySetAsSeries(BufferBL, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferDev, True)
    ArraySetAsSeries(BufferRAW, True)
    ArraySetAsSeries(BufferAvgRAW, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_avg, 0, MODE_SMA, PRICE_CLOSE)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_avg), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_dev = iStdDev(None, PERIOD_CURRENT, period_avg, 0, MODE_SMA, PRICE_CLOSE)
    if handle_dev == INVALID_HANDLE:
        Print('The iStdDev(', _str(period_avg), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ChartRedraw()
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 1
        ArrayInitialize(BufferPFE, EMPTY_VALUE)
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferTL, 0)
        ArrayInitialize(BufferBL, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferDev, 0)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferAvgRAW, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_dev, 0, 0, count, BufferDev)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferTL[i] = BufferMA[i] + (deviation * BufferDev[i])
        BufferBL[i] = BufferMA[i] - (deviation * BufferDev[i])
        BufferTop[i] = (BufferTL[i] if InpShowDev else EMPTY_VALUE)
        BufferBottom[i] = (BufferBL[i] if InpShowDev else EMPTY_VALUE)
        ROCSlow = ((100.0 * (_fdiv(close[i], close[i + period_sroc]) - 1)) if (close[i + period_sroc] != 0) else 0)
        ROCFast = ((100.0 * (_fdiv(close[i], close[i + period_froc]) - 1)) if (close[i + period_froc] != 0) else 0)
        x = sqrt((ROCSlow * ROCSlow) + 100.0)
        y = sqrt((ROCFast * ROCFast) + 1.0) + pds
        z = _fdiv(x, (y if (y != 0) else 1))
        BufferRAW[i] = ((100.0 * z) if (close[i] > close[i + period_sroc]) else (-100.0 * z))
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferRAW, BufferAvgRAW) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        scale = (_fdiv(200.0, BufferTL[i] - BufferBL[i]) if (BufferTL[i] != BufferBL[i]) else 0)
        BufferPFE[i] = ((BufferBL[i] + _fdiv(100.0 + BufferAvgRAW[i], scale)) if (scale != 0) else EMPTY_VALUE)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PFEOverlay(_MQL5Indicator):
    name = 'PFE_Overlay'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastROC': 1,  # Fast ROC period
        'InpPeriodSlowROC': 9,  # Slow ROC period
        'InpPeriodMA': 5,  # MA period
        'InpPDS': 10,  # PDS
        'InpPeriodAVG': 20,  # Avg period
        'InpDeviation': 2.0,  # Deviation
        'InpShowDev': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show deviations
    }

