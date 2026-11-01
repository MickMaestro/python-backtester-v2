"""Boa_ZigZag_Price — converted from MQL5: MQL5 Indicators/Boa_ZigZag_Price/Boa_ZigZag_Price.mq5

Казахский удав
Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: mandorr@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'mandorr@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 9}, 'colors': {1: [13850042, 3329330]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'Boa_ZigZag'}, 'levels': [], 'description': ['Казахский удав'], 'name': 'Boa_ZigZag_Price', 'source': 'MQL5 Indicators/Boa_ZigZag_Price/Boa_ZigZag_Price.mq5', 'folder': 'Boa_ZigZag_Price', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'Boa_ZigZag_Price', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'nSize', 'py': 'nSize', 'param': 'nSize', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 8421376, 'label': '', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SirName = _input('SirName', 'Boa_ZigZag_Price')  # Первая часть имени графических объектов
Length = _input('Length', 6)
ShowPrice = _input('ShowPrice', True)
nSize = _input('nSize', 1)
UpColor = _input('UpColor', clrTeal)
DnColor = _input('DnColor', clrRed)
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
UpLable_ = ""
DnLable_ = ""

def OnInit():
    global DnLable_, UpLable_, min_rates_total
    min_rates_total = _int(Length) + 1
    UpLable_ = SirName + '_Up_'
    DnLable_ = SirName + '_Dn_'
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer, True)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'Boa_ZigZag(Length=', Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnDeinit(reason):
    ObjectsDeleteAll(0, SirName, 0, OBJ_ARROW_RIGHT_PRICE)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    climit = 0
    bar = 0
    HH = 0.0
    LL = 0.0
    BH = 0.0
    BL = 0.0
    zu = 0
    zd = 0
    Swing = 0
    Swing_n = 0
    limit = rates_total - min_rates_total
    climit = limit
    Swing = 0
    Swing_n = 0
    zu = limit
    zd = limit
    BH = high[limit]
    BL = low[limit]
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = 0.0
        HH = high[ArrayMaximum(high, bar + 1, Length)]
        LL = low[ArrayMinimum(low, bar + 1, Length)]
        if low[bar] < LL and high[bar] > HH:
            Swing = 2
            if Swing_n == 1:
                zu = bar + 1
            if Swing_n == -1:
                zd = bar + 1
        else:
            if low[bar] < LL:
                Swing = -1
            if high[bar] > HH:
                Swing = 1
        if Swing != Swing_n and Swing_n != 0:
            if Swing == 2:
                Swing = -Swing_n
                BH = high[bar]
                BL = low[bar]
            if Swing == 1:
                IndBuffer[zd] = BL
                stime = TimeToString(time[zd], TIME_DATE | TIME_MINUTES)
                CreateArrowRightPrice(0, DnLable_ + stime, 0, time[zd], BL, DnColor, nSize)
            if Swing == -1:
                IndBuffer[zu] = BH
                stime = TimeToString(time[zu], TIME_DATE | TIME_MINUTES)
                CreateArrowRightPrice(0, UpLable_ + stime, 0, time[zu], BH, UpColor, nSize)
            BH = high[bar]
            BL = low[bar]
        if Swing == 1:
            if high[bar] >= BH:
                BH = high[bar]
                zu = bar
        if Swing == -1:
            if low[bar] <= BL:
                BL = low[bar]
                zd = bar
        Swing_n = Swing
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = climit
    for bar in range(bar, 0 - 1, -1):
        if not IndBuffer[bar]:
            ColorIndBuffer[bar] = ColorIndBuffer[bar + 1]
        if IndBuffer[bar] and IndBuffer[bar] > high[bar + 1]:
            ColorIndBuffer[bar] = 1.0
        if IndBuffer[bar] and IndBuffer[bar] < low[bar + 1]:
            ColorIndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    ChartRedraw(0)
    return rates_total

def CreateArrowRightPrice(chart_id, name, nwin, Time, Price, Color, Size):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, Time, Price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, Size)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BoaZigZagPrice(_MQL5Indicator):
    name = 'Boa_ZigZag_Price'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 6,
        'ShowPrice': True,
        'nSize': 1,
    }

