"""lsma_angle_candle — converted from MQL5: MQL5 Indicators/LSMA_Angle_Candle/lsma_angle_candle.mq5

LSMA_Angle_Candle
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711935, 255, 8421504, 16748574, 16711680]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': ['LSMA_Angle_Candle'], 'name': 'lsma_angle_candle', 'source': 'MQL5 Indicators/LSMA_Angle_Candle/lsma_angle_candle.mq5', 'folder': 'LSMA_Angle_Candle', 'inputs': [{'mql': 'LSMAPeriod', 'py': 'LSMAPeriod', 'param': 'LSMAPeriod', 'type': 'uint', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'AngleTreshold', 'py': 'AngleTreshold', 'param': 'AngleTreshold', 'type': 'int', 'default': 15, 'label': 'Порог срабатывания', 'sinput': False}, {'mql': 'StartLSMAShift', 'py': 'StartLSMAShift', 'param': 'StartLSMAShift', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'EndLSMAShift', 'py': 'EndLSMAShift', 'param': 'EndLSMAShift', 'type': 'uint', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LSMAPeriod = _input('LSMAPeriod', 25)
AngleTreshold = _input('AngleTreshold', _int(15.0))  # Порог срабатывания
StartLSMAShift = _input('StartLSMAShift', 4)
EndLSMAShift = _input('EndLSMAShift', 0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = 32
    Ind_Handle[0] = iCustom(None, 0, 'LSMA_Angle_', LSMAPeriod, AngleTreshold, StartLSMAShift, EndLSMAShift, PRICE_OPEN)
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iLSMA_Angle_[' + _str(0) + ']!')
        return INIT_FAILED
    Ind_Handle[1] = iCustom(None, 0, 'LSMA_Angle_', LSMAPeriod, AngleTreshold, StartLSMAShift, EndLSMAShift, PRICE_HIGH)
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iLSMA_Angle_[' + _str(1) + ']!')
        return INIT_FAILED
    Ind_Handle[2] = iCustom(None, 0, 'LSMA_Angle_', LSMAPeriod, AngleTreshold, StartLSMAShift, EndLSMAShift, PRICE_LOW)
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iLSMA_Angle_[' + _str(2) + ']!')
        return INIT_FAILED
    Ind_Handle[3] = iCustom(None, 0, 'LSMA_Angle_', LSMAPeriod, AngleTreshold, StartLSMAShift, EndLSMAShift, PRICE_CLOSE)
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iLSMA_Angle_[' + _str(3) + ']!')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    short_name = 'LSMA_Angle_Candle'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
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
    if (((BarsCalculated(Ind_Handle[0]) < rates_total or BarsCalculated(Ind_Handle[1]) < rates_total) or BarsCalculated(Ind_Handle[2]) < rates_total) or BarsCalculated(Ind_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle[0], 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[1], 0, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[2], 0, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[3], 0, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        if ExtCloseBuffer[bar] > AngleTreshold:
            if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
                clr = 4
            elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
                clr = 0
        if ExtCloseBuffer[bar] < (-AngleTreshold):
            if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
                clr = 4
            elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
                clr = 0
        if ExtCloseBuffer[bar] < AngleTreshold and ExtCloseBuffer[bar] > (-AngleTreshold):
            if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
                clr = 3
            elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
                clr = 1
        ExtColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LsmaAngleCandle(_MQL5Indicator):
    name = 'lsma_angle_candle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LSMAPeriod': 25,
        'AngleTreshold': 15,  # Порог срабатывания
        'StartLSMAShift': 4,
        'EndLSMAShift': 0,
    }

