"""onnewbarcalculate — converted from MQL5: MQL5 Indicators/The _New bar_ event handler for the indicators/onnewbarcalculate.mq5

Copyright: Copyright 2010, Lizar; Link: Lizar@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.libcisnewbar import *  # #include libcisnewbar.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010, Lizar', 'link': 'Lizar@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'onnewbarcalculate', 'source': 'MQL5 Indicators/The _New bar_ event handler for the indicators/onnewbarcalculate.mq5', 'folder': 'The _New bar_ event handler for the indicators', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['libcisnewbar.mqh']}


def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    period_seconds = PeriodSeconds(Period())
    new_time = _idiv(TimeCurrent(), period_seconds) * period_seconds
    if current_chart.isNewBar_1(new_time):
        OnNewBarCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread)
    return rates_total

def OnNewBarCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    PrintFormat('Новый бар: %s', TimeToString(TimeCurrent(), TIME_SECONDS))
    return rates_total

# ---- global variables initialised from expressions
current_chart = _alloc(CisNewBar)  # CisNewBar class instance (used for the current chart)
current_chart.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Onnewbarcalculate(_MQL5Indicator):
    name = 'onnewbarcalculate'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

