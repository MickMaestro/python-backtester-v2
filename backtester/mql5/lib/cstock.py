"""CStock.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.stockstruct import *  # StockStruct.mqh


class CStock(MqlObject):
    _q_fields = ('m_stock', 'm_tm_shift_srv_gmt', 'm_srv_utc_delta', 'm_timeopen', 'm_timeclose', 'm_stock_name', 'm_stock_text', 'm_caps', 'm_active_stock', 'm_created')
    def __init__(self, aStock=0, aCaps=False):
        self.m_stock = 0
        self.m_tm_shift_srv_gmt = 0
        self.m_srv_utc_delta = 0
        self.m_timeopen = 0
        self.m_timeclose = 0
        self.m_stock_name = ""
        self.m_stock_text = ""
        self.m_caps = False
        self.m_active_stock = False
        self.m_created = False
        self.m_stock = aStock
        self.m_caps = aCaps
        self.m_tm_shift_srv_gmt = TimeTradeServer() - TimeGMT()
        self.m_created = True
    def _q_dtor(self):
        pass
    def DSTime(self, aTime, aSummer, checkSrv=False):
        stm = MqlDateTime()
        s_stm = MqlDateTime()
        TimeToStruct(aTime, stm)
        if checkSrv == True:
            if stm.mon < 3 and stm.mon > 0:
                return False
            if stm.mon == 3:
                if stm.day > 25 and (stm.day + 7 - stm.day_of_week) > 31:
                    s_stm.day = stm.day
                    s_stm.day_of_week = stm.day_of_week
                    s_stm.day_of_year = stm.day_of_year
                    s_stm.hour = stm.hour - 1
                    s_stm.min = stm.min
                    s_stm.mon = stm.mon
                    s_stm.sec = stm.sec
                    s_stm.year = stm.year
                    aSummer.v = StructToTime(s_stm)
                    return True
                else:
                    return False
            if stm.mon > 3 and stm.mon < 10:
                s_stm.day = stm.day
                s_stm.day_of_week = stm.day_of_week
                s_stm.day_of_year = stm.day_of_year
                s_stm.hour = stm.hour - 1
                s_stm.min = stm.min
                s_stm.mon = stm.mon
                s_stm.sec = stm.sec
                s_stm.year = stm.year
                aSummer.v = StructToTime(s_stm)
                return True
            if stm.mon == 10:
                if stm.day > 25 and (stm.day + 7 - stm.day_of_week) > 31:
                    return False
                else:
                    s_stm.day = stm.day
                    s_stm.day_of_week = stm.day_of_week
                    s_stm.day_of_year = stm.day_of_year
                    s_stm.hour = stm.hour - 1
                    s_stm.min = stm.min
                    s_stm.mon = stm.mon
                    s_stm.sec = stm.sec
                    s_stm.year = stm.year
                    aSummer.v = StructToTime(s_stm)
                    return True
            if stm.mon > 10 and stm.mon <= 12:
                return False
        _sw1 = self.m_stock
        if _sw1 in (Tokio, Singapore, Shanghai, Dubai, Moscow, Yohannensburg, Riyadh):
            return False
        elif _sw1 in (London, Zurich, Frankfurt):
            if stm.mon < 3 and stm.mon > 0:
                return False
            if stm.mon == 3:
                if stm.day > 25 and (stm.day + 7 - stm.day_of_week) > 31:
                    s_stm.day = stm.day
                    s_stm.day_of_week = stm.day_of_week
                    s_stm.day_of_year = stm.day_of_year
                    s_stm.hour = stm.hour - 1
                    s_stm.min = stm.min
                    s_stm.mon = stm.mon
                    s_stm.sec = stm.sec
                    s_stm.year = stm.year
                    aSummer.v = StructToTime(s_stm)
                    return True
                else:
                    return False
            if stm.mon > 3 and stm.mon < 10:
                s_stm.day = stm.day
                s_stm.day_of_week = stm.day_of_week
                s_stm.day_of_year = stm.day_of_year
                s_stm.hour = stm.hour - 1
                s_stm.min = stm.min
                s_stm.mon = stm.mon
                s_stm.sec = stm.sec
                s_stm.year = stm.year
                aSummer.v = StructToTime(s_stm)
                return True
            if stm.mon == 10:
                if stm.day > 25 and (stm.day + 7 - stm.day_of_week) > 31:
                    return False
                else:
                    s_stm.day = stm.day
                    s_stm.day_of_week = stm.day_of_week
                    s_stm.day_of_year = stm.day_of_year
                    s_stm.hour = stm.hour - 1
                    s_stm.min = stm.min
                    s_stm.mon = stm.mon
                    s_stm.sec = stm.sec
                    s_stm.year = stm.year
                    aSummer.v = StructToTime(s_stm)
                    return True
            if stm.mon > 10 and stm.mon <= 12:
                return False
        elif _sw1 in (NewYork, Chicago, Toronto):
            if stm.mon < 3 and stm.mon > 0:
                return False
            if stm.mon == 3:
                if stm.day > 7 and (stm.day + stm.day_of_week) > 14:
                    s_stm.day = stm.day
                    s_stm.day_of_week = stm.day_of_week
                    s_stm.day_of_year = stm.day_of_year
                    s_stm.hour = stm.hour - 1
                    s_stm.min = stm.min
                    s_stm.mon = stm.mon
                    s_stm.sec = stm.sec
                    s_stm.year = stm.year
                    aSummer.v = StructToTime(s_stm)
                    return True
                else:
                    return False
            if stm.mon > 3 and stm.mon < 11:
                s_stm.day = stm.day
                s_stm.day_of_week = stm.day_of_week
                s_stm.day_of_year = stm.day_of_year
                s_stm.hour = stm.hour - 1
                s_stm.min = stm.min
                s_stm.mon = stm.mon
                s_stm.sec = stm.sec
                s_stm.year = stm.year
                aSummer.v = StructToTime(s_stm)
                return True
            if stm.mon == 11:
                if stm.day > 0 and (stm.day + stm.day_of_week) > 7:
                    return False
                else:
                    s_stm.day = stm.day
                    s_stm.day_of_week = stm.day_of_week
                    s_stm.day_of_year = stm.day_of_year
                    s_stm.hour = stm.hour - 1
                    s_stm.min = stm.min
                    s_stm.mon = stm.mon
                    s_stm.sec = stm.sec
                    s_stm.year = stm.year
                    aSummer.v = StructToTime(s_stm)
                    return True
            if stm.mon == 12:
                return False
        elif _sw1 == Wellington:
            if stm.mon < 4 and stm.mon > 0:
                s_stm.day = stm.day
                s_stm.day_of_week = stm.day_of_week
                s_stm.day_of_year = stm.day_of_year
                s_stm.hour = stm.hour - 1
                s_stm.min = stm.min
                s_stm.mon = stm.mon
                s_stm.sec = stm.sec
                s_stm.year = stm.year
                aSummer.v = StructToTime(s_stm)
                return True
            if stm.mon == 4:
                if stm.day > 0 and (stm.day + stm.day_of_week) > 7:
                    return False
                else:
                    s_stm.day = stm.day
                    s_stm.day_of_week = stm.day_of_week
                    s_stm.day_of_year = stm.day_of_year
                    s_stm.hour = stm.hour - 1
                    s_stm.min = stm.min
                    s_stm.mon = stm.mon
                    s_stm.sec = stm.sec
                    s_stm.year = stm.year
                    aSummer.v = StructToTime(s_stm)
                    return True
            if stm.mon > 4 and stm.mon < 9:
                return False
            if stm.mon == 9:
                if stm.day > 25 and (stm.day + 7 - stm.day_of_week) > 31:
                    s_stm.day = stm.day
                    s_stm.day_of_week = stm.day_of_week
                    s_stm.day_of_year = stm.day_of_year
                    s_stm.hour = stm.hour - 1
                    s_stm.min = stm.min
                    s_stm.mon = stm.mon
                    s_stm.sec = stm.sec
                    s_stm.year = stm.year
                    aSummer.v = StructToTime(s_stm)
                    return True
                else:
                    return False
            if stm.mon > 9 and stm.mon <= 12:
                s_stm.day = stm.day
                s_stm.day_of_week = stm.day_of_week
                s_stm.day_of_year = stm.day_of_year
                s_stm.hour = stm.hour - 1
                s_stm.min = stm.min
                s_stm.mon = stm.mon
                s_stm.sec = stm.sec
                s_stm.year = stm.year
                aSummer.v = StructToTime(s_stm)
                return True
        elif _sw1 == Sidney:
            if stm.mon < 4 and stm.mon > 0:
                s_stm.day = stm.day
                s_stm.day_of_week = stm.day_of_week
                s_stm.day_of_year = stm.day_of_year
                s_stm.hour = stm.hour - 1
                s_stm.min = stm.min
                s_stm.mon = stm.mon
                s_stm.sec = stm.sec
                s_stm.year = stm.year
                aSummer.v = StructToTime(s_stm)
                return True
            if stm.mon == 4:
                if stm.day > 0 and (stm.day + stm.day_of_week) > 7:
                    return False
                else:
                    s_stm.day = stm.day
                    s_stm.day_of_week = stm.day_of_week
                    s_stm.day_of_year = stm.day_of_year
                    s_stm.hour = stm.hour - 1
                    s_stm.min = stm.min
                    s_stm.mon = stm.mon
                    s_stm.sec = stm.sec
                    s_stm.year = stm.year
                    aSummer.v = StructToTime(s_stm)
                    return True
            if stm.mon > 4 and stm.mon < 10:
                return False
            if stm.mon == 10:
                if stm.day > 0 and (stm.day + 7 - stm.day_of_week) > 7:
                    s_stm.day = stm.day
                    s_stm.day_of_week = stm.day_of_week
                    s_stm.day_of_year = stm.day_of_year
                    s_stm.hour = stm.hour - 1
                    s_stm.min = stm.min
                    s_stm.mon = stm.mon
                    s_stm.sec = stm.sec
                    s_stm.year = stm.year
                    aSummer.v = StructToTime(s_stm)
                    return True
                else:
                    return False
            if stm.mon > 10 and stm.mon <= 12:
                s_stm.day = stm.day
                s_stm.day_of_week = stm.day_of_week
                s_stm.day_of_year = stm.day_of_year
                s_stm.hour = stm.hour - 1
                s_stm.min = stm.min
                s_stm.mon = stm.mon
                s_stm.sec = stm.sec
                s_stm.year = stm.year
                aSummer.v = StructToTime(s_stm)
                return True
        return False
    def StockShedule(self, aTime, aDTOpen, aDTClose):
        one_hour_seconds = 3600
        srv_shift = _idiv(_int(self.m_tm_shift_srv_gmt), 3600)
        dummy = Box(0)
        server_summer = self.DSTime(aTime, dummy, True)
        stock_summer = False
        _sw2 = self.m_stock
        if _sw2 == Tokio:
            if not server_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 0 + srv_shift, 0)
            else:
                aDTOpen.v = self.SetTimeOpen(aTime, 1 + srv_shift, 0)
            aDTClose.v = aDTOpen.v + (6 * one_hour_seconds)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == Singapore:
            if not server_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 1 + srv_shift, 0)
            else:
                aDTOpen.v = self.SetTimeOpen(aTime, 2 + srv_shift, 0)
            aDTClose.v = aDTOpen.v + (8 * one_hour_seconds)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == Shanghai:
            if not server_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 1 + srv_shift, 30)
            else:
                aDTOpen.v = self.SetTimeOpen(aTime, 2 + srv_shift, 30)
            aDTClose.v = aDTOpen.v + (5 * one_hour_seconds) + _idiv(one_hour_seconds, 2)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == Dubai:
            if not server_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 6 + srv_shift, 0)
            else:
                aDTOpen.v = self.SetTimeOpen(aTime, 7 + srv_shift, 0)
            aDTClose.v = aDTOpen.v + (3 * one_hour_seconds) + _idiv(one_hour_seconds, 2)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == Moscow:
            aDTOpen.v = self.SetTimeOpen(aTime, 6 + srv_shift, 0)
            aDTClose.v = aDTOpen.v + (8 * one_hour_seconds) + (_idiv(one_hour_seconds, 4) * 3)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == London:
            if server_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 7 + srv_shift, 0)
            else:
                aDTOpen.v = self.SetTimeOpen(aTime, 8 + srv_shift, 0)
            aDTClose.v = aDTOpen.v + (8 * one_hour_seconds) + _idiv(one_hour_seconds, 2)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == Zurich:
            aDTOpen.v = self.SetTimeOpen(aTime, 7 + srv_shift, 0)
            aDTClose.v = aDTOpen.v + (8 * one_hour_seconds) + _idiv(one_hour_seconds, 2)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == Frankfurt:
            aDTOpen.v = self.SetTimeOpen(aTime, 7 + srv_shift, 0)
            aDTClose.v = aDTOpen.v + (8 * one_hour_seconds) + _idiv(one_hour_seconds, 2)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == Yohannensburg:
            aDTOpen.v = self.SetTimeOpen(aTime, 7 + srv_shift, 0)
            aDTClose.v = aDTOpen.v + (8 * one_hour_seconds)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == Riyadh:
            if not server_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 8 + srv_shift, 0)
            else:
                aDTOpen.v = self.SetTimeOpen(aTime, 9 + srv_shift, 0)
            aDTClose.v = aDTOpen.v + (4 * one_hour_seconds) + _idiv(one_hour_seconds, 2)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == NewYork:
            stock_summer = self.DSTime(aTime, dummy)
            if (not server_summer) and (not stock_summer):
                aDTOpen.v = self.SetTimeOpen(aTime, 14 + srv_shift, 30)
            if (not server_summer) and stock_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 13 + srv_shift, 30)
            if server_summer and (not stock_summer):
                aDTOpen.v = self.SetTimeOpen(aTime, 14 + srv_shift, 30)
            if server_summer and stock_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 13 + srv_shift, 30)
            aDTClose.v = aDTOpen.v + (6 * one_hour_seconds) + _idiv(one_hour_seconds, 2)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == Toronto:
            stock_summer = self.DSTime(aTime, dummy)
            if (not server_summer) and (not stock_summer):
                aDTOpen.v = self.SetTimeOpen(aTime, 14 + srv_shift, 30)
            if (not server_summer) and stock_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 13 + srv_shift, 30)
            if server_summer and (not stock_summer):
                aDTOpen.v = self.SetTimeOpen(aTime, 14 + srv_shift, 30)
            if server_summer and stock_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 13 + srv_shift, 30)
            aDTClose.v = aDTOpen.v + (6 * one_hour_seconds) + _idiv(one_hour_seconds, 2)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == Chicago:
            stock_summer = self.DSTime(aTime, dummy)
            if (not server_summer) and (not stock_summer):
                aDTOpen.v = self.SetTimeOpen(aTime, 14 + srv_shift, 30)
            if (not server_summer) and stock_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 13 + srv_shift, 30)
            if server_summer and (not stock_summer):
                aDTOpen.v = self.SetTimeOpen(aTime, 14 + srv_shift, 30)
            if server_summer and stock_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 13 + srv_shift, 30)
            aDTClose.v = aDTOpen.v + (6 * one_hour_seconds) + _idiv(one_hour_seconds, 2)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == Wellington:
            stock_summer = self.DSTime(aTime, dummy)
            if (not server_summer) and stock_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 21 + srv_shift, 0)
            if (not server_summer) and (not stock_summer):
                aDTOpen.v = self.SetTimeOpen(aTime, 22 + srv_shift, 0)
            if server_summer and stock_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 23 + srv_shift, 0)
            if server_summer and (not stock_summer):
                aDTOpen.v = self.SetTimeOpen(aTime, 22 + srv_shift, 0)
            aDTClose.v = aDTOpen.v + (6 * one_hour_seconds) + (_idiv(one_hour_seconds, 4) * 3)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
        elif _sw2 == Sidney:
            stock_summer = self.DSTime(aTime, dummy)
            if (not server_summer) and stock_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 23 + srv_shift, 0)
            if (not server_summer) and (not stock_summer):
                aDTOpen.v = self.SetTimeOpen(aTime, 0 + srv_shift, 0)
            if server_summer and stock_summer:
                aDTOpen.v = self.SetTimeOpen(aTime, 1 + srv_shift, 0)
            if server_summer and (not stock_summer):
                aDTOpen.v = self.SetTimeOpen(aTime, 0 + srv_shift, 0)
            aDTClose.v = aDTOpen.v + (6 * one_hour_seconds)
            aDTClose.v = self.ChangeWeekend(aDTClose.v)
    def SetTimeOpen(self, aSrvTime, aSrvHH, aSrvMM):
        stm_srv = MqlDateTime()
        aTime00 = 0
        if aSrvHH >= 24:
            aSrvHH = aSrvHH - 24
        TimeToStruct(aSrvTime, stm_srv)
        stm_srv.hour = aSrvHH
        stm_srv.min = aSrvMM
        stm_srv.sec = 0
        aTime00 = StructToTime(stm_srv)
        return aTime00
    def StockIsActive(self):
        return self.m_active_stock
    def StockTimeOpen(self):
        return self.m_timeopen
    def StockTimeClose(self):
        return self.m_timeclose
    def StockText(self, aCaps=False):
        ret_str = ''
        _sw3 = self.m_stock
        if _sw3 == Tokio:
            if aCaps:
                ret_str = 'TOKIO'
            else:
                ret_str = 'Tokio'
        elif _sw3 == Singapore:
            if aCaps:
                ret_str = 'SINGAPORE'
            else:
                ret_str = 'Singapore'
        elif _sw3 == Shanghai:
            if aCaps:
                ret_str = 'SHANGHAI'
            else:
                ret_str = 'Shanghai'
        elif _sw3 == Dubai:
            if aCaps:
                ret_str = 'DUBAI'
            else:
                ret_str = 'Dubai'
        elif _sw3 == Moscow:
            if aCaps:
                ret_str = 'MOSCOW'
            else:
                ret_str = 'Moscow'
        elif _sw3 == London:
            if aCaps:
                ret_str = 'LONDON'
            else:
                ret_str = 'London'
        elif _sw3 == Zurich:
            if aCaps:
                ret_str = 'ZURICH'
            else:
                ret_str = 'Zurich'
        elif _sw3 == Frankfurt:
            if aCaps:
                ret_str = 'FRANKFURT'
            else:
                ret_str = 'Frankfurt'
        elif _sw3 == Yohannensburg:
            if aCaps:
                ret_str = 'YOHANNENSBURG'
            else:
                ret_str = 'Yohannensburg'
        elif _sw3 == Riyadh:
            if aCaps:
                ret_str = 'RIYADH'
            else:
                ret_str = 'Riyadh'
        elif _sw3 == NewYork:
            if aCaps:
                ret_str = 'NEW YORK'
            else:
                ret_str = 'New York'
        elif _sw3 == Toronto:
            if aCaps:
                ret_str = 'TORONTO'
            else:
                ret_str = 'Toronto'
        elif _sw3 == Chicago:
            if aCaps:
                ret_str = 'CHICAGO'
            else:
                ret_str = 'Chicago'
        elif _sw3 == Wellington:
            if aCaps:
                ret_str = 'WELLINGTON'
            else:
                ret_str = 'Wellington'
        elif _sw3 == Sidney:
            if aCaps:
                ret_str = 'SIDNEY'
            else:
                ret_str = 'Sidney'
        return ret_str
    def StockName(self, aPrefix='', aSuffix=''):
        ret_str = ''
        _sw4 = self.m_stock
        if _sw4 == Tokio:
            ret_str = aPrefix + 'Tok_' + aSuffix
        elif _sw4 == Singapore:
            ret_str = aPrefix + 'Sin_' + aSuffix
        elif _sw4 == Shanghai:
            ret_str = aPrefix + 'Sha_' + aSuffix
        elif _sw4 == Dubai:
            ret_str = aPrefix + 'Dub_' + aSuffix
        elif _sw4 == Moscow:
            ret_str = aPrefix + 'Mos_' + aSuffix
        elif _sw4 == London:
            ret_str = aPrefix + 'Lon_' + aSuffix
        elif _sw4 == Zurich:
            ret_str = aPrefix + 'Zur_' + aSuffix
        elif _sw4 == Frankfurt:
            ret_str = aPrefix + 'Fra_' + aSuffix
        elif _sw4 == Yohannensburg:
            ret_str = aPrefix + 'Yoh_' + aSuffix
        elif _sw4 == Riyadh:
            ret_str = aPrefix + 'Riy_' + aSuffix
        elif _sw4 == NewYork:
            ret_str = aPrefix + 'New_' + aSuffix
        elif _sw4 == Toronto:
            ret_str = aPrefix + 'Tor_' + aSuffix
        elif _sw4 == Chicago:
            ret_str = aPrefix + 'Chi_' + aSuffix
        elif _sw4 == Wellington:
            ret_str = aPrefix + 'Wel_' + aSuffix
        elif _sw4 == Sidney:
            ret_str = aPrefix + 'Sid_' + aSuffix
        return ret_str
    def ChangeWeekend(self, aTime):
        dt_changed = aTime
        stm = MqlDateTime()
        TimeToStruct(aTime, stm)
        if stm.day_of_week == 6:
            dt_changed = aTime + 172800
        if stm.day_of_week == 0:
            dt_changed = aTime - 172800
        return dt_changed
    def Created(self):
        return self.m_created

__all__ = ['CStock']
