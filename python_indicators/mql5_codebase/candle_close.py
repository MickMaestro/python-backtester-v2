"""Candle Close — converted from MQL5: MQL5 Indicators/Candle Time Count Down/Candle Close.mq5

Copyright: Copyright 2023, Obunadike Chioma; Link: https://devbidden.netlify.app; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, Obunadike Chioma', 'link': 'https://devbidden.netlify.app', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Candle Close', 'source': 'MQL5 Indicators/Candle Time Count Down/Candle Close.mq5', 'folder': 'Candle Time Count Down', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}


def OnInit():
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    Comment('Current candle to close in: ', main_can())
    return rates_total

def candl_lef():
    last_tr = iTime(Symbol(), PERIOD_CURRENT, 1)
    c_time = iTime(Symbol(), PERIOD_CURRENT, 0)
    interval = c_time - last_tr
    next_ = last_tr + interval + interval
    diff = next_ - TimeCurrent()
    return diff

def hour():
    tm = MqlDateTime()
    TimeToStruct(candl_lef(), tm)
    hrt = tm.hour
    hrt_m = ''
    if hrt < 10:
        if hrt == 0:
            hrt_m = '00'
        if hrt == 1:
            hrt_m = '01'
        if hrt == 2:
            hrt_m = '02'
        if hrt == 3:
            hrt_m = '03'
        if hrt == 4:
            hrt_m = '04'
        if hrt == 5:
            hrt_m = '05'
        if hrt == 6:
            hrt_m = '06'
        if hrt == 7:
            hrt_m = '07'
        if hrt == 8:
            hrt_m = '08'
        if hrt == 9:
            hrt_m = '09'
    else:
        hrt_m = IntegerToString(hrt)
    return hrt_m

def homin():
    tm = MqlDateTime()
    TimeToStruct(candl_lef(), tm)
    hrt = tm.min
    hrt_m = ''
    if hrt < 10:
        if hrt == 0:
            hrt_m = '00'
        if hrt == 1:
            hrt_m = '01'
        if hrt == 2:
            hrt_m = '02'
        if hrt == 3:
            hrt_m = '03'
        if hrt == 4:
            hrt_m = '04'
        if hrt == 5:
            hrt_m = '05'
        if hrt == 6:
            hrt_m = '06'
        if hrt == 7:
            hrt_m = '07'
        if hrt == 8:
            hrt_m = '08'
        if hrt == 9:
            hrt_m = '09'
    else:
        hrt_m = IntegerToString(hrt)
    return hrt_m

def secon():
    tm = MqlDateTime()
    TimeToStruct(candl_lef(), tm)
    hrt = tm.sec
    hrt_m = ''
    if hrt < 10:
        if hrt == 0:
            hrt_m = '00'
        if hrt == 1:
            hrt_m = '01'
        if hrt == 2:
            hrt_m = '02'
        if hrt == 3:
            hrt_m = '03'
        if hrt == 4:
            hrt_m = '04'
        if hrt == 5:
            hrt_m = '05'
        if hrt == 6:
            hrt_m = '06'
        if hrt == 7:
            hrt_m = '07'
        if hrt == 8:
            hrt_m = '08'
        if hrt == 9:
            hrt_m = '09'
    else:
        hrt_m = IntegerToString(hrt)
    return hrt_m

def main_can():
    return hour() + ':' + homin() + ':' + secon()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleClose(_MQL5Indicator):
    name = 'Candle Close'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

