"""price_channel_central — converted from MQL5: MQL5 Indicators/Price_Channel_Central_HTF/price_channel_central.mq5

Price Channel Central
Copyright: Yuriy Tokman (YTG); Link: http://ytg.com.ua/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Yuriy Tokman (YTG)', 'link': 'http://ytg.com.ua/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [65280], 2: [16711680], 3: [255], 4: [16711935], 5: [16748574]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 5, 5: 5}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Chanell Upper', 2: 'Chanell Middle', 3: 'Chanell Lower', 4: 'Price_Channel_Central Sell', 5: 'Price_Channel_Central Buy'}, 'levels': [], 'description': ['Price Channel Central'], 'name': 'price_channel_central', 'source': 'MQL5 Indicators/Price_Channel_Central_HTF/price_channel_central.mq5', 'folder': 'Price_Channel_Central_HTF', 'inputs': [{'mql': 'Bars_Count', 'py': 'Bars_Count', 'param': 'Bars_Count', 'type': 'uint', 'default': 32, 'label': '', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 8421376, 'label': '', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Bars_Count = _input('Bars_Count', 32)
Upper_color = _input('Upper_color', clrTeal)
Middle_color = _input('Middle_color', clrBlue)
Lower_color = _input('Lower_color', clrRed)
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0
upper_name = ""
middle_name = ""
lower_name = ""

def OnInit():
    global ATR_Handle, lower_name, middle_name, min_rates_total, upper_name
    ATR_Period = 15
    min_rates_total = _int(MathMax(Bars_Count, ATR_Period)) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    upper_name = 'Price_Channel_Central upper text lable'
    middle_name = 'Price_Channel_Central middle text lable'
    lower_name = 'Price_Channel_Central lower text lable'
    SetIndexBuffer(0, HighestBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MiddleBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, SellBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    ArraySetAsSeries(MiddleBuffer, True)
    ArraySetAsSeries(SellBuffer, True)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'Price_Channel_Central(', Bars_Count, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, upper_name)
    ObjectDelete(0, middle_name)
    ObjectDelete(0, lower_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(ATR, True)
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HH = high[ArrayMaximum(high, bar, Bars_Count)]
        LL = low[ArrayMinimum(low, bar, Bars_Count)]
        MM = (HH + LL) / 2
        HighestBuffer[bar] = HH
        LowestBuffer[bar] = LL
        MiddleBuffer[bar] = MM
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if close[bar] > HighestBuffer[bar + 1]:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if close[bar] < LowestBuffer[bar + 1]:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    SetRightPrice(0, upper_name, 0, time[0], HighestBuffer[0], Upper_color, 'Georgia')
    SetRightPrice(0, middle_name, 0, time[0], MiddleBuffer[0], Middle_color, 'Georgia')
    SetRightPrice(0, lower_name, 0, time[0], LowestBuffer[0], Lower_color, 'Georgia')
    return rates_total

def CreateRightPrice(chart_id, name, nwin, time, price, Color, Font):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetRightPrice(chart_id, name, nwin, time, price, Color, Font):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color, Font)
    else:
        ObjectMove(chart_id, name, 0, time, price)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceChannelCentral(_MQL5Indicator):
    name = 'price_channel_central'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Bars_Count': 32,
    }

