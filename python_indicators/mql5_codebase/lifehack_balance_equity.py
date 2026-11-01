"""LifeHack_Balance_Equity — converted from MQL5: MQL5 Indicators/LifeHack Balance Equity/LifeHack_Balance_Equity.mq5

Balance Equity Indicator
Copyright: Copyright © 2016, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.008

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.008', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [32768]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Balance', 2: 'Equity'}, 'levels': [], 'description': ['Balance Equity Indicator'], 'name': 'LifeHack_Balance_Equity', 'source': 'MQL5 Indicators/LifeHack Balance Equity/LifeHack_Balance_Equity.mq5', 'folder': 'LifeHack Balance Equity', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BalanceBuffer = Arr(0, 0.0)
EquityBuffer = Arr(0, 0.0)
Visiblebars = 300

def OnDeinit(reason):
    pass

def OnInit():
    SetIndexBuffer(0, BalanceBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, EquityBuffer, INDICATOR_DATA)
    ArraySetAsSeries(BalanceBuffer, True)
    ArraySetAsSeries(EquityBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Balance Equity ')
    PlotIndexSetString(0, PLOT_LABEL, 'Balance')
    PlotIndexSetString(1, PLOT_LABEL, 'Equity')
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if prev_calculated == 0:
        for i in range(0, rates_total):
            BalanceBuffer[i] = AccountInfoDouble(ACCOUNT_BALANCE)
            EquityBuffer[i] = AccountInfoDouble(ACCOUNT_EQUITY)
        return rates_total
    BalanceBuffer[0] = AccountInfoDouble(ACCOUNT_BALANCE)
    EquityBuffer[0] = AccountInfoDouble(ACCOUNT_EQUITY)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LifeHackBalanceEquity(_MQL5Indicator):
    name = 'LifeHack_Balance_Equity'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

