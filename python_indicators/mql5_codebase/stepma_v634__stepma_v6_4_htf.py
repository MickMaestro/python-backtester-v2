"""stepma_v634 — converted from MQL5: MQL5 Indicators/StepMA_v6.4_HTF/stepma_v634.mq5

Indicator of the pabloski trading system.
Copyright: Copyright © 2006, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [8421376], 2: [9639167], 3: [8421376], 4: [9639167]}, 'widths': {1: 1, 2: 1, 3: 4, 4: 4}, 'styles': {}, 'labels': {1: 'Lower StepMA', 2: 'Upper StepMA', 3: 'StepMA Buy', 4: 'StepMA Sell'}, 'levels': [], 'description': ['Indicator of the pabloski trading system.'], 'name': 'stepma_v634', 'source': 'MQL5 Indicators/StepMA_v6.4_HTF/stepma_v634.mq5', 'folder': 'StepMA_v6.4_HTF', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 10, 'label': 'ATR Length', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 0.9, 'label': 'Sensivity Factor', 'sinput': False}, {'mql': 'StepSize', 'py': 'StepSize', 'param': 'StepSize', 'type': 'uint', 'default': 0, 'label': 'Constant Step Size (if need)', 'sinput': False}, {'mql': 'HighLow', 'py': 'HighLow', 'param': 'HighLow', 'type': 'bool', 'default': False, 'label': 'High/Low Mode Switch (more sensitive)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 10)  # ATR Length
Kv = _input('Kv', 0.9)  # Sensivity Factor
StepSize = _input('StepSize', 0)  # Constant Step Size (if need)
HighLow = _input('HighLow', False)  # High/Low Mode Switch (more sensitive)
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
dStep = 0.0
min_rates_total = 0

def OnInit():
    global dStep, min_rates_total
    min_rates_total = _int(Length + 1)
    dStep = Kv * StepSize
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 172)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 172)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'StepMA'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_ATRmax1, _s_OnCalculate_ATRmin1, _s_OnCalculate_smax1, _s_OnCalculate_smin1, _s_OnCalculate_trend1
    if rates_total < min_rates_total:
        return 0
    limit = 0
    trend0 = 0
    Step = 0
    smin0 = 0.0
    smax0 = 0.0
    ATRmin0 = 0.0
    ATRmax0 = 0.0
    AvgRange = 0.0
    ATR0 = 0.0
    xStep = 0.0
    x2Step = 0.0
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_ATRmax1 = -999999999.9
        _s_OnCalculate_ATRmin1 = 999999999.9
        _s_OnCalculate_smin1 = Close[limit]
        _s_OnCalculate_smax1 = Close[limit]
        _s_OnCalculate_trend1 = 0
    else:
        limit = rates_total - prev_calculated
    for bar in range(limit, 0 - 1, -1):
        UpBuffer[bar] = 0.0
        DnBuffer[bar] = 0.0
        trend0 = _s_OnCalculate_trend1
        if not StepSize:
            AvgRange = 0.0
            for iii in range(0, _int(Length)):
                AvgRange += High[bar + iii] - Low[bar + iii]
            ATR0 = AvgRange / Length
            ATRmax0 = MathMax(_s_OnCalculate_ATRmax1, ATR0)
            ATRmin0 = MathMin(_s_OnCalculate_ATRmin1, ATR0)
            Step = _int(_fdiv(0.5 * Kv * (ATRmax0 + ATRmin0), Point()))
        else:
            Step = _int(dStep)
        xStep = Step * Point()
        x2Step = 2.0 * xStep
        if HighLow:
            smax0 = Low[bar] + x2Step
            smin0 = High[bar] - x2Step
        else:
            smax0 = Close[bar] + x2Step
            smin0 = Close[bar] - x2Step
        if Close[bar] > _s_OnCalculate_smax1:
            trend0 = 1
        if Close[bar] < _s_OnCalculate_smin1:
            trend0 = -1
        if trend0 > 0:
            smin0 = MathMax(smin0, _s_OnCalculate_smin1)
            UpBuffer[bar] = smin0
        else:
            smax0 = MathMin(smax0, _s_OnCalculate_smax1)
            DnBuffer[bar] = smax0
        if bar:
            _s_OnCalculate_smin1 = smin0
            _s_OnCalculate_smax1 = smax0
            _s_OnCalculate_ATRmax1 = ATRmax0
            _s_OnCalculate_ATRmin1 = ATRmin0
            _s_OnCalculate_trend1 = trend0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    for bar in range(limit, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if UpBuffer[bar + 1] > 0.0 and DnBuffer[bar] > 0.0:
            BuyBuffer[bar] = DnBuffer[bar]
        if DnBuffer[bar + 1] > 0.0 and UpBuffer[bar] > 0.0:
            SellBuffer[bar] = UpBuffer[bar]
    return rates_total

# ---- static local variables
_s_OnCalculate_smin1 = 0.0
_s_OnCalculate_smax1 = 0.0
_s_OnCalculate_ATRmin1 = 0.0
_s_OnCalculate_ATRmax1 = 0.0
_s_OnCalculate_trend1 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StepmaV634(_MQL5Indicator):
    name = 'stepma_v634'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # ATR Length
        'Kv': 0.9,  # Sensivity Factor
        'StepSize': 0,  # Constant Step Size (if need)
        'HighLow': False,  # High/Low Mode Switch (more sensitive)
    }

