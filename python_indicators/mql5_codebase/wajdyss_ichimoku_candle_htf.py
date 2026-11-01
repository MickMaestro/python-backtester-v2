"""wajdyss_Ichimoku_Candle_HTF — converted from MQL5: MQL5 Indicators/Wajdyss_Ichimoku_Candle_HTF/wajdyss_Ichimoku_Candle_HTF.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711935, 2763429, 16711680, 16776960]}, 'widths': {}, 'styles': {}, 'labels': {1: 'wajdyss_Ichimoku Open;wajdyss_Ichimoku High;wajdyss_Ichimoku Low;wajdyss_Ichimoku Close'}, 'levels': [], 'description': [], 'name': 'wajdyss_Ichimoku_Candle_HTF', 'source': 'MQL5 Indicators/Wajdyss_Ichimoku_Candle_HTF/wajdyss_Ichimoku_Candle_HTF.mq5', 'folder': 'Wajdyss_Ichimoku_Candle_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'Kijun', 'py': 'Kijun', 'param': 'Kijun', 'type': 'uint', 'default': 26, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
Kijun = _input('Kijun', 26)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ColorBears не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    short_name = 'wajdyss_Ichimoku_Candle' + ' ' + Symbol() + '(' + GetStringTimeframe(Period()) + ')'
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'wajdyss_Ichimoku_Candle', Kijun)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора wajdyss_Ichimoku_Candle')
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
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    if not CountIndicatorBar("", TimeFrame, Ind_Handle, time, open, high, low, close, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def CountIndicatorBar(Symb, TFrame, IndHandle, Time, Open, High, Low, Close, Rates_Total, Prev_Calculated, Min_Rates_Total):
    global _s_CountIndicatorBar_LastCountBar
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicatorBar_LastCountBar = limit
    else:
        limit = _s_CountIndicatorBar_LastCountBar + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TimeFrame, _DT(Time[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if Time[bar] >= IndTime[0] and Time[bar + 1] < IndTime[0]:
            _s_CountIndicatorBar_LastCountBar = bar
            Col = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, 4, _DT(Time[bar]), 1, Col) <= 0:
                return (0 != 0)
            ExtOpenBuffer[bar] = Open[bar]
            ExtLowBuffer[bar] = Low[bar]
            ExtHighBuffer[bar] = High[bar]
            ExtCloseBuffer[bar] = Close[bar]
            if Col[0] > 1:
                if Open[bar] <= Close[bar]:
                    ExtColorBuffer[bar] = 3.0
                else:
                    ExtColorBuffer[bar] = 2.0
            else:
                if Open[bar] >= Close[bar]:
                    ExtColorBuffer[bar] = 0.0
                else:
                    ExtColorBuffer[bar] = 1.0
        else:
            ExtOpenBuffer[bar] = Open[bar]
            ExtLowBuffer[bar] = Low[bar]
            ExtHighBuffer[bar] = High[bar]
            ExtCloseBuffer[bar] = Close[bar]
            if ExtColorBuffer[bar + 1] > 1:
                if Open[bar] <= Close[bar]:
                    ExtColorBuffer[bar] = 3.0
                else:
                    ExtColorBuffer[bar] = 2.0
            else:
                if Open[bar] >= Close[bar]:
                    ExtColorBuffer[bar] = 0.0
                else:
                    ExtColorBuffer[bar] = 1.0
    return True

# ---- static local variables
_s_CountIndicatorBar_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WajdyssIchimokuCandleHTF(_MQL5Indicator):
    name = 'wajdyss_Ichimoku_Candle_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'Kijun': 26,
    }

