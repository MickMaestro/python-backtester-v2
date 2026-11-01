"""Intraday Currencies Performance — converted from MQL5: MQL5 Indicators/Intraday Currencies Performance/Intraday Currencies Performance.mq5

Copyright: Studio Sofrollo; Link: studiosofrollo@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Studio Sofrollo', 'link': 'studiosofrollo@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 22, 'indicator_plots': 8}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Intraday Currencies Performance', 'source': 'MQL5 Indicators/Intraday Currencies Performance/Intraday Currencies Performance.mq5', 'folder': 'Intraday Currencies Performance', 'inputs': [{'mql': 'grandezzacarattere', 'py': 'grandezzacarattere', 'param': 'grandezzacarattere', 'type': 'int', 'default': 10, 'label': 'Font size', 'sinput': False}, {'mql': 'Color_USD', 'py': 'Color_USD', 'param': None, 'type': 'color', 'default': 0, 'label': 'USD line color', 'sinput': False}, {'mql': 'Color_EUR', 'py': 'Color_EUR', 'param': None, 'type': 'color', 'default': 0, 'label': 'EUR line color', 'sinput': False}, {'mql': 'Color_GBP', 'py': 'Color_GBP', 'param': None, 'type': 'color', 'default': 0, 'label': 'GBP line color', 'sinput': False}, {'mql': 'Color_CHF', 'py': 'Color_CHF', 'param': None, 'type': 'color', 'default': 0, 'label': 'CHF line color', 'sinput': False}, {'mql': 'Color_JPY', 'py': 'Color_JPY', 'param': None, 'type': 'color', 'default': 0, 'label': 'JPY line color', 'sinput': False}, {'mql': 'Color_AUD', 'py': 'Color_AUD', 'param': None, 'type': 'color', 'default': 0, 'label': 'AUD line color', 'sinput': False}, {'mql': 'Color_CAD', 'py': 'Color_CAD', 'param': None, 'type': 'color', 'default': 0, 'label': 'CAD line color', 'sinput': False}, {'mql': 'Color_NZD', 'py': 'Color_NZD', 'param': None, 'type': 'color', 'default': 0, 'label': 'NZD line color', 'sinput': False}, {'mql': 'wid_main', 'py': 'wid_main', 'param': 'wid_main', 'type': 'int', 'default': 1, 'label': 'Line width', 'sinput': False}, {'mql': 'style_slave', 'py': 'style_slave', 'param': 'style_slave', 'type': 'int', 'default': 0, 'label': 'Line style', 'sinput': False}, {'mql': 'tm', 'py': 'tm', 'param': None, 'type': 'string', 'default': '00:00', 'label': 'Time in the format hours:minutes', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Aqua = 0xFFFF00  # MQL4 colour name
Blue = 0xFF0000  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name
Orange = 0x00A5FF  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# ---- inputs and global variables
grandezzacarattere = _input('grandezzacarattere', 10)  # Font size
wid_main = _input('wid_main', 1)  # Line width
style_slave = _input('style_slave', STYLE_SOLID)  # Line style
y_pos = 0  # Y coordinate variable for the informatory objects
pair1 = 'EURUSD'  # Cross 1
pair2 = 'GBPUSD'  # Cross 2
pair3 = 'AUDUSD'  # Cross 3
pair4 = 'NZDUSD'  # Cross 4
pair5 = 'USDJPY'  # Cross 5
pair6 = 'USDCAD'  # Cross 6
pair7 = 'USDCHF'  # Cross 7
tm = _input('tm', '00:00')  # Time in the format hours:minutes
Shift = 0  # horizontal shift of the indicator in bars
USD = Arr(0, 0.0)
EUR = Arr(0, 0.0)
GBP = Arr(0, 0.0)
AUD = Arr(0, 0.0)
CAD = Arr(0, 0.0)
JPY = Arr(0, 0.0)
NZD = Arr(0, 0.0)
CHF = Arr(0, 0.0)
OscBuffer1 = 0.0
OscBuffer2 = 0.0
OscBuffer3 = 0.0
OscBuffer4 = 0.0
OscBuffer5 = 0.0
OscBuffer6 = 0.0
OscBuffer7 = 0.0
open1 = Arr(0, 0.0)
close1 = Arr(0, 0.0)
open2 = Arr(0, 0.0)
close2 = Arr(0, 0.0)
open3 = Arr(0, 0.0)
close3 = Arr(0, 0.0)
open4 = Arr(0, 0.0)
close4 = Arr(0, 0.0)
open5 = Arr(0, 0.0)
close5 = Arr(0, 0.0)
open6 = Arr(0, 0.0)
close6 = Arr(0, 0.0)
open7 = Arr(0, 0.0)
close7 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, USD, INDICATOR_DATA)
    SetIndexBuffer(1, EUR, INDICATOR_DATA)
    SetIndexBuffer(2, GBP, INDICATOR_DATA)
    SetIndexBuffer(3, AUD, INDICATOR_DATA)
    SetIndexBuffer(4, CAD, INDICATOR_DATA)
    SetIndexBuffer(5, JPY, INDICATOR_DATA)
    SetIndexBuffer(6, NZD, INDICATOR_DATA)
    SetIndexBuffer(7, CHF, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(6, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(7, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(8, open1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, close1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, open2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, close2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, open3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, close3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, open4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, close4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, open5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(17, close5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(18, open6, INDICATOR_CALCULATIONS)
    SetIndexBuffer(19, close6, INDICATOR_CALCULATIONS)
    SetIndexBuffer(20, open7, INDICATOR_CALCULATIONS)
    SetIndexBuffer(21, close7, INDICATOR_CALCULATIONS)
    shortname = Box("")
    StringConcatenate(shortname, 'Intr.Curr.%' + ' (' + tm + ')', '')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    PlotIndexSetString(0, PLOT_LABEL, '% USD')
    PlotIndexSetString(1, PLOT_LABEL, '% EUR')
    PlotIndexSetString(2, PLOT_LABEL, '% GBP')
    PlotIndexSetString(3, PLOT_LABEL, '% AUD')
    PlotIndexSetString(4, PLOT_LABEL, '% CAD')
    PlotIndexSetString(5, PLOT_LABEL, '% JPY')
    PlotIndexSetString(6, PLOT_LABEL, '% NZD')
    PlotIndexSetString(7, PLOT_LABEL, '% CHF')
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, Color_USD)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, Color_EUR)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, Color_GBP)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, Color_AUD)
    PlotIndexSetInteger(4, PLOT_LINE_COLOR, Color_CAD)
    PlotIndexSetInteger(5, PLOT_LINE_COLOR, Color_JPY)
    PlotIndexSetInteger(6, PLOT_LINE_COLOR, Color_NZD)
    PlotIndexSetInteger(7, PLOT_LINE_COLOR, Color_CHF)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(4, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(5, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(6, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(7, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, wid_main)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, wid_main)
    PlotIndexSetInteger(2, PLOT_LINE_WIDTH, wid_main)
    PlotIndexSetInteger(3, PLOT_LINE_WIDTH, wid_main)
    PlotIndexSetInteger(4, PLOT_LINE_WIDTH, wid_main)
    PlotIndexSetInteger(5, PLOT_LINE_WIDTH, wid_main)
    PlotIndexSetInteger(6, PLOT_LINE_WIDTH, wid_main)
    PlotIndexSetInteger(7, PLOT_LINE_WIDTH, wid_main)
    perfscrivi(' USD', Color_USD)
    perfscrivi(' EUR', Color_EUR)
    perfscrivi(' GBP', Color_GBP)
    perfscrivi(' AUD', Color_AUD)
    perfscrivi(' CAD', Color_CAD)
    perfscrivi(' JPY', Color_JPY)
    perfscrivi(' NZD', Color_NZD)
    perfscrivi(' CHF', Color_CHF)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global OscBuffer1, OscBuffer2, OscBuffer3, OscBuffer4, OscBuffer5, OscBuffer6, OscBuffer7, _s_OnCalculate_Open1, _s_OnCalculate_Open2, _s_OnCalculate_Open3, _s_OnCalculate_Open4, _s_OnCalculate_Open5, _s_OnCalculate_Open6, _s_OnCalculate_Open7
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    CopyOpen(pair1, PERIOD_CURRENT, 0, rates_total, open1)
    CopyClose(pair1, PERIOD_CURRENT, 0, rates_total, close1)
    CopyOpen(pair2, PERIOD_CURRENT, 0, rates_total, open2)
    CopyClose(pair2, PERIOD_CURRENT, 0, rates_total, close2)
    CopyOpen(pair3, PERIOD_CURRENT, 0, rates_total, open3)
    CopyClose(pair3, PERIOD_CURRENT, 0, rates_total, close3)
    CopyOpen(pair4, PERIOD_CURRENT, 0, rates_total, open4)
    CopyClose(pair4, PERIOD_CURRENT, 0, rates_total, close4)
    CopyOpen(pair5, PERIOD_CURRENT, 0, rates_total, open5)
    CopyClose(pair5, PERIOD_CURRENT, 0, rates_total, close5)
    CopyOpen(pair6, PERIOD_CURRENT, 0, rates_total, open6)
    CopyClose(pair6, PERIOD_CURRENT, 0, rates_total, close6)
    CopyOpen(pair7, PERIOD_CURRENT, 0, rates_total, open7)
    CopyClose(pair7, PERIOD_CURRENT, 0, rates_total, close7)
    bar = first
    for bar in range(bar, rates_total):
        if TimeToString(time[bar], TIME_MINUTES) == tm:
            _s_OnCalculate_Open1 = open1[bar]
            _s_OnCalculate_Open2 = open2[bar]
            _s_OnCalculate_Open3 = open3[bar]
            _s_OnCalculate_Open4 = open4[bar]
            _s_OnCalculate_Open5 = open5[bar]
            _s_OnCalculate_Open6 = open6[bar]
            _s_OnCalculate_Open7 = open7[bar]
        if _s_OnCalculate_Open1 == 0:
            OscBuffer1 = 1.0
        else:
            OscBuffer1 = _fdiv(close1[bar] - _s_OnCalculate_Open1, _s_OnCalculate_Open1) * 100
        if _s_OnCalculate_Open2 == 0:
            OscBuffer2 = 1.0
        else:
            OscBuffer2 = _fdiv(close2[bar] - _s_OnCalculate_Open2, _s_OnCalculate_Open2) * 100
        if _s_OnCalculate_Open3 == 0:
            OscBuffer3 = 1.0
        else:
            OscBuffer3 = _fdiv(close3[bar] - _s_OnCalculate_Open3, _s_OnCalculate_Open3) * 100
        if _s_OnCalculate_Open4 == 0:
            OscBuffer4 = 1.0
        else:
            OscBuffer4 = _fdiv(close4[bar] - _s_OnCalculate_Open4, _s_OnCalculate_Open4) * 100
        if _s_OnCalculate_Open5 == 0:
            OscBuffer5 = 1.0
        else:
            OscBuffer5 = _fdiv(close5[bar] - _s_OnCalculate_Open5, _s_OnCalculate_Open5) * 100
        if _s_OnCalculate_Open6 == 0:
            OscBuffer6 = 1.0
        else:
            OscBuffer6 = _fdiv(close6[bar] - _s_OnCalculate_Open6, _s_OnCalculate_Open6) * 100
        if _s_OnCalculate_Open7 == 0:
            OscBuffer7 = 1.0
        else:
            OscBuffer7 = _fdiv(close7[bar] - _s_OnCalculate_Open7, _s_OnCalculate_Open7) * 100
        USD[bar] = (OscBuffer5 + OscBuffer6 + OscBuffer7 - OscBuffer1 - OscBuffer2 - OscBuffer3 - OscBuffer4) / 8
        EUR[bar] = ((7 * OscBuffer1) - OscBuffer2 - OscBuffer3 - OscBuffer4 + OscBuffer5 + OscBuffer6 + OscBuffer7) / 8
        GBP[bar] = ((7 * OscBuffer2) + OscBuffer6 + OscBuffer7 + OscBuffer5 - OscBuffer1 - OscBuffer3 - OscBuffer4) / 8
        AUD[bar] = ((7 * OscBuffer3) - OscBuffer2 - OscBuffer1 - OscBuffer4 + OscBuffer5 + OscBuffer6 + OscBuffer7) / 8
        CAD[bar] = ((-7 * OscBuffer6) + OscBuffer7 + OscBuffer5 - OscBuffer1 - OscBuffer2 - OscBuffer3 - OscBuffer4) / 8
        JPY[bar] = ((-7 * OscBuffer5) - OscBuffer1 - OscBuffer2 - OscBuffer3 - OscBuffer4 + OscBuffer6 + OscBuffer7) / 8
        NZD[bar] = ((7 * OscBuffer4) - OscBuffer1 - OscBuffer2 - OscBuffer3 + OscBuffer5 + OscBuffer6 + OscBuffer7) / 8
        CHF[bar] = ((-7 * OscBuffer7) + OscBuffer6 + OscBuffer5 - OscBuffer1 - OscBuffer2 - OscBuffer3 - OscBuffer4) / 8
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def perfscrivi(name, _color):
    global y_pos
    ObjectCreate(0, name, OBJ_LABEL, ChartWindowFind(), 0, 0)
    ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, 0)
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y_pos)
    ObjectSetString(0, name, OBJPROP_TEXT, name)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, grandezzacarattere)
    ObjectSetInteger(0, name, OBJPROP_COLOR, _color)
    y_pos += _int(MathRound(grandezzacarattere * 1.5))
    return 0

# ---- global variables initialised from expressions
Color_USD = _input('Color_USD', _uint(Lime))  # USD line color
Color_EUR = _input('Color_EUR', _uint(Blue))  # EUR line color
Color_GBP = _input('Color_GBP', _uint(Red))  # GBP line color
Color_CHF = _input('Color_CHF', _uint(Magenta))  # CHF line color
Color_JPY = _input('Color_JPY', _uint(Yellow))  # JPY line color
Color_AUD = _input('Color_AUD', _uint(Aqua))  # AUD line color
Color_CAD = _input('Color_CAD', _uint(White))  # CAD line color
Color_NZD = _input('Color_NZD', _uint(Orange))  # NZD line color

# ---- static local variables
_s_OnCalculate_Open1 = 0.0
_s_OnCalculate_Open2 = 0.0
_s_OnCalculate_Open3 = 0.0
_s_OnCalculate_Open4 = 0.0
_s_OnCalculate_Open5 = 0.0
_s_OnCalculate_Open6 = 0.0
_s_OnCalculate_Open7 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IntradayCurrenciesPerformance(_MQL5Indicator):
    name = 'Intraday Currencies Performance'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'grandezzacarattere': 10,  # Font size
        'wid_main': 1,  # Line width
        'style_slave': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Line style
    }

