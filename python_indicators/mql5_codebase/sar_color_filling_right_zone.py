"""SAR Color Filling Right zone — converted from MQL5: MQL5 Indicators/SAR Color Filling Right zone/SAR Color Filling Right zone.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 12, 2: 7}, 'colors': {1: [16748574, 17919], 2: [16763541, 8693503]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0}, 'labels': {1: 'SAR', 2: 'SAR Filling'}, 'levels': [], 'description': [], 'name': 'SAR Color Filling Right zone', 'source': 'MQL5 Indicators/SAR Color Filling Right zone/SAR Color Filling Right zone.mq5', 'folder': 'SAR Color Filling Right zone', 'inputs': [{'mql': 'Inp_SAR_step', 'py': 'Inp_SAR_step', 'param': 'Inp_SAR_step', 'type': 'double', 'default': 0.02, 'label': 'SAR: price increment step - acceleration factor', 'sinput': False}, {'mql': 'Inp_SAR_maximum', 'py': 'Inp_SAR_maximum', 'param': 'Inp_SAR_maximum', 'type': 'double', 'default': 0.2, 'label': 'SAR: maximum value of step', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_SAR_step = _input('Inp_SAR_step', 0.02)  # SAR: price increment step - acceleration factor
Inp_SAR_maximum = _input('Inp_SAR_maximum', 0.2)  # SAR: maximum value of step
SARBuffer = Arr(0, 0.0)
SARColors = Arr(0, 0.0)
SARFillingBuffer1 = Arr(0, 0.0)
SARFillingBuffer2 = Arr(0, 0.0)
handle_iSAR = 0  # variable for storing the handle of the iSAR indicator
bars_calculated = 0  # we will keep the number of values in the Parabolic SAR indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iSAR, m_init_error
    ObjectDelete(ChartID(), 'SAR Rectangle')
    SetIndexBuffer(0, SARBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SARColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, SARFillingBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, SARFillingBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = StringFormat('SAR(%.2f,%.2f)', Inp_SAR_step, Inp_SAR_maximum)
    PlotIndexSetString(0, PLOT_LABEL, short_name)
    handle_iSAR = iSAR(Symbol(), Period(), Inp_SAR_step, Inp_SAR_maximum)
    if handle_iSAR == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iSAR indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    values_to_copy = 0
    calculated = BarsCalculated(handle_iSAR)
    if calculated <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(SARBuffer, handle_iSAR, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    price1 = 0.0
    price2 = 0.0
    clr = clrRed
    for i in range(limit, rates_total):
        if SARBuffer[i] <= low[i]:
            SARColors[i] = 0.0
            SARFillingBuffer1[i] = low[i]
            SARFillingBuffer2[i] = SARBuffer[i]
            price1 = low[i]
            price2 = SARBuffer[i]
            clr = 0xFFCA95
        if SARBuffer[i] >= high[i]:
            SARColors[i] = 1.0
            SARFillingBuffer1[i] = high[i]
            SARFillingBuffer2[i] = SARBuffer[i]
            price1 = SARBuffer[i]
            price2 = high[i]
            clr = 0x84A6FF
    chart_id = ChartID()
    if ObjectFind(chart_id, 'SAR Rectangle') < 0:
        RectangleCreate(chart_id, 'SAR Rectangle', 0, time[rates_total - 1], price1, 2524608000, price2, clr)
    else:
        RectanglePointChange(chart_id, 'SAR Rectangle', 0, time[rates_total - 1], price1, clr)
        RectanglePointChange(chart_id, 'SAR Rectangle', 1, 2524608000, price2, clr)
    return rates_total

def FillArrayFromBuffer(sar_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, sar_buffer) < 0:
        PrintFormat('Failed to copy data from the iSAR indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    ObjectDelete(ChartID(), 'SAR Rectangle')
    if handle_iSAR != INVALID_HANDLE:
        IndicatorRelease(handle_iSAR)

def RectangleCreate(chart_ID=0, name='Rectangle', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrRed, style=STYLE_SOLID, width=1, fill=True, back=False, selection=True, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_RECTANGLE, sub_window, time1, price1, time2, price2):
        Print('RectangleCreate', ': failed to create a rectangle! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_FILL, fill)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def RectanglePointChange(chart_ID=0, name='Rectangle', point_index=0, time=0, price=0.0, clr=clrRed):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, point_index, time, price):
        Print('RectanglePointChange', ': failed to move the anchor point! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SARColorFillingRightZone(_MQL5Indicator):
    name = 'SAR Color Filling Right zone'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_SAR_step': 0.02,  # SAR: price increment step - acceleration factor
        'Inp_SAR_maximum': 0.2,  # SAR: maximum value of step
    }

