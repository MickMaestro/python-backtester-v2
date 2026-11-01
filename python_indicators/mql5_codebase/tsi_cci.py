"""tsi_cci — converted from MQL5: MQL5 Indicators/TSI_CCI/tsi_cci.mq5

TSI_CCI
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16711680, 6053069]}, 'widths': {}, 'styles': {}, 'labels': {1: 'TSI_CCI'}, 'levels': [50.0, 0.0, -50.0], 'description': ['TSI_CCI'], 'name': 'tsi_cci', 'source': 'MQL5 Indicators/TSI_CCI/tsi_cci.mq5', 'folder': 'TSI_CCI', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'uint', 'default': 15, 'label': 'Период индикатора CCI', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 1, 'label': 'Цена индикатора CCI', 'sinput': False}, {'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'uint', 'default': 1, 'label': 'Период моментума', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 5, 'label': 'Глубина первого усреднения', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 8, 'label': 'Глубина второго усреднения', 'sinput': False}, {'mql': 'XLength3', 'py': 'XLength3', 'param': 'XLength3', 'type': 'uint', 'default': 10, 'label': 'Глубина усреднения сигнальной линии', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_EMA)  # Метод усреднения
CCIPeriod = _input('CCIPeriod', 15)  # Период индикатора CCI
CCIPrice = _input('CCIPrice', PRICE_CLOSE)  # Цена индикатора CCI
MomPeriod = _input('MomPeriod', 1)  # Период моментума
XLength1 = _input('XLength1', 5)  # Глубина первого усреднения
XLength2 = _input('XLength2', 8)  # Глубина второго усреднения
XLength3 = _input('XLength3', 10)  # Глубина усреднения сигнальной линии
XPhase = _input('XPhase', 15)  # Параметр сглаживания
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
Ind_Handle = 0
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0
min_rates_4 = 0

def OnInit():
    global Ind_Handle, min_rates_1, min_rates_2, min_rates_3, min_rates_4, min_rates_total
    min_rates_1 = _int(CCIPeriod)
    min_rates_2 = min_rates_1 + _int(MomPeriod)
    min_rates_3 = min_rates_2 + XMA1.GetStartBars(XMA_Method, XLength1, XPhase)
    min_rates_4 = min_rates_3 + XMA1.GetStartBars(XMA_Method, XLength2, XPhase)
    min_rates_total = min_rates_4 + XMA1.GetStartBars(XMA_Method, XLength3, XPhase)
    Ind_Handle = iCCI(Symbol(), PERIOD_CURRENT, CCIPeriod, CCIPrice)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора TSI_MACD')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TSI_CCI')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or BarsCalculated(Ind_Handle) < rates_total:
        return 0
    CCI = Arr(0, 0.0)
    mtm = 0.0
    xmtm = 0.0
    xxmtm = 0.0
    absmtm = 0.0
    xabsmtm = 0.0
    xxabsmtm = 0.0
    tsi = 0.0
    xtsi = 0.0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar1 = 0
    maxbar2 = 0
    maxbar3 = 0
    maxbar4 = 0
    ArraySetAsSeries(CCI, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_1 - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    maxbar1 = rates_total - min_rates_1 - 1
    maxbar2 = rates_total - min_rates_2 - 1
    maxbar3 = rates_total - min_rates_3 - 1
    maxbar4 = rates_total - min_rates_4 - 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        mtm = Mom.MomentumSeries(maxbar1, prev_calculated, rates_total, MomPeriod, CCI[bar], bar, True)
        absmtm = MathAbs(mtm)
        xmtm = XMA1.XMASeries(maxbar2, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, mtm, bar, True)
        xabsmtm = XMA2.XMASeries(maxbar2, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, absmtm, bar, True)
        xxmtm = XMA3.XMASeries(maxbar3, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, xmtm, bar, True)
        xxabsmtm = XMA4.XMASeries(maxbar3, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, xabsmtm, bar, True)
        if xxabsmtm:
            tsi = _fdiv(100 * xxmtm, xxabsmtm)
        else:
            tsi = 0.0
        if not tsi:
            tsi = 1e-09
        xtsi = XMA5.XMASeries(maxbar4, prev_calculated, rates_total, XMA_Method, XPhase, XLength3, tsi, bar, True)
        if not xtsi:
            xtsi = 1e-09
        UpBuffer[bar] = tsi
        DnBuffer[bar] = xtsi
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()
XMA4 = _alloc(CXMA)
XMA4.__init__()
XMA5 = _alloc(CXMA)
XMA5.__init__()
Mom = _alloc(CMomentum)
Mom.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TsiCci(_MQL5Indicator):
    name = 'tsi_cci'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения
        'CCIPeriod': 15,  # Период индикатора CCI
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена индикатора CCI
        'MomPeriod': 1,  # Период моментума
        'XLength1': 5,  # Глубина первого усреднения
        'XLength2': 8,  # Глубина второго усреднения
        'XLength3': 10,  # Глубина усреднения сигнальной линии
        'XPhase': 15,  # Параметр сглаживания
    }

