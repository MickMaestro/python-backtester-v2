"""lsma_angle_ — converted from MQL5: MQL5 Indicators/LSMA_Angle_Candle/lsma_angle_.mq5

Copyright: Copyright © 2005, Robert L. Hill aka MrPip; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Robert L. Hill aka MrPip', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 15631086, 8421504, 16748574, 16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'LSMA_Angle'}, 'levels': [], 'description': [], 'name': 'lsma_angle_', 'source': 'MQL5 Indicators/LSMA_Angle_Candle/lsma_angle_.mq5', 'folder': 'LSMA_Angle_Candle', 'inputs': [{'mql': 'LSMAPeriod', 'py': 'LSMAPeriod', 'param': 'LSMAPeriod', 'type': 'uint', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'AngleTreshold', 'py': 'AngleTreshold', 'param': 'AngleTreshold', 'type': 'int', 'default': 15, 'label': 'Порог срабатывания', 'sinput': False}, {'mql': 'StartLSMAShift', 'py': 'StartLSMAShift', 'param': 'StartLSMAShift', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'EndLSMAShift', 'py': 'EndLSMAShift', 'param': 'EndLSMAShift', 'type': 'uint', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_PRICE_TYPE
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
_enum('ENUM_PRICE_TYPE', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
LSMAPeriod = _input('LSMAPeriod', 25)
AngleTreshold = _input('AngleTreshold', _int(15.0))  # Порог срабатывания
StartLSMAShift = _input('StartLSMAShift', 4)
EndLSMAShift = _input('EndLSMAShift', 0)
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
mFactor = 0.0
dFactor = 0.0
ShiftDif = 0.0
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def LSMA(Rperiod, Open, Low, High, Close, shift):
    iii = 0
    sum_ = 0.0
    length = 0
    lengthvar = 0.0
    tmp = 0.0
    wt = 0.0
    length = Rperiod
    sum_ = 0.0
    iii = length
    for iii in range(iii, 1 - 1, -1):
        lengthvar = length + 1
        lengthvar = lengthvar / 3
        tmp = (iii - lengthvar) * PriceSeries(IPC, length - iii + shift, Open, Low, High, Close)
        sum_ += tmp
    else:
        iii = _range_end(iii, 1 - 1, -1)
    wt = _fdiv(sum_ * 6, length * (length + 1))
    return wt

def OnInit():
    global ShiftDif, dFactor, mFactor, min_rates_total
    min_rates_total = _int(MathMax(LSMAPeriod + StartLSMAShift, LSMAPeriod + EndLSMAShift))
    dFactor = (2 * 3.14159) / 180.0
    mFactor = 100000.0
    Sym = StringSubstr(Symbol(), 3, 3)
    if Sym == 'JPY':
        mFactor = 1000.0
    ShiftDif = StartLSMAShift - EndLSMAShift
    mFactor = _fdiv(mFactor, ShiftDif)
    if EndLSMAShift >= StartLSMAShift:
        Print('Error: EndLSMAShift >= StartLSMAShift')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'LSMA_Angle')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, AngleTreshold)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -AngleTreshold)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrTeal)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrTeal)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    clr = 0
    fEndMA = 0.0
    fStartMA = 0.0
    fAngle = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        fEndMA = LSMA(LSMAPeriod, open, low, high, close, bar + EndLSMAShift)
        fStartMA = LSMA(LSMAPeriod, open, low, high, close, bar + StartLSMAShift)
        fAngle = (mFactor * (fEndMA - fStartMA)) / 2
        IndBuffer[bar] = fAngle
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        if IndBuffer[bar] > AngleTreshold:
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 3
        if IndBuffer[bar] < (-AngleTreshold):
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LsmaAngle(_MQL5Indicator):
    name = 'lsma_angle_'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LSMAPeriod': 25,
        'AngleTreshold': 15,  # Порог срабатывания
        'StartLSMAShift': 4,
        'EndLSMAShift': 0,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
    }

