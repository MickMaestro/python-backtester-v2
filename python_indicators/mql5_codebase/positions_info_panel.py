"""Positions_Info_Panel — converted from MQL5: MQL5 Indicators/Positions Info Panel/Positions_Info_Panel.mq5

Copyright: Copyright © 2016, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Missing include files: Positions Info Panel Dialog.mqh
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.001', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Positions_Info_Panel', 'source': 'MQL5 Indicators/Positions Info Panel/Positions_Info_Panel.mq5', 'folder': 'Positions Info Panel', 'inputs': [], 'short_form': True, 'has_oncalculate': True, 'missing_includes': ['Positions Info Panel Dialog.mqh'], 'imports': [], 'libraries': []}


def OnInit():
    EventSetTimer(3)
    if not ExtDialog.Create(0, 'PIP', 0, 10, 20, 80, 70):
        return INIT_FAILED
    ExtDialog.Run()
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    return rates_total

def OnTimer():
    ExtDialog.CommentOut()

def OnChartEvent(id_, lparam, dparam, sparam):
    ExtDialog.ChartEvent(id_, lparam, dparam, sparam)

def OnDeinit(reason):
    EventKillTimer()
    ExtDialog.Destroy(reason)

# ---- global variables initialised from expressions
ExtDialog = CPIPDialog()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PositionsInfoPanel(_MQL5Indicator):
    name = 'Positions_Info_Panel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

