"""crossindex — converted from MQL5: MQL5 Indicators/CrossIndex/crossindex.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {2: 17}, 'colors': {2: [11186720, 9639167]}, 'widths': {}, 'styles': {}, 'labels': {2: 'ExtOpenBuffer; ExtHighBuffer; ExtLowBuffer; ExtCloseBuffer'}, 'levels': [], 'description': [], 'name': 'crossindex', 'source': 'MQL5 Indicators/CrossIndex/crossindex.mq5', 'folder': 'CrossIndex', 'inputs': [{'mql': 'CrossIndex', 'py': 'CrossIndex', 'param': None, 'type': 'string', 'default': 'EURJPY', 'label': 'Currency pair', 'sinput': False}, {'mql': 'BidColor', 'py': 'BidColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'BidStyle', 'py': 'BidStyle', 'param': 'BidStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant in a zero buffer', 'sinput': False}, {'mql': 'IndicatorDigits', 'py': 'IndicatorDigits_v', 'param': 'IndicatorDigits_v', 'type': 'int', 'default': 3, 'label': 'Indicator display accuracy format', 'sinput': False}, {'mql': 'Direct', 'py': 'Direct', 'param': 'Direct', 'type': 'bool', 'default': True, 'label': 'Chart inversion', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Red = 0x0000FF  # MQL4 colour name

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
CrossIndex = _input('CrossIndex', 'EURJPY')  # Currency pair
BidStyle = _input('BidStyle', STYLE_SOLID)
IPC = _input('IPC', PRICE_CLOSE)  # Price constant in a zero buffer
IndicatorDigits_v = _input('IndicatorDigits_v', 3)  # Indicator display accuracy format
Direct = _input('Direct', True)  # Chart inversion
InitResult = False
prev_calculated_ = 0
ExtBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)

def Rates_Total(symbol, Rates_total):
    bars = Bars(symbol, PERIOD_CURRENT)
    error = GetLastError()
    ResetLastError()
    if error == 4401:
        return 0
    rates_total_ = MathMin(Rates_total, bars)
    Time = Arr(1, 0, dyn=False)
    if CopyTime(symbol, 0, bars - 1, 1, Time) <= 0:
        return 0
    if Time[0] != _s_Rates_Total_LastTime[0]:
        _s_Rates_Total_LastTime[0] = Time[0]
        return 0
    return rates_total_

def SynchroCheck(symbol, BarTime, Bar):
    TimeN = Arr(1, 0, dyn=False)
    if not BarTime:
        return (0 != 0)
    if CopyTime(symbol, 0, Bar, 1, TimeN) <= 0:
        return (0 != 0)
    elif TimeN[0] != BarTime:
        return (0 != 0)
    return True

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    else:
        return Close[bar]

def OnInit():
    global InitResult
    InitResult = True
    if not SymbolInfoInteger(CrossIndex, SYMBOL_SELECT):
        if GetLastError() == ERR_MARKET_UNKNOWN_SYMBOL:
            Print('OnInit', '(): ', CrossIndex, ' - There is no such a symbol!!!')
            InitResult = False
        elif not SymbolSelect(CrossIndex, True):
            Print('OnInit', '(): Failed to add a symbol for a currency ', CrossIndex, ' to the MarketWatch window!!!')
            InitResult = False
    SetIndexBuffer(1, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtCloseBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(5, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(0, ExtBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtBuffer, True)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorsBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, IndicatorDigits_v)
    short_name = Box("")
    StringConcatenate(short_name, 'CrossIndex ', CrossIndex, ',', StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1))
    IndicatorSetString(INDICATOR_SHORTNAME, short_name.v)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, BidColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, BidStyle)
    EventSetTimer(1)

def OnTimer():
    global prev_calculated_
    rates_total = Bars(Symbol(), PERIOD_CURRENT)
    if not InitResult:
        prev_calculated_ = 0
        return
    cross_rates_total = 0
    to_copy = 0
    limit = 0
    bar = 0
    cross_rates_total = Rates_Total(CrossIndex, rates_total)
    time0 = SeriesInfoInteger(Symbol(), PERIOD_CURRENT, SERIES_LASTBAR_DATE)
    if (not cross_rates_total) or (not SynchroCheck(CrossIndex, time0, 0)):
        if prev_calculated_ > rates_total or prev_calculated_ <= 0:
            prev_calculated_ = 0
            return
        limit = rates_total - prev_calculated_
        bar = limit - 1
        for bar in range(bar, 0 - 1, -1):
            ExtColorsBuffer[bar] = 1.0
            ExtBuffer[bar] = ExtBuffer[bar + 1]
            ExtOpenBuffer[bar] = ExtCloseBuffer[bar + 1]
            ExtCloseBuffer[bar] = ExtCloseBuffer[bar + 1]
            ExtHighBuffer[bar] = ExtCloseBuffer[bar + 1]
            ExtLowBuffer[bar] = ExtCloseBuffer[bar + 1]
        else:
            bar = _range_end(bar, 0 - 1, -1)
        return
    if prev_calculated_ > rates_total or prev_calculated_ <= 0:
        limit = cross_rates_total - 1
        draw_begin = rates_total - limit + 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, draw_begin)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, draw_begin)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, draw_begin)
        PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, draw_begin)
        PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, draw_begin)
        PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, draw_begin)
        bar = limit
        for bar in range(bar, rates_total):
            ExtOpenBuffer[bar] = 0.0
            ExtCloseBuffer[bar] = 0.0
            ExtHighBuffer[bar] = 0.0
            ExtLowBuffer[bar] = 0.0
        else:
            bar = _range_end(bar, rates_total, 1)
    else:
        limit = rates_total - prev_calculated_
        if limit > (cross_rates_total - 1):
            prev_calculated_ = 0
            return
    to_copy = limit + 1
    if CopyOpen(CrossIndex, PERIOD_CURRENT, 0, to_copy, ExtOpenBuffer) <= 0:
        prev_calculated_ = 0
        return
    if CopyHigh(CrossIndex, PERIOD_CURRENT, 0, to_copy, ExtHighBuffer) <= 0:
        prev_calculated_ = 0
        return
    if CopyLow(CrossIndex, PERIOD_CURRENT, 0, to_copy, ExtLowBuffer) <= 0:
        prev_calculated_ = 0
        return
    if CopyClose(CrossIndex, PERIOD_CURRENT, 0, to_copy, ExtCloseBuffer) <= 0:
        prev_calculated_ = 0
        return
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorsBuffer[bar] = 0.0
        else:
            ExtColorsBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtBuffer[bar] = PriceSeries(IPC, bar, ExtOpenBuffer, ExtLowBuffer, ExtHighBuffer, ExtCloseBuffer)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, ExtCloseBuffer[0])
    if prev_calculated_ == 0:
        ChartRedraw(0)
    prev_calculated_ = rates_total

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

# ---- global variables initialised from expressions
BidColor = _input('BidColor', _uint(Red))

# ---- static local variables
_s_Rates_Total_LastTime = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Crossindex(_MQL5Indicator):
    name = 'crossindex'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BidStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'ExchIndWeighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant in a zero buffer
        'IndicatorDigits_v': 3,  # Indicator display accuracy format
        'Direct': True,  # Chart inversion
    }

