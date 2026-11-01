"""TASSKlT — converted from MQL5: MQL5 Indicators/TASSKlT_HTF/TASSKlT.mq5

Простой визуализатор тренда
Copyright: Copyright © 2009, KurlFX; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, KurlFX', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 11, 2: 5, 3: 5, 4: 1}, 'colors': {1: [16711935, 3329330], 2: [16711935], 3: [65280], 4: [36095]}, 'widths': {1: 4, 2: 4, 3: 4, 4: 2}, 'styles': {4: 0}, 'labels': {1: 'TASSKlT Dn', 2: 'TASSKlT Sell', 3: 'TASSKlT Buy', 4: 'TASSKlT End'}, 'levels': [], 'description': ['Простой визуализатор тренда'], 'name': 'TASSKlT', 'source': 'MQL5 Indicators/TASSKlT_HTF/TASSKlT.mq5', 'folder': 'TASSKlT_HTF', 'inputs': [{'mql': 'ADXperiod1', 'py': 'ADXperiod1', 'param': 'ADXperiod1', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'ADXperiod2', 'py': 'ADXperiod2', 'param': 'ADXperiod2', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'ADXperiod3', 'py': 'ADXperiod3', 'param': 'ADXperiod3', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ADXperiod1 = _input('ADXperiod1', 10)
ADXperiod2 = _input('ADXperiod2', 14)
ADXperiod3 = _input('ADXperiod3', 20)
To = Arr(0, 0.0)
Tc = Arr(0, 0.0)
ColorT = Arr(0, 0.0)
Up = Arr(0, 0.0)
Dn = Arr(0, 0.0)
Ex = Arr(0, 0.0)
MxP = 0
MnP = 0
MdP = 0
ADX1_Handle = 0
ADX2_Handle = 0
ADX3_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ADX1_Handle, ADX2_Handle, ADX3_Handle, ATR_Handle, MdP, MnP, MxP, min_rates_total
    MxP = MathMax(MathMax(ADXperiod1, ADXperiod2), ADXperiod3)
    MnP = MathMin(MathMin(ADXperiod1, ADXperiod2), ADXperiod3)
    if MxP == ADXperiod1:
        MdP = MathMax(ADXperiod2, ADXperiod3)
    elif MxP == ADXperiod2:
        MdP = MathMax(ADXperiod1, ADXperiod3)
    else:
        MdP = MathMax(ADXperiod2, ADXperiod1)
    ATR_Period = 15
    min_rates_total = MathMax(MxP, ATR_Period) + 2
    ADX1_Handle = iADX(None, 0, MnP)
    if ADX1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iADX1')
        return INIT_FAILED
    ADX2_Handle = iADX(None, 0, MdP)
    if ADX2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iADX2')
        return INIT_FAILED
    ADX3_Handle = iADX(None, 0, MxP)
    if ADX3_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iADX3')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, To, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(To, True)
    SetIndexBuffer(1, Tc, INDICATOR_DATA)
    ArraySetAsSeries(Tc, True)
    SetIndexBuffer(2, ColorT, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorT, True)
    SetIndexBuffer(3, Dn, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_ARROW, 226)
    ArraySetAsSeries(Dn, True)
    SetIndexBuffer(4, Up, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_ARROW, 225)
    ArraySetAsSeries(Up, True)
    SetIndexBuffer(5, Ex, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ex, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'TASSKlT'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(ADX1_Handle) < rates_total) or BarsCalculated(ADX2_Handle) < rates_total) or BarsCalculated(ADX3_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ADX1 = Arr(0, 0.0)
    PADX1 = Arr(0, 0.0)
    MADX1 = Arr(0, 0.0)
    ADX2 = Arr(0, 0.0)
    ADX3 = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    to_copy += 1
    if CopyBuffer(ADX1_Handle, MAIN_LINE, 0, to_copy, ADX1) <= 0:
        return 0
    if CopyBuffer(ADX2_Handle, MAIN_LINE, 0, to_copy, ADX2) <= 0:
        return 0
    if CopyBuffer(ADX3_Handle, MAIN_LINE, 0, to_copy, ADX3) <= 0:
        return 0
    if CopyBuffer(ADX1_Handle, PLUSDI_LINE, 0, to_copy, PADX1) <= 0:
        return 0
    if CopyBuffer(ADX1_Handle, MINUSDI_LINE, 0, to_copy, MADX1) <= 0:
        return 0
    ArraySetAsSeries(ADX1, True)
    ArraySetAsSeries(PADX1, True)
    ArraySetAsSeries(MADX1, True)
    ArraySetAsSeries(ADX2, True)
    ArraySetAsSeries(ADX3, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        f1 = False
        f2 = False
        f3 = False
        To[bar] = EMPTY_VALUE
        Tc[bar] = EMPTY_VALUE
        Up[bar] = EMPTY_VALUE
        Dn[bar] = EMPTY_VALUE
        Ex[bar] = EMPTY_VALUE
        if ADX1[bar + 1] < ADX1[bar]:
            f1 = True
        if ADX2[bar + 1] < ADX2[bar]:
            f2 = True
        if ADX3[bar + 1] < ADX3[bar]:
            f3 = True
        if (((f1 and f2) and f3) and ADX1[bar] > 35.0) and ADX2[bar] > 30.0:
            di = PADX1[bar] - MADX1[bar]
            hi = MathMax(open[bar], close[bar])
            lo = MathMin(open[bar], close[bar])
            op = open[bar]
            if di > 0:
                To[bar] = lo
                Tc[bar] = hi
                ColorT[bar] = 1.0
                if To[bar + 1] == EMPTY_VALUE:
                    Up[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            else:
                To[bar] = hi
                Tc[bar] = lo
                ColorT[bar] = 0.0
                if To[bar + 1] == EMPTY_VALUE:
                    Dn[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        else:
            if To[bar + 1] != EMPTY_VALUE:
                Ex[bar] = close[bar + 1]
            else:
                Ex[bar] = Ex[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TASSKlT(_MQL5Indicator):
    name = 'TASSKlT'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ADXperiod1': 10,
        'ADXperiod2': 14,
        'ADXperiod3': 20,
    }

