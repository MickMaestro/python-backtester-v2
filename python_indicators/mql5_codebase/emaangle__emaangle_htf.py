"""emaangle — converted from MQL5: MQL5 Indicators/EMAAngle_HTF/emaangle.mq5

Copyright: Copyright © 2008, jpkfox; Link: http://www.strategybuilderfx.com/forums/showthread.php?t=15274&page=1&pp=8; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, jpkfox', 'link': 'http://www.strategybuilderfx.com/forums/showthread.php?t=15274&page=1&pp=8', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 8388736, 8421504, 8421376, 65407]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'EMAAngle'}, 'levels': [], 'description': [], 'name': 'emaangle', 'source': 'MQL5 Indicators/EMAAngle_HTF/emaangle.mq5', 'folder': 'EMAAngle_HTF', 'inputs': [{'mql': 'EMAPeriod', 'py': 'EMAPeriod', 'param': 'EMAPeriod', 'type': 'uint', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'AngleTreshold', 'py': 'AngleTreshold', 'param': 'AngleTreshold', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'StartEMAShift', 'py': 'StartEMAShift', 'param': 'StartEMAShift', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'EndEMAShift', 'py': 'EndEMAShift', 'param': 'EndEMAShift', 'type': 'uint', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
EMAPeriod = _input('EMAPeriod', 34)
MAType = _input('MAType', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
AngleTreshold = _input('AngleTreshold', 3.0)
StartEMAShift = _input('StartEMAShift', 6)
EndEMAShift = _input('EndEMAShift', 0)
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
MA_Handle = 0
dFactor = 0.0
mFactor = 0.0

def OnInit():
    global MA_Handle, dFactor, mFactor, min_rates_total
    if StartEMAShift <= EndEMAShift:
        Print('Неверное значение входного параметров StartEMAShift и EndEMAShift!!!')
        return
    min_rates_total = _int(EMAPeriod + MathMax(StartEMAShift, EndEMAShift))
    MA_Handle = iMA(None, 0, EMAPeriod, 0, MAType, MAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
    dFactor = 3.14159 / 180.0
    mFactor = 10000.0
    if Symbol() == 'USDJPY':
        mFactor = 100.0
    ShiftDif = StartEMAShift - EndEMAShift
    mFactor = _fdiv(mFactor, ShiftDif)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EMAAngle(' + _str(EMAPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, AngleTreshold)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -AngleTreshold)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(MA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    clr = 0
    fEndMA = 0.0
    fStartMA = 0.0
    fAngle = 0.0
    MA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(MA, True)
    to_copy = limit + min_rates_total + 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        fEndMA = MA[bar + EndEMAShift]
        fStartMA = MA[bar + StartEMAShift]
        fAngle = mFactor * (fEndMA - fStartMA)
        IndBuffer[bar] = fAngle
        clr = 2
        if fAngle > 0:
            if fAngle > AngleTreshold:
                clr = 4
            else:
                clr = 3
        if fAngle < 0:
            if fAngle < (-AngleTreshold):
                clr = 0
            else:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Emaangle(_MQL5Indicator):
    name = 'emaangle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'EMAPeriod': 34,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'AngleTreshold': 3.0,
        'StartEMAShift': 6,
        'EndEMAShift': 0,
    }

