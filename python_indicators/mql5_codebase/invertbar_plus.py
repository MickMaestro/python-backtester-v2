"""InvertBar_Plus — converted from MQL5: MQL5 Indicators/InvertBar_Plus/InvertBar_Plus.mq5

Перевёрнутый свечной график в отдельном окне с линиями Ask и Bid
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 16}, 'colors': {1: [8421376, 8421504, 16711935]}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: 'InvertedOpen;InvertedHigh;InvertedLow;InvertedClose'}, 'levels': [], 'description': ['Перевёрнутый свечной график в отдельном окне с линиями Ask и Bid'], 'name': 'InvertBar_Plus', 'source': 'MQL5 Indicators/InvertBar_Plus/InvertBar_Plus.mq5', 'folder': 'InvertBar_Plus', 'inputs': [{'mql': 'AskShow', 'py': 'AskShow', 'param': 'AskShow', 'type': 'bool', 'default': True, 'label': 'отображать Ask', 'sinput': False}, {'mql': 'AskColor', 'py': 'AskColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'цвет линии Ask', 'sinput': False}, {'mql': 'AskStyle', 'py': 'AskStyle', 'param': 'AskStyle', 'type': 'int', 'default': 0, 'label': 'стиль линии Ask', 'sinput': False}, {'mql': 'BidShow', 'py': 'BidShow', 'param': 'BidShow', 'type': 'bool', 'default': True, 'label': 'отображать  Bid', 'sinput': False}, {'mql': 'BidColor', 'py': 'BidColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет линии  Bid', 'sinput': False}, {'mql': 'BidStyle', 'py': 'BidStyle', 'param': 'BidStyle', 'type': 'int', 'default': 0, 'label': 'стиль линии Bid', 'sinput': False}, {'mql': 'IndicatorDigits', 'py': 'IndicatorDigits_v', 'param': 'IndicatorDigits_v', 'type': 'int', 'default': 6, 'label': 'формат точности отображения индикатора', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AskShow = _input('AskShow', True)  # отображать Ask
AskColor = _input('AskColor', clrBlue)  # цвет линии Ask
AskStyle = _input('AskStyle', STYLE_SOLID)  # стиль линии Ask
BidShow = _input('BidShow', True)  # отображать  Bid
BidColor = _input('BidColor', clrRed)  # цвет линии  Bid
BidStyle = _input('BidStyle', STYLE_SOLID)  # стиль линии Bid
IndicatorDigits_v = _input('IndicatorDigits_v', 6)  # формат точности отображения индикатора
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 1
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
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, IndicatorDigits_v)
    short_name = 'InvertBar_Plus'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    if BidShow and AskShow:
        IndicatorSetInteger(INDICATOR_LEVELS, 2)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, AskColor)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, AskStyle)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, BidColor)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, BidStyle)
    if BidShow and (not AskShow):
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, BidColor)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, BidStyle)
    if (not BidShow) and AskShow:
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, AskColor)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, AskStyle)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(spread, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtOpenBuffer[bar] = _fdiv(1.0, open[bar])
        ExtCloseBuffer[bar] = _fdiv(1.0, close[bar])
        ExtHighBuffer[bar] = _fdiv(1.0, low[bar])
        ExtLowBuffer[bar] = _fdiv(1.0, high[bar])
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if BidShow and AskShow:
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, ExtCloseBuffer[0])
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, _fdiv(1.0, close[0] + (spread[0] * Point())))
    if BidShow and (not AskShow):
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, _fdiv(1.0, close[0] + (spread[0] * Point())))
    if (not BidShow) and AskShow:
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, ExtCloseBuffer[0])
    return rates_total

def CreateRightPrice(chart_id, name, nwin, time, price, Color, fontsize, text):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, fontsize)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, False)

def SetRightPrice(chart_id, name, nwin, time, price, Color, fontsize, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color, fontsize, text)
    else:
        ObjectMove(chart_id, name, 0, time, price)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class InvertBarPlus(_MQL5Indicator):
    name = 'InvertBar_Plus'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AskShow': True,  # отображать Ask
        'AskStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии Ask
        'BidShow': True,  # отображать  Bid
        'BidStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # стиль линии Bid
        'IndicatorDigits_v': 6,  # формат точности отображения индикатора
    }

