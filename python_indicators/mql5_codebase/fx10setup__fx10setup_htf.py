"""fx10setup — converted from MQL5: MQL5 Indicators/Fx10Setup_HTF/fx10setup.mq5

Copyright: Copyright © 2006, palanka; Link: http://www.metaquotes.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, palanka', 'link': 'http://www.metaquotes.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2, 'indicator_maximum': 1.1, 'indicator_minimum': 0.3}, 'types': {1: 3, 2: 3}, 'colors': {1: [3329330], 2: [4678655]}, 'widths': {1: 5, 2: 5}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper Fx10Setup', 2: 'Lower Fx10Setup'}, 'levels': [], 'description': [], 'name': 'fx10setup', 'source': 'MQL5 Indicators/Fx10Setup_HTF/fx10setup.mq5', 'folder': 'Fx10Setup_HTF', 'inputs': [{'mql': 'ParmMult', 'py': 'ParmMult', 'param': 'ParmMult', 'type': 'double', 'default': 2.0, 'label': 'Multiply the standard parameters by this scale factor', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ParmMult = _input('ParmMult', 2.0)  # Multiply the standard parameters by this scale factor
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtMapBufferUp = Arr(0, 0.0)
ExtMapBufferDown = Arr(0, 0.0)
FsMa_Handle = 0
SlMa_Handle = 0
STO_Handle = 0
MACD_Handle = 0
RSI_Handle = 0
min_rates_total = 0

def OnInit():
    global FsMa_Handle, MACD_Handle, RSI_Handle, STO_Handle, SlMa_Handle, min_rates_total
    RSI_Handle = iRSI(None, 0, _int(14 * ParmMult), PRICE_CLOSE)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    MACD_Handle = iMACD(None, 0, _int(12 * ParmMult), _int(26 * ParmMult), _int(9 * ParmMult), PRICE_CLOSE)
    if MACD_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMACD')
        return INIT_FAILED
    FsMa_Handle = iMA(None, 0, _int(5 * ParmMult), 0, MODE_LWMA, PRICE_CLOSE)
    if FsMa_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора fast iMA')
        return INIT_FAILED
    SlMa_Handle = iMA(None, 0, _int(10 * ParmMult), 0, MODE_SMA, PRICE_CLOSE)
    if SlMa_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора slow iMA')
        return INIT_FAILED
    STO_Handle = iStochastic(None, 0, _int(5 * ParmMult), _int(3 * ParmMult), _int(3 * ParmMult), MODE_SMA, STO_CLOSECLOSE)
    if STO_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iStochastic')
        return INIT_FAILED
    min_rates_total = _int((12 * ParmMult) + (26 * ParmMult) + (9 * ParmMult))
    SetIndexBuffer(0, ExtMapBufferUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ExtMapBufferDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'Fx10Setup(', DoubleToString(ParmMult, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((rates_total < min_rates_total or BarsCalculated(RSI_Handle) < rates_total) or BarsCalculated(MACD_Handle) < rates_total) or BarsCalculated(STO_Handle) < rates_total) or BarsCalculated(FsMa_Handle) < rates_total) or BarsCalculated(SlMa_Handle) < rates_total:
        return 0
    RSI = Arr(0, 0.0)
    FsMa = Arr(0, 0.0)
    SlMa = Arr(0, 0.0)
    MMacd = Arr(0, 0.0)
    SMacd = Arr(0, 0.0)
    MSto = Arr(0, 0.0)
    SSto = Arr(0, 0.0)
    StochUp = False
    StochDown = False
    RsiUp = False
    RsiDown = False
    MacdUp = False
    MacdDown = False
    limit = 0
    to_copy = 0
    bar = 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(MMacd, True)
    ArraySetAsSeries(SMacd, True)
    ArraySetAsSeries(MSto, True)
    ArraySetAsSeries(SSto, True)
    ArraySetAsSeries(FsMa, True)
    ArraySetAsSeries(SlMa, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    if CopyBuffer(MACD_Handle, MAIN_LINE, 0, to_copy, MMacd) <= 0:
        return 0
    if CopyBuffer(MACD_Handle, SIGNAL_LINE, 0, to_copy, SMacd) <= 0:
        return 0
    if CopyBuffer(STO_Handle, MAIN_LINE, 0, to_copy, MSto) <= 0:
        return 0
    if CopyBuffer(STO_Handle, SIGNAL_LINE, 0, to_copy, SSto) <= 0:
        return 0
    if CopyBuffer(FsMa_Handle, 0, 0, to_copy, FsMa) <= 0:
        return 0
    if CopyBuffer(SlMa_Handle, 0, 0, to_copy, SlMa) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtMapBufferUp[bar] = EMPTY_VALUE
        ExtMapBufferDown[bar] = EMPTY_VALUE
        if FsMa[bar] > SlMa[bar]:
            RsiUp = RSI[bar] >= 55.0
            StochUp = MSto[bar] > SSto[bar]
            MacdUp = MMacd[bar] > SMacd[bar]
            if (StochUp and RsiUp) and MacdUp:
                ExtMapBufferUp[bar] = 1.0
        elif FsMa[bar] < SlMa[bar]:
            RsiDown = RSI[bar] <= 45.0
            StochDown = MSto[bar] < SSto[bar]
            MacdDown = MMacd[bar] < SMacd[bar]
            if (StochDown and RsiDown) and MacdDown:
                ExtMapBufferDown[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fx10setup(_MQL5Indicator):
    name = 'fx10setup'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ParmMult': 2.0,  # Multiply the standard parameters by this scale factor
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }
    y_range = (0.3, 1.1)

