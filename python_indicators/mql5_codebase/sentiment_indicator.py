"""Sentiment_Indicator — converted from MQL5: MQL5 Indicators/Sentiment/Sentiment_Indicator.mq5

Copyright: Copyright 2015, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2015, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Sentiment_Indicator', 'source': 'MQL5 Indicators/Sentiment/Sentiment_Indicator.mq5', 'folder': 'Sentiment', 'inputs': [{'mql': 'MinVolume', 'py': 'MinVolume', 'param': 'MinVolume', 'type': 'int', 'default': 10000, 'label': 'Мин. объем ордеров', 'sinput': False}, {'mql': 'MinTraders', 'py': 'MinTraders', 'param': 'MinTraders', 'type': 'int', 'default': 150, 'label': 'Мин. кол-во ордеров', 'sinput': False}, {'mql': 'DiffVolumes', 'py': 'DiffVolumes', 'param': 'DiffVolumes', 'type': 'double', 'default': 2.0, 'label': 'Разница объемов ордеров', 'sinput': False}, {'mql': 'DiffTraders', 'py': 'DiffTraders', 'param': 'DiffTraders', 'type': 'double', 'default': 1.5, 'label': 'Разница ордеров', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

SYMBOL_SESSION_BUY_ORDERS = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_BUY_ORDERS_VOLUME = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_SELL_ORDERS = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_SELL_ORDERS_VOLUME = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
MinVolume = _input('MinVolume', 10000)  # Мин. объем ордеров
MinTraders = _input('MinTraders', 150)  # Мин. кол-во ордеров
DiffVolumes = _input('DiffVolumes', 2.0)  # Разница объемов ордеров
DiffTraders = _input('DiffTraders', 1.5)  # Разница ордеров

def OnInit():
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, 'chart-text')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    BUYorders = SymbolInfoInteger(Symbol(), SYMBOL_SESSION_BUY_ORDERS)
    if BUYorders == 0:
        BUYorders = 1
    SELLorders = SymbolInfoInteger(Symbol(), SYMBOL_SESSION_SELL_ORDERS)
    if SELLorders == 0:
        SELLorders = 1
    BUYvolume = SymbolInfoDouble(Symbol(), SYMBOL_SESSION_BUY_ORDERS_VOLUME)
    if BUYvolume == 0:
        BUYvolume = 1.0
    SELLvolume = SymbolInfoDouble(Symbol(), SYMBOL_SESSION_SELL_ORDERS_VOLUME)
    if SELLvolume == 0:
        SELLvolume = 1.0
    DiffTradersCurr = _fdiv(float(BUYorders), float(SELLorders))
    DiffVolumesCurr = _fdiv(BUYvolume, SELLvolume)
    if ((DiffVolumesCurr >= DiffVolumes and DiffTradersCurr >= DiffTraders) and (SymbolInfoInteger(Symbol(), SYMBOL_SESSION_BUY_ORDERS) >= MinTraders or SymbolInfoInteger(Symbol(), SYMBOL_SESSION_SELL_ORDERS) >= MinTraders)) and (SymbolInfoDouble(Symbol(), SYMBOL_SESSION_BUY_ORDERS_VOLUME) >= MinVolume or SymbolInfoDouble(Symbol(), SYMBOL_SESSION_SELL_ORDERS_VOLUME) >= MinVolume):
        DisplayTextOnChart('chart-text', 'Интерес: BUY', clrMidnightBlue)
    else:
        DiffTradersCurr = _fdiv(float(SELLorders), float(BUYorders))
        DiffVolumesCurr = _fdiv(SELLvolume, BUYvolume)
        if ((DiffVolumesCurr >= DiffVolumes and DiffTradersCurr >= DiffTraders) and (SymbolInfoInteger(Symbol(), SYMBOL_SESSION_BUY_ORDERS) >= MinTraders or SymbolInfoInteger(Symbol(), SYMBOL_SESSION_SELL_ORDERS) >= MinTraders)) and (SymbolInfoDouble(Symbol(), SYMBOL_SESSION_BUY_ORDERS_VOLUME) >= MinVolume or SymbolInfoDouble(Symbol(), SYMBOL_SESSION_SELL_ORDERS_VOLUME) >= MinVolume):
            DisplayTextOnChart('chart-text', 'Интерес: SELL', clrFireBrick)
        else:
            DisplayTextOnChart('chart-text', 'Интерес: ---', clrLawnGreen)
    return rates_total

def DisplayTextOnChart(objetName, textToDisplay, textColor, xPos=10, yPos=20):
    if ObjectFind(0, objetName) < 0:
        ObjectCreate(0, objetName, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, objetName, OBJPROP_XDISTANCE, xPos)
    ObjectSetInteger(0, objetName, OBJPROP_YDISTANCE, yPos)
    ObjectSetString(0, objetName, OBJPROP_TEXT, textToDisplay)
    ObjectSetString(0, objetName, OBJPROP_FONT, 'Verdana')
    ObjectSetInteger(0, objetName, OBJPROP_COLOR, textColor)
    ObjectSetInteger(0, objetName, OBJPROP_FONTSIZE, 10)
    ObjectSetInteger(0, objetName, OBJPROP_SELECTABLE, False)
    ChartRedraw(0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SentimentIndicator(_MQL5Indicator):
    name = 'Sentiment_Indicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MinVolume': 10000,  # Мин. объем ордеров
        'MinTraders': 150,  # Мин. кол-во ордеров
        'DiffVolumes': 2.0,  # Разница объемов ордеров
        'DiffTraders': 1.5,  # Разница ордеров
    }

