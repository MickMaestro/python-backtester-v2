"""currencyindex — converted from MQL5: MQL5 Indicators/MultiCurrency/currencyindex.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {2: 17}, 'colors': {2: [65280, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {2: 'Open; High; Low; Close'}, 'levels': [], 'description': [], 'name': 'currencyindex', 'source': 'MQL5 Indicators/MultiCurrency/currencyindex.mq5', 'folder': 'MultiCurrency', 'inputs': [{'mql': 'CurrencyIndex', 'py': 'CurrencyIndex', 'param': None, 'type': 'string', 'default': 'USD', 'label': 'index currency', 'sinput': False}, {'mql': 'ExchangeIndex0', 'py': 'ExchangeIndex0', 'param': None, 'type': 'string', 'default': 'EUR', 'label': 'exchange currency 0', 'sinput': False}, {'mql': 'ExchangeIndex1', 'py': 'ExchangeIndex1', 'param': None, 'type': 'string', 'default': 'GBP', 'label': 'exchange currency 1', 'sinput': False}, {'mql': 'ExchangeIndex2', 'py': 'ExchangeIndex2', 'param': None, 'type': 'string', 'default': 'AUD', 'label': 'exchange currency 2', 'sinput': False}, {'mql': 'ExchangeIndex3', 'py': 'ExchangeIndex3', 'param': None, 'type': 'string', 'default': 'CAD', 'label': 'exchange currency 3', 'sinput': False}, {'mql': 'ExchangeIndex4', 'py': 'ExchangeIndex4', 'param': None, 'type': 'string', 'default': 'CHF', 'label': 'exchange currency 4', 'sinput': False}, {'mql': 'ExchangeIndex5', 'py': 'ExchangeIndex5', 'param': None, 'type': 'string', 'default': 'JPY', 'label': 'exchange currency 5', 'sinput': False}, {'mql': 'ExchangeIndex6', 'py': 'ExchangeIndex6', 'param': None, 'type': 'string', 'default': '', 'label': 'exchange currency 6', 'sinput': False}, {'mql': 'ExchangeIndex7', 'py': 'ExchangeIndex7', 'param': None, 'type': 'string', 'default': '', 'label': 'exchange currency 7', 'sinput': False}, {'mql': 'ExchangeIndex8', 'py': 'ExchangeIndex8', 'param': None, 'type': 'string', 'default': '', 'label': 'exchange currency 8', 'sinput': False}, {'mql': 'ExchangeIndex9', 'py': 'ExchangeIndex9', 'param': None, 'type': 'string', 'default': '', 'label': 'exchange currency 9', 'sinput': False}, {'mql': 'ExchangeIndex10', 'py': 'ExchangeIndex10', 'param': None, 'type': 'string', 'default': '', 'label': 'exchange currency 10', 'sinput': False}, {'mql': 'ExchangeIndex11', 'py': 'ExchangeIndex11', 'param': None, 'type': 'string', 'default': '', 'label': 'exchange currency 11', 'sinput': False}, {'mql': 'BidColor', 'py': 'BidColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'BidStyle', 'py': 'BidStyle', 'param': 'BidStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant in a zero buffer', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Red = 0x0000FF  # MQL4 colour name

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_'})

# ---- inputs and global variables
CurrencyIndex = _input('CurrencyIndex', 'USD')  # index currency
ExchangeIndex0 = _input('ExchangeIndex0', 'EUR')  # exchange currency 0
ExchangeIndex1 = _input('ExchangeIndex1', 'GBP')  # exchange currency 1
ExchangeIndex2 = _input('ExchangeIndex2', 'AUD')  # exchange currency 2
ExchangeIndex3 = _input('ExchangeIndex3', 'CAD')  # exchange currency 3
ExchangeIndex4 = _input('ExchangeIndex4', 'CHF')  # exchange currency 4
ExchangeIndex5 = _input('ExchangeIndex5', 'JPY')  # exchange currency 5
ExchangeIndex6 = _input('ExchangeIndex6', '')  # exchange currency 6
ExchangeIndex7 = _input('ExchangeIndex7', '')  # exchange currency 7
ExchangeIndex8 = _input('ExchangeIndex8', '')  # exchange currency 8
ExchangeIndex9 = _input('ExchangeIndex9', '')  # exchange currency 9
ExchangeIndex10 = _input('ExchangeIndex10', '')  # exchange currency 10
ExchangeIndex11 = _input('ExchangeIndex11', '')  # exchange currency 11
BidStyle = _input('BidStyle', STYLE_SOLID)
IPC = _input('IPC', PRICE_CLOSE)  # price constant in a zero buffer
ExtBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
Pow = 0.0
Init = False
Sign = Arr(12, 0, dyn=False)
Symbol_ = Arr(12, "", dyn=False)

def Rates_Total(Symbols):
    Bars_ = Arr(12, 0, dyn=False)
    for count in range(0, 12):
        if Sign[count] != 0:
            Bars_[count] = Bars(Symbols[count], PERIOD_CURRENT)
        else:
            Bars_[count] = 999999999
    error = GetLastError()
    ResetLastError()
    if error == 4401:
        return -1
    return Bars_[ArrayMinimum(Bars_, 0, WHOLE_ARRAY)]

def SynchroCheck(Symbols):
    Time0 = Arr(1, 0, dyn=False)
    TimeN = Arr(1, 0, dyn=False)
    Time0[0] = 0
    for count in range(0, 12):
        if Sign[count] != 0 and CopyTime(Symbols[count], 0, 0, 1, Time0) > 0:
            break
    if Time0[0] == 0:
        return False
    for count in range(0, 12):
        if Sign[count] != 0:
            if CopyTime(Symbols[count], 0, 0, 1, TimeN) <= 0:
                return False
            elif TimeN[0] != Time0[0]:
                return False
    return True

def OnInit():
    global Init, Pow
    symb = ""
    symbol = Arr(12, "", dyn=False)
    symbol[0] = ExchangeIndex0
    symbol[1] = ExchangeIndex1
    symbol[2] = ExchangeIndex2
    symbol[3] = ExchangeIndex3
    symbol[4] = ExchangeIndex4
    symbol[5] = ExchangeIndex5
    symbol[6] = ExchangeIndex6
    symbol[7] = ExchangeIndex7
    symbol[8] = ExchangeIndex8
    symbol[9] = ExchangeIndex9
    symbol[10] = ExchangeIndex10
    symbol[11] = ExchangeIndex11
    for count in range(0, 12):
        if symbol[count] == '':
            Symbol_[count] = ''
            Sign[count] = 0
            continue
        symb = CurrencyIndex + symbol[count]
        if SymbolInfoInteger(symb, SYMBOL_SELECT):
            Symbol_[count] = symb
            Sign[count] = 1
        else:
            if GetLastError() == ERR_MARKET_UNKNOWN_SYMBOL:
                symb = symbol[count] + CurrencyIndex
                ResetLastError()
                if not SymbolInfoInteger(symb, SYMBOL_SELECT):
                    if GetLastError() != ERR_MARKET_UNKNOWN_SYMBOL:
                        ResetLastError()
                        if SymbolSelect(symb, True):
                            Symbol_[count] = symb
                            Sign[count] = -1
                        else:
                            Symbol_[count] = ''
                            Sign[count] = 0
                            Print('OnInit', '(): Failed to add the symbol for the currency ', symbol[count], ' to the MarketWatch window!!!')
                            continue
                    else:
                        Symbol_[count] = ''
                        Sign[count] = 0
                        Print('OnInit', '(): Failed to find the symbol for the currency ', symbol[count], '!!!')
                        continue
                else:
                    if SymbolSelect(symb, True):
                        Symbol_[count] = symb
                        Sign[count] = -1
                    else:
                        Symbol_[count] = ''
                        Sign[count] = 0
                        Print('OnInit', '(): Failed to add the symbol for the currency ', symbol[count], ' to the MarketWatch window!!!')
                        continue
            elif SymbolSelect(symb, True):
                Symbol_[count] = symb
                Sign[count] = 1
            else:
                Symbol_[count] = ''
                Sign[count] = 0
                Print('OnInit', '(): Failed to find or add the symbol for the currency ', symbol[count], ' to the MarketWatch window!!!')
                continue
    sum_ = 0
    for count in range(0, 12):
        if Sign[count]:
            sum_ += 1
    Pow = _fdiv(1.0, sum_)
    Init = False
    for count in range(0, 12):
        if Symbol_[count] == Symbol():
            Init = True
    SetIndexBuffer(1, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtCloseBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(5, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(0, ExtBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtBuffer, True)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorsBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, 6)
    short_name = 'CurrencyIndex ' + CurrencyIndex
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, BidColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, BidStyle)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    Bars_ = Rates_Total(Symbol_)
    if Bars_ < 1 or (not Init):
        return 0
    if not SynchroCheck(Symbol_):
        return prev_calculated
    to_copy = 0
    bar = 0
    rates = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(rates, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = Bars_
        draw_begin = rates_total - to_copy
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, draw_begin)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, draw_begin)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, draw_begin)
        PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, draw_begin)
        PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, draw_begin)
        PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, draw_begin)
        bar = to_copy
        for bar in range(bar, rates_total):
            ExtOpenBuffer[bar] = 0.0
            ExtCloseBuffer[bar] = 0.0
            ExtHighBuffer[bar] = 0.0
            ExtLowBuffer[bar] = 0.0
        else:
            bar = _range_end(bar, rates_total, 1)
    else:
        to_copy = rates_total - prev_calculated + 1
        if to_copy > Bars_:
            return 0
    bar = 0
    for bar in range(bar, to_copy):
        ExtOpenBuffer[bar] = 1.0
        ExtCloseBuffer[bar] = 1.0
        ExtHighBuffer[bar] = 1.0
        ExtLowBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, to_copy, 1)
    for count in range(0, 12):
        if Sign[count] == 0:
            continue
        if CopyRates(Symbol_[count], PERIOD_CURRENT, 0, to_copy, rates) <= 0:
            return 0
        if Sign[count] > 0:
            bar = 0
            for bar in range(bar, to_copy):
                ExtOpenBuffer[bar] *= rates[bar].open
                ExtCloseBuffer[bar] *= rates[bar].close
                ExtHighBuffer[bar] *= rates[bar].high
                ExtLowBuffer[bar] *= rates[bar].low
            else:
                bar = _range_end(bar, to_copy, 1)
        if Sign[count] < 0:
            bar = 0
            for bar in range(bar, to_copy):
                ExtOpenBuffer[bar] = _fdiv(ExtOpenBuffer[bar], rates[bar].open)
                ExtCloseBuffer[bar] = _fdiv(ExtCloseBuffer[bar], rates[bar].close)
                ExtHighBuffer[bar] = _fdiv(ExtHighBuffer[bar], rates[bar].low)
                ExtLowBuffer[bar] = _fdiv(ExtLowBuffer[bar], rates[bar].high)
            else:
                bar = _range_end(bar, to_copy, 1)
    bar = 0
    for bar in range(bar, to_copy):
        ExtOpenBuffer[bar] = MathPow(ExtOpenBuffer[bar], Pow)
        ExtCloseBuffer[bar] = MathPow(ExtCloseBuffer[bar], Pow)
        ExtHighBuffer[bar] = MathPow(ExtHighBuffer[bar], Pow)
        ExtLowBuffer[bar] = MathPow(ExtLowBuffer[bar], Pow)
    else:
        bar = _range_end(bar, to_copy, 1)
    bar = 0
    for bar in range(bar, to_copy):
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorsBuffer[bar] = 0.0
        else:
            ExtColorsBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, to_copy, 1)
    bar = 0
    for bar in range(bar, to_copy):
        _sw1 = IPC
        if _sw1 == PRICE_CLOSE_:
            ExtBuffer[bar] = ExtCloseBuffer[bar]
        elif _sw1 == PRICE_OPEN_:
            ExtBuffer[bar] = ExtOpenBuffer[bar]
        elif _sw1 == PRICE_HIGH_:
            ExtBuffer[bar] = ExtHighBuffer[bar]
        elif _sw1 == PRICE_LOW_:
            ExtBuffer[bar] = ExtLowBuffer[bar]
    else:
        bar = _range_end(bar, to_copy, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, ExtCloseBuffer[0])
    return rates_total

# ---- global variables initialised from expressions
BidColor = _input('BidColor', _uint(Red))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Currencyindex(_MQL5Indicator):
    name = 'currencyindex'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BidStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low'}, default=1),  # price constant in a zero buffer
    }

