"""iUSDx — converted from MQL5: MQL5 Indicators/iUSDx (USD index) Multicurrency Indicator/iUSDx.mq5

iUSDx Multicurrency Indicator (USD Index).
The indicator show the value of USD index via the currencies: EUR, JPY, GBP, CAD, SEK и CHF.
The MCM Control Panel needed for the multicurrency mode
Copyright: Copyright 2010, Lizar; Link: https://login.mql5.com/ru/users/Lizar; Version: VERSION

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Missing include files: Control panel MCM.mqh
- Functions not available here: DeinitControlPanelMCM, EventToPeriod, InitControlPanelMCM
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.iusdx import *  # #include iUSDx.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010, Lizar', 'link': 'https://login.mql5.com/ru/users/Lizar', 'version': 'VERSION', 'window': 'separate', 'indicator_plots': 1, 'indicator_buffers': 7}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['iUSDx Multicurrency Indicator (USD Index).', 'The indicator show the value of USD index via the currencies: EUR, JPY, GBP, CAD, SEK и CHF.', 'The MCM Control Panel needed for the multicurrency mode'], 'name': 'iUSDx', 'source': 'MQL5 Indicators/iUSDx (USD index) Multicurrency Indicator/iUSDx.mq5', 'folder': 'iUSDx (USD index) Multicurrency Indicator', 'inputs': [{'mql': 'count', 'py': 'count', 'param': 'count', 'type': 'int', 'default': 500, 'label': 'Number of bars for the calculation', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': ['Control panel MCM.mqh'], 'imports': [], 'libraries': ['iUSDx.mqh']}

CHARTEVENT_NEWBAR_NO = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
count = _input('count', 500)  # Number of bars for the calculation
iUSDx_Ind = Arr(0, 0.0)
currency = 'USD'  # USD
symbol_total = 6  # Pairs, used in the calculation
calculate = 0
buffer = Arr(0, None)

def OnInit():
    _missing('InitControlPanelMCM')()
    ArrayResize(buffer, symbol_total)
    ArrayResize(currency_weight, symbol_total)
    currency_weight[0].symbol = 'EURUSD'
    currency_weight[0].weight = 0.576
    currency_weight[1].symbol = 'USDJPY'
    currency_weight[1].weight = 0.136
    currency_weight[2].symbol = 'GBPUSD'
    currency_weight[2].weight = 0.119
    currency_weight[3].symbol = 'USDCAD'
    currency_weight[3].weight = 0.091
    currency_weight[4].symbol = 'USDSEK'
    currency_weight[4].weight = 0.042
    currency_weight[5].symbol = 'USDCHF'
    currency_weight[5].weight = 0.036
    SetIndexBuffer(0, iUSDx_Ind, INDICATOR_DATA)
    i = 0
    while i < symbol_total:
        buffer[i] = CUSDx()
        SetIndexBuffer(i + 1, buffer[i].buffer, INDICATOR_CALCULATIONS)
        buffer[i].SetCurrencyAndWeight(currency_weight[i].symbol, currency_weight[i].weight)
        i += 1
    ArraySetAsSeries(iUSDx_Ind, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'iUSDx ' + '1.00 Build 1 (17 Dec 2010)')
    PlotIndexSetString(0, PLOT_LABEL, 'iUSDx')
    return 0

def OnChartEvent(id_, lparam, dparam, sparam):
    custom_id = id_ - CHARTEVENT_CUSTOM - 1
    if custom_id >= 0:
        if lparam != CHARTEVENT_NEWBAR_NO:
            if _missing('EventToPeriod')(lparam) == Period() and sparam == Symbol():
                iUSDx_Ind[0] = EMPTY_VALUE
                i = 0
                while i < symbol_total:
                    buffer[i].USDxSymbol()
                    i += 1
                iUSDx(symbol_total)
                return
            buffer[custom_id].USDxSymbol()
            iUSDx(symbol_total)
            return
        else:
            buffer[custom_id].InitSymbol(count, currency, sparam)
            Init_iUSDx(symbol_total, calculate)
            return

def Init_iUSDx(total, count_iUSDx):
    for bar in range(count_iUSDx - 1, 0 - 1, -1):
        iUSDx(total, bar)
    return

def iUSDx(total, bar=0):
    iUSDx_Ind[bar] = 50.14348112
    for i in range(0, total):
        if buffer[i].buffer[bar] != EMPTY_VALUE and buffer[i].GetInit():
            iUSDx_Ind[bar] *= buffer[i].buffer[bar]
        else:
            iUSDx_Ind[bar] = EMPTY_VALUE
            return
    if iUSDx_Ind[bar] < 5:
        iUSDx_Ind[bar] = EMPTY_VALUE
    return

def OnCalculate(rates_total, prev_calculated, begin, price):
    global calculate
    if prev_calculated == 0:
        ArrayInitialize(iUSDx_Ind, EMPTY_VALUE)
        calculate = MathMin(rates_total, TerminalInfoInteger(TERMINAL_MAXBARS))
        calculate = MathMin(calculate, count)
    return rates_total

def OnDeinit(reason):
    for i in range(0, symbol_total):
        _delete(buffer[i])
    _missing('DeinitControlPanelMCM')()

# ---- global variables initialised from expressions
currency_weight = Arr(0, 0, factory=stCurrencyWeight)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IUSDx(_MQL5Indicator):
    name = 'iUSDx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'count': 500,  # Number of bars for the calculation
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

