"""Perfect_Seconds_Chart — converted from MQL5: MQL5 Indicators/Perfect Seconds Chart/Perfect_Seconds_Chart.mq5

Copyright: Copyright 2024, Rajesh Kumar Nait; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Functions not available here: CustomRatesDelete, CustomRatesUpdate, CustomSymbolCreate, CustomSymbolDelete, CustomSymbolSetInteger
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Rajesh Kumar Nait', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Perfect_Seconds_Chart', 'source': 'MQL5 Indicators/Perfect Seconds Chart/Perfect_Seconds_Chart.mq5', 'folder': 'Perfect Seconds Chart', 'inputs': [{'mql': 'Seconds', 'py': 'Seconds', 'param': 'Seconds', 'type': 'int', 'default': 1, 'label': 'Seconds for candles interval', 'sinput': False}, {'mql': 'delete_rates', 'py': 'delete_rates', 'param': 'delete_rates', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'delete_symbol', 'py': 'delete_symbol', 'param': 'delete_symbol', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
symname = ""
Seconds = _input('Seconds', 1)  # Seconds for candles interval
delete_rates = _input('delete_rates', True)
delete_symbol = _input('delete_symbol', True)
canc = Arr(0, 0.0)
cano = Arr(0, 0.0)
canh = Arr(0, 0.0)
canl = Arr(0, 0.0)
cant = Arr(0, 0.0)
seconds = Arr(0, 0.0, dims=(4,))
copyt = -1

def OnInit():
    global symname
    if MQL_TESTER:
        return INIT_SUCCEEDED
    SetIndexBuffer(0, cano, INDICATOR_DATA)
    SetIndexBuffer(1, canh, INDICATOR_DATA)
    SetIndexBuffer(2, canl, INDICATOR_DATA)
    SetIndexBuffer(3, canc, INDICATOR_DATA)
    symname = Symbol() + '.' + IntegerToString(Seconds) + 'second'
    if not SymbolSelect(symname, True):
        if not _missing('CustomSymbolCreate')(symname):
            Print('Failed to create symbol')
        if not _missing('CustomSymbolSetInteger')(symname, SYMBOL_DIGITS, SymbolInfoInteger(Symbol(), SYMBOL_DIGITS)):
            Print('Unable to set')
        if not SymbolSelect(symname, True):
            Print('Cant select symbol')
        else:
            Print('Symbol ' + symname + 'created')
    EventSetTimer(Seconds)
    IndicatorSetString(INDICATOR_SHORTNAME, _str(Seconds) + ' seconds chart')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    EventKillTimer()
    if delete_rates:
        _missing('CustomRatesDelete')(symname, 0, 4089218400)
    if delete_symbol:
        SymbolSelect(symname, False)
        _missing('CustomSymbolDelete')(symname)
        Print('Symbol ' + symname + ' deleted')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if MQL_TESTER:
        return INIT_SUCCEEDED
    bars = Bars(None, 0)
    if bars < rates_total:
        return -1
    if copyt != -1:
        RunSecondsCalc()
    return rates_total

def OnTimer():
    global copyt
    close = Arr(0, 0.0)
    if CopyRates(None, 0, 0, 1, ratesc) == False:
        copyt = -1
        return
    size = ArrayRange(seconds, 0)
    ArrayResize(seconds, size + 1)
    seconds[size][0] = ratesc[0].close
    seconds[size][1] = ratesc[0].close
    seconds[size][2] = ratesc[0].close
    seconds[size][3] = ratesc[0].close
    RunSecondsTimer()

def RunSecondsTimer():
    global copyt
    size = ArrayRange(seconds, 0)
    ArrayResize(seconds, size + 1)
    closeValue = ratesc[0].close
    if size > 0:
        seconds[size][0] = closeValue
        seconds[size][1] = closeValue
        seconds[size][2] = closeValue
        seconds[size][3] = closeValue
        tempRates = Arr(1, 0, dyn=False, factory=MqlRates)
        if CopyRates(Symbol(), PERIOD_M1, 0, 1, tempRates) == -1:
            Print('Failed to copy rates ', GetLastError())
            copyt = -1
            return
        seconds[size - 1][2] = MathMax(seconds[size - 1][2], tempRates[0].close)
        seconds[size - 1][3] = MathMin(seconds[size - 1][3], tempRates[0].close)
        seconds[size - 1][1] = tempRates[0].close
        rates[0].high = seconds[size - 1][2]
        rates[0].low = seconds[size - 1][3]
        rates[0].open = seconds[size - 1][0]
        rates[0].close = seconds[size - 1][1]
        rates[0].time = StringToTime(TimeToString(TimeGMT(), TIME_SECONDS))
        if _missing('CustomRatesUpdate')(symname, rates) == -1:
            copyt = -1
        else:
            copyt = rates[0].time

def RunSecondsCalc():
    global copyt
    size = ArrayRange(seconds, 0)
    if size > 0:
        tempRates = Arr(1, 0, dyn=False, factory=MqlRates)
        if CopyRates(None, 0, 0, 1, tempRates) == -1:
            Print('Failed to copy rates ', GetLastError())
            copyt = -1
            return
        seconds[size - 1][2] = MathMax(seconds[size - 1][2], tempRates[0].close)
        seconds[size - 1][3] = MathMin(seconds[size - 1][3], tempRates[0].close)
        seconds[size - 1][1] = tempRates[0].close
        rates[0].high = seconds[size - 1][2]
        rates[0].low = seconds[size - 1][3]
        rates[0].open = seconds[size - 1][0]
        rates[0].close = seconds[size - 1][1]
        if _missing('CustomRatesUpdate')(symname, rates) == -1:
            copyt = -1
        else:
            copyt = rates[0].time

# ---- global variables initialised from expressions
ratesc = Arr(1, 0, dyn=False, factory=MqlRates)
rates = Arr(1, 0, dyn=False, factory=MqlRates)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PerfectSecondsChart(_MQL5Indicator):
    name = 'Perfect_Seconds_Chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Seconds': 1,  # Seconds for candles interval
        'delete_rates': True,
        'delete_symbol': True,
    }

