"""marketfacilitationindex — converted from MQL5: MQL5 Indicators/Market Facilitation Index (BW MFI)/marketfacilitationindex.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [65280, 1262987, 16711680, 13353215]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'marketfacilitationindex', 'source': 'MQL5 Indicators/Market Facilitation Index (BW MFI)/marketfacilitationindex.mq5', 'folder': 'Market Facilitation Index (BW MFI)', 'inputs': [{'mql': 'InpVolumeType', 'py': 'InpVolumeType', 'param': 'InpVolumeType', 'type': 'int', 'default': 0, 'label': 'Volumes', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpVolumeType = _input('InpVolumeType', VOLUME_TICK)  # Volumes
ExtMFIBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtMFIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BWMFI')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def CalculateMFI(start, rates_total, High, Low, Volume):
    i = start
    mfi_up = True
    vol_up = True
    if i > 0:
        n = i
        while n > 0:
            if ExtMFIBuffer[n] > ExtMFIBuffer[n - 1]:
                mfi_up = True
                break
            if ExtMFIBuffer[n] < ExtMFIBuffer[n - 1]:
                mfi_up = False
                break
            n -= 1
        n = i
        while n > 0:
            if Volume[n] > Volume[n - 1]:
                vol_up = True
                break
            if Volume[n] < Volume[n - 1]:
                vol_up = False
                break
            n -= 1
    while i < rates_total:
        if Volume[i] == 0:
            if i > 0:
                ExtMFIBuffer[i] = ExtMFIBuffer[i - 1]
            else:
                ExtMFIBuffer[i] = 0.0
        else:
            ExtMFIBuffer[i] = _fdiv(_fdiv(High[i] - Low[i], Point()), Volume[i])
        if i > 0:
            if ExtMFIBuffer[i] > ExtMFIBuffer[i - 1]:
                mfi_up = True
            if ExtMFIBuffer[i] < ExtMFIBuffer[i - 1]:
                mfi_up = False
            if Volume[i] > Volume[i - 1]:
                vol_up = True
            if Volume[i] < Volume[i - 1]:
                vol_up = False
        if mfi_up and vol_up:
            ExtColorBuffer[i] = 0.0
        if (not mfi_up) and (not vol_up):
            ExtColorBuffer[i] = 1.0
        if mfi_up and (not vol_up):
            ExtColorBuffer[i] = 2.0
        if (not mfi_up) and vol_up:
            ExtColorBuffer[i] = 3.0
        i += 1

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    start = 0
    if start < prev_calculated:
        start = prev_calculated - 1
    if InpVolumeType == VOLUME_TICK:
        CalculateMFI(start, rates_total, High, Low, TickVolume)
    else:
        CalculateMFI(start, rates_total, High, Low, Volume)
    if rates_total > 1:
        ctm = TimeTradeServer()
        lasttm = Time[rates_total - 1]
        nexttm = lasttm + PeriodSeconds()
        if (ctm < nexttm and ctm >= lasttm) and nexttm != lasttm:
            correction_koef = _fdiv(float(1 + ctm - lasttm), float(nexttm - lasttm))
            ExtMFIBuffer[rates_total - 1] *= correction_koef
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Marketfacilitationindex(_MQL5Indicator):
    name = 'marketfacilitationindex'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volumes
    }

