"""mfcs_currency_correlation_chart — converted from MQL5: MQL5 Indicators/MFCS Currency Correlation Chart/mfcs_currency_correlation_chart.mq5

Copyright: Copyright 2011, Mansukh Patidar.; Link: http://www.mpatidar.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, Mansukh Patidar.', 'link': 'http://www.mpatidar.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 16}, 'colors': {1: [16748574, 17919, 12632256]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MFCS Currency Correlation Chart'}, 'levels': [], 'description': [], 'name': 'mfcs_currency_correlation_chart', 'source': 'MQL5 Indicators/MFCS Currency Correlation Chart/mfcs_currency_correlation_chart.mq5', 'folder': 'MFCS Currency Correlation Chart', 'inputs': [{'mql': 'symbol', 'py': 'symbol', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': '', 'sinput': False}, {'mql': 'inverted', 'py': 'inverted', 'param': 'inverted', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'monochrome', 'py': 'monochrome', 'param': 'monochrome', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'show_bid', 'py': 'show_bid', 'param': 'show_bid', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'bid_color', 'py': 'bid_color', 'param': None, 'type': 'color', 'default': 12632256, 'label': '', 'sinput': False}, {'mql': 'show_ask', 'py': 'show_ask', 'param': 'show_ask', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'ask_color', 'py': 'ask_color', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CCChartBuffer1 = Arr(0, 0.0)
CCChartBuffer2 = Arr(0, 0.0)
CCChartBuffer3 = Arr(0, 0.0)
CCChartBuffer4 = Arr(0, 0.0)
ColorBarsColor = Arr(0, 0.0)
bars_calculated = 0
symbol = _input('symbol', 'GBPUSD')
inverted = _input('inverted', False)
monochrome = _input('monochrome', False)
show_bid = _input('show_bid', True)
bid_color = _input('bid_color', clrSilver)
show_ask = _input('show_ask', False)
ask_color = _input('ask_color', clrRed)
STC_Period = 5
STC_Slowing = 3
STC_D = 3
STCHandle = 0
ask_line_id = ''
bid_line_id = ''
inv_warning = ''

def OnInit():
    global STCHandle, ask_line_id, bars_calculated, bid_line_id, inv_warning
    SetIndexBuffer(0, CCChartBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, CCChartBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, CCChartBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, CCChartBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ColorBarsColor, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, _int(SymbolInfoInteger(symbol, SYMBOL_DIGITS)))
    label = 'MFCS Currency Correlation Chart(' + symbol + ')'
    if inverted:
        label = label + ' - INVERTED'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    STCHandle = iStochastic(symbol, Period(), STC_Period, STC_D, STC_Slowing, MODE_EMA, STO_LOWHIGH)
    bars_calculated = 0
    ask_line_id = symbol + '_ask_line_id_' + IntegerToString(MathRand())
    bid_line_id = symbol + '_bid_line_id_' + IntegerToString(MathRand())
    inv_warning = 'MFCS CC-' + symbol + IntegerToString(MathRand()) + '' + IntegerToString(MathRand())
    if inverted:
        chart_max_price = ChartGetDouble(0, CHART_PRICE_MAX, ChartWindowFind())
        ObjectCreate(0, inv_warning, OBJ_LABEL, ChartWindowFind(), TimeCurrent(), chart_max_price)
        ObjectSetInteger(0, inv_warning, OBJPROP_XDISTANCE, 20)
        ObjectSetInteger(0, inv_warning, OBJPROP_YDISTANCE, 20)
        ObjectSetInteger(0, inv_warning, OBJPROP_COLOR, clrRed)
        ObjectSetString(0, inv_warning, OBJPROP_TEXT, 'INVERTED')
        ObjectSetString(0, inv_warning, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, inv_warning, OBJPROP_FONTSIZE, 18)
        ObjectSetInteger(0, inv_warning, OBJPROP_SELECTABLE, False)
    return 0

def OnDeinit(reason):
    ObjectDelete(0, ask_line_id)
    ObjectDelete(0, bid_line_id)
    ObjectDelete(0, inv_warning)
    IndicatorRelease(STCHandle)

def DisplayBidAskLines():
    tick = MqlTick()
    SymbolInfoTick(symbol, tick)
    if inverted:
        tick.ask = _fdiv(1, tick.ask)
        tick.bid = _fdiv(1, tick.bid)
    if show_ask:
        if ObjectFind(0, ask_line_id) < 0:
            ObjectCreate(0, ask_line_id, OBJ_HLINE, ChartWindowFind(), TimeCurrent(), tick.ask)
        ObjectSetDouble(0, ask_line_id, OBJPROP_PRICE, tick.ask)
        ObjectSetInteger(0, ask_line_id, OBJPROP_COLOR, ask_color)
    if show_bid:
        if ObjectFind(0, bid_line_id) < 0:
            ObjectCreate(0, bid_line_id, OBJ_HLINE, ChartWindowFind(), TimeCurrent(), tick.bid)
        ObjectSetDouble(0, bid_line_id, OBJPROP_PRICE, tick.bid)
        ObjectSetInteger(0, bid_line_id, OBJPROP_COLOR, bid_color)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < STC_Period:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        to_copy += 1
    limit = 0
    i = 0
    if prev_calculated < STC_Period:
        limit = STC_Period
    else:
        limit = prev_calculated - 1
    rates = Arr(1, 0, dyn=False, factory=MqlRates)
    DisplayBidAskLines()
    i = limit
    for i in range(i, rates_total):
        buffer_index = i
        rates[0].close = 0.0
        rates[0].open = 0.0
        rates[0].low = 0.0
        rates[0].high = 0.0
        copied = CopyRates(symbol, Period(), rates_total - buffer_index - 1, 1, rates)
        if copied and rates[0].open > 0.0:
            if inverted:
                if rates[0].open != 0:
                    rates[0].open = _fdiv(1, rates[0].open)
                if rates[0].high != 0:
                    rates[0].high = _fdiv(1, rates[0].high)
                if rates[0].low != 0:
                    rates[0].low = _fdiv(1, rates[0].low)
                if rates[0].close != 0:
                    rates[0].close = _fdiv(1, rates[0].close)
            CCChartBuffer1[buffer_index] = rates[0].open
            CCChartBuffer2[buffer_index] = rates[0].high
            CCChartBuffer3[buffer_index] = rates[0].low
            CCChartBuffer4[buffer_index] = rates[0].close
            if monochrome:
                ColorBarsColor[i] = 2.0
            elif rates[0].open > rates[0].close:
                ColorBarsColor[i] = 1.0
            else:
                ColorBarsColor[i] = 0.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MfcsCurrencyCorrelationChart(_MQL5Indicator):
    name = 'mfcs_currency_correlation_chart'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inverted': False,
        'monochrome': False,
        'show_bid': True,
        'show_ask': False,
    }

