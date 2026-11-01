"""mamasign — converted from MQL5: MQL5 Indicators/MAMA_HTF_Signal/mamasign.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [9639167], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'LeadingSign Sell', 2: 'LeadingSign Buy'}, 'levels': [], 'description': [], 'name': 'mamasign', 'source': 'MQL5 Indicators/MAMA_HTF_Signal/mamasign.mq5', 'folder': 'MAMA_HTF_Signal', 'inputs': [{'mql': 'FastLimit', 'py': 'FastLimit', 'param': 'FastLimit', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'SlowLimit', 'py': 'SlowLimit', 'param': 'SlowLimit', 'type': 'double', 'default': 0.05, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
FastLimit = _input('FastLimit', 0.5)
SlowLimit = _input('SlowLimit', 0.05)
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def CountVelue(Array1, Array2):
    Resalt = ((0.0962 * Array1[0]) + (0.5769 * Array1[2]) - (0.5769 * Array1[4]) - (0.0962 * Array1[6])) * ((0.075 * Array2[1]) + 0.54)
    return Resalt

def ReCountArray(Array):
    Array[6] = Array[5]
    Array[5] = Array[4]
    Array[4] = Array[3]
    Array[3] = Array[2]
    Array[2] = Array[1]
    Array[1] = Array[0]
    return

def SmoothVelue(Array):
    return (0.2 * Array[0]) + (0.8 * Array[1])

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, 7 + 1)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 171)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 171)
    shortname = Box("")
    StringConcatenate(shortname, 'MAMASign(', FastLimit, ', ', SlowLimit, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_FAMA_, _s_OnCalculate_MAMA_
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    DeltaPhase = 0.0
    alpha = 0.0
    MAMA = 0.0
    FAMA = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    if prev_calculated == 0:
        first = min_rates_total
        ArrayInitialize(_s_OnCalculate_smooth, 0.0)
        ArrayInitialize(_s_OnCalculate_detrender, 0.0)
        ArrayInitialize(_s_OnCalculate_period, 0.0)
        ArrayInitialize(_s_OnCalculate_Phase, 0.0)
        ArrayInitialize(_s_OnCalculate_Q1, 0.0)
        ArrayInitialize(_s_OnCalculate_I1, 0.0)
        ArrayInitialize(_s_OnCalculate_I2, 0.0)
        ArrayInitialize(_s_OnCalculate_Q2, 0.0)
        ArrayInitialize(_s_OnCalculate_jI, 0.0)
        ArrayInitialize(_s_OnCalculate_jQ, 0.0)
        ArrayInitialize(_s_OnCalculate_Re, 0.0)
        ArrayInitialize(_s_OnCalculate_Im, 0.0)
        _s_OnCalculate_MAMA_ = PriceSeries(IPC, first - 1, open, low, high, close)
        _s_OnCalculate_FAMA_ = PriceSeries(IPC, first - 1, open, low, high, close)
    else:
        first = prev_calculated - 1
    MAMA = _s_OnCalculate_MAMA_
    FAMA = _s_OnCalculate_FAMA_
    bar = first
    for bar in range(bar, rates_total):
        _s_OnCalculate_smooth[0] = ((4 * PriceSeries(IPC, bar, open, low, high, close)) + (3 * PriceSeries(IPC, bar - 1, open, low, high, close)) + (2 * PriceSeries(IPC, bar - 2, open, low, high, close)) + (1 * PriceSeries(IPC, bar - 3, open, low, high, close))) / 10.0
        _s_OnCalculate_detrender[0] = CountVelue(_s_OnCalculate_smooth, _s_OnCalculate_period)
        _s_OnCalculate_Q1[0] = CountVelue(_s_OnCalculate_detrender, _s_OnCalculate_period)
        _s_OnCalculate_I1[0] = _s_OnCalculate_detrender[3]
        _s_OnCalculate_jI[0] = CountVelue(_s_OnCalculate_I1, _s_OnCalculate_I1)
        _s_OnCalculate_jQ[0] = CountVelue(_s_OnCalculate_Q1, _s_OnCalculate_Q1)
        _s_OnCalculate_I2[0] = _s_OnCalculate_I1[0] - _s_OnCalculate_jQ[0]
        _s_OnCalculate_Q2[0] = _s_OnCalculate_Q1[0] + _s_OnCalculate_jI[0]
        _s_OnCalculate_I2[0] = SmoothVelue(_s_OnCalculate_I2)
        _s_OnCalculate_Q2[0] = SmoothVelue(_s_OnCalculate_Q2)
        _s_OnCalculate_Re[0] = (_s_OnCalculate_I2[0] * _s_OnCalculate_I2[1]) + (_s_OnCalculate_Q2[0] * _s_OnCalculate_Q2[1])
        _s_OnCalculate_Im[0] = (_s_OnCalculate_I2[0] * _s_OnCalculate_Q2[1]) - (_s_OnCalculate_Q2[0] * _s_OnCalculate_I2[1])
        _s_OnCalculate_Re[0] = SmoothVelue(_s_OnCalculate_Re)
        _s_OnCalculate_Im[0] = SmoothVelue(_s_OnCalculate_Im)
        if _s_OnCalculate_Im[0] and _s_OnCalculate_Re[0]:
            res = MathArctan(_fdiv(_s_OnCalculate_Im[0], _s_OnCalculate_Re[0]))
            if res:
                _s_OnCalculate_period[0] = _fdiv(6.285714, res)
            else:
                _s_OnCalculate_period[0] = 6.285714
        else:
            _s_OnCalculate_period[0] = 6.285714
        if _s_OnCalculate_period[0] > (1.5 * _s_OnCalculate_period[1]):
            _s_OnCalculate_period[0] = 1.5 * _s_OnCalculate_period[1]
        if _s_OnCalculate_period[0] < (0.67 * _s_OnCalculate_period[1]):
            _s_OnCalculate_period[0] = 0.67 * _s_OnCalculate_period[1]
        if _s_OnCalculate_period[0] < 6.0:
            _s_OnCalculate_period[0] = 6.0
        if _s_OnCalculate_period[0] > 50.0:
            _s_OnCalculate_period[0] = 50.0
        _s_OnCalculate_period[0] = (0.2 * _s_OnCalculate_period[0]) + (0.8 * _s_OnCalculate_period[1])
        if _s_OnCalculate_I1[0]:
            _s_OnCalculate_Phase[0] = 57.27272987 * MathArctan(_fdiv(_s_OnCalculate_Q1[0], _s_OnCalculate_I1[0]))
        else:
            _s_OnCalculate_Phase[0] = 57.27272987
        DeltaPhase = _s_OnCalculate_Phase[1] - _s_OnCalculate_Phase[0]
        if DeltaPhase < 1:
            DeltaPhase = 1.0
        alpha = _fdiv(FastLimit, DeltaPhase)
        if alpha < SlowLimit:
            alpha = SlowLimit
        MAMA = (alpha * PriceSeries(IPC, bar, open, low, high, close)) + ((1.0 - alpha) * _s_OnCalculate_MAMA_)
        FAMA = (0.5 * alpha * MAMA) + ((1.0 - (0.5 * alpha)) * _s_OnCalculate_FAMA_)
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_FAMA_ > _s_OnCalculate_MAMA_ and FAMA < MAMA:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_FAMA_ < _s_OnCalculate_MAMA_ and FAMA > MAMA:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar < (rates_total - 1):
            ReCountArray(_s_OnCalculate_smooth)
            ReCountArray(_s_OnCalculate_detrender)
            ReCountArray(_s_OnCalculate_period)
            ReCountArray(_s_OnCalculate_Phase)
            ReCountArray(_s_OnCalculate_Q1)
            ReCountArray(_s_OnCalculate_I1)
            ReCountArray(_s_OnCalculate_I2)
            ReCountArray(_s_OnCalculate_Q2)
            ReCountArray(_s_OnCalculate_jI)
            ReCountArray(_s_OnCalculate_jQ)
            ReCountArray(_s_OnCalculate_Re)
            ReCountArray(_s_OnCalculate_Im)
            _s_OnCalculate_MAMA_ = MAMA
            _s_OnCalculate_FAMA_ = FAMA
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]

# ---- static local variables
_s_OnCalculate_smooth = Arr(7, 0.0, dyn=False)
_s_OnCalculate_detrender = Arr(7, 0.0, dyn=False)
_s_OnCalculate_Q1 = Arr(7, 0.0, dyn=False)
_s_OnCalculate_I1 = Arr(7, 0.0, dyn=False)
_s_OnCalculate_I2 = Arr(7, 0.0, dyn=False)
_s_OnCalculate_Q2 = Arr(7, 0.0, dyn=False)
_s_OnCalculate_jI = Arr(7, 0.0, dyn=False)
_s_OnCalculate_jQ = Arr(7, 0.0, dyn=False)
_s_OnCalculate_Re = Arr(7, 0.0, dyn=False)
_s_OnCalculate_Im = Arr(7, 0.0, dyn=False)
_s_OnCalculate_period = Arr(7, 0.0, dyn=False)
_s_OnCalculate_Phase = Arr(7, 0.0, dyn=False)
_s_OnCalculate_MAMA_ = 0.0
_s_OnCalculate_FAMA_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Mamasign(_MQL5Indicator):
    name = 'mamasign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastLimit': 0.5,
        'SlowLimit': 0.05,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
    }

