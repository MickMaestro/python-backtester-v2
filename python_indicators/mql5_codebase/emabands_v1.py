"""emabands_v1 — converted from MQL5: MQL5 Indicators/EMA Bands/emabands_v1.mq5

MACD_Cloud
Copyright: Copyright © 2006, Forex-TSD.com ; Link: http://www.forex-tsd.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Forex-TSD.com ', 'link': 'http://www.forex-tsd.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 7}, 'colors': {1: [10025880], 2: [13353215]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Upper Cloud', 2: 'Lower Cloud'}, 'levels': [], 'description': ['MACD_Cloud'], 'name': 'emabands_v1', 'source': 'MQL5 Indicators/EMA Bands/emabands_v1.mq5', 'folder': 'EMA Bands', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Delta', 'py': 'Delta', 'param': 'Delta', 'type': 'uint', 'default': 150, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 13)
MAType = _input('MAType', MODE_EMA)
Delta = _input('Delta', 150)
min_rates_total = 0
ExtHHBuffer = Arr(0, 0.0)
ExtHLBuffer = Arr(0, 0.0)
ExtLHBuffer = Arr(0, 0.0)
ExtLLBuffer = Arr(0, 0.0)
dDelta = 0.0
MAh_Handle = 0
MAl_Handle = 0

def OnInit():
    global MAh_Handle, MAl_Handle, dDelta, min_rates_total
    min_rates_total = MAPeriod
    dDelta = Delta * Point()
    MAh_Handle = iMA(None, 0, MAPeriod, 0, MAType, PRICE_HIGH)
    if MAh_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of iMA h')
        return INIT_FAILED
    MAl_Handle = iMA(None, 0, MAPeriod, 0, MAType, PRICE_LOW)
    if MAl_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of iMA l')
        return INIT_FAILED
    SetIndexBuffer(0, ExtHHBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtHHBuffer, True)
    SetIndexBuffer(1, ExtHLBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtHLBuffer, True)
    SetIndexBuffer(2, ExtLHBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtLHBuffer, True)
    SetIndexBuffer(3, ExtLLBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtLLBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EMABands_v1')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if (BarsCalculated(MAh_Handle) < rates_total or BarsCalculated(MAl_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MAh_Handle, MAIN_LINE, 0, to_copy, ExtHLBuffer) <= 0:
        return 0
    if CopyBuffer(MAl_Handle, MAIN_LINE, 0, to_copy, ExtLHBuffer) <= 0:
        return 0
    for bar in range(limit, 0 - 1, -1):
        ExtHHBuffer[bar] = ExtHLBuffer[bar] + dDelta
        ExtLLBuffer[bar] = ExtLHBuffer[bar] - dDelta
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EmabandsV1(_MQL5Indicator):
    name = 'emabands_v1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 13,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'Delta': 150,
    }

