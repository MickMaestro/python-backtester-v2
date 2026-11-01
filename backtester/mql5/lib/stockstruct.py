"""StockStruct.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *

# enum STOCK_NAME
Tokio = 0
Singapore = 1
Shanghai = 2
Dubai = 3
Moscow = 4
London = 5
Zurich = 6
Frankfurt = 7
Yohannensburg = 8
Riyadh = 9
NewYork = 10
Toronto = 11
Chicago = 12
Wellington = 13
Sidney = 14
_enum('STOCK_NAME', {0: 'Tokio', 1: 'Singapore', 2: 'Shanghai', 3: 'Dubai', 4: 'Moscow', 5: 'London', 6: 'Zurich', 7: 'Frankfurt', 8: 'Yohannensburg', 9: 'Riyadh', 10: 'NewYork', 11: 'Toronto', 12: 'Chicago', 13: 'Wellington', 14: 'Sidney'})


class SBackground(MqlObject):
    _q_fields = ('FontSizeV', 'FontSizeH', 'FontNameV', 'FontNameH', 'nPrefix', 'iStockCanvasH', 'iStockLabelIndH', 'iStockLabelIndL', 'iStockLabelIndW', 'cFgTextActive', 'cFgTextSleep', 'cBgRectActive', 'cBgRectSleep')
    def __init__(self, *args):
        self.FontSizeV = 0
        self.FontSizeH = 0
        self.FontNameV = ""
        self.FontNameH = ""
        self.nPrefix = ""
        self.iStockCanvasH = 0
        self.iStockLabelIndH = 0
        self.iStockLabelIndL = 0
        self.iStockLabelIndW = 0
        self.cFgTextActive = 0
        self.cFgTextSleep = 0
        self.cBgRectActive = 0
        self.cBgRectSleep = 0

__all__ = ['Tokio', 'Singapore', 'Shanghai', 'Dubai', 'Moscow', 'London', 'Zurich', 'Frankfurt', 'Yohannensburg', 'Riyadh', 'NewYork', 'Toronto', 'Chicago', 'Wellington', 'Sidney', 'SBackground']
