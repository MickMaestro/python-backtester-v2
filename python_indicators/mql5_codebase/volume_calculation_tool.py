"""Volume Calculation Tool — converted from MQL5: MQL5 Indicators/Trade Volume Calculation Tool/Volume Calculation Tool.mq5

Copyright: Copyright 2023, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [8388736]}, 'widths': {}, 'styles': {1: 0}, 'labels': {1: 'Virtual SL'}, 'levels': [], 'description': [], 'name': 'Volume Calculation Tool', 'source': 'MQL5 Indicators/Trade Volume Calculation Tool/Volume Calculation Tool.mq5', 'folder': 'Trade Volume Calculation Tool', 'inputs': [{'mql': 'riskPercent', 'py': 'riskPercent', 'param': 'riskPercent', 'type': 'double', 'default': 2.0, 'label': 'Percentage to risk', 'sinput': False}, {'mql': 'posType', 'py': 'posType', 'param': 'posType', 'type': 'int', 'default': 0, 'label': 'Position Type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum PositionType
buy = 0
sell = 1
_enum('PositionType', {0: 'buy', 1: 'sell'})

# ---- inputs and global variables
riskPercent = _input('riskPercent', 2.0)  # Percentage to risk
posType = _input('posType', buy)  # Position Type
virtSL = Arr(0, 0.0)
bid = 0.0
ask = 0.0
BidAsk = 0.0
stopLoss = 0.0
lotSize = 0.0

def OnInit():
    global ask, bid
    SetIndexBuffer(0, virtSL, INDICATOR_DATA)
    bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ask = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
    ArraySetAsSeries(virtSL, True)
    Comment('Click on the chart at the desired stop loss level...')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global BidAsk, ask, bid
    bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ask = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
    ((BidAsk := ask) if (posType == buy) else (BidAsk := bid))
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global lotSize, stopLoss
    if id_ == CHARTEVENT_CLICK:
        all_bars = Bars(Symbol(), Period())
        for x in range(10, 0 - 1, -1):
            virtSL[x] = GetMouseY(dparam)
        for x in range(11, all_bars):
            virtSL[x] = EMPTY_VALUE
        stopLoss = MathAbs(BidAsk - GetMouseY(dparam))
        lotSize = LotSizeCalc(riskPercent, stopLoss)
        calculation = '.:: Position Volume Calculator ::.' + '\n\n' + 'Risking: ' + DoubleToString(riskPercent, 2) + '%' + '\n\n' + 'Lot size to use: ' + DoubleToString(lotSize, 2) + '\n' + 'Stop loss points: ' + DoubleToString(_fdiv(stopLoss, Point()), 2)
        Comment(calculation)

def GetMouseY(dparam):
    chartHeightInPixels = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    priceRange = ChartGetDouble(0, CHART_PRICE_MAX) - ChartGetDouble(0, CHART_PRICE_MIN)
    pixelsPerPrice = _fdiv(chartHeightInPixels, priceRange)
    mouseYValue = ChartGetDouble(0, CHART_PRICE_MAX) - _fdiv(dparam, pixelsPerPrice)
    return mouseYValue

def LotSizeCalc(riskPct, SLDistance):
    if riskPct < 0 or riskPct > 100:
        Print('Error: Invalid risk percentage')
        return -1.0
    freeMargin = AccountInfoDouble(ACCOUNT_MARGIN_FREE)
    tickSize = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_SIZE)
    tickValue = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_VALUE)
    volumeStep = SymbolInfoDouble(Symbol(), SYMBOL_VOLUME_STEP)
    minLot = SymbolInfoDouble(Symbol(), SYMBOL_VOLUME_MIN)
    maxLot = SymbolInfoDouble(Symbol(), SYMBOL_VOLUME_MAX)
    riskVolumeStep = _fdiv(SLDistance, tickSize) * tickValue * volumeStep
    risk = (riskPct * freeMargin) / 100
    lots = MathFloor(_fdiv(risk, riskVolumeStep)) * volumeStep
    if lots < minLot:
        lots = minLot
    if lots > maxLot:
        lots = maxLot
    return lots

def OnDeinit(reason):
    Comment('')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeCalculationTool(_MQL5Indicator):
    name = 'Volume Calculation Tool'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'riskPercent': 2.0,  # Percentage to risk
        'posType': _Choice({0: 'Buy', 1: 'Sell'}, default=0),  # Position Type
    }

