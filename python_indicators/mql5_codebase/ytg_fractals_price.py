"""ytg_fractals_price — converted from MQL5: MQL5 Indicators/ytg_Fractals_Price/ytg_fractals_price.mq5

Copyright: Copyright © 2007, Yuriy Tokman; Link: yuriytokman@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Yuriy Tokman', 'link': 'yuriytokman@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Up Fractal', 2: 'Down Fractal'}, 'levels': [], 'description': [''], 'name': 'ytg_fractals_price', 'source': 'MQL5 Indicators/ytg_Fractals_Price/ytg_fractals_price.mq5', 'folder': 'ytg_Fractals_Price', 'inputs': [{'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'int', 'default': 119, 'label': 'upper fractal label', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'int', 'default': 119, 'label': 'lower fractal label', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'nSize', 'py': 'nSize', 'param': 'nSize', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 8421376, 'label': '', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UpLable = _input('UpLable', 119)  # upper fractal label
DnLable = _input('DnLable', 119)  # lower fractal label
ShowPrice = _input('ShowPrice', True)
nSize = _input('nSize', 1)
UpColor = _input('UpColor', clrTeal)
DnColor = _input('DnColor', clrRed)
ExtDownFractalsBuffer = Arr(0, 0.0)
ExtUpFractalsBuffer = Arr(0, 0.0)
min_rates_total = 0
UpLable_ = ""
DnLable_ = ""

def CreateArrowRightPrice(chart_id, name, nwin, Time, Price, Color, Size):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, Time, Price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, Size)

def Deinit():
    total = 0
    name = ""
    sirname = ""
    total = ObjectsTotal(0, 0, -1) - 1
    for numb in range(total, 0 - 1, -1):
        name = ObjectName(0, numb, 0, -1)
        sirname = StringSubstr(name, 0, StringLen(UpLable_))
        if sirname == UpLable_:
            ObjectDelete(0, name)
    total = ObjectsTotal(0, 0, -1) - 1
    for numb in range(total, 0 - 1, -1):
        name = ObjectName(0, numb, 0, -1)
        sirname = StringSubstr(name, 0, StringLen(DnLable_))
        if sirname == DnLable_:
            ObjectDelete(0, name)
    ChartRedraw(0)

def OnInit():
    global DnLable_, UpLable_, min_rates_total
    min_rates_total = 5
    UpLable_ = 'Up_Fractals_Price'
    DnLable_ = 'Dn_Fractals_Price'
    SetIndexBuffer(0, ExtDownFractalsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, UpLable)
    ArraySetAsSeries(ExtDownFractalsBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, ExtUpFractalsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, DnLable)
    ArraySetAsSeries(ExtUpFractalsBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Fractals_Price'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnDeinit(reason):
    Deinit()

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bFound = False
    dCurrent = 0.0
    stime = ""
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 3
    else:
        if rates_total == prev_calculated:
            return rates_total
        limit = rates_total - prev_calculated + 2
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Time, True)
    for bar in range(2, limit + 1):
        ExtUpFractalsBuffer[bar] = 0.0
        ExtDownFractalsBuffer[bar] = 0.0
        bFound = False
        dCurrent = High[bar]
        if ((dCurrent > High[bar + 1] and dCurrent > High[bar + 2]) and dCurrent > High[bar - 1]) and dCurrent > High[bar - 2]:
            bFound = True
            ExtUpFractalsBuffer[bar] = dCurrent
            if ShowPrice:
                stime = TimeToString(Time[bar], TIME_DATE | TIME_MINUTES)
                CreateArrowRightPrice(0, DnLable_ + stime, 0, Time[bar], High[bar], DnColor, nSize)
        if (not bFound) and (rates_total - bar - 1) >= 3:
            if (((dCurrent == High[bar + 1] and dCurrent > High[bar + 2]) and dCurrent > High[bar + 3]) and dCurrent > High[bar - 1]) and dCurrent > High[bar - 2]:
                bFound = True
                ExtUpFractalsBuffer[bar] = dCurrent
        if (not bFound) and (rates_total - bar - 1) >= 4:
            if ((((dCurrent >= High[bar + 1] and dCurrent == High[bar + 2]) and dCurrent > High[bar + 3]) and dCurrent > High[bar + 4]) and dCurrent > High[bar - 1]) and dCurrent > High[bar - 2]:
                bFound = True
                ExtUpFractalsBuffer[bar] = dCurrent
        if (not bFound) and (rates_total - bar - 1) >= 5:
            if (((((dCurrent >= High[bar + 1] and dCurrent == High[bar + 2]) and dCurrent == High[bar + 3]) and dCurrent > High[bar + 4]) and dCurrent > High[bar + 5]) and dCurrent > High[bar - 1]) and dCurrent > High[bar - 2]:
                bFound = True
                ExtUpFractalsBuffer[bar] = dCurrent
        if (not bFound) and (rates_total - bar - 1) >= 6:
            if ((((((dCurrent >= High[bar + 1] and dCurrent == High[bar + 2]) and dCurrent >= High[bar + 3]) and dCurrent == High[bar + 4]) and dCurrent > High[bar + 5]) and dCurrent > High[bar + 6]) and dCurrent > High[bar - 1]) and dCurrent > High[bar - 2]:
                bFound = True
                ExtUpFractalsBuffer[bar] = dCurrent
        bFound = False
        dCurrent = Low[bar]
        if ((dCurrent < Low[bar + 1] and dCurrent < Low[bar + 2]) and dCurrent < Low[bar - 1]) and dCurrent < Low[bar - 2]:
            bFound = True
            ExtDownFractalsBuffer[bar] = dCurrent
            if ShowPrice:
                stime = TimeToString(Time[bar], TIME_DATE | TIME_MINUTES)
                CreateArrowRightPrice(0, UpLable_ + stime, 0, Time[bar], Low[bar], UpColor, nSize)
        if (not bFound) and (rates_total - bar - 1) >= 3:
            if (((dCurrent == Low[bar + 1] and dCurrent < Low[bar + 2]) and dCurrent < Low[bar + 3]) and dCurrent < Low[bar - 1]) and dCurrent < Low[bar - 2]:
                bFound = True
                ExtDownFractalsBuffer[bar] = dCurrent
        if (not bFound) and (rates_total - bar - 1) >= 4:
            if ((((dCurrent <= Low[bar + 1] and dCurrent == Low[bar + 2]) and dCurrent < Low[bar + 3]) and dCurrent < Low[bar + 4]) and dCurrent < Low[bar - 1]) and dCurrent < Low[bar - 2]:
                bFound = True
                ExtDownFractalsBuffer[bar] = dCurrent
        if (not bFound) and (rates_total - bar - 1) >= 5:
            if (((((dCurrent <= Low[bar + 1] and dCurrent == Low[bar + 2]) and dCurrent == Low[bar + 3]) and dCurrent < Low[bar + 4]) and dCurrent < Low[bar + 5]) and dCurrent < Low[bar - 1]) and dCurrent < Low[bar - 2]:
                bFound = True
                ExtDownFractalsBuffer[bar] = dCurrent
        if (not bFound) and (rates_total - bar - 1) >= 6:
            if ((((((dCurrent <= Low[bar + 1] and dCurrent == Low[bar + 2]) and dCurrent <= Low[bar + 3]) and dCurrent == Low[bar + 4]) and dCurrent < Low[bar + 5]) and dCurrent < Low[bar + 6]) and dCurrent < Low[bar - 1]) and dCurrent < Low[bar - 2]:
                bFound = True
                ExtDownFractalsBuffer[bar] = dCurrent
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class YtgFractalsPrice(_MQL5Indicator):
    name = 'ytg_fractals_price'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'UpLable': 119,  # upper fractal label
        'DnLable': 119,  # lower fractal label
        'ShowPrice': True,
        'nSize': 1,
    }

