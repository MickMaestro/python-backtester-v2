"""XFisher_org_v1_X20 — converted from MQL5: MQL5 Indicators/XFisher_org_v1_X20/XFisher_org_v1_X20.mq5

XFisher_org_v1_X20
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1}, 'colors': {1: [13828244]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [1.5, 0.0, -1.5], 'description': ['XFisher_org_v1_X20'], 'name': 'XFisher_org_v1_X20', 'source': 'MQL5 Indicators/XFisher_org_v1_X20/XFisher_org_v1_X20.mq5', 'folder': 'XFisher_org_v1_X20', 'inputs': [{'mql': 'FLength', 'py': 'FLength', 'param': 'FLength', 'type': 'uint', 'default': 3, 'label': 'стартовая глубина усреднения', 'sinput': False}, {'mql': 'step', 'py': 'step', 'param': 'step', 'type': 'uint', 'default': 1, 'label': 'шаг изменения глубины усреднения', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 3, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_APPLIED_PRICE_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
FLength = _input('FLength', 3)  # стартовая глубина усреднения
step = _input('step', 1)  # шаг изменения глубины усреднения
MA_SMethod = _input('MA_SMethod', MODE_JJMA)  # Метод сглаживания
MA_Length = _input('MA_Length', 3)  # Глубина сглаживания
MA_Phase = _input('MA_Phase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Spear_Handle = Arr(20, 0, dyn=False)
min_rates_total = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer',)
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(FLength + (step * (20 - 1))) + 1
    min_rates_total += GetStartBars(MA_SMethod, MA_Length, MA_Phase)
    period = FLength
    for numb in range(0, 20):
        period += step
        Spear_Handle[numb] = iCustom(None, 0, 'XFisher_org_v1', period, MA_SMethod, MA_Length, MA_Phase, IPC, 0)
        if Spear_Handle[numb] == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора XFisher_org_v1 ', numb)
        shortname = Box('')
        StringConcatenate(shortname, 'XFisher_org_v1 X', 20, '*', period, ')')
        PlotIndexSetString(numb, PLOT_LABEL, shortname.v)
        PlotIndexSetDouble(numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(numb, PLOT_DRAW_BEGIN, min_rates_total)
        PlotIndexSetInteger(numb, PLOT_SHOW_DATA, False)
        SetIndexBuffer(numb, Ind[numb].IndBuffer, INDICATOR_DATA)
        ArraySetAsSeries(Ind[numb].IndBuffer, True)
        PlotIndexSetInteger(numb, PLOT_DRAW_TYPE, PlotIndexGetInteger(0, PLOT_DRAW_TYPE))
        PlotIndexSetInteger(numb, PLOT_LINE_STYLE, PlotIndexGetInteger(0, PLOT_LINE_STYLE))
        PlotIndexSetInteger(numb, PLOT_LINE_WIDTH, PlotIndexGetInteger(0, PLOT_LINE_WIDTH))
        PlotIndexSetInteger(numb, PLOT_LINE_COLOR, PlotIndexGetInteger(0, PLOT_LINE_COLOR))
    shortname = Box("")
    StringConcatenate(shortname, 'XFisher_org_v1 X', 20, '*', FLength, '(', step, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    for numb in range(0, 20):
        if BarsCalculated(Spear_Handle[numb]) < min_rates_total:
            return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated + 1
    for numb in range(0, 20):
        if CopyBuffer(Spear_Handle[numb], 0, 0, to_copy, Ind[numb].IndBuffer) <= 0:
            return 0
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(20, 0, dyn=False, factory=CIndicatorsBuffers)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XFisherOrgV1X20(_MQL5Indicator):
    name = 'XFisher_org_v1_X20'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FLength': 3,  # стартовая глубина усреднения
        'step': 1,  # шаг изменения глубины усреднения
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания
        'MA_Length': 3,  # Глубина сглаживания
        'MA_Phase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
    }

