"""itrend — converted from MQL5: MQL5 Indicators/iTrend/itrend.mq5

Copyright: Copyright © 2004, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [6908265, 65280, 7451452, 255, 2763429], 2: [16711680]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'iTrend Histogram', 2: 'iTrend TrendLine'}, 'levels': [], 'description': [], 'name': 'itrend', 'source': 'MQL5 Indicators/iTrend/itrend.mq5', 'folder': 'iTrend', 'inputs': [{'mql': 'Power_Period', 'py': 'Power_Period', 'param': 'Power_Period', 'type': 'int', 'default': 13, 'label': 'Indicator period', 'sinput': False}, {'mql': 'Power_Price', 'py': 'Power_Price', 'param': 'Power_Price', 'type': 'int', 'default': 1, 'label': 'Indicators price', 'sinput': False}, {'mql': 'Price_Type', 'py': 'Price_Type', 'param': 'Price_Type', 'type': 'int', 'default': 1, 'label': 'Calculated price', 'sinput': False}, {'mql': 'Bands_Mode', 'py': 'Bands_Mode', 'param': 'Bands_Mode', 'type': 'int', 'default': 0, 'label': 'Bollinger type', 'sinput': False}, {'mql': 'Bands_Period', 'py': 'Bands_Period', 'param': 'Bands_Period', 'type': 'int', 'default': 20, 'label': 'Bollinger period', 'sinput': False}, {'mql': 'Bands_Deviation', 'py': 'Bands_Deviation', 'param': 'Bands_Deviation', 'type': 'int', 'default': 2, 'label': 'Number of standard Bollinger deviations', 'sinput': False}, {'mql': 'direction', 'py': 'direction', 'param': 'direction', 'type': 'bool', 'default': True, 'label': 'Histogram inversion', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum BandsMode
BASE_LINE_ = 0
UPPER_BAND_ = 1
LOWER_BAND_ = 2
_enum('BandsMode', {0: 'BASE_LINE_', 1: 'UPPER_BAND_', 2: 'LOWER_BAND_'})

# ---- inputs and global variables
Power_Period = _input('Power_Period', 13)  # Indicator period
Power_Price = _input('Power_Price', 0)  # Indicators price
Price_Type = _input('Price_Type', 0)  # Calculated price
Bands_Mode = _input('Bands_Mode', BASE_LINE)  # Bollinger type
Bands_Period = _input('Bands_Period', 20)  # Bollinger period
Bands_Deviation = _input('Bands_Deviation', 2)  # Number of standard Bollinger deviations
direction = _input('direction', True)  # Histogram inversion
HistBuffer = Arr(0, 0.0)
ColorHistBuffer = Arr(0, 0.0)
LineBuffer = Arr(0, 0.0)
Direct = 0
min_rates_total = 0
BandsHandle = 0
BearsHandle = 0
BullsHandle = 0

def PointHistogram_X5(rates_total, prev_calculated, limit, Buffer, ColorBuffer, bar):
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit.v -= 1
    bar = limit.v
    for bar in range(bar, 0 - 1, -1):
        ColorHistBuffer[bar] = 0.0
        if Buffer[bar] > 0:
            if Buffer[bar] > Buffer[bar + 1]:
                ColorBuffer[bar] = 1.0
            if Buffer[bar] < Buffer[bar + 1]:
                ColorBuffer[bar] = 2.0
        if Buffer[bar] < 0:
            if Buffer[bar] < Buffer[bar + 1]:
                ColorBuffer[bar] = 3.0
            if Buffer[bar] > Buffer[bar + 1]:
                ColorBuffer[bar] = 4.0
    else:
        bar = _range_end(bar, 0 - 1, -1)

def OnInit():
    global BandsHandle, BearsHandle, BullsHandle, Direct, min_rates_total
    min_rates_total = MathMax(Power_Period, Bands_Period)
    Direct = (2 * direction) - 1
    BandsHandle = iBands(None, 0, Bands_Period, 0, Bands_Deviation, Power_Price)
    if BandsHandle == INVALID_HANDLE:
        Print(' Failed to get handle of the iBands indicator')
    BearsHandle = iBearsPower(None, 0, Power_Period)
    if BearsHandle == INVALID_HANDLE:
        Print(' Failed to get handle of the iBearsPower indicator')
    BullsHandle = iBullsPower(None, 0, Power_Period)
    if BearsHandle == INVALID_HANDLE:
        Print(' Failed to get handle of the iBullsPower indicator')
    SetIndexBuffer(0, HistBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(HistBuffer, True)
    SetIndexBuffer(1, ColorHistBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    ArraySetAsSeries(ColorHistBuffer, True)
    SetIndexBuffer(2, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LineBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'iTrend( ', Power_Period, ', ', Bands_Period, ', ', Bands_Deviation, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if ((BarsCalculated(BandsHandle) < rates_total or BarsCalculated(BearsHandle) < rates_total) or BarsCalculated(BullsHandle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = Box(0)
    bar = 0
    Bands = Arr(0, 0.0)
    Bears = Arr(0, 0.0)
    Bulls = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit.v = rates_total - min_rates_total - 1 - begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        limit.v = rates_total - prev_calculated
    to_copy = limit.v + 1
    if (CopyBuffer(BandsHandle, Bands_Mode, 0, to_copy, Bands) <= 0 or CopyBuffer(BearsHandle, 0, 0, to_copy, Bears) <= 0) or CopyBuffer(BullsHandle, 0, 0, to_copy, Bulls) <= 0:
        return 0
    ArraySetAsSeries(Bands, True)
    ArraySetAsSeries(Bears, True)
    ArraySetAsSeries(Bulls, True)
    ArraySetAsSeries(price, True)
    bar = limit.v
    for bar in range(bar, 0 - 1, -1):
        HistBuffer[bar] = Direct * (price[bar] - Bands[bar])
        LineBuffer[bar] = Bears[bar] + Bulls[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    PointHistogram_X5(rates_total, prev_calculated, limit, HistBuffer, ColorHistBuffer, bar)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Itrend(_MQL5Indicator):
    name = 'itrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Power_Period': 13,  # Indicator period
        'Power_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Indicators price
        'Price_Type': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Calculated price
        'Bands_Mode': _Choice({0: 'Middle Bollinger', 1: 'Upper Bollinger', 2: 'Lower Bollinger'}, default=0),  # Bollinger type
        'Bands_Period': 20,  # Bollinger period
        'Bands_Deviation': 2,  # Number of standard Bollinger deviations
        'direction': True,  # Histogram inversion
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

