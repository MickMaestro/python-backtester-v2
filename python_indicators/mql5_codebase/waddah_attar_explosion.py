"""waddah_attar_explosion — converted from MQL5: MQL5 Indicators/Waddah Attar Explosion/waddah_attar_explosion.mq5

Copyright: Copyright © 2006, Eng. Waddah Attar; Link: waddahattar@hotmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Eng. Waddah Attar', 'link': 'waddahattar@hotmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3, 'indicator_minimum': 0.0}, 'types': {1: 10, 2: 1, 3: 1}, 'colors': {1: [8421504, 65280, 16711935], 2: [16711680], 3: [255]}, 'widths': {1: 2, 2: 2, 3: 1}, 'styles': {1: 0, 2: 0, 3: 4}, 'labels': {1: 'MACD', 2: 'Signal Line', 3: 'DeadZonePip Level'}, 'levels': [], 'description': [], 'name': 'waddah_attar_explosion', 'source': 'MQL5 Indicators/Waddah Attar Explosion/waddah_attar_explosion.mq5', 'folder': 'Waddah Attar Explosion', 'inputs': [{'mql': 'Fast_MA', 'py': 'Fast_MA', 'param': 'Fast_MA', 'type': 'int', 'default': 20, 'label': 'Period of the fast MACD moving average', 'sinput': False}, {'mql': 'Slow_MA', 'py': 'Slow_MA', 'param': 'Slow_MA', 'type': 'int', 'default': 40, 'label': 'Period of the slow MACD moving average', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'int', 'default': 20, 'label': 'Bollinger period', 'sinput': False}, {'mql': 'BBDeviation', 'py': 'BBDeviation', 'param': 'BBDeviation', 'type': 'double', 'default': 2.0, 'label': 'Number of Bollinger deviations', 'sinput': False}, {'mql': 'Sensetive', 'py': 'Sensetive', 'param': 'Sensetive', 'type': 'int', 'default': 150, 'label': '', 'sinput': False}, {'mql': 'DeadZonePip', 'py': 'DeadZonePip', 'param': 'DeadZonePip', 'type': 'int', 'default': 400, 'label': '', 'sinput': False}, {'mql': 'ExplosionPower', 'py': 'ExplosionPower', 'param': 'ExplosionPower', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'TrendPower', 'py': 'TrendPower', 'param': 'TrendPower', 'type': 'int', 'default': 150, 'label': '', 'sinput': False}, {'mql': 'AlertWindow', 'py': 'AlertWindow', 'param': 'AlertWindow', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'AlertLong', 'py': 'AlertLong', 'param': 'AlertLong', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertShort', 'py': 'AlertShort', 'param': 'AlertShort', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertExitLong', 'py': 'AlertExitLong', 'param': 'AlertExitLong', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertExitShort', 'py': 'AlertExitShort', 'param': 'AlertExitShort', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Fast_MA = _input('Fast_MA', 20)  # Period of the fast MACD moving average
Slow_MA = _input('Slow_MA', 40)  # Period of the slow MACD moving average
BBPeriod = _input('BBPeriod', 20)  # Bollinger period
BBDeviation = _input('BBDeviation', 2.0)  # Number of Bollinger deviations
Sensetive = _input('Sensetive', 150)
DeadZonePip = _input('DeadZonePip', 400)
ExplosionPower = _input('ExplosionPower', 15)
TrendPower = _input('TrendPower', 150)
AlertWindow = _input('AlertWindow', False)
AlertCount = _input('AlertCount', 2)
AlertLong = _input('AlertLong', False)
AlertShort = _input('AlertShort', False)
AlertExitLong = _input('AlertExitLong', False)
AlertExitShort = _input('AlertExitShort', False)
min_rates_total = 0
MACD_Handle = 0
BB_Handle = 0
bask = 0.0
bbid = 0.0
LastTime1 = 0
LastTime2 = 0
LastTime3 = 0
LastTime4 = 0
Status = 0
PrevStatus = 0
IndBuffer1 = Arr(0, 0.0)
ColorIndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)

def OnInit():
    global BB_Handle, LastTime1, LastTime2, LastTime3, LastTime4, MACD_Handle, PrevStatus, Status, min_rates_total
    min_rates_total = BBPeriod + 1
    LastTime1 = 1
    LastTime2 = 1
    LastTime3 = 1
    LastTime4 = 1
    Status = 0
    PrevStatus = -1
    MACD_Handle = iMACD(None, 0, Fast_MA, Slow_MA, 9, PRICE_CLOSE)
    if MACD_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMACD indicator')
    BB_Handle = iBands(None, 0, BBPeriod, 0, BBDeviation, PRICE_CLOSE)
    if BB_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iBands indicator')
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer1, True)
    SetIndexBuffer(1, ColorIndBuffer1, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorIndBuffer1, True)
    SetIndexBuffer(2, IndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer2, True)
    SetIndexBuffer(3, IndBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer3, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Waddah Attar Explosion')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LastTime1, LastTime2, LastTime3, LastTime4, PrevStatus, Status, bask, bbid
    if (BarsCalculated(MACD_Handle) < rates_total or BarsCalculated(BB_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    MACD = Arr(0, 0.0)
    BandsUp = Arr(0, 0.0)
    BandsDn = Arr(0, 0.0)
    Trend1 = 0.0
    Trend2 = 0.0
    Explo1 = 0.0
    Explo2 = 0.0
    Dead = 0.0
    pwrt = 0.0
    pwre = 0.0
    Ask = 0.0
    Bid = 0.0
    SirName = Box("")
    ArraySetAsSeries(spread, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(MACD, True)
    ArraySetAsSeries(BandsUp, True)
    ArraySetAsSeries(BandsDn, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(BB_Handle, 1, 0, to_copy, BandsUp) <= 0:
        return 0
    if CopyBuffer(BB_Handle, 2, 0, to_copy, BandsDn) <= 0:
        return 0
    to_copy += 2
    if CopyBuffer(MACD_Handle, 0, 0, to_copy, MACD) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Trend1 = (MACD[bar] - MACD[bar + 1]) * Sensetive
        Trend2 = (MACD[bar + 2] - MACD[bar + 3]) * Sensetive
        Explo1 = BandsUp[bar] - BandsDn[bar]
        Explo2 = BandsUp[bar + 1] - BandsDn[bar + 1]
        Dead = Point() * DeadZonePip
        IndBuffer1[bar] = MathAbs(Trend1)
        Bid = close[bar]
        Ask = Bid + spread[bar]
        if Trend1 > 0:
            ColorIndBuffer1[bar] = 1.0
        if Trend1 < 0:
            ColorIndBuffer1[bar] = 2.0
        IndBuffer2[bar] = Explo1
        IndBuffer3[bar] = Dead
        if bar == 0:
            if (((((((Trend1 > 0 and Trend1 > Explo1) and Trend1 > Dead) and Explo1 > Dead) and Explo1 > Explo2) and Trend1 > Trend2) and LastTime1 < AlertCount) and AlertLong == True) and Ask != bask:
                pwrt = _fdiv(100 * (Trend1 - Trend2), Trend1)
                pwre = _fdiv(100 * (Explo1 - Explo2), Explo1)
                bask = Ask
                if pwre >= ExplosionPower and pwrt >= TrendPower:
                    SirName.v = ''
                    StringConcatenate(SirName, LastTime1, '- ', Symbol(), ' - BUY ', ' (', DoubleToString(bask, Digits()), ') Trend PWR ', DoubleToString(pwrt, 0), ' - Exp PWR ', DoubleToString(pwre, 0))
                    if AlertWindow == True:
                        Alert(SirName.v)
                    else:
                        Print(SirName.v)
                    LastTime1 += 1
                Status = 1
            if (((((((Trend1 < 0 and MathAbs(Trend1) > Explo1) and MathAbs(Trend1) > Dead) and Explo1 > Dead) and Explo1 > Explo2) and MathAbs(Trend1) > MathAbs(Trend2)) and LastTime2 < AlertCount) and AlertShort == True) and Bid != bbid:
                pwrt = _fdiv(100 * (MathAbs(Trend1) - MathAbs(Trend2)), MathAbs(Trend1))
                pwre = _fdiv(100 * (Explo1 - Explo2), Explo1)
                bbid = Bid
                if pwre >= ExplosionPower and pwrt >= TrendPower:
                    SirName.v = ''
                    StringConcatenate(SirName, LastTime2, '- ', Symbol(), ' - Sell ', ' (', DoubleToString(bask, Digits()), ') Trend PWR ', DoubleToString(pwrt, 0), ' - Exp PWR ', DoubleToString(pwre, 0))
                    if AlertWindow == True:
                        Alert(SirName.v)
                    else:
                        Print(SirName.v)
                    LastTime2 += 1
                Status = 2
            if (((((((Trend1 > 0 and Trend1 < Explo1) and Trend1 < Trend2) and Trend2 > Explo2) and Trend1 > Dead) and Explo1 > Dead) and LastTime3 <= AlertCount) and AlertExitLong == True) and Bid != bbid:
                bbid = Bid
                SirName.v = ''
                StringConcatenate(SirName, LastTime3, '- ', Symbol(), ' - Exit BUY ', ' ', DoubleToString(bbid, Digits()))
                if AlertWindow == True:
                    Alert(SirName.v)
                else:
                    Print(SirName.v)
                Status = 3
                LastTime3 += 1
            if (((((((Trend1 < 0 and MathAbs(Trend1) < Explo1) and MathAbs(Trend1) < MathAbs(Trend2)) and MathAbs(Trend2) > Explo2) and Trend1 > Dead) and Explo1 > Dead) and LastTime4 <= AlertCount) and AlertExitShort == True) and Ask != bask:
                bask = Ask
                SirName.v = ''
                StringConcatenate(SirName, LastTime4, '- ', Symbol(), ' - Exit SELL ', ' ', DoubleToString(bask, Digits()))
                if AlertWindow == True:
                    Alert(SirName.v)
                else:
                    Print(SirName.v)
                Status = 4
                LastTime4 += 1
            PrevStatus = Status
        if Status != PrevStatus:
            LastTime1 = 1
            LastTime2 = 1
            LastTime3 = 1
            LastTime4 = 1
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WaddahAttarExplosion(_MQL5Indicator):
    name = 'waddah_attar_explosion'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fast_MA': 20,  # Period of the fast MACD moving average
        'Slow_MA': 40,  # Period of the slow MACD moving average
        'BBPeriod': 20,  # Bollinger period
        'BBDeviation': 2.0,  # Number of Bollinger deviations
        'Sensetive': 150,
        'DeadZonePip': 400,
        'ExplosionPower': 15,
        'TrendPower': 150,
        'AlertWindow': False,
        'AlertCount': 2,
        'AlertLong': False,
        'AlertShort': False,
        'AlertExitLong': False,
        'AlertExitShort': False,
    }

