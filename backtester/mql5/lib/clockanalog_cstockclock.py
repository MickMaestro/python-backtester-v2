"""CStockClock.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.clockanalog_stockclockenums import *  # StockClockEnums.mqh
from backtester.mql5.lib.clockanalog_cgtrendline import *  # CGTrendLine.mqh
from backtester.mql5.lib.clockanalog_cgraphbase import *  # CGraphBase.mqh
from backtester.mql5.lib.clockanalog_cgbitmaplabel import *  # CGBitmapLabel.mqh
from backtester.mql5.lib.clockanalog_cglabel import *  # CGLabel.mqh
from backtester.mql5.lib.clockanalog_cgbutton import *  # CGButton.mqh


class CStockClock(MqlObject):
    _q_fields = ('m_dst_event', 'm_folder', 'm_name_back', 'm_name_move', 'm_name_hide', 'm_scheme', 'm_x', 'm_y', 'm_width', 'm_height', 'm_x0', 'm_y0', 'm_x0_rel', 'm_y0_rel', 'm_radius_hh', 'm_radius_mh', 'm_radius_sh', 'm_xmove', 'm_ymove', 'm_xback', 'm_yback', 'm_xhide', 'm_yhide', 'm_x_label', 'm_y_label', 'm_xmove_rel', 'm_ymove_rel', 'm_xback_rel', 'm_yback_rel', 'm_xhide_rel', 'm_yhide_rel', 'm_x_label_rel', 'm_y_label_rel', 'm_xcpt_rel', 'm_ycpt_rel', 'm_xhidden', 'm_yhidden', 'm_button_width', 'm_button_height', 'm_header_height', 'm_xboundary', 'm_yboundary', 'm_dt0', 'm_dt_hh', 'm_dt_mh', 'm_dt_sh', 'm_pr0', 'm_pr_hh', 'm_pr_mh', 'm_pr_sh', 'm_tmd', 'm_show_second_hand', 'm_clock_hidden', 'm_error_position', 'm_debug_on', 'm_bcolor', 'm_wcolor', 'm_secstyle', 'm_clock_skin', 'm_header', 'm_hand_second', 'm_hand_minute', 'm_hand_hour', 'm_clockname', 'm_button_move', 'm_button_back', 'm_button_hide')
    _q_ptrs = ('m_clock_skin', 'm_header', 'm_hand_second', 'm_hand_minute', 'm_hand_hour', 'm_clockname', 'm_button_move', 'm_button_back', 'm_button_hide',)
    def __init__(self, x, y, folder, show_second_hand=False, scheme=black):
        self.m_dst_event = 0
        self.m_folder = ""
        self.m_name_back = ""
        self.m_name_move = ""
        self.m_name_hide = ""
        self.m_scheme = 0
        self.m_x = 0
        self.m_y = 0
        self.m_width = 0
        self.m_height = 0
        self.m_x0 = 0
        self.m_y0 = 0
        self.m_x0_rel = 0
        self.m_y0_rel = 0
        self.m_radius_hh = 0
        self.m_radius_mh = 0
        self.m_radius_sh = 0
        self.m_xmove = 0
        self.m_ymove = 0
        self.m_xback = 0
        self.m_yback = 0
        self.m_xhide = 0
        self.m_yhide = 0
        self.m_x_label = 0
        self.m_y_label = 0
        self.m_xmove_rel = 0
        self.m_ymove_rel = 0
        self.m_xback_rel = 0
        self.m_yback_rel = 0
        self.m_xhide_rel = 0
        self.m_yhide_rel = 0
        self.m_x_label_rel = 0
        self.m_y_label_rel = 0
        self.m_xcpt_rel = 0
        self.m_ycpt_rel = 0
        self.m_xhidden = 0
        self.m_yhidden = 0
        self.m_button_width = 0
        self.m_button_height = 0
        self.m_header_height = 0
        self.m_xboundary = 0
        self.m_yboundary = 0
        self.m_dt0 = 0
        self.m_dt_hh = 0
        self.m_dt_mh = 0
        self.m_dt_sh = 0
        self.m_pr0 = 0.0
        self.m_pr_hh = 0.0
        self.m_pr_mh = 0.0
        self.m_pr_sh = 0.0
        self.m_tmd = 0
        self.m_show_second_hand = False
        self.m_clock_hidden = False
        self.m_error_position = False
        self.m_debug_on = False
        self.m_bcolor = 0
        self.m_wcolor = 0
        self.m_secstyle = 0
        self.m_clock_skin = None
        self.m_header = None
        self.m_hand_second = None
        self.m_hand_minute = None
        self.m_hand_hour = None
        self.m_clockname = None
        self.m_button_move = None
        self.m_button_back = None
        self.m_button_hide = None
        self.m_x = x
        self.m_y = y
        self.m_width = 401
        self.m_height = 400
        self.m_x0_rel = 200
        self.m_y0_rel = 220
        self.m_xmove_rel = 1
        self.m_ymove_rel = 1
        self.m_xback_rel = 382
        self.m_yback_rel = 1
        self.m_xhide_rel = 364
        self.m_yhide_rel = 1
        self.m_x_label_rel = 200
        self.m_y_label_rel = 10
        self.m_x0 = x + self.m_x0_rel
        self.m_y0 = y + self.m_y0_rel
        self.m_radius_hh = 119
        self.m_radius_mh = 159
        self.m_radius_sh = 159
        self.m_button_height = 17
        self.m_button_width = 17
        self.m_header_height = 20
        self.m_xcpt_rel = 6
        self.m_ycpt_rel = 6
        self.m_clock_hidden = False
        self.m_xhidden = 0
        self.m_bcolor = clrGreenYellow
        self.m_wcolor = clrDarkOrange
        self.m_secstyle = STYLE_SOLID
        result = Box(-1)
        ResetLastError()
        if not ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, 0, result):
            Print('CStockClock::CStockClock', ': CHART_HEIGHT_IN_PIXELS. Error Code = ', GetLastError())
        self.m_yboundary = _int(result.v)
        self.m_yhidden = -500
        result.v = -1
        ResetLastError()
        if not ChartGetInteger(0, CHART_WIDTH_IN_PIXELS, 0, result):
            Print('CStockClock::CStockClock', ': CHART_WIDTH_IN_PIXELS. Error Code = ', GetLastError())
        self.m_xboundary = _int(result.v)
        self.m_folder = '//Images//' + folder + '//'
        self.m_show_second_hand = show_second_hand
        self.m_scheme = scheme
        self.m_clock_skin = CGBitmapLabel('ClockStockSkin')
        self.m_header = CGBitmapLabel('ClockHeader')
        self.m_hand_second = CGTrendline('ClockHandSecond')
        self.m_hand_minute = CGTrendline('ClockHandMinute')
        self.m_hand_hour = CGTrendline('ClockHandHour')
        self.m_clockname = CGLabel('ClockNameLabel')
        self.m_name_move = 'ClockButtonMove'
        self.m_name_back = 'ClockButtonBack'
        self.m_name_hide = 'ClockButtonHide'
        self.m_button_move = CGButton(self.m_name_move)
        self.m_button_back = CGButton(self.m_name_back)
        self.m_button_hide = CGButton(self.m_name_hide)
        self.m_debug_on = False
    def _q_dtor(self):
        _delete(self.m_clock_skin)
        _delete(self.m_header)
        _delete(self.m_hand_second)
        _delete(self.m_hand_minute)
        _delete(self.m_hand_hour)
        _delete(self.m_button_move)
        _delete(self.m_button_back)
        _delete(self.m_button_hide)
        _delete(self.m_clockname)
    def DstEventFileBlack(self):
        file_name = self.m_folder + 'clock_analog_error_999.bmp'
        h60m = 0
        time = 0
        stmG = MqlDateTime()
        stm = MqlDateTime()
        if not self.m_debug_on:
            time = TimeGMT()
            TimeToStruct(time, stm)
        else:
            time = self.m_tmd
            TimeToStruct(TimeGMT(), stmG)
            TimeToStruct(self.m_tmd, stm)
            stm.hour = stmG.hour
            stm.min = stmG.min
            stm.sec = stmG.sec
        h60m = (stm.hour * 60) + stm.min
        _sw1 = self.m_dst_event
        if _sw1 == dst_111:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_0100.bmp'
            if h60m >= 90 and h60m < 225:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_0130.bmp'
            if h60m >= 225 and h60m < 300:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_0345.bmp'
            if h60m >= 300 and h60m < 360:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_0500.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_1000.bmp'
            if h60m >= 750 and h60m < 870:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_1230.bmp'
            if h60m >= 870 and h60m < 900:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_1430.bmp'
            if h60m >= 900 and h60m < 945:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_1500.bmp'
            if h60m >= 945 and h60m < 990:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_1545.bmp'
            if h60m >= 990 and h60m < 1260:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_1630.bmp'
            if h60m >= 1260 and h60m < 1380:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_2100.bmp'
            if h60m >= 1380 and h60m < 1440:
                file_name = self.m_folder + '111//' + 'clock_analog_black_111_2300.bmp'
        elif _sw1 == dst_203:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0100.bmp'
            if h60m >= 90 and h60m < 225:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0130.bmp'
            if h60m >= 225 and h60m < 300:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0345.bmp'
            if h60m >= 300 and h60m < 360:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0500.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_1000.bmp'
            if h60m >= 750 and h60m < 810:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_1230.bmp'
            if h60m >= 810 and h60m < 900:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_1330.bmp'
            if h60m >= 900 and h60m < 945:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_1500.bmp'
            if h60m >= 945 and h60m < 990:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_1545.bmp'
            if h60m >= 990 and h60m < 1200:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_1630.bmp'
            if h60m >= 1200 and h60m < 1260:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_2000.bmp'
            if h60m >= 1260 and h60m < 1380:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_2100.bmp'
            if h60m >= 1380 and h60m < 1440:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_2300.bmp'
        elif _sw1 == dst_403:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_0100.bmp'
            if h60m >= 90 and h60m < 225:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_0130.bmp'
            if h60m >= 225 and h60m < 300:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_0345.bmp'
            if h60m >= 300 and h60m < 360:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_0500.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_1000.bmp'
            if h60m >= 750 and h60m < 810:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_1230.bmp'
            if h60m >= 810 and h60m < 900:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_1330.bmp'
            if h60m >= 900 and h60m < 930:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_1500.bmp'
            if h60m >= 930 and h60m < 945:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_1530.bmp'
            if h60m >= 945 and h60m < 1200:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_1545.bmp'
            if h60m >= 1200 and h60m < 1260:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_2000.bmp'
            if h60m >= 1260 and h60m < 1380:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_2100.bmp'
            if h60m >= 1380 and h60m < 1440:
                file_name = self.m_folder + '403//' + 'clock_analog_black_403_2300.bmp'
        elif _sw1 == dst_104:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_0100.bmp'
            if h60m >= 90 and h60m < 285:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_0130.bmp'
            if h60m >= 285 and h60m < 360:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_0445.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_1000.bmp'
            if h60m >= 750 and h60m < 810:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_1230.bmp'
            if h60m >= 810 and h60m < 900:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_1330.bmp'
            if h60m >= 900 and h60m < 930:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_1500.bmp'
            if h60m >= 930 and h60m < 945:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_1530.bmp'
            if h60m >= 945 and h60m < 1200:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_1545.bmp'
            if h60m >= 1200 and h60m < 1320:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_2000.bmp'
            if h60m >= 1320 and h60m < 1440:
                file_name = self.m_folder + '104//' + 'clock_analog_black_104_2200.bmp'
        elif _sw1 == dst_409:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_0100.bmp'
            if h60m >= 90 and h60m < 225:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_0130.bmp'
            if h60m >= 225 and h60m < 360:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_0345.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_1000.bmp'
            if h60m >= 750 and h60m < 810:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_1230.bmp'
            if h60m >= 810 and h60m < 900:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_1330.bmp'
            if h60m >= 900 and h60m < 930:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_1500.bmp'
            if h60m >= 930 and h60m < 945:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_1530.bmp'
            if h60m >= 945 and h60m < 1200:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_1545.bmp'
            if h60m >= 1200 and h60m < 1260:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_2000.bmp'
            if h60m >= 1260 and h60m < 1440:
                file_name = self.m_folder + '409//' + 'clock_analog_black_409_2100.bmp'
        elif _sw1 == dst_110:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_0100.bmp'
            if h60m >= 90 and h60m < 225:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_0130.bmp'
            if h60m >= 225 and h60m < 300:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_0345.bmp'
            if h60m >= 300 and h60m < 360:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_0500.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_1000.bmp'
            if h60m >= 750 and h60m < 810:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_1230.bmp'
            if h60m >= 810 and h60m < 900:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_1330.bmp'
            if h60m >= 900 and h60m < 930:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_1500.bmp'
            if h60m >= 930 and h60m < 945:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_1530.bmp'
            if h60m >= 945 and h60m < 1200:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_1545.bmp'
            if h60m >= 1200 and h60m < 1260:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_2000.bmp'
            if h60m >= 1260 and h60m < 1380:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_2100.bmp'
            if h60m >= 1380 and h60m < 1440:
                file_name = self.m_folder + '110//' + 'clock_analog_black_110_2300.bmp'
        elif _sw1 == dst_410:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0100.bmp'
            if h60m >= 90 and h60m < 225:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0130.bmp'
            if h60m >= 225 and h60m < 300:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0345.bmp'
            if h60m >= 300 and h60m < 360:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0500.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_1000.bmp'
            if h60m >= 750 and h60m < 810:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_1230.bmp'
            if h60m >= 810 and h60m < 900:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_1330.bmp'
            if h60m >= 900 and h60m < 945:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_1500.bmp'
            if h60m >= 945 and h60m < 990:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_1545.bmp'
            if h60m >= 990 and h60m < 1200:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_1630.bmp'
            if h60m >= 1200 and h60m < 1260:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_2000.bmp'
            if h60m >= 1260 and h60m < 1380:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_2100.bmp'
            if h60m >= 1380 and h60m < 1440:
                file_name = self.m_folder + '203//' + 'clock_analog_black_203_2300.bmp'
        elif _sw1 == dst_999:
            file_name = self.m_folder + 'clock_analog_error_999.bmp'
        else:
            file_name = self.m_folder + 'clock_analog_error_999.bmp'
        return file_name
    def DstEventFileWhite(self):
        file_name = self.m_folder + 'clock_analog_error_999.bmp'
        h60m = 0
        time = 0
        stmG = MqlDateTime()
        stm = MqlDateTime()
        if not self.m_debug_on:
            time = TimeGMT()
            TimeToStruct(time, stm)
        else:
            time = self.m_tmd
            TimeToStruct(TimeGMT(), stmG)
            TimeToStruct(self.m_tmd, stm)
            stm.hour = stmG.hour
            stm.min = stmG.min
            stm.sec = stmG.sec
        h60m = (stm.hour * 60) + stm.min
        _sw2 = self.m_dst_event
        if _sw2 == dst_111:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_0100.bmp'
            if h60m >= 90 and h60m < 225:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_0130.bmp'
            if h60m >= 225 and h60m < 300:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_0345.bmp'
            if h60m >= 300 and h60m < 360:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_0500.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_1000.bmp'
            if h60m >= 750 and h60m < 870:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_1230.bmp'
            if h60m >= 870 and h60m < 900:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_1430.bmp'
            if h60m >= 900 and h60m < 945:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_1500.bmp'
            if h60m >= 945 and h60m < 990:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_1545.bmp'
            if h60m >= 990 and h60m < 1260:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_1630.bmp'
            if h60m >= 1260 and h60m < 1380:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_2100.bmp'
            if h60m >= 1380 and h60m < 1440:
                file_name = self.m_folder + '111//' + 'clock_analog_white_111_2300.bmp'
        elif _sw2 == dst_203:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0100.bmp'
            if h60m >= 90 and h60m < 225:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0130.bmp'
            if h60m >= 225 and h60m < 300:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0345.bmp'
            if h60m >= 300 and h60m < 360:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0500.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_1000.bmp'
            if h60m >= 750 and h60m < 810:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_1230.bmp'
            if h60m >= 810 and h60m < 900:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_1330.bmp'
            if h60m >= 900 and h60m < 945:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_1500.bmp'
            if h60m >= 945 and h60m < 990:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_1545.bmp'
            if h60m >= 990 and h60m < 1200:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_1630.bmp'
            if h60m >= 1200 and h60m < 1260:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_2000.bmp'
            if h60m >= 1260 and h60m < 1380:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_2100.bmp'
            if h60m >= 1380 and h60m < 1440:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_2300.bmp'
        elif _sw2 == dst_403:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_0100.bmp'
            if h60m >= 90 and h60m < 225:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_0130.bmp'
            if h60m >= 225 and h60m < 300:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_0345.bmp'
            if h60m >= 300 and h60m < 360:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_0500.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_1000.bmp'
            if h60m >= 750 and h60m < 810:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_1230.bmp'
            if h60m >= 810 and h60m < 900:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_1330.bmp'
            if h60m >= 900 and h60m < 930:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_1500.bmp'
            if h60m >= 930 and h60m < 945:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_1530.bmp'
            if h60m >= 945 and h60m < 1200:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_1545.bmp'
            if h60m >= 1200 and h60m < 1260:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_2000.bmp'
            if h60m >= 1260 and h60m < 1380:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_2100.bmp'
            if h60m >= 1380 and h60m < 1440:
                file_name = self.m_folder + '403//' + 'clock_analog_white_403_2300.bmp'
        elif _sw2 == dst_104:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_0100.bmp'
            if h60m >= 90 and h60m < 285:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_0130.bmp'
            if h60m >= 285 and h60m < 360:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_0445.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_1000.bmp'
            if h60m >= 750 and h60m < 810:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_1230.bmp'
            if h60m >= 810 and h60m < 900:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_1330.bmp'
            if h60m >= 900 and h60m < 930:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_1500.bmp'
            if h60m >= 930 and h60m < 945:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_1530.bmp'
            if h60m >= 945 and h60m < 1200:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_1545.bmp'
            if h60m >= 1200 and h60m < 1320:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_2000.bmp'
            if h60m >= 1320 and h60m < 1440:
                file_name = self.m_folder + '104//' + 'clock_analog_white_104_2200.bmp'
        elif _sw2 == dst_409:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_0100.bmp'
            if h60m >= 90 and h60m < 225:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_0130.bmp'
            if h60m >= 225 and h60m < 360:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_0345.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_1000.bmp'
            if h60m >= 750 and h60m < 810:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_1230.bmp'
            if h60m >= 810 and h60m < 900:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_1330.bmp'
            if h60m >= 900 and h60m < 930:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_1500.bmp'
            if h60m >= 930 and h60m < 945:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_1530.bmp'
            if h60m >= 945 and h60m < 1200:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_1545.bmp'
            if h60m >= 1200 and h60m < 1260:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_2000.bmp'
            if h60m >= 1260 and h60m < 1440:
                file_name = self.m_folder + '409//' + 'clock_analog_white_409_2100.bmp'
        elif _sw2 == dst_110:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_0100.bmp'
            if h60m >= 90 and h60m < 225:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_0130.bmp'
            if h60m >= 225 and h60m < 300:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_0345.bmp'
            if h60m >= 300 and h60m < 360:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_0500.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_1000.bmp'
            if h60m >= 750 and h60m < 810:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_1230.bmp'
            if h60m >= 810 and h60m < 900:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_1330.bmp'
            if h60m >= 900 and h60m < 930:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_1500.bmp'
            if h60m >= 930 and h60m < 945:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_1530.bmp'
            if h60m >= 945 and h60m < 1200:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_1545.bmp'
            if h60m >= 1200 and h60m < 1260:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_2000.bmp'
            if h60m >= 1260 and h60m < 1380:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_2100.bmp'
            if h60m >= 1380 and h60m < 1440:
                file_name = self.m_folder + '110//' + 'clock_analog_white_110_2300.bmp'
        elif _sw2 == dst_410:
            if h60m >= 0 and h60m < 60:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0000.bmp'
            if h60m >= 60 and h60m < 90:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0100.bmp'
            if h60m >= 90 and h60m < 225:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0130.bmp'
            if h60m >= 225 and h60m < 300:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0345.bmp'
            if h60m >= 300 and h60m < 360:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0500.bmp'
            if h60m >= 360 and h60m < 420:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0600.bmp'
            if h60m >= 420 and h60m < 480:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0700.bmp'
            if h60m >= 480 and h60m < 540:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0800.bmp'
            if h60m >= 540 and h60m < 600:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_0900.bmp'
            if h60m >= 600 and h60m < 750:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_1000.bmp'
            if h60m >= 750 and h60m < 810:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_1230.bmp'
            if h60m >= 810 and h60m < 900:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_1330.bmp'
            if h60m >= 900 and h60m < 945:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_1500.bmp'
            if h60m >= 945 and h60m < 990:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_1545.bmp'
            if h60m >= 990 and h60m < 1200:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_1630.bmp'
            if h60m >= 1200 and h60m < 1260:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_2000.bmp'
            if h60m >= 1260 and h60m < 1380:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_2100.bmp'
            if h60m >= 1380 and h60m < 1440:
                file_name = self.m_folder + '203//' + 'clock_analog_white_203_2300.bmp'
        elif _sw2 == dst_999:
            file_name = self.m_folder + 'clock_analog_error_999.bmp'
        else:
            file_name = self.m_folder + 'clock_analog_error_999.bmp'
        return file_name
    def DSTime(self):
        time = 0
        stm = MqlDateTime()
        stm_first = MqlDateTime()
        stm_last = MqlDateTime()
        if not self.m_debug_on:
            time = TimeGMT()
        else:
            time = self.m_tmd
        TimeToStruct(time, stm)
        tm_first = 0
        tm_last = 0
        day_of_week = 0
        day_of_week_first = 0
        day_of_week_last = 0
        day_of_change1 = 0
        day_of_change2 = 0
        day_of_change_last = 0
        self.m_dst_event = dst_999
        tm_first = time - ((stm.day - 1) * 86400)
        tm_last = tm_first + 2592000
        if (stm.mon == 4 or stm.mon == 9) or stm.mon == 11:
            tm_last = tm_first + 2505600
        TimeToStruct(tm_first, stm_first)
        TimeToStruct(tm_last, stm_last)
        if stm_first.day_of_week != 0:
            day_of_week_first = stm_first.day_of_week
        else:
            day_of_week_first = 7
        if stm_last.day_of_week != 0:
            day_of_week_last = stm_last.day_of_week
        else:
            day_of_week_last = 7
        if stm.day_of_week != 0:
            day_of_week = stm.day_of_week
        else:
            day_of_week = 7
        day_of_change1 = 8 - day_of_week_first
        day_of_change2 = 15 - day_of_week_first
        if (stm.mon >= 1 and stm.mon <= 2) or stm.mon == 12:
            self.m_dst_event = dst_111
        if stm.mon == 3:
            self.m_dst_event = dst_111
            if stm.day >= day_of_change2:
                self.m_dst_event = dst_203
            day_of_change_last = 31 - stm_last.day_of_week
            if stm.day >= day_of_change_last:
                self.m_dst_event = dst_403
        if stm.mon == 4:
            self.m_dst_event = dst_403
            if stm.day >= day_of_change1:
                self.m_dst_event = dst_104
        if stm.mon > 4 and stm.mon < 9:
            self.m_dst_event = dst_104
        if stm.mon == 9:
            self.m_dst_event = dst_104
            day_of_change_last = 30 - stm_last.day_of_week
            if stm.day >= day_of_change_last:
                self.m_dst_event = dst_409
        if stm.mon == 10:
            self.m_dst_event = dst_409
            if stm.day >= day_of_change1:
                self.m_dst_event = dst_110
            day_of_change_last = 31 - stm_last.day_of_week
            if stm.day >= day_of_change_last:
                self.m_dst_event = dst_410
        if stm.mon == 11:
            self.m_dst_event = dst_410
            if stm.day >= day_of_change1:
                self.m_dst_event = dst_111
    def DefaultsSkin(self):
        self.m_clock_skin.Create()
        _sw3 = self.m_scheme
        if _sw3 == black:
            self.m_clock_skin.SetFileOn(self.m_folder + 'clock_analog_black_start.bmp')
        elif _sw3 == white:
            self.m_clock_skin.SetFileOn(self.m_folder + 'clock_analog_white_start.bmp')
        else:
            self.m_clock_skin.SetFileOn(self.m_folder + 'clock_analog_black_start.bmp')
        self.m_clock_skin.SetXDist(self.m_x)
        self.m_clock_skin.SetYDist(self.m_y + self.m_header_height)
        self.m_clock_skin.SetXSize(self.m_width)
        self.m_clock_skin.SetYSize(self.m_height)
        self.m_clock_skin.SetXOffset(0)
        self.m_clock_skin.SetYOffset(0)
        self.m_clock_skin.SetState(True)
        self.m_clock_skin.SetCorner(CORNER_LEFT_UPPER)
        self.m_clock_skin.SetAnchor(ANCHOR_LEFT_UPPER)
        self.m_clock_skin.SetColor(clrNONE)
        self.m_clock_skin.SetStyle(STYLE_SOLID)
        self.m_clock_skin.SetPointWidth(1)
        self.m_clock_skin.SetBack(True)
        self.m_clock_skin.SetSelected(False)
        self.m_clock_skin.SetSelectable(False)
        self.m_clock_skin.SetZOrder(0)
        self.m_clock_skin.SetHidden(True)
    def DefaultsHeader(self):
        self.m_header.Create()
        _sw4 = self.m_scheme
        if _sw4 == black:
            self.m_header.SetFileOn(self.m_folder + 'clock_analog_header_black.bmp')
        elif _sw4 == white:
            self.m_header.SetFileOn(self.m_folder + 'clock_analog_header_white.bmp')
        else:
            self.m_header.SetFileOn(self.m_folder + 'clock_analog_header_black.bmp')
        self.m_header.SetXDist(self.m_x)
        self.m_header.SetYDist(self.m_y)
        self.m_header.SetXSize(self.m_width)
        self.m_header.SetYSize(self.m_header_height)
        self.m_header.SetXOffset(0)
        self.m_header.SetYOffset(0)
        self.m_header.SetState(True)
        self.m_header.SetCorner(CORNER_LEFT_UPPER)
        self.m_header.SetAnchor(ANCHOR_LEFT_UPPER)
        self.m_header.SetColor(clrNONE)
        self.m_header.SetStyle(STYLE_SOLID)
        self.m_header.SetPointWidth(1)
        self.m_header.SetBack(True)
        self.m_header.SetSelected(False)
        self.m_header.SetSelectable(False)
        self.m_header.SetZOrder(0)
        self.m_header.SetHidden(True)
    def SetExtSecond(self, bColor, wColor, style):
        self.m_bcolor = bColor
        self.m_wcolor = wColor
        self.m_secstyle = style
    def DefaultsHours(self):
        self.m_hand_hour.Create()
        _sw5 = self.m_scheme
        if _sw5 == black:
            self.m_hand_hour.SetColor(0x646464)
        elif _sw5 == white:
            self.m_hand_hour.SetColor(0x9B9B9B)
        else:
            self.m_hand_hour.SetColor(0x646464)
        self.m_hand_hour.SetStyle(STYLE_SOLID)
        self.m_hand_hour.SetWidth(5)
        self.m_hand_hour.SetRay(False)
        self.m_hand_hour.SetBack(True)
        self.m_hand_hour.SetSelected(False)
        self.m_hand_hour.SetSelectable(False)
        self.m_hand_hour.SetHidden(True)
        self.m_hand_hour.SetZOrder(0)
    def DefaultsMinute(self):
        self.m_hand_minute.Create()
        _sw6 = self.m_scheme
        if _sw6 == black:
            self.m_hand_minute.SetColor(0x646464)
        elif _sw6 == white:
            self.m_hand_minute.SetColor(0x9B9B9B)
        else:
            self.m_hand_minute.SetColor(0x646464)
        self.m_hand_minute.SetStyle(STYLE_SOLID)
        self.m_hand_minute.SetWidth(3)
        self.m_hand_minute.SetRay(False)
        self.m_hand_minute.SetBack(True)
        self.m_hand_minute.SetSelected(False)
        self.m_hand_minute.SetSelectable(False)
        self.m_hand_minute.SetHidden(True)
        self.m_hand_minute.SetZOrder(0)
    def DefaultsSecond(self):
        a_color = clrNONE
        self.m_hand_second.Create()
        _sw7 = self.m_scheme
        if _sw7 == black:
            a_color = self.m_bcolor
        elif _sw7 == white:
            a_color = self.m_wcolor
        else:
            a_color = self.m_bcolor
        if not self.m_show_second_hand:
            a_color = clrNONE
        self.m_hand_second.SetColor(a_color)
        self.m_hand_second.SetStyle(self.m_secstyle)
        self.m_hand_second.SetWidth(1)
        self.m_hand_second.SetRay(False)
        self.m_hand_second.SetBack(True)
        self.m_hand_second.SetSelected(False)
        self.m_hand_second.SetSelectable(False)
        self.m_hand_second.SetHidden(True)
        self.m_hand_second.SetZOrder(0)
    def DefaultsMove(self):
        self.m_xmove = self.m_x + self.m_xmove_rel
        self.m_ymove = self.m_y + self.m_ymove_rel
        cFG = 0
        cBG = 0
        cBD = 0
        self.m_button_move.Create()
        _sw8 = self.m_scheme
        if _sw8 == black:
            cFG = 0x000000
            cBG = 0x646464
            cBD = clrNONE
        elif _sw8 == white:
            cFG = 0xFFFFFF
            cBG = 0x9B9B9B
            cBD = clrNONE
        else:
            cFG = 0x000000
            cBG = 0x646464
            cBD = clrNONE
        self.m_button_move.SetXDist(self.m_xmove)
        self.m_button_move.SetYDist(self.m_ymove)
        self.m_button_move.SetXSize(self.m_button_height)
        self.m_button_move.SetYSize(self.m_button_width)
        self.m_button_move.SetBack(True)
        self.m_button_move.SetState(False)
        self.m_button_move.SetChar(78)
        self.m_button_move.SetColorFG(cFG)
        self.m_button_move.SetColorBG(cBG)
        self.m_button_move.SetColorBD(cBD)
        self.m_button_move.SetCorner(CORNER_LEFT_UPPER)
        self.m_button_move.SetFontName('Wingdings 2')
        self.m_button_move.SetFontSize(14)
        self.m_button_move.SetSelected(False)
        self.m_button_move.SetSelectable(False)
        self.m_button_move.SetHidden(True)
    def DefaultsBack(self):
        self.m_xback = self.m_x + self.m_xback_rel
        self.m_yback = self.m_y + self.m_yback_rel
        cFG = 0
        cBG = 0
        cBD = 0
        self.m_button_back.Create()
        _sw9 = self.m_scheme
        if _sw9 == black:
            cFG = 0x000000
            cBG = 0x646464
            cBD = clrNONE
        elif _sw9 == white:
            cFG = 0xFFFFFF
            cBG = 0x9B9B9B
            cBD = clrNONE
        else:
            cFG = 0x000000
            cBG = 0x646464
            cBD = clrNONE
        self.m_button_back.SetXDist(self.m_xback)
        self.m_button_back.SetYDist(self.m_yback)
        self.m_button_back.SetXSize(self.m_button_width)
        self.m_button_back.SetYSize(self.m_button_height)
        self.m_button_back.SetBack(True)
        self.m_button_back.SetState(True)
        self.m_button_back.SetChar(181)
        self.m_button_back.SetColorFG(cFG)
        self.m_button_back.SetColorBG(cBG)
        self.m_button_back.SetColorBD(cBD)
        self.m_button_back.SetCorner(CORNER_LEFT_UPPER)
        self.m_button_back.SetFontName('Wingdings')
        self.m_button_back.SetFontSize(14)
        self.m_button_back.SetSelected(False)
        self.m_button_back.SetSelectable(False)
        self.m_button_back.SetHidden(True)
    def DefaultsHide(self):
        self.m_xhide = self.m_x + self.m_xhide_rel
        self.m_yhide = self.m_y + self.m_yhide_rel
        cFG = 0
        cBG = 0
        cBD = 0
        self.m_button_hide.Create()
        _sw10 = self.m_scheme
        if _sw10 == black:
            cFG = 0x000000
            cBG = 0x646464
            cBD = clrNONE
        elif _sw10 == white:
            cFG = 0xFFFFFF
            cBG = 0x9B9B9B
            cBD = clrNONE
        else:
            cFG = 0x000000
            cBG = 0x646464
            cBD = clrNONE
        self.m_button_hide.SetXDist(self.m_xhide)
        self.m_button_hide.SetYDist(self.m_yhide)
        self.m_button_hide.SetXSize(self.m_button_width)
        self.m_button_hide.SetYSize(self.m_button_height)
        self.m_button_hide.SetBack(True)
        self.m_button_hide.SetState(False)
        self.m_button_hide.SetChar(244)
        self.m_button_hide.SetColorFG(cFG)
        self.m_button_hide.SetColorBG(cBG)
        self.m_button_hide.SetColorBD(cBD)
        self.m_button_hide.SetCorner(CORNER_LEFT_UPPER)
        self.m_button_hide.SetFontName('Wingdings')
        self.m_button_hide.SetFontSize(10)
        self.m_button_hide.SetSelected(False)
        self.m_button_hide.SetSelectable(False)
        self.m_button_hide.SetHidden(True)
    def DefaultsHeaderLabel(self):
        self.m_x_label = self.m_x + self.m_x_label_rel
        self.m_y_label = self.m_y + self.m_y_label_rel
        self.m_clockname.Create()
        cFG = 0
        _sw11 = self.m_scheme
        if _sw11 == black:
            cFG = 0x000000
        elif _sw11 == white:
            cFG = 0xFFFFFF
        else:
            cFG = 0x000000
        self.m_clockname.SetXDist(self.m_x_label)
        self.m_clockname.SetYDist(self.m_y_label)
        self.m_clockname.SetBack(True)
        self.m_clockname.SetText('market 24-hours GMT clock')
        self.m_clockname.SetColorText(cFG)
        self.m_clockname.SetCorner(CORNER_LEFT_UPPER)
        self.m_clockname.SetAnchor(ANCHOR_CENTER)
        self.m_clockname.SetFontName('Arial')
        self.m_clockname.SetFontSize(12)
        self.m_clockname.SetSelected(False)
        self.m_clockname.SetSelectable(False)
        self.m_clockname.SetHidden(True)
    def HandSecondMove(self):
        angle = 0.0
        x = 0
        y = 0
        subwin = Box(0)
        stm = MqlDateTime()
        TimeToStruct(TimeGMT(), stm)
        error_code = 0
        ResetLastError()
        if not ChartXYToTimePrice(0, self.m_x0, self.m_y0, subwin, _AttrRef(self, 'm_dt0'), _AttrRef(self, 'm_pr0')):
            error_code = GetLastError()
        angle = (stm.sec * (2 * M_PI)) / 60
        x = _int(self.m_x0 + NormalizeDouble(self.m_radius_sh * MathSin(angle), 0))
        y = _int(self.m_y0 - NormalizeDouble(self.m_radius_sh * MathCos(angle), 0))
        ResetLastError()
        if not ChartXYToTimePrice(0, x, y, subwin, _AttrRef(self, 'm_dt_sh'), _AttrRef(self, 'm_pr_sh')):
            error_code = GetLastError()
        if error_code == 0:
            self.m_hand_second.SetPositions(self.m_dt0, self.m_pr0, self.m_dt_sh, self.m_pr_sh)
        else:
            self.m_hand_second.SetPositions(0, 0.0, 0, 0.0)
    def HandMinuteMove(self):
        angle = 0.0
        x = 0
        y = 0
        subwin = Box(0)
        stm = MqlDateTime()
        TimeToStruct(TimeGMT(), stm)
        error_code = 0
        ResetLastError()
        if not ChartXYToTimePrice(0, self.m_x0, self.m_y0, subwin, _AttrRef(self, 'm_dt0'), _AttrRef(self, 'm_pr0')):
            error_code = GetLastError()
        angle = (stm.min * (2 * M_PI)) / 60
        x = _int(self.m_x0 + NormalizeDouble(self.m_radius_mh * MathSin(angle), 0))
        y = _int(self.m_y0 - NormalizeDouble(self.m_radius_mh * MathCos(angle), 0))
        ResetLastError()
        if not ChartXYToTimePrice(0, x, y, subwin, _AttrRef(self, 'm_dt_mh'), _AttrRef(self, 'm_pr_mh')):
            error_code = GetLastError()
        if error_code == 0:
            self.m_hand_minute.SetPositions(self.m_dt0, self.m_pr0, self.m_dt_mh, self.m_pr_mh)
        else:
            self.m_hand_minute.SetPositions(0, 0.0, 0, 0.0)
    def HandHourMove(self):
        angle = 0.0
        x = 0
        y = 0
        subwin = Box(0)
        stm = MqlDateTime()
        TimeToStruct(TimeGMT(), stm)
        error_code = 0
        ResetLastError()
        if not ChartXYToTimePrice(0, self.m_x0, self.m_y0, subwin, _AttrRef(self, 'm_dt0'), _AttrRef(self, 'm_pr0')):
            error_code = GetLastError()
        angle = ((stm.hour * (2 * M_PI)) / 24) + ((stm.min * (2 * M_PI)) / 1440)
        x = _int(self.m_x0 + NormalizeDouble(self.m_radius_hh * MathSin(angle), 0))
        y = _int(self.m_y0 - NormalizeDouble(self.m_radius_hh * MathCos(angle), 0))
        ResetLastError()
        if not ChartXYToTimePrice(0, x, y, subwin, _AttrRef(self, 'm_dt_hh'), _AttrRef(self, 'm_pr_hh')):
            error_code = GetLastError()
        if error_code == 0:
            self.m_hand_hour.SetPositions(self.m_dt0, self.m_pr0, self.m_dt_hh, self.m_pr_hh)
        else:
            self.m_hand_hour.SetPositions(0, 0.0, 0, 0.0)
    def ProcessingDstEvent(self):
        image_old = self.m_clock_skin.GetFileOn()
        image_new = ""
        self.DSTime()
        _sw12 = self.m_scheme
        if _sw12 == black:
            image_new = self.DstEventFileBlack()
        elif _sw12 == white:
            image_new = self.DstEventFileWhite()
        else:
            image_new = self.DstEventFileBlack()
        if image_old != image_new:
            self.m_clock_skin.SetFileOn(image_new)
    def ShowSecondHand(self):
        return self.m_show_second_hand
    def SetPositions(self, x, y):
        self.m_x = x
        self.m_y = y
        self.m_xmove = self.m_x + self.m_xmove_rel
        self.m_ymove = self.m_y + self.m_ymove_rel
        self.m_xback = self.m_x + self.m_xback_rel
        self.m_yback = self.m_y + self.m_yback_rel
        self.m_xhide = self.m_x + self.m_xhide_rel
        self.m_yhide = self.m_y + self.m_yhide_rel
        self.m_x_label = self.m_x + self.m_x_label_rel
        self.m_y_label = self.m_y + self.m_y_label_rel
        self.m_button_move.SetXDist(self.m_xmove)
        self.m_button_move.SetYDist(self.m_ymove)
        self.m_button_back.SetXDist(self.m_xback)
        self.m_button_back.SetYDist(self.m_yback)
        self.m_button_hide.SetXDist(self.m_xhide)
        self.m_button_hide.SetYDist(self.m_yhide)
        self.m_header.SetXDist(self.m_x)
        self.m_header.SetYDist(self.m_y)
        self.m_clock_skin.SetXDist(self.m_x)
        self.m_clock_skin.SetYDist(self.m_y + self.m_header_height)
        self.m_clockname.SetXDist(self.m_x_label)
        self.m_clockname.SetYDist(self.m_y_label)
        self.m_x0 = x + self.m_x0_rel
        self.m_y0 = y + self.m_y0_rel
        self.HandSecondMove()
        self.HandHourMove()
        self.HandMinuteMove()
    def SetStateBack(self, aValue=False):
        self.m_clock_skin.SetBack(aValue)
        self.m_header.SetBack(aValue)
        self.m_hand_second.SetBack(aValue)
        self.m_hand_minute.SetBack(aValue)
        self.m_hand_hour.SetBack(aValue)
        self.m_button_back.SetBack(aValue)
        self.m_button_move.SetBack(aValue)
        self.m_button_hide.SetBack(aValue)
        self.m_clockname.SetBack(aValue)
    def SetStateMove(self, aValue=False):
        self.m_button_move.SetState(aValue)
    def SetBackOn(self):
        self.m_button_back.SetState(True)
    def SetMoveOff(self):
        self.m_button_move.SetState(False)
    def ClockShow(self):
        self.m_clock_hidden = False
        self.m_clock_skin.SetXDist(self.m_x)
        self.m_clock_skin.SetYDist(self.m_y + self.m_header_height)
        self.m_x0 = self.m_x + self.m_x0_rel
        self.m_y0 = self.m_y + self.m_y0_rel
        _sw13 = self.m_scheme
        if _sw13 == black:
            self.m_hand_hour.SetColor(0x646464)
            self.m_hand_minute.SetColor(0x646464)
            self.m_hand_second.SetColor(clrGreenYellow)
        elif _sw13 == white:
            self.m_hand_hour.SetColor(0x9B9B9B)
            self.m_hand_minute.SetColor(0x9B9B9B)
            self.m_hand_second.SetColor(clrDarkOrange)
        else:
            self.m_hand_hour.SetColor(0x646464)
            self.m_hand_minute.SetColor(0x646464)
            self.m_hand_second.SetColor(clrGreenYellow)
    def SetDebugDate(self, yy, mn, dd):
        error_str = ""
        tm = 0
        tm = StringToTime(' ' + IntegerToString(yy) + '.' + IntegerToString(mn, 2, 48) + '.' + IntegerToString(dd, 2, 48) + ' 00:00 ')
        stm = MqlDateTime()
        TimeToStruct(tm, stm)
        if (yy != stm.year or mn != stm.mon) or dd != stm.day:
            error_str = 'Input Date error. New debuging date is assigned:' + TimeToString(tm, TIME_DATE)
            Print('CStockClock::SetDebugDate', error_str)
        self.m_debug_on = True
        self.m_tmd = StructToTime(stm)
    def ClockHide(self):
        center_x = 0
        center_y = 0
        self.m_clock_hidden = True
        self.m_clock_skin.SetXDist(self.m_xhidden)
        self.m_clock_skin.SetYDist(self.m_yhidden + self.m_header_height)
        center_x = self.m_xhidden + self.m_x0_rel
        center_y = self.m_yhidden + self.m_y0_rel
        self.m_hand_hour.SetColor(clrNONE)
        self.m_hand_minute.SetColor(clrNONE)
        self.m_hand_second.SetColor(clrNONE)
    def ClockHidden(self):
        return self.m_clock_hidden
    def StateBack(self):
        return self.m_button_back.State()
    def StateMove(self):
        return self.m_button_move.State()
    def StateHide(self):
        return self.m_button_hide.State()
    def EventBack(self, id_, lparam, dparam, sparam):
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if sparam == self.m_name_back:
                if self.StateBack():
                    self.SetStateBack(True)
                    return
                if not self.StateBack():
                    self.SetStateBack(False)
                    return
    def EventMove(self, id_, lparam, dparam, sparam):
        left = _int(lparam)
        top = _int(dparam)
        left_icon = 0
        top_icon = 0
        right_icon = 0
        bottom_icon = 0
        if id_ == CHARTEVENT_CLICK:
            left_icon = self.m_button_move.XDistance()
            top_icon = self.m_button_move.YDistance()
            right_icon = left_icon + self.m_button_width
            bottom_icon = top_icon + self.m_button_height
            if self.StateMove():
                if ((left > right_icon or left < left_icon) or top < top_icon) or top > bottom_icon:
                    self.SetPositions(left, top)
                    self.SetStateMove(False)
                    return
    def EventHide(self, id_, lparam, dparam, sparam):
        if id_ == CHARTEVENT_OBJECT_CLICK:
            if sparam == self.m_name_hide:
                if self.m_clock_hidden:
                    self.ClockShow()
                    return
                if not self.m_clock_hidden:
                    self.ClockHide()
                    return

__all__ = ['CStockClock']
