"""maenv_02b — converted from MQL5: MQL5 Indicators/MA-Env/maenv_02b.mq5

MaEnv
Copyright: Copyright © 2011, basisforex@gmail.com; Link: basisforex@gmail.com; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, basisforex@gmail.com', 'link': 'basisforex@gmail.com', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 9}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, 'colors': {1: [16777215], 2: [16776960], 3: [16776960], 4: [16711680], 5: [16711680], 6: [65535], 7: [65535], 8: [255], 9: [255]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, 'styles': {}, 'labels': {1: 'MA', 2: 'Up1', 3: 'Dn2', 4: 'Up2', 5: 'Dn2', 6: 'Up3', 7: 'Dn3', 8: 'Up4', 9: 'Dn4'}, 'levels': [], 'description': ['MaEnv'], 'name': 'maenv_02b', 'source': 'MQL5 Indicators/MA-Env/maenv_02b.mq5', 'folder': 'MA-Env', 'inputs': [{'mql': 'type', 'py': 'type_', 'param': 'type_', 'type': 'int', 'default': 0, 'label': 'type of the function', 'sinput': False}, {'mql': 'ma_period_1', 'py': 'ma_period_1', 'param': 'ma_period_1', 'type': 'int', 'default': 30, 'label': 'period of ma', 'sinput': False}, {'mql': 'ma_period_2', 'py': 'ma_period_2', 'param': 'ma_period_2', 'type': 'int', 'default': 50, 'label': 'period of ma', 'sinput': False}, {'mql': 'ma_period_3', 'py': 'ma_period_3', 'param': 'ma_period_3', 'type': 'int', 'default': 100, 'label': 'period of ma', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'type of smoothing', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'type of price', 'sinput': False}, {'mql': 'symbol', 'py': 'symbol', 'param': None, 'type': 'string', 'default': ' ', 'label': 'symbol', 'sinput': False}, {'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 0, 'label': 'timeframe', 'sinput': False}, {'mql': 'ma_shift', 'py': 'ma_shift', 'param': 'ma_shift', 'type': 'int', 'default': 0, 'label': 'shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Creation
Call_iMA = 0
_enum('Creation', {0: 'Call_iMA'})

# ---- inputs and global variables
aquaUp1 = Arr(0, 0.0)
aquaDn1 = Arr(0, 0.0)
aquaUp2 = Arr(0, 0.0)
aquaDn2 = Arr(0, 0.0)
aquaUp3 = Arr(0, 0.0)
aquaDn3 = Arr(0, 0.0)
aquaUp4 = Arr(0, 0.0)
aquaDn4 = Arr(0, 0.0)
BorisKoeff = 0
type_ = _input('type_', Call_iMA)  # type of the function
ma_period_1 = _input('ma_period_1', 30)  # period of ma
ma_period_2 = _input('ma_period_2', 50)  # period of ma
ma_period_3 = _input('ma_period_3', 100)  # period of ma
ma_method = _input('ma_method', MODE_SMA)  # type of smoothing
applied_price = _input('applied_price', PRICE_CLOSE)  # type of price
symbol = _input('symbol', ' ')  # symbol
period = _input('period', PERIOD_CURRENT)  # timeframe
ma_shift = _input('ma_shift', 0)  # shift
iMABuffer = Arr(0, 0.0)
handle = 0
bars_calculated = 0

def OnInit():
    global handle
    SetIndexBuffer(0, iMABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, ma_shift)
    SetIndexBuffer(1, aquaUp1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, ma_shift)
    SetIndexBuffer(2, aquaDn1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, ma_shift)
    SetIndexBuffer(3, aquaUp2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, ma_shift)
    SetIndexBuffer(4, aquaDn2, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, ma_shift)
    SetIndexBuffer(5, aquaUp3, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_SHIFT, ma_shift)
    SetIndexBuffer(6, aquaDn3, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_SHIFT, ma_shift)
    SetIndexBuffer(7, aquaUp4, INDICATOR_DATA)
    PlotIndexSetInteger(7, PLOT_SHIFT, ma_shift)
    SetIndexBuffer(8, aquaDn4, INDICATOR_DATA)
    PlotIndexSetInteger(8, PLOT_SHIFT, ma_shift)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'MaEnv'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    if type_ == Call_iMA:
        handle = _idiv(iMA(None, 0, ma_period_1, 0, ma_method, applied_price) + iMA(None, 0, ma_period_2, 0, ma_method, applied_price) + iMA(None, 0, ma_period_3, 0, ma_method, applied_price), 3)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    values_to_copy = 0
    calculated = BarsCalculated(handle)
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
    if not FillArrayFromBuffer(iMABuffer, ma_shift, handle, values_to_copy):
        return 0
    for i in range(0, rates_total):
        Boril = GetBorisKoeff()
        if Digits() == 4 or Digits() == 2:
            aquaUp1[i] = iMABuffer[i] + (6.18 * Point() * Boril)
            aquaDn1[i] = iMABuffer[i] - (6.18 * Point() * Boril)
            aquaUp2[i] = iMABuffer[i] + (16.18 * Point() * Boril)
            aquaDn2[i] = iMABuffer[i] - (16.18 * Point() * Boril)
            aquaUp3[i] = iMABuffer[i] + (26.18 * Point() * Boril)
            aquaDn3[i] = iMABuffer[i] - (26.18 * Point() * Boril)
            aquaUp4[i] = iMABuffer[i] + (36.18 * Point() * Boril)
            aquaDn4[i] = iMABuffer[i] - (36.18 * Point() * Boril)
        if Digits() == 5 or Digits() == 3:
            aquaUp1[i] = iMABuffer[i] + (61.8 * Point() * Boril)
            aquaDn1[i] = iMABuffer[i] - (61.8 * Point() * Boril)
            aquaUp2[i] = iMABuffer[i] + (161.8 * Point() * Boril)
            aquaDn2[i] = iMABuffer[i] - (161.8 * Point() * Boril)
            aquaUp3[i] = iMABuffer[i] + (261.8 * Point() * Boril)
            aquaDn3[i] = iMABuffer[i] - (261.8 * Point() * Boril)
            aquaUp4[i] = iMABuffer[i] + (361.8 * Point() * Boril)
            aquaDn4[i] = iMABuffer[i] - (361.8 * Point() * Boril)
    return rates_total

def GetBorisKoeff():
    if Period() <= 5:
        return 1
    elif Period() <= 15:
        return 2
    elif Period() <= 30:
        return 3
    elif Period() <= 60:
        return 4
    elif Period() <= 240:
        return 5
    elif Period() <= 1440:
        return 7
    elif Period() <= 10080:
        return 9
    else:
        return 15

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    Comment('')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Maenv02b(_MQL5Indicator):
    name = 'maenv_02b'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'type_': _Choice({0: 'Call_iMA'}, default=0),  # type of the function
        'ma_period_1': 30,  # period of ma
        'ma_period_2': 50,  # period of ma
        'ma_period_3': 100,  # period of ma
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # type of smoothing
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # type of price
        'period': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # timeframe
        'ma_shift': 0,  # shift
    }

