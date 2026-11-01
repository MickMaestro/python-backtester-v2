"""ichimoku_cloud — converted from MQL5: MQL5 Indicators/Ichimoku Cloud/ichimoku_cloud.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [10025880, 14204888]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Senkou Span A;Senkou Span B'}, 'levels': [], 'description': [], 'name': 'ichimoku_cloud', 'source': 'MQL5 Indicators/Ichimoku Cloud/ichimoku_cloud.mq5', 'folder': 'Ichimoku Cloud', 'inputs': [{'mql': 'InpTenkan', 'py': 'InpTenkan', 'param': 'InpTenkan', 'type': 'int', 'default': 9, 'label': 'Tenkan-sen', 'sinput': False}, {'mql': 'InpKijun', 'py': 'InpKijun', 'param': 'InpKijun', 'type': 'int', 'default': 26, 'label': 'Kijun-sen', 'sinput': False}, {'mql': 'InpSenkou', 'py': 'InpSenkou', 'param': 'InpSenkou', 'type': 'int', 'default': 52, 'label': 'Senkou Span', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTenkan = _input('InpTenkan', 9)  # Tenkan-sen
InpKijun = _input('InpKijun', 26)  # Kijun-sen
InpSenkou = _input('InpSenkou', 52)  # Senkou Span
min_rates_total = 0
ExtSpanABuffer = Arr(0, 0.0)
ExtSpanBBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = MathMax(InpTenkan, MathMax(InpKijun, InpSenkou))
    SetIndexBuffer(0, ExtSpanABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpKijun)
    ArraySetAsSeries(ExtSpanABuffer, True)
    SetIndexBuffer(1, ExtSpanBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, -InpKijun)
    ArraySetAsSeries(ExtSpanBBuffer, True)
    shortname = 'ZerolagStochs'
    IndicatorSetString(INDICATOR_SHORTNAME, 'Senkou Span A;Senkou Span B(' + _str(InpSenkou) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    HH = 0.0
    LL = 0.0
    ExtTenkan = 0.0
    ExtKijun = 0.0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    for bar in range(limit, 0 - 1, -1):
        HH = High[ArrayMaximum(High, bar, InpTenkan)]
        LL = Low[ArrayMinimum(Low, bar, InpTenkan)]
        ExtTenkan = (HH + LL) / 2.0
        HH = High[ArrayMaximum(High, bar, InpKijun)]
        LL = Low[ArrayMinimum(Low, bar, InpKijun)]
        ExtKijun = (HH + LL) / 2.0
        ExtSpanABuffer[bar] = (ExtTenkan + ExtKijun) / 2.0
        HH = High[ArrayMaximum(High, bar, InpSenkou)]
        LL = Low[ArrayMinimum(Low, bar, InpSenkou)]
        ExtSpanBBuffer[bar] = (HH + LL) / 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IchimokuCloud(_MQL5Indicator):
    name = 'ichimoku_cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTenkan': 9,  # Tenkan-sen
        'InpKijun': 26,  # Kijun-sen
        'InpSenkou': 52,  # Senkou Span
    }

