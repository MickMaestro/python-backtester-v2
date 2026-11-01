"""ZigZag_NK_Color_Price — converted from MQL5: MQL5 Indicators/ZigZag_NK_Color_Price/ZigZag_NK_Color_Price.mq5

ZigZag
Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 13}, 'colors': {1: [16711935, 14822282]}, 'widths': {1: 2}, 'styles': {1: 1}, 'labels': {1: 'ZigZag'}, 'levels': [], 'description': ['ZigZag'], 'name': 'ZigZag_NK_Color_Price', 'source': 'MQL5 Indicators/ZigZag_NK_Color_Price/ZigZag_NK_Color_Price.mq5', 'folder': 'ZigZag_NK_Color_Price', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'ZigZag_NK_Color_Price', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'nSize', 'py': 'nSize', 'param': 'nSize', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 8421376, 'label': '', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SirName = _input('SirName', 'ZigZag_NK_Color_Price')  # Первая часть имени графических объектов
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
ShowPrice = _input('ShowPrice', True)
nSize = _input('nSize', 1)
UpColor = _input('UpColor', clrTeal)
DnColor = _input('DnColor', clrRed)
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
LASTlowpos = 0
LASThighpos = 0
LASTColor = 0
LASTlow0 = 0.0
LASTlow1 = 0.0
LASThigh0 = 0.0
LASThigh1 = 0.0
min_rates_total = 0
UpLable_ = ""
DnLable_ = ""

def OnInit():
    global DnLable_, UpLable_, min_rates_total
    min_rates_total = ExtDepth + ExtBackstep
    UpLable_ = SirName + '_Up_'
    DnLable_ = SirName + '_Dn_'
    SetIndexBuffer(0, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighestBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetString(0, PLOT_LABEL, 'ZigZag_NK_Color')
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    ArraySetAsSeries(ColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'ZigZag_NK_Color(ExtDepth=', ExtDepth, 'ExtDeviation = ', ExtDeviation, 'ExtBackstep = ', ExtBackstep, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnDeinit(reason):
    ObjectsDeleteAll(0, SirName, 0, OBJ_ARROW_RIGHT_PRICE)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LASThigh0, LASThigh1, LASThighpos, LASTlow0, LASTlow1, LASTlowpos
    if rates_total < min_rates_total:
        return 0
    limit = 0
    climit = 0
    bar = 0
    back = 0
    lasthighpos = 0
    lastlowpos = 0
    curlow = 0.0
    curhigh = 0.0
    lasthigh0 = 0.0
    lastlow0 = 0.0
    lasthigh1 = 0.0
    lastlow1 = 0.0
    val = 0.0
    res = 0.0
    Max = False
    Min = False
    stime = ""
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        climit = limit
        lastlow1 = -1.0
        lasthigh1 = -1.0
        lastlowpos = -1
        lasthighpos = -1
    else:
        limit = rates_total - prev_calculated
        climit = limit + min_rates_total
        lastlow0 = LASTlow0
        lasthigh0 = LASThigh0
        lastlow1 = LASTlow1
        lasthigh1 = LASThigh1
        lastlowpos = LASTlowpos + limit
        lasthighpos = LASThighpos + limit
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and (not bar):
            LASTlow0 = lastlow0
            LASThigh0 = lasthigh0
        val = low[ArrayMinimum(low, bar, ExtDepth)]
        if val == lastlow0:
            val = 0.0
        else:
            lastlow0 = val
            if (low[bar] - val) > (ExtDeviation * Point()):
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = LowestBuffer[bar + back]
                    if res and res > val:
                        LowestBuffer[bar + back] = 0.0
                        stime = TimeToString(time[bar + back], TIME_DATE | TIME_MINUTES)
                        ObjectDelete(0, DnLable_ + stime)
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        LowestBuffer[bar] = val
        if val:
            stime = TimeToString(time[bar], TIME_DATE | TIME_MINUTES)
            CreateArrowRightPrice(0, DnLable_ + stime, 0, time[bar], val, DnColor, nSize)
        val = high[ArrayMaximum(high, bar, ExtDepth)]
        if val == lasthigh0:
            val = 0.0
        else:
            lasthigh0 = val
            if (val - high[bar]) > (ExtDeviation * Point()):
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = HighestBuffer[bar + back]
                    if res and res < val:
                        HighestBuffer[bar + back] = 0.0
                        stime = TimeToString(time[bar + back], TIME_DATE | TIME_MINUTES)
                        ObjectDelete(0, UpLable_ + stime)
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        HighestBuffer[bar] = val
        if val:
            stime = TimeToString(time[bar], TIME_DATE | TIME_MINUTES)
            CreateArrowRightPrice(0, UpLable_ + stime, 0, time[bar], val, UpColor, nSize)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and (not bar):
            LASTlow1 = lastlow1
            LASThigh1 = lasthigh1
            LASTlowpos = lastlowpos
            LASThighpos = lasthighpos
        curlow = LowestBuffer[bar]
        curhigh = HighestBuffer[bar]
        if (not curlow) and (not curhigh):
            continue
        if curhigh:
            if lasthigh1 > 0:
                if lasthigh1 < curhigh:
                    HighestBuffer[lasthighpos] = 0.0
                    stime = TimeToString(time[lasthighpos], TIME_DATE | TIME_MINUTES)
                    ObjectDelete(0, UpLable_ + stime)
                else:
                    HighestBuffer[bar] = 0.0
                    stime = TimeToString(time[bar], TIME_DATE | TIME_MINUTES)
                    ObjectDelete(0, UpLable_ + stime)
            if lasthigh1 < curhigh or lasthigh1 < 0:
                lasthigh1 = curhigh
                lasthighpos = bar
            lastlow1 = -1.0
        if curlow:
            if lastlow1 > 0:
                if lastlow1 > curlow:
                    LowestBuffer[lastlowpos] = 0.0
                    stime = TimeToString(time[lastlowpos], TIME_DATE | TIME_MINUTES)
                    ObjectDelete(0, DnLable_ + stime)
                else:
                    LowestBuffer[bar] = 0.0
                    stime = TimeToString(time[bar], TIME_DATE | TIME_MINUTES)
                    ObjectDelete(0, DnLable_ + stime)
            if curlow < lastlow1 or lastlow1 < 0:
                lastlow1 = curlow
                lastlowpos = bar
            lasthigh1 = -1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = climit
    for bar in range(bar, 0 - 1, -1):
        Max = (HighestBuffer[bar] != 0)
        Min = (LowestBuffer[bar] != 0)
        if (not Max) and (not Min):
            ColorBuffer[bar] = ColorBuffer[bar + 1]
        if Max and Min:
            if ColorBuffer[bar + 1] == 0:
                ColorBuffer[bar] = 1.0
            else:
                ColorBuffer[bar] = 0.0
        if Max and (not Min):
            ColorBuffer[bar] = 1.0
        if (not Max) and Min:
            ColorBuffer[bar] = 0.0
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


class ZigZagNKColorPrice(_MQL5Indicator):
    name = 'ZigZag_NK_Color_Price'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
        'ShowPrice': True,
        'nSize': 1,
    }

