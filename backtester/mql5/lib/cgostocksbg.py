"""CGOStocksBG.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.object import *  # Object.mqh
from backtester.mql5.lib.stdliberr import *  # StdLibErr.mqh
from backtester.mql5.lib.cgstockasbg import *  # CGStockAsBG.mqh
from backtester.mql5.lib.cstock import *  # CStock.mqh
from backtester.mql5.lib.stockstruct import *  # StockStruct.mqh
from backtester.mql5.lib.cstockstyles import *  # CStockStyles.mqh
from backtester.mql5.lib.cgcanvas import *  # CGCanvas.mqh
from backtester.mql5.lib.cgraphbase import *  # CGraphBase.mqh
from backtester.mql5.lib.cglabel import *  # CGLabel.mqh


class CGOStocksBG(CObject):
    _q_fields = ('m_id', 'm_subwin', 'm_scheme', 'm_created', 'm_caption', 'm_dt_start', 'm_prefix', 'm_suffix', 'm_top_indent', 'm_bottom_indent', 'm_ydist', 'm_window_height', 'm_ptr_stock_bg0', 'm_ptr_stock_bg1', 'm_ptr_stock_bg2', 'm_ptr_stock_bg3', 'm_ptr_stock_bg4', 'm_ptr_stock_bg5', 'm_ptr_stock_bg6', 'm_ptr_stock_bg7', 'm_ptr_stock_bg8', 'm_ptr_stock_bg9', 'm_ptr_stock_bg10', 'm_ptr_stock_bg11', 'm_ptr_stock_bg12', 'm_ptr_stock_bg13', 'm_ptr_stock_bg14')
    _q_ptrs = ('m_ptr_stock_bg0', 'm_ptr_stock_bg1', 'm_ptr_stock_bg2', 'm_ptr_stock_bg3', 'm_ptr_stock_bg4', 'm_ptr_stock_bg5', 'm_ptr_stock_bg6', 'm_ptr_stock_bg7', 'm_ptr_stock_bg8', 'm_ptr_stock_bg9', 'm_ptr_stock_bg10', 'm_ptr_stock_bg11', 'm_ptr_stock_bg12', 'm_ptr_stock_bg13', 'm_ptr_stock_bg14',)
    def __init__(self, aDTime, aTop=0, aDown=20, aScheme=0, aPrefix='ST_', aSuffix='', aCaption=False, aID=0, aSubwin=0):
        CObject.__init__(self)
        self.m_id = 0
        self.m_subwin = 0
        self.m_scheme = 0
        self.m_created = False
        self.m_caption = False
        self.m_dt_start = 0
        self.m_prefix = ""
        self.m_suffix = ""
        self.m_top_indent = 0
        self.m_bottom_indent = 0
        self.m_ydist = Arr(15, 0, dyn=False)
        self.m_window_height = 0
        self.m_ptr_stock_bg0 = None
        self.m_ptr_stock_bg1 = None
        self.m_ptr_stock_bg2 = None
        self.m_ptr_stock_bg3 = None
        self.m_ptr_stock_bg4 = None
        self.m_ptr_stock_bg5 = None
        self.m_ptr_stock_bg6 = None
        self.m_ptr_stock_bg7 = None
        self.m_ptr_stock_bg8 = None
        self.m_ptr_stock_bg9 = None
        self.m_ptr_stock_bg10 = None
        self.m_ptr_stock_bg11 = None
        self.m_ptr_stock_bg12 = None
        self.m_ptr_stock_bg13 = None
        self.m_ptr_stock_bg14 = None
        self.m_created = False
        self.m_scheme = aScheme
        self.m_prefix = aPrefix
        self.m_suffix = aSuffix
        self.m_id = aID
        self.m_subwin = aSubwin
        self.m_caption = aCaption
        self.m_window_height = self.GetWindowHeight(self.m_id, self.m_subwin)
        self.m_top_indent = aTop
        self.m_bottom_indent = aDown
        self.m_dt_start = aDTime
        indent = 0
        band = 0
        free_space = 0
        free_space = self.m_window_height - 300 - self.m_top_indent - self.m_bottom_indent
        indent = _idiv(free_space, 16)
        band = _idiv(self.m_window_height, 15)
        self.m_ydist[0] = indent + self.m_top_indent
        for i in range(1, 15):
            self.m_ydist[i] = self.m_ydist[i - 1] + indent + 20
        self.m_ptr_stock_bg0 = CGStockAsBG(Tokio, self.m_dt_start, self.m_ydist[0], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg1 = CGStockAsBG(Singapore, self.m_dt_start, self.m_ydist[1], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg2 = CGStockAsBG(Shanghai, self.m_dt_start, self.m_ydist[2], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg3 = CGStockAsBG(Dubai, self.m_dt_start, self.m_ydist[3], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg4 = CGStockAsBG(Moscow, self.m_dt_start, self.m_ydist[4], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg5 = CGStockAsBG(London, self.m_dt_start, self.m_ydist[5], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg6 = CGStockAsBG(Zurich, self.m_dt_start, self.m_ydist[6], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg7 = CGStockAsBG(Frankfurt, self.m_dt_start, self.m_ydist[7], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg8 = CGStockAsBG(Yohannensburg, self.m_dt_start, self.m_ydist[8], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg9 = CGStockAsBG(Riyadh, self.m_dt_start, self.m_ydist[9], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg10 = CGStockAsBG(NewYork, self.m_dt_start, self.m_ydist[10], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg11 = CGStockAsBG(Toronto, self.m_dt_start, self.m_ydist[11], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg12 = CGStockAsBG(Chicago, self.m_dt_start, self.m_ydist[12], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg13 = CGStockAsBG(Wellington, self.m_dt_start, self.m_ydist[13], self.m_prefix, self.m_suffix, self.m_scheme)
        self.m_ptr_stock_bg14 = CGStockAsBG(Sidney, self.m_dt_start, self.m_ydist[14], self.m_prefix, self.m_suffix, self.m_scheme)
        if (((((((((((((self.m_ptr_stock_bg0.Created() and self.m_ptr_stock_bg1.Created()) and self.m_ptr_stock_bg2.Created()) and self.m_ptr_stock_bg3.Created()) and self.m_ptr_stock_bg4.Created()) and self.m_ptr_stock_bg5.Created()) and self.m_ptr_stock_bg6.Created()) and self.m_ptr_stock_bg7.Created()) and self.m_ptr_stock_bg8.Created()) and self.m_ptr_stock_bg9.Created()) and self.m_ptr_stock_bg10.Created()) and self.m_ptr_stock_bg11.Created()) and self.m_ptr_stock_bg12.Created()) and self.m_ptr_stock_bg13.Created()) and self.m_ptr_stock_bg14.Created():
            self.m_created = True
    def _q_dtor(self):
        self.DeInit()
    def GetWindowHeight(self, chart_ID=0, sub_window=0):
        result = Box(-1)
        ResetLastError()
        if not ChartGetInteger(chart_ID, CHART_HEIGHT_IN_PIXELS, sub_window, result):
            Print('CGOStocksBG::GetWindowHeight' + ', Error Code = ', GetLastError())
        return _int(result.v)
    def ProcessingStocks(self, aDTime):
        self.m_dt_start = aDTime
        self.m_window_height = self.GetWindowHeight(self.m_id, self.m_subwin)
        indent = 0
        band = 0
        free_space = 0
        free_space = self.m_window_height - 300 - self.m_top_indent - self.m_bottom_indent
        indent = _idiv(free_space, 16)
        band = _idiv(self.m_window_height, 15)
        self.m_ydist[0] = indent + self.m_top_indent
        for i in range(1, 15):
            self.m_ydist[i] = self.m_ydist[i - 1] + indent + 20
        if self.m_created:
            self.m_ptr_stock_bg0.SetPositionProps(self.m_dt_start, self.m_ydist[0])
            self.m_ptr_stock_bg0.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg1.SetPositionProps(self.m_dt_start, self.m_ydist[1])
            self.m_ptr_stock_bg1.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg2.SetPositionProps(self.m_dt_start, self.m_ydist[2])
            self.m_ptr_stock_bg2.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg3.SetPositionProps(self.m_dt_start, self.m_ydist[3])
            self.m_ptr_stock_bg3.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg4.SetPositionProps(self.m_dt_start, self.m_ydist[4])
            self.m_ptr_stock_bg4.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg5.SetPositionProps(self.m_dt_start, self.m_ydist[5])
            self.m_ptr_stock_bg5.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg6.SetPositionProps(self.m_dt_start, self.m_ydist[6])
            self.m_ptr_stock_bg6.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg7.SetPositionProps(self.m_dt_start, self.m_ydist[7])
            self.m_ptr_stock_bg7.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg8.SetPositionProps(self.m_dt_start, self.m_ydist[8])
            self.m_ptr_stock_bg8.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg9.SetPositionProps(self.m_dt_start, self.m_ydist[9])
            self.m_ptr_stock_bg9.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg10.SetPositionProps(self.m_dt_start, self.m_ydist[10])
            self.m_ptr_stock_bg10.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg11.SetPositionProps(self.m_dt_start, self.m_ydist[11])
            self.m_ptr_stock_bg11.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg12.SetPositionProps(self.m_dt_start, self.m_ydist[12])
            self.m_ptr_stock_bg12.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg13.SetPositionProps(self.m_dt_start, self.m_ydist[13])
            self.m_ptr_stock_bg13.ProcessingColor(self.m_dt_start)
            self.m_ptr_stock_bg14.SetPositionProps(self.m_dt_start, self.m_ydist[14])
            self.m_ptr_stock_bg14.ProcessingColor(self.m_dt_start)
    def SetPositionsDefaults(self):
        self.m_dt_start = TimeCurrent()
        if self.m_created:
            self.m_ptr_stock_bg0.SetPositionPropsXY()
            self.m_ptr_stock_bg1.SetPositionPropsXY()
            self.m_ptr_stock_bg2.SetPositionPropsXY()
            self.m_ptr_stock_bg3.SetPositionPropsXY()
            self.m_ptr_stock_bg4.SetPositionPropsXY()
            self.m_ptr_stock_bg5.SetPositionPropsXY()
            self.m_ptr_stock_bg6.SetPositionPropsXY()
            self.m_ptr_stock_bg7.SetPositionPropsXY()
            self.m_ptr_stock_bg8.SetPositionPropsXY()
            self.m_ptr_stock_bg9.SetPositionPropsXY()
            self.m_ptr_stock_bg10.SetPositionPropsXY()
            self.m_ptr_stock_bg11.SetPositionPropsXY()
            self.m_ptr_stock_bg12.SetPositionPropsXY()
            self.m_ptr_stock_bg13.SetPositionPropsXY()
            self.m_ptr_stock_bg14.SetPositionPropsXY()
    def ReDraw(self):
        ChartRedraw(self.m_id)
    def Created(self):
        return self.m_created
    def DeInit(self):
        _delete(self.m_ptr_stock_bg0)
        _delete(self.m_ptr_stock_bg1)
        _delete(self.m_ptr_stock_bg2)
        _delete(self.m_ptr_stock_bg3)
        _delete(self.m_ptr_stock_bg4)
        _delete(self.m_ptr_stock_bg5)
        _delete(self.m_ptr_stock_bg6)
        _delete(self.m_ptr_stock_bg7)
        _delete(self.m_ptr_stock_bg8)
        _delete(self.m_ptr_stock_bg9)
        _delete(self.m_ptr_stock_bg10)
        _delete(self.m_ptr_stock_bg11)
        _delete(self.m_ptr_stock_bg12)
        _delete(self.m_ptr_stock_bg13)
        _delete(self.m_ptr_stock_bg14)

__all__ = ['CGOStocksBG']
