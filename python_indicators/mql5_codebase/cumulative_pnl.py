"""Cumulative PnL — converted from MQL5: MQL5 Indicators/Equity and Balance Indicator - History based/Cumulative PnL.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [16711680]}, 'widths': {1: 1, 2: 2}, 'styles': {}, 'labels': {1: 'Balance', 2: 'Equity'}, 'levels': [], 'description': [], 'name': 'Cumulative PnL', 'source': 'MQL5 Indicators/Equity and Balance Indicator - History based/Cumulative PnL.mq5', 'folder': 'Equity and Balance Indicator - History based', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BalanceBuffer = Arr(0, 0.0)
EquityBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BalanceBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, EquityBuffer, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(start, rates_total):
        balance = 0.0
        unrealizedPnL = 0.0
        HistorySelect(0, time[i])
        j = 0
        while j < HistoryDealsTotal():
            ticket = HistoryDealGetTicket(j)
            if ticket > 0 and HistoryDealGetInteger(ticket, DEAL_TIME) <= time[i]:
                balance += HistoryDealGetDouble(ticket, DEAL_PROFIT)
                balance += HistoryDealGetDouble(ticket, DEAL_SWAP)
                balance += HistoryDealGetDouble(ticket, DEAL_COMMISSION)
            j += 1
        openSymbols = Arr(0, "")
        openVolumes = Arr(0, 0.0)
        openPrices = Arr(0, 0.0)
        openCount = 0
        j = 0
        while j < HistoryDealsTotal():
            ticket = HistoryDealGetTicket(j)
            if ticket == 0:
                j += 1
                continue
            if HistoryDealGetInteger(ticket, DEAL_TIME) > time[i]:
                j += 1
                continue
            symbol = HistoryDealGetString(ticket, DEAL_SYMBOL)
            dealVolume = HistoryDealGetDouble(ticket, DEAL_VOLUME)
            price = HistoryDealGetDouble(ticket, DEAL_PRICE)
            type_ = HistoryDealGetInteger(ticket, DEAL_TYPE)
            entry = HistoryDealGetInteger(ticket, DEAL_ENTRY)
            idx = -1
            for k in range(0, openCount):
                if openSymbols[k] == symbol:
                    idx = k
                    break
            if idx == -1:
                idx = ((openCount := openCount + 1) - 1)
                ArrayResize(openSymbols, openCount)
                ArrayResize(openVolumes, openCount)
                ArrayResize(openPrices, openCount)
                openSymbols[idx] = symbol
                openVolumes[idx] = 0.0
                openPrices[idx] = 0.0
            if entry == DEAL_ENTRY_IN:
                oldVolume = openVolumes[idx]
                totalCost = (MathAbs(oldVolume) * openPrices[idx]) + (dealVolume * price)
                if type_ == DEAL_TYPE_BUY:
                    openVolumes[idx] += dealVolume
                elif type_ == DEAL_TYPE_SELL:
                    openVolumes[idx] -= dealVolume
                if MathAbs(openVolumes[idx]) > 1e-05:
                    openPrices[idx] = _fdiv(totalCost, MathAbs(openVolumes[idx]))
            elif entry == DEAL_ENTRY_OUT:
                openVolumes[idx] += (dealVolume if (type_ == DEAL_TYPE_BUY) else (-dealVolume))
            j += 1
        for j in range(0, openCount):
            if MathAbs(openVolumes[j]) < 1e-05:
                continue
            currentPrice = 0.0
            if openSymbols[j] == Symbol():
                currentPrice = close[i]
            else:
                closeArray = Arr(1, 0.0, dyn=False)
                if CopyClose(openSymbols[j], Period(), _DT(time[i]), 1, closeArray) > 0:
                    currentPrice = closeArray[0]
                else:
                    continue
            pnl = openVolumes[j] * (currentPrice - openPrices[j])
            accCurrency = AccountInfoString(ACCOUNT_CURRENCY)
            profitCurrency = SymbolInfoString(openSymbols[j], SYMBOL_CURRENCY_PROFIT)
            if accCurrency != profitCurrency:
                tickValue = SymbolInfoDouble(openSymbols[j], SYMBOL_TRADE_TICK_VALUE)
                tickSize = SymbolInfoDouble(openSymbols[j], SYMBOL_TRADE_TICK_SIZE)
                if tickSize > 0:
                    pnl = _fdiv(pnl * tickValue, tickSize)
            unrealizedPnL += pnl
        if i == (rates_total - 1):
            p = 0
            while p < PositionsTotal():
                if PositionSelectByTicket(PositionGetTicket(p)):
                    unrealizedPnL += PositionGetDouble(POSITION_SWAP)
                p += 1
        BalanceBuffer[i] = balance
        EquityBuffer[i] = balance + unrealizedPnL
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CumulativePnL(_MQL5Indicator):
    name = 'Cumulative PnL'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

