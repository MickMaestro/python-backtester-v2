"""powertrend — converted from MQL5: MQL5 Indicators/PowerTrend/powertrend.mq5

Copyright: Copyright © 2007, SVS.; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, SVS.', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 3, 2: 3, 3: 3, 4: 3}, 'colors': {1: [7451452], 2: [16711680], 3: [255], 4: [0]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'PowerTrend', 2: 'PowerTrend', 3: 'PowerTrend', 4: 'PowerTrend'}, 'levels': [0.0], 'description': [], 'name': 'powertrend', 'source': 'MQL5 Indicators/PowerTrend/powertrend.mq5', 'folder': 'PowerTrend', 'inputs': [{'mql': 'Power_Period', 'py': 'Power_Period', 'param': 'Power_Period', 'type': 'int', 'default': 6, 'label': 'Indicator period', 'sinput': False}, {'mql': 'Power_Method', 'py': 'Power_Method', 'param': 'Power_Method', 'type': 'int', 'default': 3, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'Power_Price', 'py': 'Power_Price', 'param': 'Power_Price', 'type': 'int', 'default': 1, 'label': 'Indicators price', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum BandsMode
BASE_LINE_ = 0
UPPER_BAND_ = 1
LOWER_BAND_ = 2
_enum('BandsMode', {0: 'BASE_LINE_', 1: 'UPPER_BAND_', 2: 'LOWER_BAND_'})

# ---- inputs and global variables
Power_Period = _input('Power_Period', 6)  # Indicator period
Power_Method = _input('Power_Method', MODE_LWMA)  # Smoothing method
Power_Price = _input('Power_Price', PRICE_CLOSE)  # Indicators price
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
ExtMapBuffer3 = Arr(0, 0.0)
ExtMapBuffer4 = Arr(0, 0.0)
p1 = 0
p2 = 0
min_rates_total = 0
MA0_Handle = Arr(0, 0)

def OnInit():
    global min_rates_total, p1, p2
    min_rates_total = (Power_Period * 2) + 1
    p2 = Power_Period * 2
    p1 = Power_Period * 1
    ArrayResize(MA0_Handle, p2)
    for count in range(0, p2):
        MA0_Handle[count] = iMA(None, 0, count + 1, 0, Power_Method, Power_Price)
        if MA0_Handle[count] == INVALID_HANDLE:
            Print(' Failed to get the handle of the iMA0 indicator')
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtMapBuffer1, True)
    SetIndexBuffer(1, ExtMapBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtMapBuffer2, True)
    SetIndexBuffer(2, ExtMapBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtMapBuffer3, True)
    SetIndexBuffer(3, ExtMapBuffer4, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtMapBuffer4, True)
    shortname = Box("")
    StringConcatenate(shortname, 'PowerTrend( ', Power_Period, ', ', EnumToString(Power_Method, 'ENUM_MA_METHOD'), ', ', EnumToString(Power_Price, 'ENUM_APPLIED_PRICE'), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < min_rates_total:
        return 0
    for count in range(0, p2):
        if BarsCalculated(MA0_Handle[count]) < rates_total:
            return 0
    limit = 0
    bar = 0
    vt0 = 0.0
    vt1 = 0.0
    vts = 0.0
    MA = Arr(0, 0.0)
    vj1 = 0.0
    vk1 = 0.0
    vd1 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - begin - min_rates_total
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + begin)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total + begin)
        PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(price, True)
    ArraySetAsSeries(MA, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        vts = 0.0
        for c in range(1, p2 + 1):
            if CopyBuffer(MA0_Handle[c - 1], 0, bar, 1, MA) <= 0:
                return 0
            vts += MA[0]
            if c == p1:
                vt0 = _fdiv(vts, p1) - MA[0]
            if c == p2:
                vt1 = _fdiv(vts, p2) - MA[0]
        vk1 = (vt0 + vt1) / 2
        vd1 = vt0 / 2
        vj1 = vt1 - vd1
        ExtMapBuffer1[bar] = vt1
        ExtMapBuffer2[bar] = vk1
        ExtMapBuffer3[bar] = vd1
        ExtMapBuffer4[bar] = vj1
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Powertrend(_MQL5Indicator):
    name = 'powertrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Power_Period': 6,  # Indicator period
        'Power_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Smoothing method
        'Power_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Indicators price
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

