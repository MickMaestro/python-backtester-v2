"""iUSDx.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class stCurrencyWeight(MqlObject):
    _q_fields = ('symbol', 'weight')
    def __init__(self, *args):
        self.symbol = ""
        self.weight = 0.0

class CUSDx(MqlObject):
    _q_fields = ('m_symbol', 'm_currency_base', 'm_currency_weight', 'm_init_flag', 'buffer')
    def __init__(self):
        self.m_symbol = ""
        self.m_currency_base = 0
        self.m_currency_weight = 0.0
        self.m_init_flag = False
        self.buffer = Arr(0, 0.0)
        self.m_init_flag = False
    def CUSDx(self):
        pass
    def SetCurrencyAndWeight(self, symbol, weight):
        self.m_symbol = symbol
        self.m_currency_weight = weight
    def InitSymbol(self, count_symbol, currency_index, symbol):
        self.m_init_flag = True
        if currency_index == SymbolInfoString(self.m_symbol, SYMBOL_CURRENCY_BASE):
            self.m_currency_base = 1
        elif currency_index == SymbolInfoString(self.m_symbol, SYMBOL_CURRENCY_PROFIT):
            self.m_currency_base = -1
        else:
            self.m_currency_base = 0
        ArraySetAsSeries(self.buffer, True)
        for bar in range(count_symbol - 1, 0 - 1, -1):
            self.USDxSymbol(bar)
        return
    def USDxSymbol(self, bar=0):
        self.buffer[bar] = EMPTY_VALUE
        if self.m_currency_base == 0:
            return
        time = Arr(1, 0, dyn=False)
        if CopyTime(Symbol(), Period(), bar, 1, time) != 1:
            return
        price = Arr(1, 0.0, dyn=False)
        if CopyClose(self.m_symbol, Period(), _DT(time[0]), _DT(time[0]), price) != 1:
            return
        self.buffer[bar] = MathPow(price[0], self.m_currency_base * self.m_currency_weight)
        return
    def GetInit(self):
        return self.m_init_flag

__all__ = ['stCurrencyWeight', 'CUSDx']
