"""Fractals On OBV — converted from MQL5: MQL5 Indicators/Fractals On OBV/Fractals On OBV.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.001', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 5, 3: 5}, 'colors': {1: [36095], 2: [8421504], 3: [8421504]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'OBV', 2: 'Fractal Up', 3: 'Fractal Down'}, 'levels': [], 'description': [], 'name': 'Fractals On OBV', 'source': 'MQL5 Indicators/Fractals On OBV/Fractals On OBV.mq5', 'folder': 'Fractals On OBV', 'inputs': [{'mql': 'Inp_OBV_applied_volume', 'py': 'Inp_OBV_applied_volume', 'param': 'Inp_OBV_applied_volume', 'type': 'int', 'default': 0, 'label': 'OBV: volume type for calculation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_OBV_applied_volume = _input('Inp_OBV_applied_volume', VOLUME_TICK)  # OBV: volume type for calculation
OBVBuffer = Arr(0, 0.0)
Fractal_Up_Buffer = Arr(0, 0.0)
Fractal_Down_Buffer = Arr(0, 0.0)
handle_iOBV = 0  # variable for storing the handle of the iOBV indicator
bars_calculated = 0  # we will keep the number of values in the On Balance Volume indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iOBV, m_init_error
    SetIndexBuffer(0, OBVBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Fractal_Up_Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, Fractal_Down_Buffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetInteger(1, PLOT_ARROW, 217)
    PlotIndexSetInteger(2, PLOT_ARROW, 218)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, 10)
    PlotIndexSetInteger(2, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    handle_iOBV = iOBV(Symbol(), Period(), Inp_OBV_applied_volume)
    if handle_iOBV == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iOBV indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    if rates_total < 5:
        return 0
    values_to_copy = 0
    calculated = BarsCalculated(handle_iOBV)
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
    if not FillArrayFromBuffer(OBVBuffer, handle_iOBV, values_to_copy):
        return 0
    bars_calculated = calculated
    start = 0
    if prev_calculated < 7:
        start = 2
        ArrayInitialize(Fractal_Up_Buffer, EMPTY_VALUE)
        ArrayInitialize(Fractal_Down_Buffer, EMPTY_VALUE)
    else:
        start = rates_total - 5
    for i in range(start, rates_total - 3):
        if ((OBVBuffer[i] > OBVBuffer[i + 1] and OBVBuffer[i] > OBVBuffer[i + 2]) and OBVBuffer[i] >= OBVBuffer[i - 1]) and OBVBuffer[i] >= OBVBuffer[i - 2]:
            Fractal_Up_Buffer[i] = OBVBuffer[i]
        else:
            Fractal_Up_Buffer[i] = EMPTY_VALUE
        if ((OBVBuffer[i] < OBVBuffer[i + 1] and OBVBuffer[i] < OBVBuffer[i + 2]) and OBVBuffer[i] <= OBVBuffer[i - 1]) and OBVBuffer[i] <= OBVBuffer[i - 2]:
            Fractal_Down_Buffer[i] = OBVBuffer[i]
        else:
            Fractal_Down_Buffer[i] = EMPTY_VALUE
    for i in range(rates_total - 3, rates_total):
        Fractal_Up_Buffer[i] = EMPTY_VALUE
        Fractal_Down_Buffer[i] = EMPTY_VALUE
    return rates_total

def FillArrayFromBuffer(obv_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, obv_buffer) < 0:
        PrintFormat('Failed to copy data from the iOBV indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iOBV != INVALID_HANDLE:
        IndicatorRelease(handle_iOBV)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalsOnOBV(_MQL5Indicator):
    name = 'Fractals On OBV'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Inp_OBV_applied_volume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # OBV: volume type for calculation
    }

