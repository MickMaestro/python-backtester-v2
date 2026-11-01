"""bbandwidth — converted from MQL5: MQL5 Indicators/Bollinger Bandwidth 1.0 for MetaTrader 5/bbandwidth.mq5

Copyright: Copyright 2010, Investors Haven; Link: http://www.InvestorsHaven.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, Investors Haven', 'link': 'http://www.InvestorsHaven.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [8388736]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'BBandwidth'}, 'levels': [], 'description': [], 'name': 'bbandwidth', 'source': 'MQL5 Indicators/Bollinger Bandwidth 1.0 for MetaTrader 5/bbandwidth.mq5', 'folder': 'Bollinger Bandwidth 1.0 for MetaTrader 5', 'inputs': [{'mql': 'InpBandsPeriod', 'py': 'InpBandsPeriod', 'param': 'InpBandsPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpBandsShift', 'py': 'InpBandsShift', 'param': 'InpBandsShift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'InpBandsDeviations', 'py': 'InpBandsDeviations', 'param': 'InpBandsDeviations', 'type': 'double', 'default': 2.0, 'label': 'Deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBandsPeriod = _input('InpBandsPeriod', 20)  # Period
InpBandsShift = _input('InpBandsShift', 0)  # Shift
InpBandsDeviations = _input('InpBandsDeviations', 2.0)  # Deviation
BBHandle = 0
BBandwidthBuffer = Arr(0, 0.0)

def OnInit():
    global BBHandle
    SetIndexBuffer(0, BBandwidthBuffer, INDICATOR_DATA)
    BBHandle = iBands(Symbol(), PERIOD_CURRENT, InpBandsPeriod, InpBandsShift, InpBandsDeviations, PRICE_CLOSE)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    pos = 0
    upper_band = Arr(0, 0.0)
    lower_band = Arr(0, 0.0)
    ArraySetAsSeries(lower_band, True)
    ArraySetAsSeries(upper_band, True)
    ArraySetAsSeries(BBandwidthBuffer, True)
    if BarsCalculated(BBHandle) < rates_total:
        return 0
    if CopyBuffer(BBHandle, 1, 0, rates_total, upper_band) <= 0:
        return 0
    if CopyBuffer(BBHandle, 2, 0, rates_total, lower_band) <= 0:
        return 0
    for i in range(pos, rates_total - 1):
        _sw1 = Digits()
        if _sw1 == 2:
            BBandwidthBuffer[i] = floor(_fdiv(upper_band[i] - lower_band[i], Point()) * 0.1)
        elif _sw1 == 3:
            BBandwidthBuffer[i] = floor(_fdiv(upper_band[i] - lower_band[i], Point()) * 0.01)
        elif _sw1 == 4:
            BBandwidthBuffer[i] = floor(_fdiv(upper_band[i] - lower_band[i], Point()))
        elif _sw1 == 5:
            BBandwidthBuffer[i] = floor(_fdiv(upper_band[i] - lower_band[i], Point()) * 0.1)
        else:
            BBandwidthBuffer[i] = floor(_fdiv(upper_band[i] - lower_band[i], Point()))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bbandwidth(_MQL5Indicator):
    name = 'bbandwidth'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBandsPeriod': 20,  # Period
        'InpBandsShift': 0,  # Shift
        'InpBandsDeviations': 2.0,  # Deviation
    }

