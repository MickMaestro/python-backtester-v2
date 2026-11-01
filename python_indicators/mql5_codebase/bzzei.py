"""bzzei — converted from MQL5: MQL5 Indicators/Nonparametric Zig Zag, Out of Price Walk/bzzei.mq5

Zig Zag indicator with following uptrend monotonicity condition:
subsequent High shouldn't be lower than any previous Low.
Similar logic applies for downtrend.
Copyright: Copyright 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 2, 2: 5, 3: 5}, 'colors': {1: [65535], 2: [16711680], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'ZigZagLine', 2: 'High', 3: 'Low'}, 'levels': [], 'description': ['Zig Zag indicator with following uptrend monotonicity condition:', "subsequent High shouldn't be lower than any previous Low.", 'Similar logic applies for downtrend.'], 'name': 'bzzei', 'source': 'MQL5 Indicators/Nonparametric Zig Zag, Out of Price Walk/bzzei.mq5', 'folder': 'Nonparametric Zig Zag, Out of Price Walk', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ZigZagLineBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
iz = 0
imaxhigh = 0
iminlow = 0
lastlow = 0
lasthigh = 0
zhigh = 0.0
zlow = 0.0

def OnInit():
    SetIndexBuffer(0, ZigZagLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 217)
    PlotIndexSetInteger(2, PLOT_ARROW, 218)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global imaxhigh, iminlow, iz, lasthigh, lastlow, zhigh, zlow
    if prev_calculated == 0:
        ArrayInitialize(ZigZagLineBuffer, 0.0)
        ArrayInitialize(HighBuffer, 0.0)
        ArrayInitialize(LowBuffer, 0.0)
        lasthigh = 0
        lastlow = lasthigh
        iminlow = lastlow
        imaxhigh = iminlow
        iz = imaxhigh
        zlow = 0.0
        zhigh = zlow
    elif (rates_total - prev_calculated) >= 2:
        Print(rates_total - prev_calculated)
    shift = 0
    ihigh = 0
    ilow = 0
    shift = iz + 1
    ihigh = shift
    ilow = ihigh
    last_bar = rates_total - 1
    ZigZagLineBuffer[last_bar] = 0.0
    LowBuffer[last_bar] = 0.0
    HighBuffer[last_bar] = 0.0
    while ihigh < last_bar:
        if zlow != 0:
            while ihigh < last_bar and low[ihigh] <= high[iz]:
                ihigh += 1
            if ihigh < last_bar:
                ilow = ihigh + 1
                while ilow < last_bar and high[ilow] >= low[ihigh]:
                    if low[ihigh] < low[ilow]:
                        ihigh = ilow
                    ilow += 1
                if ilow < last_bar and high[ilow] < low[ihigh]:
                    lastlow = iz
                    iz = ihigh
                    zhigh = low[iz]
                    ZigZagLineBuffer[iz] = zhigh
                    zlow = 0.0
                    shift = iz
                    iminlow = shift
                    while (shift := shift - 1) > lasthigh:
                        if low[iminlow] >= low[shift]:
                            iminlow = shift
                    LowBuffer[iminlow] = low[iminlow]
                ihigh = ilow
        elif zhigh != 0:
            while ilow < last_bar and high[ilow] >= low[iz]:
                ilow += 1
            if ilow < last_bar:
                ihigh = ilow + 1
                while ihigh < last_bar and low[ihigh] <= high[ilow]:
                    if high[ilow] > high[ihigh]:
                        ilow = ihigh
                    ihigh += 1
                if ihigh < last_bar and low[ihigh] > high[ilow]:
                    lasthigh = iz
                    iz = ilow
                    zlow = high[iz]
                    ZigZagLineBuffer[iz] = zlow
                    zhigh = 0.0
                    shift = iz
                    imaxhigh = shift
                    while (shift := shift - 1) > lastlow:
                        if high[imaxhigh] <= high[shift]:
                            imaxhigh = shift
                    HighBuffer[imaxhigh] = high[imaxhigh]
                ilow = ihigh
        else:
            while (shift := shift + 1) < last_bar and low[ihigh] < high[ilow]:
                if low[ihigh] < low[shift]:
                    ihigh = shift
                if high[ilow] > high[shift]:
                    ilow = shift
            if shift < last_bar:
                if ihigh < ilow:
                    iz = ihigh
                    zhigh = low[iz]
                    ihigh += 1
                    ilow = ihigh
                else:
                    iz = ilow
                    zlow = high[iz]
                    ilow += 1
                    ihigh = ilow
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bzzei(_MQL5Indicator):
    name = 'bzzei'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

