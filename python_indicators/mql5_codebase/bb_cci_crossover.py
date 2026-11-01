"""bb_cci_crossover — converted from MQL5: MQL5 Indicators/BB_CCI_CrossOver/bb_cci_crossover.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'BB_CCI_CrossOver Sell', 2: 'BB_CCI_CrossOver Buy'}, 'levels': [], 'description': [], 'name': 'bb_cci_crossover', 'source': 'MQL5 Indicators/BB_CCI_CrossOver/bb_cci_crossover.mq5', 'folder': 'BB_CCI_CrossOver', 'inputs': [{'mql': 'CCI_Period', 'py': 'CCI_Period', 'param': 'CCI_Period', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'NivelCCI_MIN', 'py': 'NivelCCI_MIN', 'param': 'NivelCCI_MIN', 'type': 'double', 'default': -80.0, 'label': '', 'sinput': False}, {'mql': 'NivelCCI_MAX', 'py': 'NivelCCI_MAX', 'param': 'NivelCCI_MAX', 'type': 'double', 'default': 80.0, 'label': '', 'sinput': False}, {'mql': 'MM_Period', 'py': 'MM_Period', 'param': 'MM_Period', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'BB_Period', 'py': 'BB_Period', 'param': 'BB_Period', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'BB_Desvio', 'py': 'BB_Desvio', 'param': 'BB_Desvio', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'PIP_DesvioMAX', 'py': 'PIP_DesvioMAX', 'param': 'PIP_DesvioMAX', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'PIP_DesvioMIN', 'py': 'PIP_DesvioMIN', 'param': 'PIP_DesvioMIN', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
CCI_Period = _input('CCI_Period', 21)
NivelCCI_MIN = _input('NivelCCI_MIN', -80.0)
NivelCCI_MAX = _input('NivelCCI_MAX', 80.0)
MM_Period = _input('MM_Period', 14)
BB_Period = _input('BB_Period', 21)
BB_Desvio = _input('BB_Desvio', 2.0)
PIP_DesvioMAX = _input('PIP_DesvioMAX', 10)
PIP_DesvioMIN = _input('PIP_DesvioMIN', 10)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
dPIP_DesvioMAX = 0.0
dPIP_DesvioMIN = 0.0
CCI_Handle = 0
ATR_Handle = 0
BB_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, BB_Handle, CCI_Handle, dPIP_DesvioMAX, dPIP_DesvioMIN, min_rates_total
    min_rates_total = MathMax(MathMax(CCI_Period, BB_Period), 10)
    dPIP_DesvioMAX = PIP_DesvioMAX * Point()
    dPIP_DesvioMIN = PIP_DesvioMIN * Point()
    CCI_Handle = iCCI(None, 0, CCI_Period, PRICE_WEIGHTED)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the CCI indicator')
    BB_Handle = iBands(None, 0, BB_Period, 0, BB_Desvio, PRICE_WEIGHTED)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Bands indicator')
    ATR_Handle = iATR(None, 0, 10)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'BB_CCI_CrossOver'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(CCI_Handle) < rates_total or BarsCalculated(BB_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    range_ = 0.0
    MM = 0.0
    UpBB = Arr(0, 0.0)
    DnBB = Arr(0, 0.0)
    CCI = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    maxbar = rates_total - 1 - CCI_Period
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(BB_Handle, UPPER_BAND, 0, to_copy, UpBB) <= 0:
        return 0
    if CopyBuffer(BB_Handle, LOWER_BAND, 0, to_copy, DnBB) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(CCI, True)
    ArraySetAsSeries(UpBB, True)
    ArraySetAsSeries(DnBB, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        range_ = (ATR[bar] * 3) / 8
        MM = _s_OnCalculate_EMA.EMASeries(maxbar, prev_calculated, rates_total, MM_Period, CCI[bar], bar, True)
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if CCI[bar] > NivelCCI_MAX:
            if CCI[bar] < MM:
                if high[bar] <= UpBB[bar]:
                    if high[bar + 1] > high[bar]:
                        if (UpBB[bar] - high[bar]) <= dPIP_DesvioMAX:
                            SellBuffer[bar] = high[bar] + range_
                elif high[bar] >= UpBB[bar]:
                    if high[bar + 1] > high[bar]:
                        SellBuffer[bar] = high[bar] + range_
        if CCI[bar] < NivelCCI_MIN:
            if CCI[bar] > MM:
                if low[bar] >= DnBB[bar]:
                    if low[bar + 1] < low[bar]:
                        if (low[bar] - DnBB[bar]) <= dPIP_DesvioMIN:
                            BuyBuffer[bar] = low[bar] - range_
                elif low[bar] <= DnBB[bar]:
                    if low[bar + 1] < low[bar]:
                        BuyBuffer[bar] = low[bar] - range_
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_EMA = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BbCciCrossover(_MQL5Indicator):
    name = 'bb_cci_crossover'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CCI_Period': 21,
        'NivelCCI_MIN': -80.0,
        'NivelCCI_MAX': 80.0,
        'MM_Period': 14,
        'BB_Period': 21,
        'BB_Desvio': 2.0,
        'PIP_DesvioMAX': 10,
        'PIP_DesvioMIN': 10,
    }

