"""x2ma_nrtr — converted from MQL5: MQL5 Indicators/X2MA NRTR/x2ma_nrtr.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [15624315]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'X2MA NRTR'}, 'levels': [], 'description': [], 'name': 'x2ma_nrtr', 'source': 'MQL5 Indicators/X2MA NRTR/x2ma_nrtr.mq5', 'folder': 'X2MA NRTR', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'First smoothing averaging method', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 12, 'label': 'First smoothing depth', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'First smoothing parameter', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'Second smoothing averaging method', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 5, 'label': 'Second smoothing depth', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'Second smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'uint', 'default': 30, 'label': 'Flat oscillations size', 'sinput': False}, {'mql': 'Max_DEV', 'py': 'Max_DEV', 'param': 'Max_DEV', 'type': 'uint', 'default': 55, 'label': 'Terminal deviation of price from X2MA that does not change the value of the average', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_SMA)  # First smoothing averaging method
Length1 = _input('Length1', 12)  # First smoothing depth
Phase1 = _input('Phase1', 15)  # First smoothing parameter
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # Second smoothing averaging method
Length2 = _input('Length2', 5)  # Second smoothing depth
Phase2 = _input('Phase2', 15)  # Second smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Step = _input('Step', 30)  # Flat oscillations size
Max_DEV = _input('Max_DEV', 55)  # Terminal deviation of price from X2MA that does not change the value of the average
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
X2MA = Arr(0, 0.0)
dPriceShift = 0.0
StartBars = 0
StartBars1 = 0
StartBars2 = 0
Max_Dev = 0.0
Norma = 0.0

def OnInit():
    global Max_Dev, Norma, StartBars, StartBars1, StartBars2, dPriceShift
    StartBars1 = XMA1.GetStartBars(MA_Method1, Length1, Phase1)
    StartBars2 = XMA2.GetStartBars(MA_Method2, Length2, Phase2)
    StartBars = StartBars1 + StartBars2
    XMA1.XMALengthCheck('Length1', Length1)
    XMA2.XMALengthCheck('Length2', Length2)
    XMA1.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    dPriceShift = Point() * PriceShift
    Max_Dev = MathMax(Max_DEV, 1) * Point()
    Norma = MathMax(Step, 1) * Point()
    SetIndexBuffer(0, X2MA, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'X2MA')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(MA_Method1)
    Smooth2 = XMA1.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'X2MA NRTR(', Length1, ', ', Length2, ', ', Smooth1, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Max_, _s_OnCalculate_Min_, _s_OnCalculate_Resalt_, _s_OnCalculate_trend_
    if rates_total < StartBars:
        return 0
    price_ = 0.0
    x1xma = 0.0
    x2xma = 0.0
    Resalt = 0.0
    Swng = 0.0
    Velue = 0.0
    Min = 0.0
    Max = 0.0
    first = 0
    bar = 0
    trend = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_Max_ = -1.0
        _s_OnCalculate_Min_ = 999999999.0
        _s_OnCalculate_trend_ = 0
        _s_OnCalculate_Resalt_ = 0.0
    else:
        first = prev_calculated - 1
    Max = _s_OnCalculate_Max_
    Min = _s_OnCalculate_Min_
    trend = _s_OnCalculate_trend_
    Resalt = _s_OnCalculate_Resalt_
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            _s_OnCalculate_Max_ = Max
            _s_OnCalculate_Min_ = Min
            _s_OnCalculate_trend_ = trend
            _s_OnCalculate_Resalt_ = Resalt
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        x1xma = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price_, bar, False)
        x2xma = XMA2.XMASeries(StartBars1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, x1xma, bar, False)
        Velue = x2xma
        Velue = _fdiv(Velue, Norma)
        Velue = NormalizeDouble(Velue, 0)
        Velue *= Norma
        Swng = price_ - Velue
        if trend >= 0:
            if Velue >= Max:
                Max = Velue
                Resalt = Velue
            elif Swng < (-Max_Dev):
                Min = Velue
                Resalt = Velue
                trend = -1
            else:
                Resalt = Max
        if trend <= 0:
            if Velue <= Min:
                Min = Velue
                Resalt = Velue
            elif Swng > Max_Dev:
                Max = Velue
                Resalt = Velue
                trend = 1
            else:
                Resalt = Min
        X2MA[bar] = Resalt + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_OnCalculate_trend_ = 0
_s_OnCalculate_Max_ = 0.0
_s_OnCalculate_Min_ = 0.0
_s_OnCalculate_Resalt_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class X2maNrtr(_MQL5Indicator):
    name = 'x2ma_nrtr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # First smoothing averaging method
        'Length1': 12,  # First smoothing depth
        'Phase1': 15,  # First smoothing parameter
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Second smoothing averaging method
        'Length2': 5,  # Second smoothing depth
        'Phase2': 15,  # Second smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Step': 30,  # Flat oscillations size
        'Max_DEV': 55,  # Terminal deviation of price from X2MA that does not change the value of the average
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

