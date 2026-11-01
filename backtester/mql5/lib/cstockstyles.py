"""CStockStyles.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.stockstruct import *  # StockStruct.mqh


class CStockStyles(MqlObject):
    _q_fields = ('m_style', 'm_scheme', 'm_created')
    def __init__(self, scheme=0):
        self.m_style = Arr(2, 0, dyn=False, factory=SBackground)
        self.m_scheme = 0
        self.m_created = False
        self.m_scheme = scheme
        self.m_created = True
    def _q_dtor(self):
        self.Deinit()
    def Deinit(self):
        pass
    def InitDefaults(self):
        _sw1 = self.m_scheme
        if _sw1 == 0:
            self.m_style[self.m_scheme].FontNameV = 'Times New Roman'
            self.m_style[self.m_scheme].FontSizeV = 12
            self.m_style[self.m_scheme].FontNameH = 'Arial'
            self.m_style[self.m_scheme].FontSizeH = 10
            self.m_style[self.m_scheme].cFgTextActive = 0x646464
            self.m_style[self.m_scheme].cFgTextSleep = 0x323232
            self.m_style[self.m_scheme].cBgRectActive = 0x1E1E1E
            self.m_style[self.m_scheme].cBgRectSleep = 0x0F0F0F
            self.m_style[self.m_scheme].iStockCanvasH = 20
            self.m_style[self.m_scheme].iStockLabelIndH = 1
            self.m_style[self.m_scheme].iStockLabelIndL = 5
            self.m_style[self.m_scheme].iStockLabelIndW = 10
        elif _sw1 == 1:
            self.m_style[self.m_scheme].FontNameV = 'Times New Roman'
            self.m_style[self.m_scheme].FontSizeV = 12
            self.m_style[self.m_scheme].FontNameH = 'Arial'
            self.m_style[self.m_scheme].FontSizeH = 10
            self.m_style[self.m_scheme].cFgTextActive = 0x9B9B9B
            self.m_style[self.m_scheme].cFgTextSleep = 0xCDCDCD
            self.m_style[self.m_scheme].cBgRectActive = 0xE1E1E1
            self.m_style[self.m_scheme].cBgRectSleep = 0xF0F0F0
            self.m_style[self.m_scheme].iStockCanvasH = 20
            self.m_style[self.m_scheme].iStockLabelIndH = 1
            self.m_style[self.m_scheme].iStockLabelIndL = 5
            self.m_style[self.m_scheme].iStockLabelIndW = 10
    def FontSizeV(self):
        return self.m_style[self.m_scheme].FontSizeV
    def FontSizeH(self):
        return self.m_style[self.m_scheme].FontSizeH
    def FontNameV(self):
        return self.m_style[self.m_scheme].FontNameV
    def FontNameH(self):
        return self.m_style[self.m_scheme].FontNameH
    def StockCanvasH(self):
        return self.m_style[self.m_scheme].iStockCanvasH
    def StockLabelIndH(self):
        return self.m_style[self.m_scheme].iStockLabelIndH
    def StockLabelIndL(self):
        return self.m_style[self.m_scheme].iStockLabelIndL
    def StockLabelIndW(self):
        return self.m_style[self.m_scheme].iStockLabelIndW
    def BgRectActive(self):
        return self.m_style[self.m_scheme].cBgRectActive
    def BgRectSleep(self):
        return self.m_style[self.m_scheme].cBgRectSleep
    def FgTextActive(self):
        return self.m_style[self.m_scheme].cFgTextActive
    def FgTextSleep(self):
        return self.m_style[self.m_scheme].cFgTextSleep
    def Created(self):
        return self.m_created

__all__ = ['CStockStyles']
