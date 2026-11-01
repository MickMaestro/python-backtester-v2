"""Risk Calculation Tool — converted from MQL5: MQL5 Indicators/Position Risk Calculation Tool/Risk Calculation Tool.mq5

Copyright: Copyright 2023, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [8388736]}, 'widths': {}, 'styles': {1: 0}, 'labels': {1: 'Virtual SL'}, 'levels': [], 'description': [], 'name': 'Risk Calculation Tool', 'source': 'MQL5 Indicators/Position Risk Calculation Tool/Risk Calculation Tool.mq5', 'folder': 'Position Risk Calculation Tool', 'inputs': [{'mql': 'lotSize', 'py': 'lotSize', 'param': 'lotSize', 'type': 'double', 'default': 1.0, 'label': 'Trade volume (lot size)', 'sinput': False}, {'mql': 'posType', 'py': 'posType', 'param': 'posType', 'type': 'int', 'default': 0, 'label': 'Position Type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum PositionType
buy = 0
sell = 1
_enum('PositionType', {0: 'buy', 1: 'sell'})

# ---- inputs and global variables
lotSize = _input('lotSize', 1.0)  # Trade volume (lot size)
posType = _input('posType', buy)  # Position Type
virtSL = Arr(0, 0.0)
balance = 0.0
maxLoss = 0.0
bid = 0.0
ask = 0.0
BidAsk = 0.0

def OnInit():
    global ask, balance, bid
    SetIndexBuffer(0, virtSL, INDICATOR_DATA)
    bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ask = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
    balance = AccountInfoDouble(ACCOUNT_BALANCE)
    ArraySetAsSeries(virtSL, True)
    Comment('Click on the chart at the desired stop loss level...')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global BidAsk, ask, balance, bid
    balance = AccountInfoDouble(ACCOUNT_BALANCE)
    bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ask = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
    ((BidAsk := ask) if (posType == buy) else bid)
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global maxLoss
    if id_ == CHARTEVENT_CLICK:
        all_bars = Bars(Symbol(), Period())
        for x in range(10, 0 - 1, -1):
            virtSL[x] = GetMouseY(dparam)
        for x in range(11, all_bars):
            virtSL[x] = EMPTY_VALUE
        virtualStopLossPoints = _fdiv(MathAbs(BidAsk - GetMouseY(dparam)), Point())
        maxLoss = MaxLossCalc(lotSize, virtualStopLossPoints)
        calculation = '.:: Position Risk Calculator ::.' + '\n\n' + 'Lot size: ' + DoubleToString(lotSize, 2) + '\n' + 'Stop loss points: ' + DoubleToString(virtualStopLossPoints, 2) + '\n\n' + 'Risking:' + '\n' + DoubleToString((maxLoss if (virtualStopLossPoints > 0) else balance), 2) + ' ' + AccountInfoString(ACCOUNT_CURRENCY) + ' ' + '(' + DoubleToString(((_fdiv(maxLoss, balance) * 100) if (virtualStopLossPoints > 0) else 100), 2) + '%' + ')'
        Comment(calculation)
        ChartNavigate(0, CHART_END)

def GetMouseY(dparam):
    chartHeightInPixels = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    priceRange = ChartGetDouble(0, CHART_PRICE_MAX) - ChartGetDouble(0, CHART_PRICE_MIN)
    pixelsPerPrice = _fdiv(chartHeightInPixels, priceRange)
    mouseYValue = ChartGetDouble(0, CHART_PRICE_MAX) - _fdiv(dparam, pixelsPerPrice)
    return mouseYValue

def MaxLossCalc(lot, sl_points):
    global maxLoss
    tickValue = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_VALUE)
    stopLossValue = sl_points * tickValue
    maxLoss = lot * stopLossValue
    return maxLoss

def OnDeinit(reason):
    Comment('')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RiskCalculationTool(_MQL5Indicator):
    name = 'Risk Calculation Tool'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'lotSize': 1.0,  # Trade volume (lot size)
        'posType': _Choice({0: 'Buy', 1: 'Sell'}, default=0),  # Position Type
    }

