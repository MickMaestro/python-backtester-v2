"""CGStockAsBG.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.cstock import *  # CStock.mqh
from backtester.mql5.lib.stockstruct import *  # StockStruct.mqh
from backtester.mql5.lib.cstockstyles import *  # CStockStyles.mqh
from backtester.mql5.lib.cgcanvas import *  # CGCanvas.mqh
from backtester.mql5.lib.cgraphbase import *  # CGraphBase.mqh
from backtester.mql5.lib.cglabel import *  # CGLabel.mqh


class CGStockAsBG(MqlObject):
    _q_fields = ('m_id', 'm_subwin', 'm_scheme', 'm_created', 'm_stock', 'm_dt_start', 'm_name_label', 'm_name_canvas', 'm_text_label', 'm_prefix', 'm_suffix', 'm_xdist', 'm_ydist', 'm_xsize', 'm_ysize', 'm_xshift', 'm_yshift', 'm_time_pos', 'm_caps', 'm_color_bg_sleep', 'm_color_bg_active', 'm_color_fg_active', 'm_color_fg_sleep', 'm_font_size', 'm_font_name', 'm_dt_open', 'm_dt_close', 'm_ptr_stock', 'm_ptr_style', 'm_ptr_canvas', 'm_ptr_label', 'm_stock_bg')
    _q_ptrs = ('m_ptr_stock', 'm_ptr_style', 'm_ptr_canvas', 'm_ptr_label', 'm_stock_bg',)
    def __init__(self, aStock=Tokio, aTStart=0, aTop=0, aPrefix='', aSuffix='', aScheme=0, aCapsOn=False, aID=0, aSubwin=0):
        self.m_id = 0
        self.m_subwin = 0
        self.m_scheme = 0
        self.m_created = False
        self.m_stock = 0
        self.m_dt_start = 0
        self.m_name_label = ""
        self.m_name_canvas = ""
        self.m_text_label = ""
        self.m_prefix = ""
        self.m_suffix = ""
        self.m_xdist = 0
        self.m_ydist = 0
        self.m_xsize = 0
        self.m_ysize = 0
        self.m_xshift = 0
        self.m_yshift = 0
        self.m_time_pos = 0
        self.m_caps = False
        self.m_color_bg_sleep = 0
        self.m_color_bg_active = 0
        self.m_color_fg_active = 0
        self.m_color_fg_sleep = 0
        self.m_font_size = 0
        self.m_font_name = ""
        self.m_dt_open = 0
        self.m_dt_close = 0
        self.m_ptr_stock = None
        self.m_ptr_style = None
        self.m_ptr_canvas = None
        self.m_ptr_label = None
        self.m_stock_bg = None
        stock_created = False
        canvas_created = False
        label_created = False
        styles_created = False
        self.m_created = False
        self.m_scheme = aScheme
        self.m_id = aID
        self.m_subwin = aSubwin
        self.m_stock = aStock
        self.m_dt_start = aTStart
        self.m_ydist = aTop
        self.m_caps = aCapsOn
        self.m_prefix = aPrefix
        self.m_ptr_stock = CStock(self.m_stock, self.m_caps)
        if self.m_ptr_stock.Created():
            stock_created = True
            self.m_name_canvas = aPrefix + self.m_ptr_stock.StockName('Cvs_') + aSuffix
            self.m_name_label = aPrefix + self.m_ptr_stock.StockName('Lbl_') + aSuffix
        else:
            ResetLastError()
            Print('CGStockAsBG::CGStockAsBG', '. Error while CStock created. Code: ', GetLastError())
        self.m_ptr_canvas = CGCanvas(self.m_name_canvas, self.m_id, self.m_subwin)
        if self.m_ptr_canvas.Created():
            canvas_created = True
        else:
            ResetLastError()
            Print('CGStockAsBG::CGStockAsBG', '. Error while CGCanvas created. Code: ', GetLastError())
        self.m_ptr_label = CGLabel(self.m_name_label, self.m_id, self.m_subwin)
        if self.m_ptr_label.Created():
            label_created = True
        else:
            ResetLastError()
            Print('CGStockAsBG::CGStockAsBG', '. Error while CGLabel created. Code: ', GetLastError())
        self.m_ptr_style = CStockStyles(self.m_scheme)
        if self.m_ptr_style.Created():
            styles_created = True
        else:
            ResetLastError()
            Print('CGStockAsBG::CGStockAsBG', '. Error while CStockStyles created. Code: ', GetLastError())
        if ((stock_created and canvas_created) and label_created) and styles_created:
            ResetLastError()
            self.m_ydist = 10
            ChartTimePriceToXY(self.m_id, self.m_subwin, self.m_dt_start, SYMBOL_ASK, _AttrRef(self, 'm_xdist'), _AttrRef(self, 'm_ydist'))
            self.m_ydist = aTop
            self.m_created = True
        self.m_ptr_style.InitDefaults()
        self.m_color_bg_active = self.m_ptr_style.BgRectActive()
        self.m_color_bg_sleep = self.m_ptr_style.BgRectSleep()
        self.m_color_fg_active = self.m_ptr_style.FgTextActive()
        self.m_color_fg_sleep = self.m_ptr_style.FgTextSleep()
        self.m_font_name = self.m_ptr_style.FontNameH()
        self.m_font_size = self.m_ptr_style.FontSizeH()
        self.SetNonPositionProps()
    def _q_dtor(self):
        _delete(self.m_ptr_stock)
        _delete(self.m_ptr_canvas)
        _delete(self.m_ptr_label)
        _delete(self.m_ptr_style)
    def SetPositionProps(self, aTime, aTop=0):
        a_temp = Box(0)
        canvas_left = Box(0)
        canvas_right = Box(0)
        canvas_top = 0
        canvas_width = 0
        canvas_height = 0
        label_left = 0
        label_top = 0
        label_width = 0
        label_height = 0
        label_text = ""
        self.m_dt_start = aTime
        self.m_ptr_stock.StockShedule(self.m_dt_start, _AttrRef(self, 'm_dt_open'), _AttrRef(self, 'm_dt_close'))
        ChartTimePriceToXY(self.m_id, self.m_subwin, self.m_dt_open, SYMBOL_ASK, canvas_left, a_temp)
        canvas_top = aTop
        canvas_height = self.m_ptr_style.StockCanvasH()
        ChartTimePriceToXY(self.m_id, self.m_subwin, self.m_dt_close, SYMBOL_ASK, canvas_right, a_temp)
        canvas_width = MathAbs(canvas_right.v - canvas_left.v)
        self.m_ptr_canvas.SetXDist(canvas_left.v)
        self.m_ptr_canvas.SetYDist(canvas_top)
        self.m_ptr_canvas.SetXSize(canvas_width)
        self.m_ptr_canvas.SetYSize(canvas_height)
        label_left = canvas_left.v + self.m_ptr_style.StockLabelIndL()
        label_top = canvas_top + self.m_ptr_style.StockLabelIndH()
        label_width = canvas_width - self.m_ptr_style.StockLabelIndW()
        label_height = canvas_height - (self.m_ptr_style.StockLabelIndH() * 2)
        label_text = self.m_ptr_stock.StockText(self.m_caps)
        self.m_ptr_label.SetXDist(label_left)
        self.m_ptr_label.SetYDist(label_top)
        self.m_ptr_label.SetXSize(label_width)
        self.m_ptr_label.SetYSize(label_top)
        self.m_ptr_label.SetText(label_text)
    def SetPositionPropsXY(self, aLeft=0, aTop=0, aWidth=100):
        canvas_left = aLeft
        canvas_top = aTop
        canvas_width = aWidth
        canvas_height = self.m_ptr_style.StockCanvasH()
        label_left = 0
        label_top = 0
        label_width = 0
        label_height = 0
        self.m_ptr_canvas.SetXDist(canvas_left)
        self.m_ptr_canvas.SetYDist(canvas_top)
        self.m_ptr_canvas.SetXSize(canvas_width)
        self.m_ptr_canvas.SetYSize(canvas_height)
        label_left = canvas_left + self.m_ptr_style.StockLabelIndL()
        label_top = canvas_top + self.m_ptr_style.StockLabelIndH()
        label_width = canvas_width - self.m_ptr_style.StockLabelIndW()
        label_height = canvas_height - (self.m_ptr_style.StockLabelIndH() * 2)
        self.m_ptr_label.SetXDist(label_left)
        self.m_ptr_label.SetYDist(label_top)
        self.m_ptr_label.SetXSize(label_width)
        self.m_ptr_label.SetYSize(label_top)
        self.m_ptr_label.SetText(self.m_ptr_stock.StockText(self.m_caps))
    def SetNonPositionProps(self):
        self.m_ptr_canvas.SetColorBG(self.m_color_bg_sleep)
        self.m_ptr_canvas.SetColorBorder(self.m_color_bg_sleep)
        self.m_ptr_canvas.SetCorner()
        self.m_ptr_canvas.SetFontName(self.m_font_name)
        self.m_ptr_canvas.SetFontSize(self.m_font_size)
        self.m_ptr_canvas.SetSelected()
        self.m_ptr_canvas.SetSelectable()
        self.m_ptr_canvas.SetReadOnly()
        self.m_ptr_canvas.SetBack(True)
        self.m_ptr_canvas.SetZOrder()
        self.m_ptr_canvas.SetHidden()
        self.m_ptr_label.SetColorText(self.m_color_fg_sleep)
        self.m_ptr_label.SetCorner()
        self.m_ptr_label.SetAnchor()
        self.m_ptr_label.SetAngle()
        self.m_ptr_label.SetFontName(self.m_font_name)
        self.m_ptr_label.SetFontSize(self.m_font_size)
        self.m_ptr_label.SetSelected()
        self.m_ptr_label.SetSelectable()
        self.m_ptr_label.SetBack(True)
        self.m_ptr_label.SetZOrder()
        self.m_ptr_label.SetHidden()
    def SetActiveColors(self):
        self.m_ptr_canvas.SetColorBG(self.m_color_bg_active)
        self.m_ptr_canvas.SetColorBorder(self.m_color_bg_active)
        self.m_ptr_label.SetColorText(self.m_color_fg_active)
    def SetSleepColors(self):
        self.m_ptr_canvas.SetColorBG(self.m_color_bg_sleep)
        self.m_ptr_canvas.SetColorBorder(self.m_color_bg_sleep)
        self.m_ptr_label.SetColorText(self.m_color_fg_sleep)
    def ProcessingColor(self, aTime, aTimeCurrent=True):
        if self.CheckActive(aTime, aTimeCurrent):
            self.SetActiveColors()
        else:
            self.SetSleepColors()
    def ReDraw(self):
        ChartRedraw(self.m_id)
    def CheckActive(self, aTime, aTimeCurrent=True):
        if aTimeCurrent:
            if TimeCurrent() >= self.m_dt_open and TimeCurrent() <= self.m_dt_close:
                return True
            else:
                return False
        else:
            if aTime >= self.m_dt_open and aTime <= self.m_dt_close:
                return True
            else:
                return False
    def Created(self):
        return self.m_created

__all__ = ['CGStockAsBG']
