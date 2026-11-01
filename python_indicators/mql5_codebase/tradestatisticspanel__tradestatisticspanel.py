"""tradestatisticspanel — converted from MQL5: MQL5 Indicators/TradeStatisticsPanel/tradestatisticspanel.mq5

Copyright: jafferwilson; Link: https://www.mql5.com/en/users/jafferwilson; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Functions not available here: ChartPriceOnDropped, ChartTimeOnDropped, ChartWindowOnDropped, ChartXOnDropped, ChartYOnDropped, FileReadLong, FileReadStruct, FileWriteLong, FileWriteStruct
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.controls_wnd import *  # #include Wnd.mqh
from backtester.mql5.lib.controls_rect import *  # #include Rect.mqh
from backtester.mql5.lib.controls_defines import *  # #include Defines.mqh
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh
from backtester.mql5.lib.controls_wndobj import *  # #include WndObj.mqh

MQL5_META = {'props': {'copyright': 'jafferwilson', 'link': 'https://www.mql5.com/en/users/jafferwilson', 'version': '1.00', 'window': 'separate', 'indicator_plots': 0, 'indicator_buffers': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'tradestatisticspanel', 'source': 'MQL5 Indicators/TradeStatisticsPanel/tradestatisticspanel.mq5', 'folder': 'TradeStatisticsPanel', 'inputs': [{'mql': 'InpFontName', 'py': 'InpFontName', 'param': None, 'type': 'string', 'default': 'Consolas', 'label': 'Font Name', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'int', 'default': 10, 'label': 'Font Size', 'sinput': False}, {'mql': 'InpFontColor', 'py': 'InpFontColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Text Color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Wnd.mqh', 'Rect.mqh', 'Defines.mqh', 'Object.mqh', 'StdLibErr.mqh', 'WndObj.mqh']}

CHAR_VALUE = 0  # MQL5 constant unknown to the converter
DEAL_ENTRY_STATE = 0  # MQL5 constant unknown to the converter
DEAL_EXTERNAL_ID = 0  # MQL5 constant unknown to the converter
DEAL_TYPE_BUY_CANCELED = 0  # MQL5 constant unknown to the converter
DEAL_TYPE_COMMISSION_AGENT_DAILY = 0  # MQL5 constant unknown to the converter
DEAL_TYPE_COMMISSION_AGENT_MONTHLY = 0  # MQL5 constant unknown to the converter
DEAL_TYPE_INTEREST = 0  # MQL5 constant unknown to the converter
DEAL_TYPE_SELL_CANCELED = 0  # MQL5 constant unknown to the converter
INT_VALUE = 0  # MQL5 constant unknown to the converter
OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter
OBJ_NO_PERIODS = 0  # MQL5 constant unknown to the converter
STAT_BALANCEDD_PERCENT = 0  # MQL5 constant unknown to the converter
STAT_BALANCEMIN = 0  # MQL5 constant unknown to the converter
STAT_BALANCE_DD = 0  # MQL5 constant unknown to the converter
STAT_BALANCE_DDREL_PERCENT = 0  # MQL5 constant unknown to the converter
STAT_BALANCE_DD_RELATIVE = 0  # MQL5 constant unknown to the converter
STAT_CONLOSSMAX = 0  # MQL5 constant unknown to the converter
STAT_CONLOSSMAX_TRADES = 0  # MQL5 constant unknown to the converter
STAT_CONPROFITMAX = 0  # MQL5 constant unknown to the converter
STAT_CONPROFITMAX_TRADES = 0  # MQL5 constant unknown to the converter
STAT_DEALS = 0  # MQL5 constant unknown to the converter
STAT_EQUITYDD_PERCENT = 0  # MQL5 constant unknown to the converter
STAT_EQUITYMIN = 0  # MQL5 constant unknown to the converter
STAT_EQUITY_DD = 0  # MQL5 constant unknown to the converter
STAT_EQUITY_DDREL_PERCENT = 0  # MQL5 constant unknown to the converter
STAT_EQUITY_DD_RELATIVE = 0  # MQL5 constant unknown to the converter
STAT_EXPECTED_PAYOFF = 0  # MQL5 constant unknown to the converter
STAT_GROSS_LOSS = 0  # MQL5 constant unknown to the converter
STAT_GROSS_PROFIT = 0  # MQL5 constant unknown to the converter
STAT_LONG_TRADES = 0  # MQL5 constant unknown to the converter
STAT_LOSSTRADES_AVGCON = 0  # MQL5 constant unknown to the converter
STAT_LOSS_TRADES = 0  # MQL5 constant unknown to the converter
STAT_MAX_CONLOSSES = 0  # MQL5 constant unknown to the converter
STAT_MAX_CONLOSS_TRADES = 0  # MQL5 constant unknown to the converter
STAT_MAX_CONPROFIT_TRADES = 0  # MQL5 constant unknown to the converter
STAT_MAX_CONWINS = 0  # MQL5 constant unknown to the converter
STAT_MAX_LOSSTRADE = 0  # MQL5 constant unknown to the converter
STAT_MAX_PROFITTRADE = 0  # MQL5 constant unknown to the converter
STAT_MIN_MARGINLEVEL = 0  # MQL5 constant unknown to the converter
STAT_PROFITTRADES_AVGCON = 0  # MQL5 constant unknown to the converter
STAT_PROFIT_FACTOR = 0  # MQL5 constant unknown to the converter
STAT_PROFIT_LONGTRADES = 0  # MQL5 constant unknown to the converter
STAT_PROFIT_SHORTTRADES = 0  # MQL5 constant unknown to the converter
STAT_PROFIT_TRADES = 0  # MQL5 constant unknown to the converter
STAT_RECOVERY_FACTOR = 0  # MQL5 constant unknown to the converter
STAT_SHARPE_RATIO = 0  # MQL5 constant unknown to the converter
STAT_SHORT_TRADES = 0  # MQL5 constant unknown to the converter
STAT_TRADES = 0  # MQL5 constant unknown to the converter
STAT_WITHDRAWAL = 0  # MQL5 constant unknown to the converter

# enum ENUM_CALC_STATE
CALC_INIT = 0
CALC_TICK = 1
CALC_DEINIT = 2
_enum('ENUM_CALC_STATE', {0: 'CALC_INIT', 1: 'CALC_TICK', 2: 'CALC_DEINIT'})

# enum deal_result
NO_VALUE = 0
WIN = 1
LOSS = 2
_enum('deal_result', {0: 'NO_VALUE', 1: 'WIN', 2: 'LOSS'})

# enum ENUM_STATISTICS_PLUS
STAT_BALANCE = 10000
STAT_EQUITY = 10001
STAT_AHPR = 10002
STAT_GHPR = 10003
STAT_Z_SCORE = 10004
STAT_LR_CORRELATION = 10005
STAT_LR_STANDARD_ERROR = 10006
STAT_AVG_PROFIT_TRADE = 10007
STAT_AVG_LOSS_TRADE = 10008
STAT_BALANCE_DD_ABSOLUTE = 10009
_enum('ENUM_STATISTICS_PLUS', {10000: 'STAT_BALANCE', 10001: 'STAT_EQUITY', 10002: 'STAT_AHPR', 10003: 'STAT_GHPR', 10004: 'STAT_Z_SCORE', 10005: 'STAT_LR_CORRELATION', 10006: 'STAT_LR_STANDARD_ERROR', 10007: 'STAT_AVG_PROFIT_TRADE', 10008: 'STAT_AVG_LOSS_TRADE', 10009: 'STAT_BALANCE_DD_ABSOLUTE'})

# ---- inputs and global variables
Laplas = Arr.of([[0.0, 0.0], [0.01, 0.00798], [0.02, 0.01596], [0.03, 0.02393], [0.04, 0.03191], [0.05, 0.03988], [0.06, 0.04784], [0.07, 0.05581], [0.08, 0.06376], [0.09, 0.07171], [0.1, 0.07966], [0.11, 0.08759], [0.12, 0.09552], [0.13, 0.10348], [0.14, 0.11134], [0.15, 0.11924], [0.16, 0.12712], [0.17, 0.13499], [0.18, 0.14285], [0.19, 0.15069], [0.2, 0.15852], [0.21, 0.16633], [0.22, 0.17413], [0.23, 0.18191], [0.24, 0.18967], [0.25, 0.19741], [0.26, 0.20514], [0.27, 0.21284], [0.28, 0.22052], [0.29, 0.22818], [0.3, 0.23582], [0.31, 0.24344], [0.32, 0.25103], [0.33, 0.2586], [0.34, 0.26614], [0.35, 0.27366], [0.36, 0.28115], [0.37, 0.28862], [0.38, 0.29605], [0.39, 0.30346], [0.4, 0.31084], [0.41, 0.31819], [0.42, 0.32552], [0.43, 0.3328], [0.44, 0.34006], [0.45, 0.34729], [0.46, 0.35448], [0.47, 0.36164], [0.48, 0.36877], [0.49, 0.37587], [0.5, 0.38292], [0.51, 0.38995], [0.52, 0.39694], [0.53, 0.40389], [0.54, 0.4108], [0.55, 0.41768], [0.56, 0.42452], [0.57, 0.43132], [0.58, 0.43809], [0.59, 0.44481], [0.6, 0.45149], [0.61, 0.45814], [0.62, 0.46474], [0.63, 0.47131], [0.64, 0.47783], [0.65, 0.48431], [0.66, 0.49075], [0.67, 0.49714], [0.68, 0.5035], [0.69, 0.50981], [0.7, 0.51607], [0.71, 0.5223], [0.72, 0.52848], [0.73, 0.53461], [0.74, 0.5407], [0.75, 0.54675], [0.76, 0.55275], [0.77, 0.5587], [0.78, 0.56461], [0.79, 0.57047], [0.8, 0.57629], [0.81, 0.58206], [0.82, 0.58778], [0.83, 0.59346], [0.84, 0.59909], [0.85, 0.60468], [0.86, 0.61021], [0.87, 0.6157], [0.88, 0.62114], [0.89, 0.62653], [0.9, 0.63188], [0.91, 0.63718], [0.92, 0.64243], [0.93, 0.64763], [0.94, 0.65278], [0.95, 0.65789], [0.96, 0.66294], [0.97, 0.66795], [0.98, 0.67291], [0.99, 0.67783], [1.0, 0.68269], [1.01, 0.6875], [1.02, 0.69227], [1.03, 0.69699], [1.04, 0.70166], [1.05, 0.70628], [1.06, 0.71086], [1.07, 0.71538], [1.08, 0.71986], [1.09, 0.72429], [1.1, 0.72867], [1.11, 0.733], [1.12, 0.73729], [1.13, 0.74152], [1.14, 0.74571], [1.15, 0.74986], [1.16, 0.75395], [1.17, 0.758], [1.18, 0.762], [1.19, 0.76595], [1.2, 0.76986], [1.21, 0.77372], [1.22, 0.77754], [1.23, 0.7813], [1.24, 0.78502], [1.25, 0.7887], [1.26, 0.79233], [1.27, 0.79592], [1.28, 0.79945], [1.29, 0.80295], [1.3, 0.8064], [1.31, 0.8098], [1.32, 0.81316], [1.33, 0.81648], [1.34, 0.81975], [1.35, 0.82298], [1.36, 0.82617], [1.37, 0.82931], [1.38, 0.83241], [1.39, 0.83547], [1.4, 0.83849], [1.41, 0.84146], [1.42, 0.84439], [1.43, 0.84728], [1.44, 0.85013], [1.45, 0.85294], [1.46, 0.85571], [1.47, 0.85844], [1.48, 0.86113], [1.49, 0.86378], [1.5, 0.86639], [1.51, 0.86696], [1.52, 0.87149], [1.53, 0.87398], [1.54, 0.87644], [1.55, 0.87886], [1.56, 0.88124], [1.57, 0.88358], [1.58, 0.88589], [1.59, 0.88817], [1.6, 0.8904], [1.61, 0.8926], [1.62, 0.89477], [1.63, 0.8969], [1.64, 0.89899], [1.65, 0.90106], [1.66, 0.90309], [1.67, 0.90508], [1.68, 0.90704], [1.69, 0.90897], [1.7, 0.91087], [1.71, 0.91273], [1.72, 0.91457], [1.73, 0.91637], [1.74, 0.91814], [1.75, 0.91988], [1.76, 0.92159], [1.77, 0.92327], [1.78, 0.92492], [1.79, 0.92655], [1.8, 0.92814], [1.81, 0.9297], [1.82, 0.93124], [1.83, 0.93275], [1.84, 0.93423], [1.85, 0.93569], [1.86, 0.93711], [1.87, 0.93852], [1.88, 0.93989], [1.89, 0.94124], [1.9, 0.94257], [1.91, 0.94387], [1.92, 0.94514], [1.93, 0.94639], [1.94, 0.94762], [1.95, 0.94882], [1.96, 0.95], [1.97, 0.95116], [1.98, 0.9523], [1.99, 0.95341], [2.0, 0.9545], [2.01, 0.95557], [2.02, 0.95662], [2.03, 0.95764], [2.04, 0.95865], [2.05, 0.95964], [2.06, 0.9606], [2.07, 0.96155], [2.08, 0.96247], [2.09, 0.96338], [2.1, 0.96427], [2.11, 0.96514], [2.12, 0.96599], [2.13, 0.96683], [2.14, 0.96765], [2.15, 0.96844], [2.16, 0.96923], [2.17, 0.96999], [2.18, 0.97074], [2.19, 0.97148], [2.2, 0.97219], [2.21, 0.97289], [2.22, 0.97358], [2.23, 0.97425], [2.24, 0.97491], [2.25, 0.97555], [2.26, 0.97618], [2.27, 0.97679], [2.28, 0.97739], [2.29, 0.97798], [2.3, 0.97855], [2.31, 0.97911], [2.32, 0.97966], [2.33, 0.98019], [2.34, 0.98072], [2.35, 0.98123], [2.36, 0.98172], [2.37, 0.98221], [2.38, 0.98269], [2.39, 0.98315], [2.4, 0.9836], [2.41, 0.98405], [2.42, 0.98448], [2.43, 0.9849], [2.44, 0.98531], [2.45, 0.98571], [2.46, 0.98611], [2.47, 0.98649], [2.48, 0.98686], [2.49, 0.98723], [2.5, 0.98758], [2.51, 0.98793], [2.52, 0.98826], [2.53, 0.98859], [2.54, 0.98891], [2.55, 0.98923], [2.56, 0.98953], [2.57, 0.98983], [2.58, 0.99012], [2.59, 0.9904], [2.6, 0.99068], [2.61, 0.99095], [2.62, 0.99121], [2.63, 0.99146], [2.64, 0.99171], [2.65, 0.99195], [2.66, 0.99219], [2.67, 0.99241], [2.68, 0.99263], [2.69, 0.99285], [2.7, 0.99307], [2.71, 0.99327], [2.72, 0.99347], [2.73, 0.99367], [2.74, 0.99386], [2.75, 0.99404], [2.76, 0.99422], [2.77, 0.99439], [2.78, 0.99456], [2.79, 0.99473], [2.8, 0.99489], [2.81, 0.99505], [2.82, 0.9952], [2.83, 0.99535], [2.84, 0.99549], [2.85, 0.99563], [2.86, 0.99576], [2.87, 0.9959], [2.88, 0.99602], [2.89, 0.99615], [2.9, 0.99627], [2.91, 0.99639], [2.92, 0.9965], [2.93, 0.99661], [2.94, 0.99672], [2.95, 0.99682], [2.96, 0.99692], [2.97, 0.99702], [2.98, 0.99712], [2.99, 0.99721], [3.0, 0.9973], [3.01, 0.99739]], fill=0.0, dims=(2,))
InpFontName = _input('InpFontName', 'Consolas')  # Font Name
InpFontSize = _input('InpFontSize', 10)  # Font Size
InpFontColor = _input('InpFontColor', clrBlack)  # Text Color

class CArray(CObject):
    _q_fields = ('m_step_resize', 'm_data_total', 'm_data_max', 'm_sort_mode')
    def __init__(self):
        CObject.__init__(self)
        self.m_step_resize = 0
        self.m_data_total = 0
        self.m_data_max = 0
        self.m_sort_mode = 0
        self.m_step_resize = 16
        self.m_data_total = 0
        self.m_data_max = 0
        self.m_sort_mode = -1
    def _q_dtor(self):
        pass
    def Step_0(self):
        return self.m_step_resize
    def Step_1(self, step):
        if step > 0:
            self.m_step_resize = step
            return True
        return False
    def Total(self):
        return self.m_data_total
    def Available(self):
        return self.m_data_max - self.m_data_total
    def Max(self):
        return self.m_data_max
    def IsSorted(self, mode=0):
        return self.m_sort_mode == mode
    def SortMode(self):
        return self.m_sort_mode
    def Clear(self):
        self.m_data_total = 0
    def Save(self, file_handle):
        if file_handle != INVALID_HANDLE:
            if _missing('FileWriteLong')(file_handle, -1) == 8:
                if FileWriteInteger(file_handle, self.Type(), INT_VALUE) == INT_VALUE:
                    return True
        return False
    def Load(self, file_handle):
        if file_handle != INVALID_HANDLE:
            if _missing('FileReadLong')(file_handle) == -1:
                if FileReadInteger(file_handle, INT_VALUE) == self.Type():
                    return True
        return False
    def Sort(self, mode=0):
        if self.IsSorted(mode):
            return
        self.m_sort_mode = mode
        if self.m_data_total <= 1:
            return
        self.QuickSort(0, self.m_data_total - 1, mode)
    def QuickSort(self, beg, end, mode=0):
        self.m_sort_mode = -1
    def Minimum(self, data, start, count):
        real_count = 0
        if self.m_data_total < 1:
            SetUserError(1000)
            return -1
        if start < 0 or start >= self.m_data_total:
            SetUserError(3)
            return -1
        real_count = ((self.m_data_total - start) if (count == WHOLE_ARRAY or (start + count) > self.m_data_total) else count)
        return ArrayMinimum(data, start, real_count)
    def Maximum(self, data, start, count):
        real_count = 0
        if self.m_data_total < 1:
            SetUserError(1000)
            return -1
        if start < 0 or start >= self.m_data_total:
            SetUserError(3)
            return -1
        real_count = ((self.m_data_total - start) if (count == WHOLE_ARRAY or (start + count) > self.m_data_total) else count)
        return ArrayMaximum(data, start, real_count)

class CArrayObj(CArray):
    _q_fields = ('m_data', 'm_free_mode')
    _q_ptrs = ('m_data',)
    def __init__(self):
        CArray.__init__(self)
        self.m_data = Arr(0, None)
        self.m_free_mode = False
        self.m_free_mode = True
        self.m_data_max = ArraySize(self.m_data)
    def _q_dtor(self):
        if self.m_data_max != 0:
            self.Shutdown()
    def FreeMode_0(self):
        return self.m_free_mode
    def FreeMode_1(self, mode):
        self.m_free_mode = mode
    def Type(self):
        return 0x7778
    def Save(self, file_handle):
        i = 0
        if not CArray.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, self.m_data_total, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        while i < self.m_data_total:
            if self.m_data[i].Save(file_handle) != True:
                break
            i += 1
        return i == self.m_data_total
    def Load(self, file_handle):
        i = 0
        num = 0
        if not CArray.Load(self, file_handle):
            return False
        num = FileReadInteger(file_handle, INT_VALUE)
        self.Clear()
        if num != 0:
            if not self.Reserve(num):
                return False
            i = 0
            for i in range(i, num):
                if not self.CreateElement(i):
                    break
                if self.m_data[i].Load(file_handle) != True:
                    break
                self.m_data_total += 1
            else:
                i = _range_end(i, num, 1)
        self.m_sort_mode = -1
        return self.m_data_total == num
    def CreateElement(self, index):
        return False
    def Reserve(self, size):
        new_size = 0
        if size <= 0:
            return False
        if self.Available() < size:
            new_size = self.m_data_max + (self.m_step_resize * (1 + _idiv(size - self.Available(), self.m_step_resize)))
            if new_size < 0:
                return False
            if _setattr(self, 'm_data_max', ArrayResize(self.m_data, new_size)) == -1:
                self.m_data_max = ArraySize(self.m_data)
            for i in range(self.m_data_total, self.m_data_max):
                self.m_data[i] = None
        return self.Available() >= size
    def Resize(self, size):
        new_size = 0
        if size < 0:
            return False
        new_size = self.m_step_resize * (1 + _idiv(size, self.m_step_resize))
        if self.m_data_total > size:
            if self.m_free_mode:
                for i in range(size, self.m_data_total):
                    if CheckPointer(self.m_data[i]) == POINTER_DYNAMIC:
                        _delete(self.m_data[i])
            self.m_data_total = size
        if self.m_data_max != new_size:
            if _setattr(self, 'm_data_max', ArrayResize(self.m_data, new_size)) == -1:
                self.m_data_max = ArraySize(self.m_data)
                return False
        return self.m_data_max == new_size
    def Shutdown(self):
        if self.m_data_max == 0:
            return True
        self.Clear()
        if ArrayResize(self.m_data, 0) == -1:
            return False
        self.m_data_max = 0
        return True
    def Add(self, element):
        if not CheckPointer(element):
            return False
        if not self.Reserve(1):
            return False
        self.m_data[_incattr(self, 'm_data_total', 1, True)] = element
        self.m_sort_mode = -1
        return True
    def AddArray(self, src):
        num = 0
        if not CheckPointer(src):
            return False
        num = src.Total()
        if not self.Reserve(num):
            return False
        for i in range(0, num):
            self.m_data[_incattr(self, 'm_data_total', 1, True)] = src.m_data[i]
        self.m_sort_mode = -1
        return True
    def Insert(self, element, pos):
        if pos < 0 or (not CheckPointer(element)):
            return False
        if not self.Reserve(1):
            return False
        self.m_data_total += 1
        if pos < (self.m_data_total - 1):
            if self.MemMove(pos + 1, pos, self.m_data_total - pos - 1) < 0:
                return False
            self.m_data[pos] = element
        else:
            self.m_data[self.m_data_total - 1] = element
        self.m_sort_mode = -1
        return True
    def InsertArray(self, src, pos):
        num = 0
        if not CheckPointer(src):
            return False
        num = src.Total()
        if not self.Reserve(num):
            return False
        if self.MemMove(num + pos, pos, self.m_data_total - pos) < 0:
            return False
        for i in range(0, num):
            self.m_data[i + pos] = src.m_data[i]
        self.m_sort_mode = -1
        return True
    def AssignArray(self, src):
        num = 0
        if not CheckPointer(src):
            return False
        num = src.m_data_total
        self.Clear()
        if self.m_data_max < num:
            if not self.Reserve(num):
                return False
        else:
            self.Resize(num)
        for i in range(0, num):
            self.m_data[i] = src.m_data[i]
            self.m_data_total += 1
        self.m_sort_mode = src.SortMode()
        return True
    def At(self, index):
        if index < 0 or index >= self.m_data_total:
            return None
        return self.m_data[index]
    def Update(self, index, element):
        if (index < 0 or (not CheckPointer(element))) or index >= self.m_data_total:
            return False
        if self.m_free_mode and CheckPointer(self.m_data[index]) == POINTER_DYNAMIC:
            _delete(self.m_data[index])
        self.m_data[index] = element
        self.m_sort_mode = -1
        return True
    def Shift(self, index, shift):
        tmp_node = None
        if (index < 0 or (index + shift) < 0) or (index + shift) >= self.m_data_total:
            return False
        if shift == 0:
            return True
        tmp_node = self.m_data[index]
        self.m_data[index] = None
        if shift > 0:
            if self.MemMove(index, index + 1, shift) < 0:
                return False
        else:
            if self.MemMove(index + shift + 1, index + shift, -shift) < 0:
                return False
        self.m_data[index + shift] = tmp_node
        self.m_sort_mode = -1
        return True
    def Detach(self, index):
        result = None
        if index >= self.m_data_total:
            return None
        result = self.m_data[index]
        self.m_data[index] = None
        if index < (self.m_data_total - 1) and self.MemMove(index, index + 1, self.m_data_total - index - 1) < 0:
            return None
        self.m_data_total -= 1
        return result
    def Delete(self, index):
        if index >= self.m_data_total:
            return False
        if index < (self.m_data_total - 1):
            if index >= 0 and self.MemMove(index, index + 1, self.m_data_total - index - 1) < 0:
                return False
        elif self.m_free_mode and CheckPointer(self.m_data[index]) == POINTER_DYNAMIC:
            _delete(self.m_data[index])
        self.m_data_total -= 1
        return True
    def DeleteRange(self, from_, to):
        if from_ < 0 or to < 0:
            return False
        if from_ > to or from_ >= self.m_data_total:
            return False
        if to >= (self.m_data_total - 1):
            to = self.m_data_total - 1
        if self.MemMove(from_, to + 1, self.m_data_total - to - 1) < 0:
            return False
        i = to - from_ + 1
        while i > 0:
            if self.m_free_mode and CheckPointer(self.m_data[self.m_data_total - 1]) == POINTER_DYNAMIC:
                _delete(self.m_data[self.m_data_total - 1])
            i -= 1
            self.m_data_total -= 1
        return True
    def Clear(self):
        if self.m_free_mode:
            for i in range(0, self.m_data_total):
                if CheckPointer(self.m_data[i]) == POINTER_DYNAMIC:
                    _delete(self.m_data[i])
                self.m_data[i] = None
        self.m_data_total = 0
    def CompareArray(self, array):
        if not CheckPointer(array):
            return False
        if self.m_data_total != array.m_data_total:
            return False
        i = 0
        while i < self.m_data_total:
            if self.m_data[i].Compare(array.m_data[i], 0) != 0:
                return False
            i += 1
        return True
    def InsertSort(self, element):
        pos = 0
        if (not CheckPointer(element)) or self.m_sort_mode == -1:
            return False
        if not self.Reserve(1):
            return False
        if self.m_data_total == 0:
            self.m_data[_incattr(self, 'm_data_total', 1, True)] = element
            return True
        mode = self.m_sort_mode
        pos = self.QuickSearch(element)
        if self.m_data[pos].Compare(element, self.m_sort_mode) > 0:
            self.Insert(element, pos)
        else:
            self.Insert(element, pos + 1)
        self.m_sort_mode = mode
        return True
    def Search(self, element):
        pos = 0
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos].Compare(element, self.m_sort_mode) == 0:
            return pos
        return -1
    def SearchGreat(self, element):
        pos = 0
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        pos = self.QuickSearch(element)
        while self.m_data[pos].Compare(element, self.m_sort_mode) <= 0:
            if (pos := pos + 1) == self.m_data_total:
                return -1
        return pos
    def SearchLess(self, element):
        pos = 0
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        pos = self.QuickSearch(element)
        while self.m_data[pos].Compare(element, self.m_sort_mode) >= 0:
            if ((pos := pos - 1) + 1) == 0:
                return -1
        return pos
    def SearchGreatOrEqual(self, element):
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        pos = self.QuickSearch(element)
        while pos < self.m_data_total:
            if self.m_data[pos].Compare(element, self.m_sort_mode) >= 0:
                return pos
            pos += 1
        return -1
    def SearchLessOrEqual(self, element):
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        for pos in range(self.QuickSearch(element), 0 - 1, -1):
            if self.m_data[pos].Compare(element, self.m_sort_mode) <= 0:
                return pos
        return -1
    def SearchFirst(self, element):
        pos = 0
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos].Compare(element, self.m_sort_mode) == 0:
            while self.m_data[pos].Compare(element, self.m_sort_mode) == 0:
                if ((pos := pos - 1) + 1) == 0:
                    break
            return pos + 1
        return -1
    def SearchLast(self, element):
        pos = 0
        if (self.m_data_total == 0 or (not CheckPointer(element))) or self.m_sort_mode == -1:
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos].Compare(element, self.m_sort_mode) == 0:
            while self.m_data[pos].Compare(element, self.m_sort_mode) == 0:
                if (pos := pos + 1) == self.m_data_total:
                    break
            return pos - 1
        return -1
    def QuickSort(self, beg, end, mode):
        i = 0
        j = 0
        p_node = None
        t_node = None
        i = beg
        j = end
        while i < end:
            p_node = self.m_data[(beg + end) >> 1]
            while i < j:
                while self.m_data[i].Compare(p_node, mode) < 0:
                    if i == (self.m_data_total - 1):
                        break
                    i += 1
                while self.m_data[j].Compare(p_node, mode) > 0:
                    if j == 0:
                        break
                    j -= 1
                if i <= j:
                    t_node = self.m_data[i]
                    self.m_data[((i := i + 1) - 1)] = self.m_data[j]
                    self.m_data[j] = t_node
                    if j == 0:
                        break
                    j -= 1
            if beg < j:
                self.QuickSort(beg, j, mode)
            beg = i
            j = end
    def QuickSearch(self, element):
        i = 0
        j = 0
        m = -1
        t_node = None
        i = 0
        j = self.m_data_total - 1
        while j >= i:
            m = (j + i) >> 1
            if m < 0 or m == (self.m_data_total - 1):
                break
            t_node = self.m_data[m]
            if t_node.Compare(element, self.m_sort_mode) == 0:
                break
            if t_node.Compare(element, self.m_sort_mode) > 0:
                j = m - 1
            else:
                i = m + 1
        return m
    def MemMove(self, dest, src, count):
        i = 0
        if (dest < 0 or src < 0) or count < 0:
            return -1
        if (src + count) > self.m_data_total:
            count = self.m_data_total - src
        if count < 0:
            return -1
        if dest == src or count == 0:
            return dest
        if (dest + count) > self.m_data_total:
            if self.m_data_max < (dest + count):
                return -1
            self.m_data_total = dest + count
        if dest < src:
            i = 0
            for i in range(i, count):
                if self.m_free_mode and CheckPointer(self.m_data[dest + i]) == POINTER_DYNAMIC:
                    _delete(self.m_data[dest + i])
                self.m_data[dest + i] = self.m_data[src + i]
                self.m_data[src + i] = None
            else:
                i = _range_end(i, count, 1)
        else:
            i = count - 1
            for i in range(i, 0 - 1, -1):
                if self.m_free_mode and CheckPointer(self.m_data[dest + i]) == POINTER_DYNAMIC:
                    _delete(self.m_data[dest + i])
                self.m_data[dest + i] = self.m_data[src + i]
                self.m_data[src + i] = None
            else:
                i = _range_end(i, 0 - 1, -1)
        return dest

class CWndContainer(CWnd):
    _q_fields = ('m_controls',)
    def __init__(self):
        CWnd.__init__(self)
        self.m_controls = CArrayObj()
    def _q_dtor(self):
        pass
    def Destroy(self, reason=0):
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(0)
            if control is None:
                continue
            control.Destroy()
            self.m_controls.Delete(0)
    def OnEvent(self, id_, lparam, dparam, sparam):
        if self.m_drag_object is not None and self.m_drag_object.OnEvent(id_, lparam, dparam, sparam):
            return True
        total = self.m_controls.Total()
        for i in range(total - 1, 0 - 1, -1):
            control = self.Control(i)
            if control is None:
                continue
            if control.OnEvent(id_, lparam, dparam, sparam):
                return True
        return False
    def OnMouseEvent(self, x, y, flags):
        if not ((self.m_state_flags & WND_STATE_FLAG_VISIBLE) != 0):
            return False
        if self.m_drag_object is not None and self.m_drag_object.OnMouseEvent(x, y, flags):
            return True
        total = self.m_controls.Total()
        for i in range(total - 1, 0 - 1, -1):
            control = self.Control(i)
            if control is None:
                continue
            if control.OnMouseEvent(x, y, flags):
                return True
        return CWnd.OnMouseEvent(self, x, y, flags)
    def ControlsTotal(self):
        return self.m_controls.Total()
    def Control(self, ind):
        return self.m_controls.At(ind)
    def ControlFind(self, id_):
        result = CWnd.ControlFind(self, id_)
        if result is not None:
            return result
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            result = control.ControlFind(id_)
            if result is not None:
                break
        return result
    def MouseFocusKill(self, id_=-1):
        if not ((self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0):
            return False
        self.Deactivate()
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.MouseFocusKill()
        return True
    def Add_1(self, control):
        if control is None:
            return False
        control.Shift(self.Left_0(), self.Top_0())
        if (self.m_state_flags & WND_STATE_FLAG_VISIBLE) != 0 and control.IsVisible():
            control.Visible(self.Contains_1(control))
        else:
            control.Hide()
        if (self.m_state_flags & WND_STATE_FLAG_ENABLE) != 0:
            control.Enable()
        else:
            control.Disable()
        return self.m_controls.Add(control)
    def Add_2(self, control):
        return self.Add_1(control)
    def Delete_1(self, control):
        if control is None:
            return False
        total = self.m_controls.Total()
        for i in range(0, total):
            pointer = self.Control(i)
            if pointer is None:
                continue
            if pointer == control:
                return self.m_controls.Delete(i)
        return False
    def Delete_2(self, control):
        return self.Delete_1(control)
    def Move_2(self, x, y):
        return self.Shift(x - self.Left_0(), y - self.Top_0())
    def Move_1(self, point):
        return self.Shift(point.x - self.Left_0(), point.y - self.Top_0())
    def Shift(self, dx, dy):
        if not CWnd.Shift(self, dx, dy):
            return False
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Shift(dx, dy)
        return True
    def Id_1(self, id_):
        id_used = 1
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            id_used += control.Id_1(id_ + id_used)
        self.m_id = id_
        return id_used
    def Id_0(self):
        return CWnd.Id_0(self)
    def Enable(self):
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Enable()
        return CWnd.Enable(self)
    def Disable(self):
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Disable()
        return CWnd.Disable(self)
    def Show(self):
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Show()
        return CWnd.Show(self)
    def Hide(self):
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Hide()
        return CWnd.Hide(self)
    def Save(self, file_handle):
        result = True
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            result &= control.Save(file_handle)
        return result
    def Load(self, file_handle):
        result = True
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            result &= control.Load(file_handle)
        return result
    def OnResize(self):
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            if not control.Align(self.Rect()):
                return False
        return True
    def OnActivate(self):
        if (self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0:
            return False
        self.Activate()
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Activate()
        return True
    def OnDeactivate(self):
        if not ((self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0):
            return False
        self.Deactivate()
        total = self.m_controls.Total()
        for i in range(0, total):
            control = self.Control(i)
            if control is None:
                continue
            control.Deactivate()
        return True

class CChartObject(CObject):
    _q_fields = ('m_chart_id', 'm_window', 'm_name', 'm_num_points')
    def __init__(self):
        CObject.__init__(self)
        self.m_chart_id = 0
        self.m_window = 0
        self.m_name = ""
        self.m_num_points = 0
        self.Detach()
    def _q_dtor(self):
        if self.m_chart_id != -1:
            ObjectDelete(self.m_chart_id, self.m_name)
    def Type(self):
        return 0x8888
    def ChartId(self):
        return self.m_chart_id
    def Window(self):
        return self.m_window
    def Name_0(self):
        return self.m_name
    def Name_1(self, name):
        if self.m_chart_id == -1:
            return False
        if ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_NAME, name):
            self.m_name = name
            return True
        return False
    def NumPoints(self):
        return self.m_num_points
    def Attach(self, chart_id, name, window, points):
        if ObjectFind(chart_id, name) < 0:
            return False
        if chart_id == 0:
            chart_id = ChartID()
        self.m_chart_id = chart_id
        self.m_window = window
        self.m_name = name
        self.m_num_points = points
        return True
    def SetPoint(self, point, time, price):
        if self.m_chart_id == -1:
            return False
        if point >= self.m_num_points:
            return False
        return ObjectMove(self.m_chart_id, self.m_name, point, time, price)
    def Delete(self):
        if self.m_chart_id == -1:
            return False
        result = ObjectDelete(self.m_chart_id, self.m_name)
        self.Detach()
        return result
    def Detach(self):
        self.m_chart_id = -1
        self.m_window = -1
        self.m_name = ""
        self.m_num_points = 0
    def Time_1(self, point):
        if self.m_chart_id == -1:
            return 0
        if point >= self.m_num_points:
            return 0
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_TIME, point)
    def Time_2(self, point, time):
        if self.m_chart_id == -1:
            return False
        if point >= self.m_num_points:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_TIME, point, time)
    def Price_1(self, point):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        if point >= self.m_num_points:
            return EMPTY_VALUE
        return ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_PRICE, point)
    def Price_2(self, point, price):
        if self.m_chart_id == -1:
            return False
        if point >= self.m_num_points:
            return False
        return ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_PRICE, point, price)
    def Color_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_COLOR))
    def Color_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_COLOR, new_color)
    def Style_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_STYLE)
    def Style_1(self, new_style):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_STYLE, new_style)
    def Width_0(self):
        if self.m_chart_id == -1:
            return -1
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_WIDTH))
    def Width_1(self, new_width):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_WIDTH, new_width)
    def Background_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BACK))
    def Background_1(self, new_back):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BACK, new_back)
    def Fill_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_FILL))
    def Fill_1(self, new_fill):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_FILL, new_fill)
    def Z_Order_0(self):
        if self.m_chart_id == -1:
            return 0
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_ZORDER)
    def Z_Order_1(self, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_ZORDER, value)
    def Selected_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_SELECTED))
    def Selected_1(self, new_sel):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_SELECTED, new_sel)
    def Selectable_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_SELECTABLE))
    def Selectable_1(self, new_sel):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_SELECTABLE, new_sel)
    def Description_0(self):
        if self.m_chart_id == -1:
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_TEXT)
    def Description_1(self, new_text):
        if self.m_chart_id == -1:
            return False
        if new_text == '':
            return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_TEXT, ' ')
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_TEXT, new_text)
    def Tooltip_0(self):
        if self.m_chart_id == -1:
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_TOOLTIP)
    def Tooltip_1(self, new_text):
        if self.m_chart_id == -1:
            return False
        if new_text == '':
            return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_TOOLTIP, ' ')
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_TOOLTIP, new_text)
    def Timeframes_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_TIMEFRAMES))
    def Timeframes_1(self, timeframes):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_TIMEFRAMES, timeframes)
    def CreateTime(self):
        if self.m_chart_id == -1:
            return 0
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_CREATETIME)
    def LevelsCount_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELS))
    def LevelsCount_1(self, new_count):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELS, new_count)
    def LevelColor_1(self, level):
        if self.m_chart_id == -1:
            return clrNONE
        if level >= self.LevelsCount_0():
            return clrNONE
        return _uint(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELCOLOR, level))
    def LevelColor_2(self, level, new_color):
        if self.m_chart_id == -1:
            return False
        if level >= self.LevelsCount_0():
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELCOLOR, level, new_color)
    def LevelStyle_1(self, level):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        if level >= self.LevelsCount_0():
            return WRONG_VALUE
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELSTYLE, level)
    def LevelStyle_2(self, level, new_style):
        if self.m_chart_id == -1:
            return False
        if level >= self.LevelsCount_0():
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELSTYLE, level, new_style)
    def LevelWidth_1(self, level):
        if self.m_chart_id == -1:
            return -1
        if level >= self.LevelsCount_0():
            return -1
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELWIDTH, level))
    def LevelWidth_2(self, level, new_width):
        if self.m_chart_id == -1:
            return False
        if level >= self.LevelsCount_0():
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELWIDTH, level, new_width)
    def LevelValue_1(self, level):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        if level >= self.LevelsCount_0():
            return EMPTY_VALUE
        return ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_LEVELVALUE, level)
    def LevelValue_2(self, level, new_value):
        if self.m_chart_id == -1:
            return False
        if level >= self.LevelsCount_0():
            return False
        return ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_LEVELVALUE, level, new_value)
    def LevelDescription_1(self, level):
        if self.m_chart_id == -1:
            return ''
        if level >= self.LevelsCount_0():
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_LEVELTEXT, level)
    def LevelDescription_2(self, level, new_text):
        if self.m_chart_id == -1:
            return False
        if level >= self.LevelsCount_0():
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_LEVELTEXT, level, new_text)
    def GetInteger_2(self, prop_id, modifier=-1):
        if self.m_chart_id == -1:
            return 0
        if modifier == -1:
            return ObjectGetInteger(self.m_chart_id, self.m_name, prop_id)
        return ObjectGetInteger(self.m_chart_id, self.m_name, prop_id, modifier)
    def GetInteger_3(self, prop_id, modifier, value):
        if self.m_chart_id == -1:
            return False
        return (ObjectGetInteger(self.m_chart_id, self.m_name, prop_id, modifier, value) != 0)
    def SetInteger_3(self, prop_id, modifier, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, prop_id, modifier, value)
    def SetInteger_2(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, prop_id, value)
    def GetDouble_2(self, prop_id, modifier=-1):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        if modifier == -1:
            return ObjectGetDouble(self.m_chart_id, self.m_name, prop_id)
        return ObjectGetDouble(self.m_chart_id, self.m_name, prop_id, modifier)
    def GetDouble_3(self, prop_id, modifier, value):
        if self.m_chart_id == -1:
            return False
        return (ObjectGetDouble(self.m_chart_id, self.m_name, prop_id, modifier, value) != 0)
    def SetDouble_3(self, prop_id, modifier, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetDouble(self.m_chart_id, self.m_name, prop_id, modifier, value)
    def SetDouble_2(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetDouble(self.m_chart_id, self.m_name, prop_id, value)
    def GetString_2(self, prop_id, modifier=-1):
        if self.m_chart_id == -1:
            return ''
        if modifier == -1:
            return ObjectGetString(self.m_chart_id, self.m_name, prop_id)
        return ObjectGetString(self.m_chart_id, self.m_name, prop_id, modifier)
    def GetString_3(self, prop_id, modifier, value):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetString(self.m_chart_id, self.m_name, prop_id, modifier, value))
    def SetString_3(self, prop_id, modifier, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, prop_id, modifier, value)
    def SetString_2(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, prop_id, value)
    def ShiftObject(self, d_time, d_price):
        result = True
        i = 0
        if self.m_chart_id == -1:
            return False
        i = 0
        while i < self.m_num_points:
            result &= self.ShiftPoint(i, d_time, d_price)
            i += 1
        return result
    def ShiftPoint(self, point, d_time, d_price):
        if self.m_chart_id == -1:
            return False
        if point >= self.m_num_points:
            return False
        time = ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_TIME, point)
        price = ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_PRICE, point)
        return ObjectMove(self.m_chart_id, self.m_name, point, time + d_time, price + d_price)
    def Save(self, file_handle):
        i = 0
        len_ = 0
        levels = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if _missing('FileWriteLong')(file_handle, -1) != 8:
            return False
        if FileWriteInteger(file_handle, self.Type(), INT_VALUE) != INT_VALUE:
            return False
        str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_NAME)
        len_ = StringLen(str_)
        if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
            return False
        if len_ != 0:
            if FileWriteString(file_handle, str_, len_) != len_:
                return False
        if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_COLOR)) != 8:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_STYLE))) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_WIDTH))) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BACK)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_SELECTABLE)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_TIMEFRAMES)), INT_VALUE) != 4:
            return False
        str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_TEXT)
        len_ = StringLen(str_)
        if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
            return False
        if len_ != 0:
            if FileWriteString(file_handle, str_, len_) != len_:
                return False
        if FileWriteInteger(file_handle, self.m_num_points, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        for i in range(i, self.m_num_points):
            if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_TIME, i)) != 8:
                return False
            if FileWriteDouble(file_handle, ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_PRICE, i)) != 8:
                return False
        else:
            i = _range_end(i, self.m_num_points, 1)
        levels = _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELS))
        if FileWriteInteger(file_handle, levels, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        for i in range(i, levels):
            if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELCOLOR, i)) != 8:
                return False
            if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELSTYLE, i))) != 4:
                return False
            if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELWIDTH, i))) != 4:
                return False
            if FileWriteDouble(file_handle, ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_LEVELVALUE, i)) != 8:
                return False
            str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_LEVELTEXT, i)
            len_ = StringLen(str_)
            if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
                return False
            if len_ != 0:
                if FileWriteString(file_handle, str_, len_) != len_:
                    return False
        else:
            i = _range_end(i, levels, 1)
        return True
    def Load(self, file_handle):
        i = 0
        len_ = 0
        num = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if _missing('FileReadLong')(file_handle) != -1:
            return False
        if FileReadInteger(file_handle, INT_VALUE) != self.Type():
            return False
        len_ = FileReadInteger(file_handle, INT_VALUE)
        str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
        if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_NAME, str_):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_COLOR, _missing('FileReadLong')(file_handle)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_STYLE, FileReadInteger(file_handle)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_WIDTH, FileReadInteger(file_handle)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BACK, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_SELECTABLE, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_TIMEFRAMES, FileReadInteger(file_handle, INT_VALUE)):
            return False
        len_ = FileReadInteger(file_handle, INT_VALUE)
        str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
        if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_TEXT, str_):
            return False
        num = FileReadInteger(file_handle, INT_VALUE)
        if num != 0:
            i = 0
            for i in range(i, num):
                if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_TIME, i, _missing('FileReadLong')(file_handle)):
                    return False
                if not ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_PRICE, i, FileReadDouble(file_handle)):
                    return False
            else:
                i = _range_end(i, num, 1)
        num = FileReadInteger(file_handle, INT_VALUE)
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELS, 0, num):
            return False
        if num != 0:
            i = 0
            for i in range(i, num):
                if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELCOLOR, i, _missing('FileReadLong')(file_handle)):
                    return False
                if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELSTYLE, i, FileReadInteger(file_handle)):
                    return False
                if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_LEVELWIDTH, i, FileReadInteger(file_handle)):
                    return False
                if not ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_LEVELVALUE, i, FileReadDouble(file_handle)):
                    return False
                len_ = FileReadInteger(file_handle, INT_VALUE)
                str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
                if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_LEVELTEXT, i, str_):
                    return False
            else:
                i = _range_end(i, num, 1)
        return True

class CChartObjectText(CChartObject):
    _q_fields = ()
    def __init__(self):
        CChartObject.__init__(self)
    def _q_dtor(self):
        pass
    def Create(self, chart_id, name, window, time, price):
        if not ObjectCreate(chart_id, name, OBJ_TEXT, window, time, price):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        return True
    def Type(self):
        return OBJ_TEXT
    def Angle_0(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_ANGLE)
    def Angle_1(self, angle):
        if self.m_chart_id == -1:
            return False
        return ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_ANGLE, angle)
    def Font_0(self):
        if self.m_chart_id == -1:
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_FONT)
    def Font_1(self, font):
        if self.m_chart_id == -1:
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_FONT, font)
    def FontSize_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_FONTSIZE))
    def FontSize_1(self, size):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_FONTSIZE, size)
    def Anchor_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_ANCHOR)
    def Anchor_1(self, anchor):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_ANCHOR, anchor)
    def Save(self, file_handle):
        len_ = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Save(self, file_handle):
            return False
        if FileWriteDouble(file_handle, ObjectGetDouble(self.m_chart_id, self.m_name, OBJPROP_ANGLE)) != 8:
            return False
        str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_FONT)
        len_ = StringLen(str_)
        if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
            return False
        if len_ != 0 and FileWriteString(file_handle, str_, len_) != len_:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_FONTSIZE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_ANCHOR)), INT_VALUE) != 4:
            return False
        return True
    def Load(self, file_handle):
        len_ = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Load(self, file_handle):
            return False
        if not ObjectSetDouble(self.m_chart_id, self.m_name, OBJPROP_ANGLE, 0, FileReadDouble(file_handle)):
            return False
        len_ = FileReadInteger(file_handle, INT_VALUE)
        str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
        if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_FONT, str_):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_FONTSIZE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_ANCHOR, FileReadInteger(file_handle, INT_VALUE)):
            return False
        return True

class CChartObjectLabel(CChartObjectText):
    _q_fields = ()
    def __init__(self):
        CChartObjectText.__init__(self)
    def _q_dtor(self):
        pass
    def Create(self, chart_id, name, window, X, Y):
        if not ObjectCreate(chart_id, name, OBJ_LABEL, window, 0, 0.0):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        if not self.Description_1(name):
            return False
        if (not self.X_Distance_1(X)) or (not self.Y_Distance_1(Y)):
            return False
        return True
    def Type(self):
        return OBJ_LABEL
    def X_Distance_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE))
    def X_Distance_1(self, X):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE, X)
    def Y_Distance_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE))
    def Y_Distance_1(self, Y):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE, Y)
    def X_Size(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE))
    def Y_Size(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE))
    def Corner_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER)
    def Corner_1(self, corner):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER, corner)
    def Time_1(self, point):
        return CChartObject.Time_1(self, point)
    def Time_2(self, point, time):
        return False
    def Price_1(self, point):
        return CChartObject.Price_1(self, point)
    def Price_2(self, point, price):
        return False
    def Save(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectText.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER)), INT_VALUE) != 4:
            return False
        return True
    def Load(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectText.Load(self, file_handle):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER, FileReadInteger(file_handle, INT_VALUE)):
            return False
        return True

class CChartObjectEdit(CChartObjectLabel):
    _q_fields = ()
    def __init__(self):
        CChartObjectLabel.__init__(self)
    def _q_dtor(self):
        pass
    def Create(self, chart_id, name, window, X, Y, sizeX, sizeY):
        if not ObjectCreate(chart_id, name, self.Type(), window, 0, 0, 0):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        if (not self.X_Distance_1(X)) or (not self.Y_Distance_1(Y)):
            return False
        if (not self.X_Size_1(sizeX)) or (not self.Y_Size_1(sizeY)):
            return False
        return True
    def Type(self):
        return OBJ_EDIT
    def X_Size_1(self, X):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE, X)
    def X_Size_0(self):
        return CChartObjectLabel.X_Size(self)
    def Y_Size_1(self, Y):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE, Y)
    def Y_Size_0(self):
        return CChartObjectLabel.Y_Size(self)
    def BackColor_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR))
    def BackColor_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR, new_color)
    def BorderColor_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BORDER_COLOR))
    def BorderColor_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BORDER_COLOR, new_color)
    def ReadOnly_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_READONLY))
    def ReadOnly_1(self, flag):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_READONLY, flag)
    def TextAlign_0(self):
        if self.m_chart_id == -1:
            return False
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_ALIGN)
    def TextAlign_1(self, align):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_ALIGN, align)
    def Angle_1(self, angle):
        return False
    def Angle_0(self):
        return CChartObjectText.Angle_0(self)
    def Save(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectLabel.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE)), INT_VALUE) != 4:
            return False
        if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR)) != 8:
            return False
        return True
    def Load(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectLabel.Load(self, file_handle):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR, _missing('FileReadLong')(file_handle)):
            return False
        return True

class CChartObjectButton(CChartObjectEdit):
    _q_fields = ()
    def __init__(self):
        CChartObjectEdit.__init__(self)
    def _q_dtor(self):
        pass
    def Type(self):
        return OBJ_BUTTON
    def State_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE))
    def State_1(self, state):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE, state)
    def Save(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectEdit.Save(self, file_handle):
            return False
        if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE)) != 8:
            return False
        return True
    def Load(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectEdit.Load(self, file_handle):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE, _missing('FileReadLong')(file_handle)):
            return False
        return True

class CChartObjectRectLabel(CChartObjectLabel):
    _q_fields = ()
    def __init__(self):
        CChartObjectLabel.__init__(self)
    def _q_dtor(self):
        pass
    def Create(self, chart_id, name, window, X, Y, sizeX, sizeY):
        if not ObjectCreate(chart_id, name, self.Type(), window, 0, 0, 0):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        if (not self.X_Distance_1(X)) or (not self.Y_Distance_1(Y)):
            return False
        if (not self.X_Size_1(sizeX)) or (not self.Y_Size_1(sizeY)):
            return False
        return True
    def Type(self):
        return OBJ_RECTANGLE_LABEL
    def X_Size_1(self, X):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE, X)
    def X_Size_0(self):
        return CChartObjectLabel.X_Size(self)
    def Y_Size_1(self, Y):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE, Y)
    def Y_Size_0(self):
        return CChartObjectLabel.Y_Size(self)
    def BackColor_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR))
    def BackColor_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR, new_color)
    def BorderType_0(self):
        if self.m_chart_id == -1:
            return False
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BORDER_TYPE)
    def BorderType_1(self, type_):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BORDER_TYPE, type_)
    def Angle_1(self, angle):
        return False
    def Angle_0(self):
        return CChartObjectText.Angle_0(self)
    def Save(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectLabel.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE)), INT_VALUE) != 4:
            return False
        if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR)) != 8:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_BORDER_TYPE)), INT_VALUE) != 4:
            return False
        return True
    def Load(self, file_handle):
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObjectLabel.Load(self, file_handle):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BGCOLOR, _missing('FileReadLong')(file_handle)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_BORDER_TYPE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        return True

class CPanel(CWndObj):
    _q_fields = ('m_rectangle', 'm_border')
    def __init__(self):
        CWndObj.__init__(self)
        self.m_rectangle = CChartObjectRectLabel()
        self.m_border = 0
        self.m_border = BORDER_FLAT
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.m_rectangle.Create(chart, name, subwin, x1, y1, self.Width_0(), self.Height_0()):
            return False
        return self.OnChange()
    def BorderType_0(self):
        return self.m_border
    def BorderType_1(self, type_):
        self.m_border = type_
        return self.m_rectangle.BorderType_1(type_)
    def OnSetText(self):
        return self.m_rectangle.Description_1(self.m_text)
    def OnSetColorBackground(self):
        return self.m_rectangle.BackColor_1(self.m_color_background)
    def OnSetColorBorder(self):
        return self.m_rectangle.Color_1(self.m_color_border)
    def OnCreate(self):
        return self.m_rectangle.Create(self.m_chart_id, self.m_name, self.m_subwin, self.m_rect.left, self.m_rect.top, self.m_rect.Width_0(), self.m_rect.Height_0())
    def OnShow(self):
        return self.m_rectangle.Timeframes_1(_int(OBJ_ALL_PERIODS))
    def OnHide(self):
        return self.m_rectangle.Timeframes_1(_int(OBJ_NO_PERIODS))
    def OnMove(self):
        return self.m_rectangle.X_Distance_1(self.m_rect.left) and self.m_rectangle.Y_Distance_1(self.m_rect.top)
    def OnResize(self):
        return self.m_rectangle.X_Size_1(self.m_rect.Width_0()) and self.m_rectangle.Y_Size_1(self.m_rect.Height_0())
    def OnChange(self):
        return CWndObj.OnChange(self) and self.m_rectangle.BorderType_1(self.m_border)

class CChartObjectBitmap(CChartObject):
    _q_fields = ()
    def __init__(self):
        CChartObject.__init__(self)
    def _q_dtor(self):
        pass
    def BmpFile_0(self):
        if self.m_chart_id == -1:
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE)
    def BmpFile_1(self, name):
        if self.m_chart_id == -1:
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, name)
    def X_Offset_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XOFFSET))
    def X_Offset_1(self, X):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XOFFSET, X)
    def Y_Offset_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YOFFSET))
    def Y_Offset_1(self, Y):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YOFFSET, Y)
    def Create(self, chart_id, name, window, time, price):
        if not ObjectCreate(chart_id, name, OBJ_BITMAP, window, time, price):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        return True
    def Type(self):
        return OBJ_BITMAP
    def Save(self, file_handle):
        len_ = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Save(self, file_handle):
            return False
        str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE)
        len_ = StringLen(str_)
        if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
            return False
        if len_ != 0 and FileWriteString(file_handle, str_, len_) != len_:
            return False
        return True
    def Load(self, file_handle):
        len_ = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Load(self, file_handle):
            return False
        len_ = FileReadInteger(file_handle, INT_VALUE)
        str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
        if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, str_):
            return False
        return True

class CChartObjectBmpLabel(CChartObject):
    _q_fields = ()
    def __init__(self):
        CChartObject.__init__(self)
    def _q_dtor(self):
        pass
    def X_Distance_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE))
    def X_Distance_1(self, X):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE, X)
    def Y_Distance_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE))
    def Y_Distance_1(self, Y):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE, Y)
    def X_Size(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XSIZE))
    def Y_Size(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YSIZE))
    def Corner_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER)
    def Corner_1(self, corner):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER, corner)
    def BmpFileOn_0(self):
        if self.m_chart_id == -1:
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 0)
    def BmpFileOn_1(self, name):
        if self.m_chart_id == -1:
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 0, name)
    def BmpFileOff_0(self):
        if self.m_chart_id == -1:
            return ''
        return ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 1)
    def BmpFileOff_1(self, name):
        if self.m_chart_id == -1:
            return False
        return ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 1, name)
    def State_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE))
    def State_1(self, state):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE, state)
    def X_Offset_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XOFFSET))
    def X_Offset_1(self, X):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XOFFSET, X)
    def Y_Offset_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YOFFSET))
    def Y_Offset_1(self, Y):
        if self.m_chart_id == -1:
            return False
        return ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YOFFSET, Y)
    def Time(self, time):
        return False
    def Price(self, price):
        return False
    def Create(self, chart_id, name, window, X, Y):
        if not ObjectCreate(chart_id, name, OBJ_BITMAP_LABEL, window, 0, 0.0):
            return False
        if not self.Attach(chart_id, name, window, 1):
            return False
        if (not self.X_Distance_1(X)) or (not self.Y_Distance_1(Y)):
            return False
        return True
    def Type(self):
        return OBJ_BITMAP_LABEL
    def Save(self, file_handle):
        len_ = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER)), INT_VALUE) != 4:
            return False
        str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 0)
        len_ = StringLen(str_)
        if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
            return False
        if len_ != 0 and FileWriteString(file_handle, str_, len_) != len_:
            return False
        str_ = ObjectGetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 1)
        len_ = StringLen(str_)
        if FileWriteInteger(file_handle, len_, INT_VALUE) != INT_VALUE:
            return False
        if len_ != 0 and FileWriteString(file_handle, str_, len_) != len_:
            return False
        if _missing('FileWriteLong')(file_handle, ObjectGetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE)) != 8:
            return False
        return True
    def Load(self, file_handle):
        len_ = 0
        str_ = ""
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if not CChartObject.Load(self, file_handle):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_XDISTANCE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_YDISTANCE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_CORNER, FileReadInteger(file_handle, INT_VALUE)):
            return False
        len_ = FileReadInteger(file_handle, INT_VALUE)
        str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
        if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 0, str_):
            return False
        len_ = FileReadInteger(file_handle, INT_VALUE)
        str_ = (FileReadString(file_handle, len_) if (len_ != 0) else '')
        if not ObjectSetString(self.m_chart_id, self.m_name, OBJPROP_BMPFILE, 1, str_):
            return False
        if not ObjectSetInteger(self.m_chart_id, self.m_name, OBJPROP_STATE, _missing('FileReadLong')(file_handle)):
            return False
        return True

class CBmpButton(CWndObj):
    _q_fields = ('m_button', 'm_border', 'm_bmp_off_name', 'm_bmp_on_name', 'm_bmp_passive_name', 'm_bmp_active_name')
    def __init__(self):
        CWndObj.__init__(self)
        self.m_button = CChartObjectBmpLabel()
        self.m_border = 0
        self.m_bmp_off_name = ""
        self.m_bmp_on_name = ""
        self.m_bmp_passive_name = ""
        self.m_bmp_active_name = ""
        self.m_border = 0
        self.m_bmp_off_name = ""
        self.m_bmp_on_name = ""
        self.m_bmp_passive_name = ""
        self.m_bmp_active_name = ""
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.m_button.Create(chart, name, subwin, x1, y1):
            return False
        return self.OnChange()
    def Border_0(self):
        return self.m_border
    def Border_1(self, value):
        self.m_border = value
        return self.m_button.Width_1(value)
    def BmpNames(self, off='', on=''):
        self.m_bmp_off_name = off
        self.m_bmp_on_name = on
        if not self.m_button.BmpFileOff_1(off):
            return False
        if not self.m_button.BmpFileOn_1(on):
            return False
        return True
    def BmpOffName_0(self):
        return self.m_bmp_off_name
    def BmpOffName_1(self, name):
        self.m_bmp_off_name = name
        if not self.m_button.BmpFileOff_1(name):
            return False
        self.Width_1(self.m_button.X_Size())
        self.Height_1(self.m_button.Y_Size())
        return True
    def BmpOnName_0(self):
        return self.m_bmp_on_name
    def BmpOnName_1(self, name):
        self.m_bmp_on_name = name
        if not self.m_button.BmpFileOn_1(name):
            return False
        self.Width_1(self.m_button.X_Size())
        self.Height_1(self.m_button.Y_Size())
        return True
    def BmpPassiveName_0(self):
        return self.m_bmp_passive_name
    def BmpPassiveName_1(self, name):
        self.m_bmp_passive_name = name
        if not ((self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0):
            return self.BmpOffName_1(name)
        return True
    def BmpActiveName_0(self):
        return self.m_bmp_active_name
    def BmpActiveName_1(self, name):
        self.m_bmp_active_name = name
        if (self.m_state_flags & WND_STATE_FLAG_ACTIVE) != 0:
            return self.BmpOffName_1(name)
        return True
    def Pressed_0(self):
        return self.m_button.State_0()
    def Pressed_1(self, pressed):
        return self.m_button.State_1(pressed)
    def Locking_0(self):
        return (self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0
    def Locking_1(self, flag):
        if flag:
            self.PropFlagsSet(WND_PROP_FLAG_CAN_LOCK)
        else:
            self.PropFlagsReset(WND_PROP_FLAG_CAN_LOCK)
    def OnSetZOrder(self):
        return self.m_button.Z_Order_1(self.m_zorder)
    def OnCreate(self):
        return self.m_button.Create(self.m_chart_id, self.m_name, self.m_subwin, self.m_rect.left, self.m_rect.top)
    def OnShow(self):
        return self.m_button.Timeframes_1(_int(OBJ_ALL_PERIODS))
    def OnHide(self):
        return self.m_button.Timeframes_1(_int(OBJ_NO_PERIODS))
    def OnMove(self):
        return self.m_button.X_Distance_1(self.m_rect.left) and self.m_button.Y_Distance_1(self.m_rect.top)
    def OnChange(self):
        return (self.m_button.Width_1(self.m_border) and self.m_button.BmpFileOff_1(self.m_bmp_off_name)) and self.m_button.BmpFileOn_1(self.m_bmp_on_name)
    def OnActivate(self):
        if self.m_bmp_active_name != "":
            self.BmpOffName_1(self.m_bmp_active_name)
        return True
    def OnDeactivate(self):
        if self.m_bmp_passive_name != "":
            self.BmpOffName_1(self.m_bmp_passive_name)
        if not ((self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0):
            self.Pressed_1(False)
        return True
    def OnMouseDown(self):
        if not ((self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0):
            self.Pressed_1(not self.Pressed_0())
        return CWnd.OnMouseDown(self)
    def OnMouseUp(self):
        if self.m_button.State_0() and (not ((self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0)):
            self.m_button.State_1(False)
        return CWnd.OnMouseUp(self)

class CScroll(CWndContainer):
    _q_fields = ('m_back', 'm_inc', 'm_dec', 'm_thumb', 'm_min_pos', 'm_max_pos', 'm_curr_pos')
    def __init__(self):
        CWndContainer.__init__(self)
        self.m_back = CPanel()
        self.m_inc = CBmpButton()
        self.m_dec = CBmpButton()
        self.m_thumb = CBmpButton()
        self.m_min_pos = 0
        self.m_max_pos = 0
        self.m_curr_pos = 0
        self.m_curr_pos = 0
        self.m_min_pos = 0
        self.m_max_pos = 0
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.CreateBack():
            return False
        if not self.CreateInc():
            return False
        if not self.CreateDec():
            return False
        if not self.CreateThumb():
            return False
        return True
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ == (0 + CHARTEVENT_CUSTOM) and lparam == self.m_inc.Id_0():
            self.OnClickInc()
            return True
        if id_ == (0 + CHARTEVENT_CUSTOM) and lparam == self.m_dec.Id_0():
            self.OnClickDec()
            return True
        if id_ == (11 + CHARTEVENT_CUSTOM) and lparam == self.m_thumb.Id_0():
            self.OnThumbDragStart()
            return True
        if (self.m_drag_object is not None and id_ == (12 + CHARTEVENT_CUSTOM)) and lparam == self.m_drag_object.Id_0():
            self.OnThumbDragProcess()
            return True
        if (self.m_drag_object is not None and id_ == (13 + CHARTEVENT_CUSTOM)) and lparam == self.m_drag_object.Id_0():
            self.OnThumbDragEnd()
            return True
        return CWndContainer.OnEvent(self, id_, lparam, dparam, sparam)
    def MinPos_0(self):
        return self.m_min_pos
    def MinPos_1(self, value):
        if self.m_min_pos != value:
            self.m_min_pos = value
            self.CurrPos_1(self.m_curr_pos)
    def MaxPos_0(self):
        return self.m_max_pos
    def MaxPos_1(self, value):
        if self.m_max_pos != value:
            self.m_max_pos = value
            self.CurrPos_1(self.m_curr_pos)
    def CurrPos_0(self):
        return self.m_curr_pos
    def CurrPos_1(self, value):
        if value < self.m_min_pos:
            value = self.m_min_pos
        if value > self.m_max_pos:
            value = self.m_max_pos
        if self.m_curr_pos != value:
            self.m_curr_pos = value
            return self.OnChangePos()
        return False
    def CreateBack(self):
        if not self.m_back.Create(self.m_chart_id, self.m_name + 'Back', self.m_subwin, 0, 0, self.Width_0(), self.Height_0()):
            return False
        if not self.m_back.ColorBackground_1(0xECECEC):
            return False
        if not self.m_back.ColorBorder_1(0xD3D3D3):
            return False
        if not self.Add_1(self.m_back):
            return False
        return True
    def CreateInc(self):
        return True
    def CreateDec(self):
        return True
    def CreateThumb(self):
        return True
    def OnClickInc(self):
        if not self.CurrPos_1(self.m_curr_pos + 1):
            return True
        EventChartCustom(-1, 7, self.m_id, 0.0, self.m_name)
        return True
    def OnClickDec(self):
        if not self.CurrPos_1(self.m_curr_pos - 1):
            return True
        EventChartCustom(-1, 8, self.m_id, 0.0, self.m_name)
        return True
    def OnShow(self):
        if self.m_id == -1:
            return True
        EventChartCustom(-1, 2, self.m_id, 0.0, self.m_name)
        return True
    def OnHide(self):
        if self.m_id == -1:
            return True
        EventChartCustom(-1, 3, self.m_id, 0.0, self.m_name)
        return True
    def OnChangePos(self):
        return True
    def OnThumbDragStart(self):
        return True
    def OnThumbDragProcess(self):
        return True
    def OnThumbDragEnd(self):
        return True
    def CalcPos(self, coord):
        return 0

class CScrollV(CScroll):
    _q_fields = ()
    def __init__(self):
        CScroll.__init__(self)
    def _q_dtor(self):
        pass
    def CreateInc(self):
        x1 = 1
        y1 = self.Height_0() - 18 + 1
        x2 = x1 + 16
        y2 = y1 + 16
        if not self.m_inc.Create(self.m_chart_id, self.m_name + 'Inc', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_inc.BmpNames('::res\\Down.bmp'):
            return False
        if not self.Add_1(self.m_inc):
            return False
        self.m_inc.PropFlags_1(WND_PROP_FLAG_CLICKS_BY_PRESS)
        return True
    def CreateDec(self):
        x1 = 1
        y1 = 1
        x2 = x1 + 16
        y2 = y1 + 16
        if not self.m_dec.Create(self.m_chart_id, self.m_name + 'Dec', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_dec.BmpNames('::res\\Up.bmp'):
            return False
        if not self.Add_1(self.m_dec):
            return False
        self.m_dec.PropFlags_1(WND_PROP_FLAG_CLICKS_BY_PRESS)
        return True
    def CreateThumb(self):
        x1 = 1
        y1 = 18 - 1
        x2 = x1 + 16
        y2 = y1 + 22
        if not self.m_thumb.Create(self.m_chart_id, self.m_name + 'Thumb', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_thumb.BmpNames('::res\\ThumbVert.bmp'):
            return False
        if not self.Add_1(self.m_thumb):
            return False
        self.m_thumb.PropFlags_1(WND_PROP_FLAG_CAN_DRAG)
        return True
    def OnResize(self):
        if self.Width_0() != 18:
            self.m_rect.Width_1(18)
        if not self.m_back.Size_1(self.Size_0()):
            return False
        if not self.m_inc.Move_2(self.m_inc.Left_0(), self.Bottom_0() - 18):
            return False
        return self.OnChangePos()
    def OnChangePos(self):
        if (self.m_max_pos - self.m_min_pos) <= 0:
            return self.Visible(False)
        elif not self.Visible(True):
            return False
        steps = self.m_max_pos - self.m_min_pos
        min_coord = self.m_dec.Bottom_0()
        max_coord = self.m_inc.Top_0() - self.m_thumb.Height_0()
        new_coord = min_coord + _idiv((max_coord - min_coord) * self.m_curr_pos, steps)
        return self.m_thumb.Move_2(self.m_thumb.Left_0(), new_coord)
    def OnThumbDragStart(self):
        if self.m_drag_object is None:
            self.m_drag_object = CDragWnd()
            if self.m_drag_object is None:
                return False
        x1 = self.m_thumb.Left_0() - 50
        y1 = self.m_thumb.Top_0() - 50
        x2 = self.m_thumb.Right_0() + 50
        y2 = self.m_thumb.Bottom_0() + 50
        self.m_drag_object.Create(self.m_chart_id, '', self.m_subwin, x1, y1, x2, y2)
        self.m_drag_object.PropFlags_1(WND_PROP_FLAG_CAN_DRAG)
        self.m_drag_object.Limits(x1, self.m_dec.Bottom_0() - 50, x2, self.m_inc.Top_0() + 50)
        self.m_drag_object.MouseX_1(self.m_thumb.MouseX_0())
        self.m_drag_object.MouseY_1(self.m_thumb.MouseY_0())
        self.m_drag_object.MouseFlags_1(self.m_thumb.MouseFlags_0())
        return True
    def OnThumbDragProcess(self):
        if self.m_drag_object is None:
            return False
        x = self.m_drag_object.Left_0() + 50
        y = self.m_drag_object.Top_0() + 50
        new_pos = self.CalcPos(y)
        if new_pos != self.m_curr_pos:
            event_id = (7 if (self.m_curr_pos < new_pos) else 8)
            self.m_curr_pos = new_pos
            EventChartCustom(-1, event_id, self.m_id, 0.0, self.m_name)
        self.m_thumb.Move_2(x, y)
        return True
    def OnThumbDragEnd(self):
        if self.m_drag_object is not None:
            self.m_thumb.MouseFlags_1(self.m_drag_object.MouseFlags_0())
            _delete(self.m_drag_object)
            self.m_drag_object = None
        return self.m_thumb.Pressed_1(False)
    def CalcPos(self, coord):
        steps = self.m_max_pos - self.m_min_pos
        min_coord = self.m_dec.Bottom_0()
        max_coord = self.m_inc.Top_0() - self.m_thumb.Height_0()
        if max_coord == min_coord:
            return 0
        if coord < min_coord or coord > max_coord:
            return self.m_curr_pos
        new_pos = _int(MathRound(_fdiv(float(coord - min_coord), max_coord - min_coord) * steps))
        return new_pos

class CScrollH(CScroll):
    _q_fields = ()
    def __init__(self):
        CScroll.__init__(self)
    def _q_dtor(self):
        pass
    def CreateInc(self):
        x1 = self.Width_0() - 18 + 1
        y1 = 1
        x2 = x1 + 16
        y2 = y1 + 16
        if not self.m_inc.Create(self.m_chart_id, self.m_name + 'Inc', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_inc.BmpNames('::res\\Right.bmp'):
            return False
        if not self.Add_1(self.m_inc):
            return False
        self.m_inc.PropFlags_1(WND_PROP_FLAG_CLICKS_BY_PRESS)
        return True
    def CreateDec(self):
        x1 = 1
        y1 = 1
        x2 = x1 + 16
        y2 = y1 + 16
        if not self.m_dec.Create(self.m_chart_id, self.m_name + 'Dec', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_dec.BmpNames('::res\\Left.bmp'):
            return False
        if not self.Add_1(self.m_dec):
            return False
        self.m_dec.PropFlags_1(WND_PROP_FLAG_CLICKS_BY_PRESS)
        return True
    def CreateThumb(self):
        x1 = 18 - 1
        y1 = 1
        x2 = x1 + 22
        y2 = y1 + 16
        if not self.m_thumb.Create(self.m_chart_id, self.m_name + 'Thumb', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_thumb.BmpNames('::res\\ThumbHor.bmp'):
            return False
        if not self.Add_1(self.m_thumb):
            return False
        self.m_thumb.PropFlags_1(WND_PROP_FLAG_CAN_DRAG)
        return True
    def OnResize(self):
        if self.Height_0() != 18:
            self.m_rect.Height_1(18)
        if not self.m_back.Size_1(self.Size_0()):
            return False
        if not self.m_inc.Move_2(self.Right_0() - 18, self.m_inc.Top_0()):
            return False
        return self.OnChangePos()
    def OnChangePos(self):
        if (self.m_max_pos - self.m_min_pos) <= 0:
            return self.Visible(False)
        elif not self.Visible(True):
            return False
        steps = self.m_max_pos - self.m_min_pos
        min_coord = self.m_dec.Right_0()
        max_coord = self.m_inc.Left_0() - self.m_thumb.Width_0()
        new_coord = min_coord + _idiv((max_coord - min_coord) * self.m_curr_pos, steps)
        return self.m_thumb.Move_2(new_coord, self.m_thumb.Top_0())
    def OnThumbDragStart(self):
        if self.m_drag_object is None:
            self.m_drag_object = CDragWnd()
            if self.m_drag_object is None:
                return False
        x1 = self.m_thumb.Left_0() - 50
        y1 = self.m_thumb.Top_0() - 50
        x2 = self.m_thumb.Right_0() + 50
        y2 = self.m_thumb.Bottom_0() + 50
        self.m_drag_object.Create(self.m_chart_id, '', self.m_subwin, x1, y1, x2, y2)
        self.m_drag_object.PropFlags_1(WND_PROP_FLAG_CAN_DRAG)
        self.m_drag_object.Limits(self.m_dec.Right_0() - 50, y1, self.m_inc.Left_0() + 50, y2)
        self.m_drag_object.MouseX_1(self.m_thumb.MouseX_0())
        self.m_drag_object.MouseY_1(self.m_thumb.MouseY_0())
        self.m_drag_object.MouseFlags_1(self.m_thumb.MouseFlags_0())
        return True
    def OnThumbDragProcess(self):
        if self.m_drag_object is None:
            return False
        x = self.m_drag_object.Left_0() + 50
        y = self.m_drag_object.Top_0() + 50
        new_pos = self.CalcPos(x)
        if new_pos != self.m_curr_pos:
            event_id = (7 if (self.m_curr_pos < new_pos) else 8)
            self.m_curr_pos = new_pos
            EventChartCustom(-1, event_id, self.m_id, 0.0, self.m_name)
        self.m_thumb.Move_2(x, y)
        return True
    def OnThumbDragEnd(self):
        if self.m_drag_object is not None:
            self.m_thumb.MouseFlags_1(self.m_drag_object.MouseFlags_0())
            _delete(self.m_drag_object)
            self.m_drag_object = None
        return self.m_thumb.Pressed_1(False)
    def CalcPos(self, coord):
        steps = self.m_max_pos - self.m_min_pos
        min_coord = self.m_dec.Right_0()
        max_coord = self.m_inc.Left_0() - self.m_thumb.Width_0()
        if max_coord == min_coord:
            return 0
        if coord < min_coord or coord > max_coord:
            return self.m_curr_pos
        new_pos = _int(MathRound(_fdiv(float(coord - min_coord), max_coord - min_coord) * steps))
        return new_pos

class CWndClient(CWndContainer):
    _q_fields = ('m_v_scrolled', 'm_h_scrolled', 'm_background', 'm_scroll_v', 'm_scroll_h')
    def __init__(self):
        CWndContainer.__init__(self)
        self.m_v_scrolled = False
        self.m_h_scrolled = False
        self.m_background = CPanel()
        self.m_scroll_v = CScrollV()
        self.m_scroll_h = CScrollH()
        self.m_v_scrolled = False
        self.m_h_scrolled = False
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.CreateBack():
            return False
        if self.m_v_scrolled and (not self.CreateScrollV()):
            return False
        if self.m_h_scrolled and (not self.CreateScrollH()):
            return False
        return True
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ == (2 + CHARTEVENT_CUSTOM) and sparam == self.m_scroll_v.Name():
            self.OnVScrollShow()
            return True
        if id_ == (3 + CHARTEVENT_CUSTOM) and sparam == self.m_scroll_v.Name():
            self.OnVScrollHide()
            return True
        if id_ == (8 + CHARTEVENT_CUSTOM) and lparam == self.m_scroll_v.Id_0():
            self.OnScrollLineUp()
            return True
        if id_ == (7 + CHARTEVENT_CUSTOM) and lparam == self.m_scroll_v.Id_0():
            self.OnScrollLineDown()
            return True
        if id_ == (2 + CHARTEVENT_CUSTOM) and sparam == self.m_scroll_h.Name():
            self.OnHScrollShow()
            return True
        if id_ == (3 + CHARTEVENT_CUSTOM) and sparam == self.m_scroll_h.Name():
            self.OnHScrollHide()
            return True
        if id_ == (8 + CHARTEVENT_CUSTOM) and lparam == self.m_scroll_h.Id_0():
            self.OnScrollLineLeft()
            return True
        if id_ == (7 + CHARTEVENT_CUSTOM) and lparam == self.m_scroll_h.Id_0():
            self.OnScrollLineRight()
            return True
        return CWndContainer.OnEvent(self, id_, lparam, dparam, sparam)
    def ColorBackground(self, value):
        return self.m_background.ColorBackground_1(value)
    def ColorBorder(self, value):
        return self.m_background.ColorBorder_1(value)
    def BorderType(self, flag):
        return self.m_background.BorderType_1(flag)
    def VScrolled_0(self):
        return self.m_v_scrolled
    def VScrolled_1(self, flag):
        if self.m_v_scrolled == flag:
            return True
        d_size = 0
        if flag:
            if not self.CreateScrollV():
                return False
            d_size = -18
        else:
            self.m_scroll_v.Destroy()
            if not self.Delete_1(self.m_scroll_v):
                return False
            d_size = 18
        self.m_v_scrolled = flag
        if self.m_h_scrolled:
            if not self.m_scroll_h.Width_1(self.m_scroll_h.Width_0() + d_size):
                return False
        return True
    def HScrolled_0(self):
        return self.m_h_scrolled
    def HScrolled_1(self, flag):
        if self.m_h_scrolled == flag:
            return True
        d_size = 0
        if flag:
            if not self.CreateScrollH():
                return False
            d_size = -18
        else:
            self.m_scroll_h.Destroy()
            if not self.Delete_1(self.m_scroll_h):
                return False
            d_size = 18
        self.m_h_scrolled = flag
        if self.m_v_scrolled:
            if not self.m_scroll_v.Height_1(self.m_scroll_v.Height_0() + d_size):
                return False
        return True
    def Id_1(self, id_):
        id_used = CWndContainer.Id_1(self, id_)
        if not self.m_v_scrolled:
            id_used += self.m_scroll_v.Id_1(id_ + id_used)
        if not self.m_h_scrolled:
            id_used += self.m_scroll_h.Id_1(id_ + id_used)
        return id_used
    def Id_0(self):
        return CWnd.Id_0(self)
    def Show(self):
        CWndContainer.Show(self)
        if not self.m_v_scrolled:
            self.m_scroll_v.Hide()
        if not self.m_h_scrolled:
            self.m_scroll_h.Hide()
        return True
    def CreateBack(self):
        if not self.m_background.Create(self.m_chart_id, self.m_name + 'Back', self.m_subwin, 0, 0, self.Width_0(), self.Height_0()):
            return False
        if not self.m_background.ColorBorder_1(0x2C2C2C):
            return False
        if not self.m_background.ColorBackground_1(0xDEDEDE):
            return False
        if not self.Add_1(self.m_background):
            return False
        return True
    def CreateScrollV(self):
        x1 = self.Width_0() - 18 - 1
        y1 = 1
        x2 = self.Width_0() - 1
        y2 = self.Height_0() - 1
        if self.m_h_scrolled:
            y2 -= 18
        if not self.m_scroll_v.Create(self.m_chart_id, self.m_name + 'VScroll', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.Add_1(self.m_scroll_v):
            return False
        return True
    def CreateScrollH(self):
        x1 = 1
        y1 = self.Height_0() - 18 - 1
        x2 = self.Width_0() - 1
        y2 = self.Height_0() - 1
        if self.m_v_scrolled:
            x2 -= 18
        if not self.m_scroll_h.Create(self.m_chart_id, self.m_name + 'HScroll', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.Add_1(self.m_scroll_h):
            return False
        return True
    def OnResize(self):
        if not CWndContainer.OnResize(self):
            return False
        d_size = 0
        self.m_background.Width_1(self.Width_0())
        self.m_background.Height_1(self.Height_0())
        if self.m_v_scrolled:
            self.m_scroll_v.Move_2(self.Right_0() - 18, self.Top_0())
            d_size = (18 if self.m_h_scrolled else 0)
            self.m_scroll_v.Height_1(self.Height_0() - d_size)
        if self.m_h_scrolled:
            self.m_scroll_h.Move_2(self.Left_0(), self.Bottom_0() - 18)
            d_size = (18 if self.m_v_scrolled else 0)
            self.m_scroll_h.Width_1(self.Width_0() - d_size)
        return True
    def OnVScrollShow(self):
        return True
    def OnVScrollHide(self):
        return True
    def OnHScrollShow(self):
        return True
    def OnHScrollHide(self):
        return True
    def OnScrollLineDown(self):
        return True
    def OnScrollLineUp(self):
        return True
    def OnScrollLineLeft(self):
        return True
    def OnScrollLineRight(self):
        return True
    def Rebound(self, rect):
        self.m_rect.SetBound_1(rect)
        return self.OnResize()

class CEdit(CWndObj):
    _q_fields = ('m_edit', 'm_read_only', 'm_align_mode')
    def __init__(self):
        CWndObj.__init__(self)
        self.m_edit = CChartObjectEdit()
        self.m_read_only = False
        self.m_align_mode = 0
        self.m_read_only = False
        self.m_align_mode = ALIGN_LEFT
        self.m_color = 0x28293B
        self.m_color_background = clrWhite
        self.m_color_border = 0xCFC3B2
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.m_edit.Create(chart, name, subwin, x1, y1, self.Width_0(), self.Height_0()):
            return False
        return self.OnChange()
    def OnEvent(self, id_, lparam, dparam, sparam):
        if self.m_name == sparam and id_ == CHARTEVENT_OBJECT_ENDEDIT:
            return self.OnObjectEndEdit()
        return CWndObj.OnEvent(self, id_, lparam, dparam, sparam)
    def ReadOnly_0(self):
        return self.m_read_only
    def ReadOnly_1(self, flag):
        self.m_read_only = flag
        return self.m_edit.ReadOnly_1(flag)
    def TextAlign_0(self):
        return self.m_align_mode
    def TextAlign_1(self, align):
        self.m_align_mode = align
        return self.m_edit.TextAlign_1(align)
    def Text_0(self):
        return self.m_edit.Description_0()
    def Text_1(self, value):
        return CWndObj.Text_1(self, value)
    def OnObjectEndEdit(self):
        EventChartCustom(-1, 6, self.m_id, 0.0, self.m_name)
        return True
    def OnSetText(self):
        return self.m_edit.Description_1(self.m_text)
    def OnSetColor(self):
        return self.m_edit.Color_1(self.m_color)
    def OnSetColorBackground(self):
        return self.m_edit.BackColor_1(self.m_color_background)
    def OnSetColorBorder(self):
        return self.m_edit.BorderColor_1(self.m_color_border)
    def OnSetFont(self):
        return self.m_edit.Font_1(self.m_font)
    def OnSetFontSize(self):
        return self.m_edit.FontSize_1(self.m_font_size)
    def OnSetZOrder(self):
        return self.m_edit.Z_Order_1(self.m_zorder)
    def OnCreate(self):
        return self.m_edit.Create(self.m_chart_id, self.m_name, self.m_subwin, self.m_rect.left, self.m_rect.top, self.m_rect.Width_0(), self.m_rect.Height_0())
    def OnShow(self):
        return self.m_edit.Timeframes_1(_int(OBJ_ALL_PERIODS))
    def OnHide(self):
        return self.m_edit.Timeframes_1(_int(OBJ_NO_PERIODS))
    def OnMove(self):
        return self.m_edit.X_Distance_1(self.m_rect.left) and self.m_edit.Y_Distance_1(self.m_rect.top)
    def OnResize(self):
        return self.m_edit.X_Size_1(self.m_rect.Width_0()) and self.m_edit.Y_Size_1(self.m_rect.Height_0())
    def OnChange(self):
        return (CWndObj.OnChange(self) and self.ReadOnly_1(self.m_read_only)) and self.TextAlign_1(self.m_align_mode)
    def OnClick(self):
        if not self.m_read_only:
            EventChartCustom(-1, 5, self.m_id, 0.0, self.m_name)
            return True
        return CWnd.OnClick(self)

class CChart(CObject):
    _q_fields = ('m_chart_id',)
    def __init__(self):
        CObject.__init__(self)
        self.m_chart_id = 0
        self.m_chart_id = -1
    def _q_dtor(self):
        if self.m_chart_id != -1:
            self.Close()
    def ChartId(self):
        return self.m_chart_id
    def Type(self):
        return 0x1111
    def Mode_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ChartGetInteger(self.m_chart_id, CHART_MODE)
    def Mode_1(self, mode):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_MODE, mode)
    def Foreground_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_FOREGROUND))
    def Foreground_1(self, foreground):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_FOREGROUND, foreground)
    def Shift_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHIFT))
    def Shift_1(self, shift):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHIFT, shift)
    def ShiftSize_0(self):
        if self.m_chart_id == -1:
            return DBL_MAX
        return ChartGetDouble(self.m_chart_id, CHART_SHIFT_SIZE)
    def ShiftSize_1(self, shift):
        if self.m_chart_id == -1:
            return False
        if shift < 10:
            shift = 10.0
        if shift > 50:
            shift = 50.0
        return ChartSetDouble(self.m_chart_id, CHART_SHIFT_SIZE, shift)
    def AutoScroll_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_AUTOSCROLL))
    def AutoScroll_1(self, auto_scroll):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_AUTOSCROLL, auto_scroll)
    def Scale_0(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_SCALE))
    def Scale_1(self, shift):
        if self.m_chart_id == -1:
            return False
        if shift < 0:
            shift = 0
        if shift > 32:
            shift = 32
        return ChartSetInteger(self.m_chart_id, CHART_SCALE, shift)
    def ScaleFix_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SCALEFIX))
    def ScaleFix_1(self, scale_fix):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SCALEFIX, scale_fix)
    def ScaleFix_11_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SCALEFIX_11))
    def ScaleFix_11_1(self, scale_fix_11):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SCALEFIX_11, scale_fix_11)
    def FixedMax_0(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_FIXED_MAX)
    def FixedMax_1(self, fixed_max):
        if self.m_chart_id == -1:
            return False
        return ChartSetDouble(self.m_chart_id, CHART_FIXED_MAX, fixed_max)
    def FixedMin_0(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_FIXED_MIN)
    def FixedMin_1(self, fixed_min):
        if self.m_chart_id == -1:
            return False
        return ChartSetDouble(self.m_chart_id, CHART_FIXED_MIN, fixed_min)
    def ScalePPB_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SCALE_PT_PER_BAR))
    def ScalePPB_1(self, scale_ppb):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SCALE_PT_PER_BAR, scale_ppb)
    def PointsPerBar_0(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_POINTS_PER_BAR)
    def PointsPerBar_1(self, points_per_bar):
        if self.m_chart_id == -1:
            return False
        return ChartSetDouble(self.m_chart_id, CHART_POINTS_PER_BAR, points_per_bar)
    def ShowOHLC_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_OHLC))
    def ShowOHLC_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_OHLC, show)
    def ShowLineBid_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_BID_LINE))
    def ShowLineBid_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_BID_LINE, show)
    def ShowLineAsk_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_ASK_LINE))
    def ShowLineAsk_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_ASK_LINE, show)
    def ShowLastLine_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_LAST_LINE))
    def ShowLastLine_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_LAST_LINE, show)
    def ShowPeriodSep_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_PERIOD_SEP))
    def ShowPeriodSep_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_PERIOD_SEP, show)
    def ShowGrid_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_GRID))
    def ShowGrid_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_GRID, show)
    def ShowVolumes_0(self):
        if self.m_chart_id == -1:
            return WRONG_VALUE
        return ChartGetInteger(self.m_chart_id, CHART_SHOW_VOLUMES)
    def ShowVolumes_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_VOLUMES, show)
    def ShowObjectDescr_0(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_SHOW_OBJECT_DESCR))
    def ShowObjectDescr_1(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_OBJECT_DESCR, show)
    def ShowDateScale(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_DATE_SCALE, show)
    def ShowPriceScale(self, show):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_SHOW_PRICE_SCALE, show)
    def ColorBackground_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_BACKGROUND))
    def ColorBackground_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_BACKGROUND, new_color)
    def ColorForeground_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_FOREGROUND))
    def ColorForeground_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_FOREGROUND, new_color)
    def ColorGrid_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_GRID))
    def ColorGrid_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_GRID, new_color)
    def ColorBarUp_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CHART_UP))
    def ColorBarUp_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CHART_UP, new_color)
    def ColorBarDown_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CHART_DOWN))
    def ColorBarDown_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CHART_DOWN, new_color)
    def ColorCandleBull_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CANDLE_BULL))
    def ColorCandleBull_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CANDLE_BULL, new_color)
    def ColorCandleBear_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CANDLE_BEAR))
    def ColorCandleBear_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CANDLE_BEAR, new_color)
    def ColorChartLine_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_CHART_LINE))
    def ColorChartLine_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_CHART_LINE, new_color)
    def ColorVolumes_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_VOLUME))
    def ColorVolumes_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_VOLUME, new_color)
    def ColorLineBid_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_BID))
    def ColorLineBid_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_BID, new_color)
    def ColorLineAsk_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_ASK))
    def ColorLineAsk_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_ASK, new_color)
    def ColorLineLast_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_LAST))
    def ColorLineLast_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_LAST, new_color)
    def ColorStopLevels_0(self):
        if self.m_chart_id == -1:
            return clrNONE
        return _uint(ChartGetInteger(self.m_chart_id, CHART_COLOR_STOP_LEVEL))
    def ColorStopLevels_1(self, new_color):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_COLOR_STOP_LEVEL, new_color)
    def BringToTop(self):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_BRING_TO_TOP, True)
    def EventObjectCreate(self, flag=True):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_EVENT_OBJECT_CREATE, flag)
    def EventObjectDelete(self, flag=True):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_EVENT_OBJECT_DELETE, flag)
    def EventMouseMove(self, flag=True):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_EVENT_MOUSE_MOVE, flag)
    def MouseScroll(self, flag=True):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, CHART_MOUSE_SCROLL, flag)
    def VisibleBars(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WIDTH_IN_BARS))
    def WindowsTotal(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WINDOWS_TOTAL))
    def WindowIsVisible(self, num):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_WINDOW_IS_VISIBLE, num))
    def WindowHandle(self):
        if self.m_chart_id == -1:
            return INVALID_HANDLE
        return _int(ChartGetInteger(self.m_chart_id, CHART_WINDOW_HANDLE))
    def FirstVisibleBar(self):
        if self.m_chart_id == -1:
            return -1
        return _int(ChartGetInteger(self.m_chart_id, CHART_FIRST_VISIBLE_BAR))
    def WidthInBars(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WIDTH_IN_BARS))
    def WidthInPixels(self):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WIDTH_IN_PIXELS))
    def HeightInPixels(self, num):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_HEIGHT_IN_PIXELS, num))
    def SubwindowY(self, num):
        if self.m_chart_id == -1:
            return 0
        return _int(ChartGetInteger(self.m_chart_id, CHART_WINDOW_YDISTANCE, num))
    def PriceMin(self, num):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_PRICE_MIN, num)
    def PriceMax(self, num):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, CHART_PRICE_MAX, num)
    def IsObject(self):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetInteger(self.m_chart_id, CHART_IS_OBJECT))
    def Attach_0(self):
        self.m_chart_id = ChartID()
    def Attach_1(self, chart):
        self.m_chart_id = chart
    def FirstChart(self):
        self.m_chart_id = ChartFirst()
    def NextChart(self):
        self.m_chart_id = ChartNext(self.m_chart_id)
    def Open(self, symbol_name, timeframe):
        self.m_chart_id = ChartOpen(symbol_name, timeframe)
        if self.m_chart_id == 0:
            self.m_chart_id = -1
        return self.m_chart_id
    def Detach(self):
        self.m_chart_id = -1
    def Close(self):
        if self.m_chart_id != -1:
            ChartClose(self.m_chart_id)
            self.m_chart_id = -1
    def Navigate(self, position, shift=0):
        if self.m_chart_id == -1:
            return False
        return ChartNavigate(self.m_chart_id, position, shift)
    def Symbol(self):
        return ChartSymbol(self.m_chart_id)
    def Period(self):
        return ChartPeriod(self.m_chart_id)
    def Redraw(self):
        ChartRedraw(self.m_chart_id)
    def GetInteger_2(self, prop_id, subwindow=0):
        if self.m_chart_id == -1:
            return 0
        return ChartGetInteger(self.m_chart_id, prop_id, subwindow)
    def GetInteger_3(self, prop_id, subwindow, value):
        if self.m_chart_id == -1:
            return False
        return (ChartGetInteger(self.m_chart_id, prop_id, subwindow, value) != 0)
    def SetInteger(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ChartSetInteger(self.m_chart_id, prop_id, value)
    def GetDouble_2(self, prop_id, subwindow=0):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return ChartGetDouble(self.m_chart_id, prop_id, subwindow)
    def GetDouble_3(self, prop_id, subwindow, value):
        if self.m_chart_id == -1:
            return False
        return (ChartGetDouble(self.m_chart_id, prop_id, subwindow, value) != 0)
    def SetDouble(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ChartSetDouble(self.m_chart_id, prop_id, value)
    def GetString_1(self, prop_id):
        if self.m_chart_id == -1:
            return ''
        return ChartGetString(self.m_chart_id, prop_id)
    def GetString_2(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return _bool(ChartGetString(self.m_chart_id, prop_id, value))
    def SetString(self, prop_id, value):
        if self.m_chart_id == -1:
            return False
        return ChartSetString(self.m_chart_id, prop_id, value)
    def SetSymbolPeriod(self, symbol, period):
        if self.m_chart_id == -1:
            return False
        return ChartSetSymbolPeriod(self.m_chart_id, symbol, period)
    def ApplyTemplate(self, filename):
        if self.m_chart_id == -1:
            return False
        return ChartApplyTemplate(self.m_chart_id, filename)
    def ScreenShot(self, filename, width, height, align_mode=ALIGN_RIGHT):
        if self.m_chart_id == -1:
            return False
        return ChartScreenShot(self.m_chart_id, filename, width, height, align_mode)
    def WindowOnDropped(self):
        if self.m_chart_id == -1:
            return 0
        return _missing('ChartWindowOnDropped')()
    def PriceOnDropped(self):
        if self.m_chart_id == -1:
            return EMPTY_VALUE
        return _missing('ChartPriceOnDropped')()
    def TimeOnDropped(self):
        if self.m_chart_id == -1:
            return False
        return _long(_missing('ChartTimeOnDropped')())
    def XOnDropped(self):
        if self.m_chart_id == -1:
            return 0
        return _int(_missing('ChartXOnDropped')())
    def YOnDropped(self):
        if self.m_chart_id == -1:
            return 0
        return _int(_missing('ChartYOnDropped')())
    def IndicatorAdd(self, subwin, handle):
        if self.m_chart_id == -1:
            return False
        return ChartIndicatorAdd(self.m_chart_id, subwin, handle)
    def IndicatorDelete(self, subwin, name):
        if self.m_chart_id == -1:
            return False
        return ChartIndicatorDelete(self.m_chart_id, subwin, name)
    def IndicatorsTotal(self, subwin):
        if self.m_chart_id == -1:
            return 0
        return ChartIndicatorsTotal(self.m_chart_id, subwin)
    def IndicatorName(self, subwin, index):
        if self.m_chart_id == -1:
            return ''
        return ChartIndicatorName(self.m_chart_id, subwin, index)
    def Save(self, file_handle):
        work_str = ""
        work_int = 0
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if _missing('FileWriteLong')(file_handle, -1) != 8:
            return False
        if FileWriteInteger(file_handle, self.Type(), INT_VALUE) != INT_VALUE:
            return False
        work_str = self.Symbol()
        work_int = StringLen(work_str)
        if FileWriteInteger(file_handle, work_int, INT_VALUE) != INT_VALUE:
            return False
        if work_int != 0:
            if FileWriteString(file_handle, work_str, work_int) != work_int:
                return False
        if FileWriteInteger(file_handle, self.Period(), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_MODE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_FOREGROUND)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHIFT)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHIFT)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_AUTOSCROLL)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SCALE)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SCALEFIX)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SCALEFIX_11)), CHAR_VALUE) != 1:
            return False
        if FileWriteDouble(file_handle, ChartGetDouble(self.m_chart_id, CHART_FIXED_MAX)) != 8:
            return False
        if FileWriteDouble(file_handle, ChartGetDouble(self.m_chart_id, CHART_FIXED_MIN)) != 8:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SCALE_PT_PER_BAR)), CHAR_VALUE) != 1:
            return False
        if FileWriteDouble(file_handle, ChartGetDouble(self.m_chart_id, CHART_POINTS_PER_BAR)) != 8:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_OHLC)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_BID_LINE)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_ASK_LINE)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_LAST_LINE)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_PERIOD_SEP)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_GRID)), CHAR_VALUE) != 1:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_VOLUMES)), INT_VALUE) != 4:
            return False
        if FileWriteInteger(file_handle, _int(ChartGetInteger(self.m_chart_id, CHART_SHOW_OBJECT_DESCR)), CHAR_VALUE) != 1:
            return False
        return True
    def Load(self, file_handle):
        resutl = True
        work_str = ""
        work_int = 0
        if file_handle == INVALID_HANDLE or self.m_chart_id == -1:
            return False
        if _missing('FileReadLong')(file_handle) != -1:
            return False
        if FileReadInteger(file_handle, INT_VALUE) != self.Type():
            return False
        work_int = FileReadInteger(file_handle)
        if work_int != 0:
            work_str = FileReadString(file_handle, work_int)
        else:
            work_str = ''
        work_int = FileReadInteger(file_handle)
        self.SetSymbolPeriod(work_str, work_int)
        if not ChartSetInteger(self.m_chart_id, CHART_MODE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_FOREGROUND, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHIFT, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHIFT, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_AUTOSCROLL, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SCALE, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SCALEFIX, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SCALEFIX_11, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetDouble(self.m_chart_id, CHART_FIXED_MAX, FileReadDatetime(file_handle)):
            return False
        if not ChartSetDouble(self.m_chart_id, CHART_FIXED_MIN, FileReadDatetime(file_handle)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SCALE_PT_PER_BAR, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetDouble(self.m_chart_id, CHART_POINTS_PER_BAR, FileReadDatetime(file_handle)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_OHLC, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_BID_LINE, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_ASK_LINE, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_LAST_LINE, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_PERIOD_SEP, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_GRID, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_VOLUMES, FileReadInteger(file_handle, INT_VALUE)):
            return False
        if not ChartSetInteger(self.m_chart_id, CHART_SHOW_OBJECT_DESCR, FileReadInteger(file_handle, CHAR_VALUE)):
            return False
        return resutl

class CDialog(CWndContainer):
    _q_fields = ('m_white_border', 'm_background', 'm_caption', 'm_button_close', 'm_client_area', 'm_panel_flag', 'm_minimized', 'm_min_rect', 'm_norm_rect')
    def __init__(self):
        CWndContainer.__init__(self)
        self.m_white_border = CPanel()
        self.m_background = CPanel()
        self.m_caption = CEdit()
        self.m_button_close = CBmpButton()
        self.m_client_area = CWndClient()
        self.m_panel_flag = False
        self.m_minimized = False
        self.m_min_rect = CRect()
        self.m_norm_rect = CRect()
        self.m_panel_flag = False
        self.m_minimized = False
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if (not self.m_panel_flag) and (not self.CreateWhiteBorder()):
            return False
        if not self.CreateBackground():
            return False
        if not self.CreateCaption():
            return False
        if not self.CreateButtonClose():
            return False
        if not self.CreateClientArea():
            return False
        self.m_norm_rect.SetBound_1(self.m_rect)
        return True
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ == (0 + CHARTEVENT_CUSTOM) and lparam == self.m_button_close.Id_0():
            self.OnClickButtonClose()
            return True
        if id_ == (0 + CHARTEVENT_CUSTOM) and lparam == self.m_caption.Id_0():
            self.OnClickCaption()
            return True
        if id_ == (11 + CHARTEVENT_CUSTOM) and lparam == self.m_caption.Id_0():
            self.OnDialogDragStart()
            return True
        if (self.m_drag_object is not None and id_ == (12 + CHARTEVENT_CUSTOM)) and lparam == self.m_drag_object.Id_0():
            self.OnDialogDragProcess()
            return True
        if (self.m_drag_object is not None and id_ == (13 + CHARTEVENT_CUSTOM)) and lparam == self.m_drag_object.Id_0():
            self.OnDialogDragEnd()
            return True
        return CWndContainer.OnEvent(self, id_, lparam, dparam, sparam)
    def Caption_0(self):
        return self.m_caption.Text_0()
    def Caption_1(self, text):
        return self.m_caption.Text_1(text)
    def Add_1(self, control):
        return self.m_client_area.Add_1(control)
    def Add_2(self, control):
        return self.m_client_area.Add_2(control)
    def Save(self, file_handle):
        if file_handle == INVALID_HANDLE:
            return False
        _missing('FileWriteStruct')(file_handle, self.m_norm_rect)
        FileWriteInteger(file_handle, self.m_min_rect.left)
        FileWriteInteger(file_handle, self.m_min_rect.top)
        FileWriteInteger(file_handle, self.m_minimized)
        return CWndContainer.Save(self, file_handle)
    def Load(self, file_handle):
        if file_handle == INVALID_HANDLE:
            return False
        if not FileIsEnding(file_handle):
            _missing('FileReadStruct')(file_handle, self.m_norm_rect)
            left = FileReadInteger(file_handle)
            top = FileReadInteger(file_handle)
            self.m_min_rect.Move_2(left, top)
            self.m_minimized = (FileReadInteger(file_handle) != 0)
        return CWndContainer.Load(self, file_handle)
    def CreateWhiteBorder(self):
        x1 = 0
        y1 = 0
        x2 = self.Width_0()
        y2 = self.Height_0()
        if not self.m_white_border.Create(self.m_chart_id, self.m_name + 'Border', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_white_border.ColorBackground_1(0xF0F0F0):
            return False
        if not self.m_white_border.ColorBorder_1(clrWhite):
            return False
        if not CWndContainer.Add_1(self, self.m_white_border):
            return False
        self.m_white_border.Alignment(WND_ALIGN_CLIENT, 0, 0, 0, 0)
        return True
    def CreateBackground(self):
        off = (0 if self.m_panel_flag else 1)
        x1 = off
        y1 = off
        x2 = self.Width_0() - off
        y2 = self.Height_0() - off
        if not self.m_background.Create(self.m_chart_id, self.m_name + 'Back', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_background.ColorBackground_1(0xF0F0F0):
            return False
        border = (0xF0F0F0 if self.m_panel_flag else 0xB6B6B6)
        if not self.m_background.ColorBorder_1(border):
            return False
        if not CWndContainer.Add_1(self, self.m_background):
            return False
        self.m_background.Alignment(WND_ALIGN_CLIENT, off, off, off, off)
        return True
    def CreateCaption(self):
        off = (0 if self.m_panel_flag else (2 * 1))
        x1 = off
        y1 = off
        x2 = self.Width_0() - off
        y2 = y1 + 22
        if not self.m_caption.Create(self.m_chart_id, self.m_name + 'Caption', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_caption.Color_1(0x3B2928):
            return False
        if not self.m_caption.ColorBackground_1(0xF0F0F0):
            return False
        if not self.m_caption.ColorBorder_1(0xF0F0F0):
            return False
        if not self.m_caption.ReadOnly_1(True):
            return False
        if not self.m_caption.Text_1(self.m_name):
            return False
        if not CWndContainer.Add_1(self, self.m_caption):
            return False
        self.m_caption.Alignment(WND_ALIGN_WIDTH, off, 0, off, 0)
        if not self.m_panel_flag:
            self.m_caption.PropFlags_1(WND_PROP_FLAG_CAN_DRAG)
        return True
    def CreateButtonClose(self):
        off = (0 if self.m_panel_flag else (2 * 1))
        x1 = self.Width_0() - off - (16 + 3)
        y1 = off + 3
        x2 = x1 + 16
        y2 = y1 + 16
        if not self.m_button_close.Create(self.m_chart_id, self.m_name + 'Close', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_button_close.BmpNames('::res\\Close.bmp'):
            return False
        if not CWndContainer.Add_1(self, self.m_button_close):
            return False
        self.m_button_close.Alignment(WND_ALIGN_RIGHT, 0, 0, off + 3, 0)
        self.CaptionAlignment(WND_ALIGN_WIDTH, off, 0, off + (16 + 3), 0)
        return True
    def CreateClientArea(self):
        off = (0 if self.m_panel_flag else (2 * 1))
        x1 = off + 2
        y1 = off + 22
        x2 = self.Width_0() - (off + 2)
        y2 = self.Height_0() - (off + 2)
        if not self.m_client_area.Create(self.m_chart_id, self.m_name + 'Client', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_client_area.ColorBackground(0xF7F7F7):
            return False
        if not self.m_client_area.ColorBorder(0xC8C8C8):
            return False
        CWndContainer.Add_1(self, self.m_client_area)
        self.m_client_area.Alignment(WND_ALIGN_CLIENT, x1, y1, x1, x1)
        return True
    def OnClickCaption(self):
        pass
    def OnClickButtonClose(self):
        self.Visible(False)
    def CaptionAlignment(self, flags, left, top, right, bottom):
        self.m_caption.Alignment(flags, left, top, right, bottom)
    def ClientAreaVisible(self, visible):
        return self.m_client_area.Visible(visible)
    def ClientAreaLeft(self):
        return self.m_client_area.Left_0()
    def ClientAreaTop(self):
        return self.m_client_area.Top_0()
    def ClientAreaRight(self):
        return self.m_client_area.Right_0()
    def ClientAreaBottom(self):
        return self.m_client_area.Bottom_0()
    def ClientAreaWidth(self):
        return self.m_client_area.Width_0()
    def ClientAreaHeight(self):
        return self.m_client_area.Height_0()
    def OnDialogDragStart(self):
        if self.m_drag_object is None:
            self.m_drag_object = CDragWnd()
            if self.m_drag_object is None:
                return False
        x1 = self.Left_0() - 50
        y1 = self.Top_0() - 50
        x2 = self.Right_0() + 50
        y2 = self.Bottom_0() + 50
        self.m_drag_object.Create(self.m_chart_id, '', self.m_subwin, x1, y1, x2, y2)
        self.m_drag_object.PropFlags_1(WND_PROP_FLAG_CAN_DRAG)
        chart = CChart()
        chart.Attach_1(self.m_chart_id)
        self.m_drag_object.Limits(-50, -50, chart.WidthInPixels() + 50, chart.HeightInPixels(self.m_subwin) + 50)
        chart.Detach()
        self.m_drag_object.MouseX_1(self.m_caption.MouseX_0())
        self.m_drag_object.MouseY_1(self.m_caption.MouseY_0())
        self.m_drag_object.MouseFlags_1(self.m_caption.MouseFlags_0())
        return True
    def OnDialogDragProcess(self):
        if self.m_drag_object is None:
            return False
        x = self.m_drag_object.Left_0() + 50
        y = self.m_drag_object.Top_0() + 50
        self.Move_2(x, y)
        return True
    def OnDialogDragEnd(self):
        if self.m_drag_object is not None:
            self.m_caption.MouseFlags_1(self.m_drag_object.MouseFlags_0())
            _delete(self.m_drag_object)
            self.m_drag_object = None
        if self.m_minimized:
            self.m_min_rect.SetBound_1(self.m_rect)
        else:
            self.m_norm_rect.SetBound_1(self.m_rect)
        return True

class CAppDialog(CDialog):
    _q_fields = ('m_button_minmax', 'm_program_name', 'm_instance_id', 'm_program_type', 'm_indicator_name', 'm_deinit_reason', 'm_subwin_Yoff', 'm_focused_wnd', 'm_top_wnd', 'm_chart')
    _q_ptrs = ('m_focused_wnd', 'm_top_wnd',)
    def __init__(self):
        CDialog.__init__(self)
        self.m_button_minmax = CBmpButton()
        self.m_program_name = ""
        self.m_instance_id = ""
        self.m_program_type = 0
        self.m_indicator_name = ""
        self.m_deinit_reason = 0
        self.m_subwin_Yoff = 0
        self.m_focused_wnd = None
        self.m_top_wnd = None
        self.m_chart = CChart()
        self.m_program_type = WRONG_VALUE
        self.m_deinit_reason = WRONG_VALUE
        self.m_subwin_Yoff = 0
        self.m_focused_wnd = None
        self.m_top_wnd = None
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not self.CreateCommon(chart, name, subwin):
            return False
        _sw1 = self.m_program_type
        if _sw1 == PROGRAM_EXPERT:
            if not self.CreateExpert(x1, y1, x2, y2):
                return False
        elif _sw1 == PROGRAM_INDICATOR:
            if not self.CreateIndicator(x1, y1, x2, y2):
                return False
        else:
            Print('CAppDialog: invalid program type')
            return False
        if not self.Caption_1(self.m_program_name):
            return False
        if not self.CreateButtonMinMax():
            return False
        self.SubwinOff()
        if self.m_minimized:
            self.Minimize()
        else:
            self.Maximize()
        return True
    def Destroy(self, reason=REASON_PROGRAM):
        if self.m_deinit_reason != WRONG_VALUE:
            return
        self.m_deinit_reason = reason
        self.IniFileSave()
        self.m_chart.Detach()
        CWndContainer.Destroy(self)
        if reason == REASON_PROGRAM:
            if self.m_program_type == PROGRAM_EXPERT:
                ExpertRemove()
            if self.m_program_type == PROGRAM_INDICATOR:
                ChartIndicatorDelete(self.m_chart_id, self.m_subwin, self.m_indicator_name)
        EventChartCustom(-1, 100, self.m_subwin, 0.0, self.m_program_name)
    def OnEvent(self, id_, lparam, dparam, sparam):
        if id_ == (0 + CHARTEVENT_CUSTOM) and lparam == self.m_button_minmax.Id_0():
            self.OnClickButtonMinMax()
            return True
        if id_ == (100 + CHARTEVENT_CUSTOM):
            self.OnAnotherApplicationClose(lparam, dparam, sparam)
            return True
        return CDialog.OnEvent(self, id_, lparam, dparam, sparam)
    def Run(self):
        self.m_chart.Redraw()
        if self.Id_1(self.m_subwin * 10000) > 10000:
            Print('CAppDialog: too many objects')
            return False
        return True
    def ChartEvent(self, id_, lparam, dparam, sparam):
        mouse_x = _int(lparam)
        mouse_y = _int(dparam) - self.m_subwin_Yoff
        _sw2 = id_
        if _sw2 == CHARTEVENT_CHART_CHANGE:
            pass
        elif _sw2 == CHARTEVENT_OBJECT_CLICK:
            return
        elif _sw2 == CHARTEVENT_CUSTOM + 9:
            if CheckPointer(self.m_focused_wnd) != POINTER_INVALID:
                if not self.m_focused_wnd.MouseFocusKill(lparam):
                    return
            self.m_focused_wnd = self.ControlFind(lparam)
            return
        elif _sw2 == CHARTEVENT_CUSTOM + 14:
            self.m_top_wnd = self.ControlFind(lparam)
            return
        elif _sw2 == CHARTEVENT_MOUSE_MOVE:
            if CheckPointer(self.m_top_wnd) != POINTER_INVALID:
                if self.m_top_wnd.OnMouseEvent(mouse_x, mouse_y, _int(StringToInteger(sparam))):
                    self.m_chart.Redraw()
                    return
            if self.OnMouseEvent(mouse_x, mouse_y, _int(StringToInteger(sparam))):
                self.m_chart.Redraw()
            return
        else:
            if self.OnEvent(id_, lparam, dparam, sparam):
                self.m_chart.Redraw()
            return
        if id_ == CHARTEVENT_CHART_CHANGE:
            if self.m_subwin != 0 and self.m_subwin != ChartWindowFind():
                fiction = 1
                self.OnAnotherApplicationClose(fiction, dparam, sparam)
            if self.m_chart.HeightInPixels(self.m_subwin) < (self.Height_0() + 1):
                self.m_button_minmax.Pressed_1(True)
                self.Minimize()
                self.m_chart.Redraw()
            if self.m_chart.WidthInPixels() != self.Width_0() and self.m_subwin != 0:
                self.Width_1(self.m_chart.WidthInPixels())
                self.m_chart.Redraw()
            self.SubwinOff()
    def Minimized(self, flag):
        self.m_minimized = flag
    def IniFileSave(self):
        filename = self.IniFileName() + self.IniFileExt()
        handle = FileOpen(filename, (FILE_WRITE | FILE_BIN) | FILE_ANSI)
        if handle != INVALID_HANDLE:
            self.Save(handle)
            FileClose(handle)
    def IniFileLoad(self):
        filename = self.IniFileName() + self.IniFileExt()
        handle = FileOpen(filename, (FILE_READ | FILE_BIN) | FILE_ANSI)
        if handle != INVALID_HANDLE:
            self.Load(handle)
            FileClose(handle)
    def IniFileName(self):
        name = ""
        name = (self.m_indicator_name if (self.m_indicator_name != "") else self.m_program_name)
        name += '_' + Symbol()
        name += '_Ini'
        return name
    def IniFileExt(self):
        return '.dat'
    def Load(self, file_handle):
        if CDialog.Load(self, file_handle):
            if self.m_minimized:
                self.m_button_minmax.Pressed_1(True)
                self.Minimize()
            else:
                self.m_button_minmax.Pressed_1(False)
                self.Maximize()
            prev_deinit_reason = FileReadInteger(file_handle)
            if prev_deinit_reason == REASON_CHARTCLOSE or prev_deinit_reason == REASON_CLOSE:
                prev_instance_id = IntegerToString(FileReadInteger(file_handle), 5, 48)
                if prev_instance_id != self.m_instance_id:
                    chart_id = self.m_chart.ChartId()
                    total = ObjectsTotal(chart_id, self.m_subwin)
                    for i in range(total - 1, 0 - 1, -1):
                        obj_name = ObjectName(chart_id, i, self.m_subwin)
                        if StringFind(obj_name, prev_instance_id) == 0:
                            ObjectDelete(chart_id, obj_name)
            return True
        return False
    def Save(self, file_handle):
        if CDialog.Save(self, file_handle):
            FileWriteInteger(file_handle, self.m_deinit_reason)
            FileWriteInteger(file_handle, _int(StringToInteger(self.m_instance_id)))
            return True
        return False
    def CreateCommon(self, chart, name, subwin):
        self.m_chart_id = chart
        self.m_name = name
        self.m_subwin = subwin
        self.m_program_name = name
        self.m_deinit_reason = WRONG_VALUE
        self.m_instance_id = self.CreateInstanceId()
        self.m_chart.Attach_1(chart)
        self.m_program_type = MQLInfoInteger(MQL_PROGRAM_TYPE)
        if ((not self.m_chart.EventObjectCreate()) or (not self.m_chart.EventObjectDelete())) or (not self.m_chart.EventMouseMove()):
            Print('CAppDialog: object events specify error')
            self.m_chart.Detach()
            return False
        return True
    def CreateExpert(self, x1, y1, x2, y2):
        self.m_subwin = 0
        self.m_min_rect.SetBound_4(10, 10, 10 + 100, 10 + ((4 * 1) + 22))
        if not CDialog.Create(self, self.m_chart.ChartId(), self.m_instance_id, self.m_subwin, x1, y1, x2, y2):
            Print('CAppDialog: expert dialog create error')
            self.m_chart.Detach()
            return False
        return True
    def CreateIndicator(self, x1, y1, x2, y2):
        width = self.m_chart.WidthInPixels()
        self.m_min_rect.LeftTop_2(0, 0)
        self.m_min_rect.Width_1(width)
        self.m_min_rect.Height_1((4 * 1) + 22 - (2 * 1))
        self.m_subwin = ChartWindowFind()
        if self.m_subwin == -1:
            Print('CAppDialog: find subwindow error')
            self.m_chart.Detach()
            return False
        total = ChartIndicatorsTotal(self.m_chart.ChartId(), self.m_subwin)
        self.m_indicator_name = ChartIndicatorName(self.m_chart.ChartId(), self.m_subwin, total - 1)
        if self.m_subwin == 0:
            return self.CreateExpert(x1, y1, x2, y2)
        if total != 1:
            Print('CAppDialog: subwindow busy')
            ChartIndicatorDelete(self.m_chart.ChartId(), self.m_subwin, ChartIndicatorName(self.m_chart.ChartId(), self.m_subwin, total - 1))
            self.m_chart.Detach()
            return False
        if not IndicatorSetInteger(INDICATOR_HEIGHT, y2 - y1 + 1):
            Print('CAppDialog: subwindow resize error')
            ChartIndicatorDelete(self.m_chart.ChartId(), self.m_subwin, ChartIndicatorName(self.m_chart.ChartId(), self.m_subwin, total - 1))
            self.m_chart.Detach()
            return False
        self.m_indicator_name = self.m_program_name + IntegerToString(self.m_subwin)
        if not IndicatorSetString(INDICATOR_SHORTNAME, self.m_indicator_name):
            Print('CAppDialog: shortname error')
            ChartIndicatorDelete(self.m_chart.ChartId(), self.m_subwin, ChartIndicatorName(self.m_chart.ChartId(), self.m_subwin, total - 1))
            self.m_chart.Detach()
            return False
        self.m_panel_flag = True
        if not CDialog.Create(self, self.m_chart.ChartId(), self.m_instance_id, self.m_subwin, 0, 0, width, y2 - y1):
            Print('CAppDialog: indicator dialog create error')
            ChartIndicatorDelete(self.m_chart.ChartId(), self.m_subwin, ChartIndicatorName(self.m_chart.ChartId(), self.m_subwin, total - 1))
            self.m_chart.Detach()
            return False
        return True
    def CreateButtonMinMax(self):
        off = (0 if self.m_panel_flag else (2 * 1))
        x1 = self.Width_0() - off - (2 * (16 + 3))
        y1 = off + 3
        x2 = x1 + 16
        y2 = y1 + 16
        if not self.m_button_minmax.Create(self.m_chart_id, self.m_name + 'MinMax', self.m_subwin, x1, y1, x2, y2):
            return False
        if not self.m_button_minmax.BmpNames('::res\\Turn.bmp', '::res\\Restore.bmp'):
            return False
        if not CWndContainer.Add_1(self, self.m_button_minmax):
            return False
        self.m_button_minmax.Locking_1(True)
        self.m_button_minmax.Alignment(WND_ALIGN_RIGHT, 0, 0, off + 16 + (2 * 3), 0)
        self.CaptionAlignment(WND_ALIGN_WIDTH, off, 0, off + (2 * (16 + 3)), 0)
        return True
    def OnClickButtonClose(self):
        self.Destroy()
    def OnClickButtonMinMax(self):
        if self.m_button_minmax.Pressed_0():
            self.Minimize()
        else:
            self.Maximize()
        self.SubwinOff()
    def OnAnotherApplicationClose(self, lparam, dparam, sparam):
        if self.m_subwin == 0:
            return
        if lparam == 0:
            return
        self.SubwinOff()
        if lparam >= self.m_subwin:
            return
        self.m_subwin = ChartWindowFind()
        self.m_indicator_name = self.m_program_name + IntegerToString(self.m_subwin)
        IndicatorSetString(INDICATOR_SHORTNAME, self.m_indicator_name)
        self.Caption_1(self.m_program_name)
        self.Run()
    def Rebound(self, rect):
        if not self.Move_1(rect.LeftTop_0()):
            return False
        if not self.Size_1(rect.Size_0()):
            return False
        if self.m_program_type == PROGRAM_INDICATOR and (not IndicatorSetInteger(INDICATOR_HEIGHT, rect.Height_0() + 1)):
            Print('CAppDialog: subwindow resize error')
            return False
        return True
    def Minimize(self):
        self.m_minimized = True
        self.Rebound(self.m_min_rect)
        self.ClientAreaVisible(False)
    def Maximize(self):
        self.m_minimized = False
        self.Rebound(self.m_norm_rect)
        self.ClientAreaVisible(True)
    def CreateInstanceId(self):
        return IntegerToString(rand(), 5, 48)
    def ProgramName(self):
        return self.m_program_name
    def SubwinOff(self):
        self.m_subwin_Yoff = self.m_chart.SubwindowY(self.m_subwin)

class CButton(CWndObj):
    _q_fields = ('m_button',)
    def __init__(self):
        CWndObj.__init__(self)
        self.m_button = CChartObjectButton()
        self.m_color = 0x28293B
        self.m_color_background = 0xEBE2DD
        self.m_color_border = 0xCFC3B2
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.m_button.Create(chart, name, subwin, x1, y1, self.Width_0(), self.Height_0()):
            return False
        return self.OnChange()
    def Pressed_0(self):
        return self.m_button.State_0()
    def Pressed_1(self, pressed):
        return self.m_button.State_1(pressed)
    def Locking_0(self):
        return (self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0
    def Locking_1(self, flag):
        if flag:
            self.PropFlagsSet(WND_PROP_FLAG_CAN_LOCK)
        else:
            self.PropFlagsReset(WND_PROP_FLAG_CAN_LOCK)
    def OnSetText(self):
        return self.m_button.Description_1(self.m_text)
    def OnSetColor(self):
        return self.m_button.Color_1(self.m_color)
    def OnSetColorBackground(self):
        return self.m_button.BackColor_1(self.m_color_background)
    def OnSetColorBorder(self):
        return self.m_button.BorderColor_1(self.m_color_border)
    def OnSetFont(self):
        return self.m_button.Font_1(self.m_font)
    def OnSetFontSize(self):
        return self.m_button.FontSize_1(self.m_font_size)
    def OnCreate(self):
        return self.m_button.Create(self.m_chart_id, self.m_name, self.m_subwin, self.m_rect.left, self.m_rect.top, self.m_rect.Width_0(), self.m_rect.Height_0())
    def OnShow(self):
        return self.m_button.Timeframes_1(_int(OBJ_ALL_PERIODS))
    def OnHide(self):
        return self.m_button.Timeframes_1(_int(OBJ_NO_PERIODS))
    def OnMove(self):
        return self.m_button.X_Distance_1(self.m_rect.left) and self.m_button.Y_Distance_1(self.m_rect.top)
    def OnResize(self):
        return self.m_button.X_Size_1(self.m_rect.Width_0()) and self.m_button.Y_Size_1(self.m_rect.Height_0())
    def OnMouseDown(self):
        if not ((self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0):
            self.Pressed_1(not self.Pressed_0())
        return CWnd.OnMouseDown(self)
    def OnMouseUp(self):
        if self.m_button.State_0() and (not ((self.m_prop_flags & WND_PROP_FLAG_CAN_LOCK) != 0)):
            self.m_button.State_1(False)
        return CWnd.OnMouseUp(self)

class CLabel(CWndObj):
    _q_fields = ('m_label',)
    def __init__(self):
        CWndObj.__init__(self)
        self.m_label = CChartObjectLabel()
        self.m_color = 0x28293B
    def _q_dtor(self):
        pass
    def Create(self, chart, name, subwin, x1, y1, x2, y2):
        if not CWnd.Create(self, chart, name, subwin, x1, y1, x2, y2):
            return False
        if not self.m_label.Create(chart, name, subwin, x1, y1):
            return False
        return self.OnChange()
    def OnSetText(self):
        return self.m_label.Description_1(self.m_text)
    def OnSetColor(self):
        return self.m_label.Color_1(self.m_color)
    def OnSetFont(self):
        return self.m_label.Font_1(self.m_font)
    def OnSetFontSize(self):
        return self.m_label.FontSize_1(self.m_font_size)
    def OnCreate(self):
        return self.m_label.Create(self.m_chart_id, self.m_name, self.m_subwin, self.m_rect.left, self.m_rect.top)
    def OnShow(self):
        return self.m_label.Timeframes_1(_int(OBJ_ALL_PERIODS))
    def OnHide(self):
        return self.m_label.Timeframes_1(_int(OBJ_NO_PERIODS))
    def OnMove(self):
        return self.m_label.X_Distance_1(self.m_rect.left) and self.m_label.Y_Distance_1(self.m_rect.top)

class CDealInfo(CObject):
    _q_fields = ('m_ticket',)
    def __init__(self):
        CObject.__init__(self)
        self.m_ticket = 0
    def _q_dtor(self):
        pass
    def Ticket_1(self, ticket):
        self.m_ticket = ticket
    def Ticket_0(self):
        return self.m_ticket
    def Order(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_ORDER)
    def Time(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_TIME)
    def TimeMsc(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_TIME_MSC)
    def DealType(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_TYPE)
    def TypeDescription(self):
        str_ = ""
        _sw3 = self.DealType()
        if _sw3 == DEAL_TYPE_BUY:
            str_ = 'Buy type'
        elif _sw3 == DEAL_TYPE_SELL:
            str_ = 'Sell type'
        elif _sw3 == DEAL_TYPE_BALANCE:
            str_ = 'Balance type'
        elif _sw3 == DEAL_TYPE_CREDIT:
            str_ = 'Credit type'
        elif _sw3 == DEAL_TYPE_CHARGE:
            str_ = 'Charge type'
        elif _sw3 == DEAL_TYPE_CORRECTION:
            str_ = 'Correction type'
        elif _sw3 == DEAL_TYPE_BONUS:
            str_ = 'Bonus type'
        elif _sw3 == DEAL_TYPE_COMMISSION:
            str_ = 'Commission type'
        elif _sw3 == DEAL_TYPE_COMMISSION_DAILY:
            str_ = 'Daily Commission type'
        elif _sw3 == DEAL_TYPE_COMMISSION_MONTHLY:
            str_ = 'Monthly Commission type'
        elif _sw3 == DEAL_TYPE_COMMISSION_AGENT_DAILY:
            str_ = 'Daily Agent Commission type'
        elif _sw3 == DEAL_TYPE_COMMISSION_AGENT_MONTHLY:
            str_ = 'Monthly Agent Commission type'
        elif _sw3 == DEAL_TYPE_INTEREST:
            str_ = 'Interest Rate type'
        elif _sw3 == DEAL_TYPE_BUY_CANCELED:
            str_ = 'Canceled Buy type'
        elif _sw3 == DEAL_TYPE_SELL_CANCELED:
            str_ = 'Canceled Sell type'
        else:
            str_ = 'Unknown type'
        return str_
    def Entry(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_ENTRY)
    def EntryDescription(self):
        str_ = ""
        _sw4 = CDealInfo.Entry(self)
        if _sw4 == DEAL_ENTRY_IN:
            str_ = 'In entry'
        elif _sw4 == DEAL_ENTRY_OUT:
            str_ = 'Out entry'
        elif _sw4 == DEAL_ENTRY_INOUT:
            str_ = 'InOut entry'
        elif _sw4 == DEAL_ENTRY_STATE:
            str_ = 'Status record'
        elif _sw4 == DEAL_ENTRY_OUT_BY:
            str_ = 'Out By entry'
        else:
            str_ = 'Unknown entry'
        return str_
    def Magic(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_MAGIC)
    def PositionId(self):
        return HistoryDealGetInteger(self.m_ticket, DEAL_POSITION_ID)
    def Volume(self):
        return HistoryDealGetDouble(self.m_ticket, DEAL_VOLUME)
    def Price(self):
        return HistoryDealGetDouble(self.m_ticket, DEAL_PRICE)
    def Commission(self):
        return HistoryDealGetDouble(self.m_ticket, DEAL_COMMISSION)
    def Swap(self):
        return HistoryDealGetDouble(self.m_ticket, DEAL_SWAP)
    def Profit(self):
        return HistoryDealGetDouble(self.m_ticket, DEAL_PROFIT)
    def Symbol(self):
        return HistoryDealGetString(self.m_ticket, DEAL_SYMBOL)
    def Comment(self):
        return HistoryDealGetString(self.m_ticket, DEAL_COMMENT)
    def ExternalId(self):
        return HistoryDealGetString(self.m_ticket, DEAL_EXTERNAL_ID)
    def InfoInteger(self, prop_id, var):
        return (HistoryDealGetInteger(self.m_ticket, prop_id, var) != 0)
    def InfoDouble(self, prop_id, var):
        return (HistoryDealGetDouble(self.m_ticket, prop_id, var) != 0)
    def InfoString(self, prop_id, var):
        return _bool(HistoryDealGetString(self.m_ticket, prop_id, var))
    def FormatAction(self, str_, action):
        _sw5 = action
        if _sw5 == DEAL_TYPE_BUY:
            str_.v = 'buy'
        elif _sw5 == DEAL_TYPE_SELL:
            str_.v = 'sell'
        elif _sw5 == DEAL_TYPE_BALANCE:
            str_.v = 'balance'
        elif _sw5 == DEAL_TYPE_CREDIT:
            str_.v = 'credit'
        elif _sw5 == DEAL_TYPE_CHARGE:
            str_.v = 'charge'
        elif _sw5 == DEAL_TYPE_CORRECTION:
            str_.v = 'correction'
        elif _sw5 == DEAL_TYPE_BONUS:
            str_.v = 'bonus'
        elif _sw5 == DEAL_TYPE_COMMISSION:
            str_.v = 'commission'
        elif _sw5 == DEAL_TYPE_COMMISSION_DAILY:
            str_.v = 'daily commission'
        elif _sw5 == DEAL_TYPE_COMMISSION_MONTHLY:
            str_.v = 'monthly commission'
        elif _sw5 == DEAL_TYPE_COMMISSION_AGENT_DAILY:
            str_.v = 'daily agent commission'
        elif _sw5 == DEAL_TYPE_COMMISSION_AGENT_MONTHLY:
            str_.v = 'monthly agent commission'
        elif _sw5 == DEAL_TYPE_INTEREST:
            str_.v = 'interest rate'
        elif _sw5 == DEAL_TYPE_BUY_CANCELED:
            str_.v = 'canceled buy'
        elif _sw5 == DEAL_TYPE_SELL_CANCELED:
            str_.v = 'canceled sell'
        else:
            str_.v = 'unknown deal type ' + _str(action)
        return str_.v
    def FormatEntry(self, str_, entry):
        _sw6 = entry
        if _sw6 == DEAL_ENTRY_IN:
            str_.v = 'in'
        elif _sw6 == DEAL_ENTRY_OUT:
            str_.v = 'out'
        elif _sw6 == DEAL_ENTRY_INOUT:
            str_.v = 'in/out'
        elif _sw6 == DEAL_ENTRY_OUT_BY:
            str_.v = 'out by'
        else:
            str_.v = 'unknown deal entry ' + _str(entry)
        return str_.v
    def FormatDeal(self, str_):
        type_ = Box("")
        tmp_long = Box(0)
        symbol_name = self.Symbol()
        digits = Digits()
        if SymbolInfoInteger(symbol_name, SYMBOL_DIGITS, tmp_long):
            digits = _int(tmp_long.v)
        _sw7 = self.DealType()
        if _sw7 in (DEAL_TYPE_BUY, DEAL_TYPE_SELL):
            str_.v = StringFormat('#%I64u %s %s %s at %s', self.Ticket_0(), self.FormatAction(type_, self.DealType()), DoubleToString(self.Volume(), 2), symbol_name, DoubleToString(self.Price(), digits))
        elif _sw7 in (DEAL_TYPE_BALANCE, DEAL_TYPE_CREDIT, DEAL_TYPE_CHARGE, DEAL_TYPE_CORRECTION, DEAL_TYPE_BONUS, DEAL_TYPE_COMMISSION, DEAL_TYPE_COMMISSION_DAILY, DEAL_TYPE_COMMISSION_MONTHLY, DEAL_TYPE_COMMISSION_AGENT_DAILY, DEAL_TYPE_COMMISSION_AGENT_MONTHLY, DEAL_TYPE_INTEREST):
            str_.v = StringFormat('#%I64u %s %s [%s]', self.Ticket_0(), self.FormatAction(type_, self.DealType()), DoubleToString(self.Profit(), 2), self.Comment())
        else:
            str_.v = 'unknown deal type ' + _str(self.DealType())
        return str_.v
    def SelectByIndex(self, index):
        ticket = HistoryDealGetTicket(index)
        if ticket == 0:
            return False
        self.Ticket_1(ticket)
        return True

class CArrayDouble(CArray):
    _q_fields = ('m_data', 'm_delta')
    def __init__(self):
        CArray.__init__(self)
        self.m_data = Arr(0, 0.0)
        self.m_delta = 0.0
        self.m_delta = 0.0
        self.m_data_max = ArraySize(self.m_data)
    def _q_dtor(self):
        if self.m_data_max != 0:
            self.Shutdown()
    def Delta(self, delta):
        self.m_delta = MathAbs(delta)
    def Type(self):
        return TYPE_DOUBLE
    def Save(self, file_handle):
        i = 0
        if not CArray.Save(self, file_handle):
            return False
        if FileWriteInteger(file_handle, self.m_data_total, INT_VALUE) != INT_VALUE:
            return False
        i = 0
        for i in range(i, self.m_data_total):
            if FileWriteDouble(file_handle, self.m_data[i]) != 8:
                break
        else:
            i = _range_end(i, self.m_data_total, 1)
        return i == self.m_data_total
    def Load(self, file_handle):
        i = 0
        num = 0
        if not CArray.Load(self, file_handle):
            return False
        num = FileReadInteger(file_handle, INT_VALUE)
        self.Clear()
        if num != 0:
            if not self.Reserve(num):
                return False
            i = 0
            for i in range(i, num):
                self.m_data[i] = FileReadDouble(file_handle)
                self.m_data_total += 1
                if FileIsEnding(file_handle):
                    break
            else:
                i = _range_end(i, num, 1)
        self.m_sort_mode = -1
        return self.m_data_total == num
    def Reserve(self, size):
        new_size = 0
        if size <= 0:
            return False
        if self.Available() < size:
            new_size = self.m_data_max + (self.m_step_resize * (1 + _idiv(size - self.Available(), self.m_step_resize)))
            if new_size < 0:
                return False
            if _setattr(self, 'm_data_max', ArrayResize(self.m_data, new_size)) == -1:
                self.m_data_max = ArraySize(self.m_data)
        return self.Available() >= size
    def Resize(self, size):
        new_size = 0
        if size < 0:
            return False
        new_size = self.m_step_resize * (1 + _idiv(size, self.m_step_resize))
        if self.m_data_max != new_size:
            if _setattr(self, 'm_data_max', ArrayResize(self.m_data, new_size)) == -1:
                self.m_data_max = ArraySize(self.m_data)
                return False
        if self.m_data_total > size:
            self.m_data_total = size
        return self.m_data_max == new_size
    def Shutdown(self):
        if self.m_data_max == 0:
            return True
        if ArrayResize(self.m_data, 0) == -1:
            return False
        self.m_data_total = 0
        self.m_data_max = 0
        return True
    def Add(self, element):
        if not self.Reserve(1):
            return False
        self.m_data[_incattr(self, 'm_data_total', 1, True)] = element
        self.m_sort_mode = -1
        return True
    def AddArray_1(self, src):
        num = ArraySize(src)
        if not self.Reserve(num):
            return False
        for i in range(0, num):
            self.m_data[_incattr(self, 'm_data_total', 1, True)] = src[i]
        self.m_sort_mode = -1
        return True
    def AddArray_2(self, src):
        num = 0
        if not CheckPointer(src):
            return False
        num = src.Total()
        if not self.Reserve(num):
            return False
        for i in range(0, num):
            self.m_data[_incattr(self, 'm_data_total', 1, True)] = src.m_data[i]
        self.m_sort_mode = -1
        return True
    def Insert(self, element, pos):
        if pos < 0 or (not self.Reserve(1)):
            return False
        self.m_data_total += 1
        if pos < (self.m_data_total - 1):
            if self.MemMove(pos + 1, pos, self.m_data_total - pos - 1) < 0:
                return False
            self.m_data[pos] = element
        else:
            self.m_data[self.m_data_total - 1] = element
        self.m_sort_mode = -1
        return True
    def InsertArray_1(self, src, pos):
        num = ArraySize(src)
        if not self.Reserve(num):
            return False
        if self.MemMove(num + pos, pos, self.m_data_total - pos) < 0:
            return False
        for i in range(0, num):
            self.m_data[i + pos] = src[i]
        self.m_sort_mode = -1
        return True
    def InsertArray_2(self, src, pos):
        num = 0
        if not CheckPointer(src):
            return False
        num = src.Total()
        if not self.Reserve(num):
            return False
        if self.MemMove(num + pos, pos, self.m_data_total - pos) < 0:
            return False
        for i in range(0, num):
            self.m_data[i + pos] = src.m_data[i]
        self.m_sort_mode = -1
        return True
    def AssignArray_1(self, src):
        num = ArraySize(src)
        self.Clear()
        if self.m_data_max < num:
            if not self.Reserve(num):
                return False
        else:
            self.Resize(num)
        for i in range(0, num):
            self.m_data[i] = src[i]
            self.m_data_total += 1
        self.m_sort_mode = -1
        return True
    def AssignArray_2(self, src):
        num = 0
        if not CheckPointer(src):
            return False
        num = src.m_data_total
        self.Clear()
        if self.m_data_max < num:
            if not self.Reserve(num):
                return False
        else:
            self.Resize(num)
        for i in range(0, num):
            self.m_data[i] = src.m_data[i]
            self.m_data_total += 1
        self.m_sort_mode = src.SortMode()
        return True
    def At(self, index):
        if index < 0 or index >= self.m_data_total:
            return DBL_MAX
        return self.m_data[index]
    def __getitem__(self, index):
        return self.At(index)
    def Minimum(self, start, count):
        return CArray.Minimum(self, self.m_data, start, count)
    def Maximum(self, start, count):
        return CArray.Maximum(self, self.m_data, start, count)
    def Update(self, index, element):
        if index < 0 or index >= self.m_data_total:
            return False
        self.m_data[index] = element
        self.m_sort_mode = -1
        return True
    def Shift(self, index, shift):
        tmp_double = 0.0
        if (index < 0 or (index + shift) < 0) or (index + shift) >= self.m_data_total:
            return False
        if shift == 0:
            return True
        tmp_double = self.m_data[index]
        if shift > 0:
            if self.MemMove(index, index + 1, shift) < 0:
                return False
        else:
            if self.MemMove(index + shift + 1, index + shift, -shift) < 0:
                return False
        self.m_data[index + shift] = tmp_double
        self.m_sort_mode = -1
        return True
    def Delete(self, index):
        if index < 0 or index >= self.m_data_total:
            return False
        if index < (self.m_data_total - 1) and self.MemMove(index, index + 1, self.m_data_total - index - 1) < 0:
            return False
        self.m_data_total -= 1
        return True
    def DeleteRange(self, from_, to):
        if from_ < 0 or to < 0:
            return False
        if from_ > to or from_ >= self.m_data_total:
            return False
        if to >= (self.m_data_total - 1):
            to = self.m_data_total - 1
        if self.MemMove(from_, to + 1, self.m_data_total - to - 1) < 0:
            return False
        self.m_data_total -= to - from_ + 1
        return True
    def CompareArray_1(self, array):
        if self.m_data_total != ArraySize(array):
            return False
        for i in range(0, self.m_data_total):
            if self.m_data[i] != array[i]:
                return False
        return True
    def CompareArray_2(self, array):
        if not CheckPointer(array):
            return False
        if self.m_data_total != array.m_data_total:
            return False
        for i in range(0, self.m_data_total):
            if self.m_data[i] != array.m_data[i]:
                return False
        return True
    def InsertSort(self, element):
        pos = 0
        if not self.IsSorted():
            return False
        if not self.Reserve(1):
            return False
        if self.m_data_total == 0:
            self.m_data[_incattr(self, 'm_data_total', 1, True)] = element
            return True
        pos = self.QuickSearch(element)
        if self.m_data[pos] > element:
            self.Insert(element, pos)
        else:
            self.Insert(element, pos + 1)
        self.m_sort_mode = 0
        return True
    def Search(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        if MathAbs(self.m_data[pos] - element) <= self.m_delta:
            return pos
        return -1
    def SearchGreat(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        while self.m_data[pos] <= (element + self.m_delta):
            if (pos := pos + 1) == self.m_data_total:
                return -1
        return pos
    def SearchLess(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        while self.m_data[pos] >= (element - self.m_delta):
            if ((pos := pos - 1) + 1) == 0:
                return -1
        return pos
    def SearchGreatOrEqual(self, element):
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        for pos in range(self.QuickSearch(element), self.m_data_total):
            if self.m_data[pos] >= element:
                return pos
        return -1
    def SearchLessOrEqual(self, element):
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        for pos in range(self.QuickSearch(element), 0 - 1, -1):
            if self.m_data[pos] <= element:
                return pos
        return -1
    def SearchFirst(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos] == element:
            while MathAbs(self.m_data[pos] - element) <= self.m_delta:
                if ((pos := pos - 1) + 1) == 0:
                    break
            return pos + 1
        return -1
    def SearchLast(self, element):
        pos = 0
        if self.m_data_total == 0 or (not self.IsSorted()):
            return -1
        pos = self.QuickSearch(element)
        if self.m_data[pos] == element:
            while MathAbs(self.m_data[pos] - element) <= self.m_delta:
                if (pos := pos + 1) == self.m_data_total:
                    break
            return pos - 1
        return -1
    def SearchLinear(self, element):
        if self.m_data_total == 0:
            return -1
        for i in range(0, self.m_data_total):
            if MathAbs(self.m_data[i] - element) <= self.m_delta:
                return i
        return -1
    def QuickSort(self, beg, end, mode=0):
        i = 0
        j = 0
        p_double = 0.0
        t_double = 0.0
        if beg < 0 or end < 0:
            return
        i = beg
        j = end
        while i < end:
            p_double = self.m_data[(beg + end) >> 1]
            while i < j:
                while self.m_data[i] < p_double:
                    if i == (self.m_data_total - 1):
                        break
                    i += 1
                while self.m_data[j] > p_double:
                    if j == 0:
                        break
                    j -= 1
                if i <= j:
                    t_double = self.m_data[i]
                    self.m_data[((i := i + 1) - 1)] = self.m_data[j]
                    self.m_data[j] = t_double
                    if j == 0:
                        break
                    j -= 1
            if beg < j:
                self.QuickSort(beg, j)
            beg = i
            j = end
    def QuickSearch(self, element):
        i = 0
        j = 0
        m = -1
        t_double = 0.0
        i = 0
        j = self.m_data_total - 1
        while j >= i:
            m = (j + i) >> 1
            if m < 0 or m >= self.m_data_total:
                break
            t_double = self.m_data[m]
            if MathAbs(t_double - element) <= self.m_delta:
                break
            if t_double > element:
                j = m - 1
            else:
                i = m + 1
        return m
    def MemMove(self, dest, src, count):
        i = 0
        if (dest < 0 or src < 0) or count < 0:
            return -1
        if (src + count) > self.m_data_total:
            count = self.m_data_total - src
        if count < 0:
            return -1
        if dest == src or count == 0:
            return dest
        if (dest + count) > self.m_data_total:
            if self.m_data_max < (dest + count):
                return -1
            self.m_data_total = dest + count
        if dest < src:
            i = 0
            for i in range(i, count):
                self.m_data[dest + i] = self.m_data[src + i]
            else:
                i = _range_end(i, count, 1)
        else:
            i = count - 1
            for i in range(i, 0 - 1, -1):
                self.m_data[dest + i] = self.m_data[src + i]
            else:
                i = _range_end(i, 0 - 1, -1)
        return dest

class CTradeStatistics(MqlObject):
    _q_fields = ('m_deal', 'm_profit_data', 'm_balance_data', 'm_sharp_balance', 'm_balance_line', 'm_err_msg', 'm_initial_deposit', 'm_withdrawal', 'm_deals', 'm_trades', 'm_profit_factor', 'm_profit', 'm_gross_profit', 'm_gross_loss', 'm_expected_payoff', 'm_balance_min', 'm_balance_dd', 'm_balance_dd_percent', 'm_balance_dd_relative', 'm_balance_dd_relative_percent', 'm_balance_dd_absolute', 'm_equity_min', 'm_equity_dd', 'm_equity_dd_percent', 'm_equity_dd_relative', 'm_equity_dd_relative_percent', 'm_equity_dd_absolute', 'm_short_trades', 'm_profit_short_trades', 'm_long_trades', 'm_profit_long_trades', 'm_profit_trades', 'm_profit_trades_percent', 'm_loss_trades', 'm_loss_trades_percent', 'm_profit_trades_avg_con', 'm_loss_trades_avg_con', 'm_larg_profit_trade', 'm_larg_loss_trade', 'm_con_profit_max', 'm_con_profit_max_trades', 'm_max_con_wins', 'm_max_con_profit_trades', 'm_con_loss_max', 'm_con_loss_max_trades', 'm_max_con_losses', 'm_max_con_loss_trades', 'm_recovery_factor', 'm_shape_ratio', 'm_min_margin_level', 'm_z_score', 'm_z_score_percent', 'm_sharpe_ratio', 'm_ghpr', 'm_ghpr_percent', 'm_ahpr', 'm_ahpr_percent', 'm_lr_correlation', 'm_lr_standard_error', 'm_series_count', 'm_wins_series_count', 'm_loss_series_count')
    def __init__(self, *args):
        self.m_deal = CDealInfo()
        self.m_profit_data = CArrayDouble()
        self.m_balance_data = CArrayDouble()
        self.m_sharp_balance = CArrayDouble()
        self.m_balance_line = CArrayDouble()
        self.m_err_msg = ""
        self.m_initial_deposit = 0.0
        self.m_withdrawal = 0.0
        self.m_deals = 0
        self.m_trades = 0
        self.m_profit_factor = 0.0
        self.m_profit = 0.0
        self.m_gross_profit = 0.0
        self.m_gross_loss = 0.0
        self.m_expected_payoff = 0.0
        self.m_balance_min = 0.0
        self.m_balance_dd = 0.0
        self.m_balance_dd_percent = 0.0
        self.m_balance_dd_relative = 0.0
        self.m_balance_dd_relative_percent = 0.0
        self.m_balance_dd_absolute = 0.0
        self.m_equity_min = 0.0
        self.m_equity_dd = 0.0
        self.m_equity_dd_percent = 0.0
        self.m_equity_dd_relative = 0.0
        self.m_equity_dd_relative_percent = 0.0
        self.m_equity_dd_absolute = 0.0
        self.m_short_trades = 0
        self.m_profit_short_trades = 0
        self.m_long_trades = 0
        self.m_profit_long_trades = 0
        self.m_profit_trades = 0
        self.m_profit_trades_percent = 0.0
        self.m_loss_trades = 0
        self.m_loss_trades_percent = 0.0
        self.m_profit_trades_avg_con = 0
        self.m_loss_trades_avg_con = 0
        self.m_larg_profit_trade = 0.0
        self.m_larg_loss_trade = 0.0
        self.m_con_profit_max = 0.0
        self.m_con_profit_max_trades = 0
        self.m_max_con_wins = 0.0
        self.m_max_con_profit_trades = 0
        self.m_con_loss_max = 0.0
        self.m_con_loss_max_trades = 0
        self.m_max_con_losses = 0.0
        self.m_max_con_loss_trades = 0
        self.m_recovery_factor = 0.0
        self.m_shape_ratio = 0.0
        self.m_min_margin_level = 0.0
        self.m_z_score = 0.0
        self.m_z_score_percent = 0.0
        self.m_sharpe_ratio = 0.0
        self.m_ghpr = 0.0
        self.m_ghpr_percent = 0.0
        self.m_ahpr = 0.0
        self.m_ahpr_percent = 0.0
        self.m_lr_correlation = 0.0
        self.m_lr_standard_error = 0.0
        self.m_series_count = 0
        self.m_wins_series_count = 0
        self.m_loss_series_count = 0
    def CalculateRL(self, data, line, Standard_Error, Correlation):
        total = data.Total()
        if total <= 2:
            return True
        s1 = 0.0
        s2 = 0.0
        a1 = 0.0
        a2 = 0.0
        b1 = 0.0
        b2 = total
        for i in range(1, total + 1):
            s1 = s1 + (data.At(i - 1) * i)
            s2 = s2 + data.At(i - 1)
            a1 = a1 + (i * i)
            a2 = a2 + i
        b1 = a2
        dif = (a1 * b2) - (a2 * b1)
        A = _fdiv((s1 * b2) - (s2 * b1), dif)
        B = _fdiv((a1 * s2) - (a2 * s1), dif)
        sign = 1
        if A < 0.0:
            sign = -1
        line.Clear()
        str_ = ''
        for i in range(1, total + 1):
            str_ = str_ + StringFormat('| %i %.2f', i, (A * i) + B)
            line.Add((A * i) + B)
        Standard_Error.v = 0.0
        sum_ = 0.0
        for i in range(0, total):
            delta = MathAbs(data.At(i) - line.At(i))
            sum_ = sum_ + (delta * delta)
        Standard_Error.v = MathSqrt(_fdiv(sum_, total - 2))
        avg_balance = 0.0
        avg_line = 0.0
        for i in range(0, total):
            avg_balance = avg_balance + data.At(i)
            avg_line = avg_line + line.At(i)
        avg_balance = _fdiv(avg_balance, total)
        avg_line = _fdiv(avg_line, total)
        cov = 0.0
        Sx = 0.0
        Sy = 0.0
        for i in range(0, total):
            cov = cov + ((data.At(i) - avg_balance) * (line.At(i) - avg_line))
            Sx = Sx + MathPow(data.At(i) - avg_balance, 2)
            Sy = Sy + MathPow(line.At(i) - avg_line, 2)
        cov = _fdiv(cov, total)
        Sx = MathSqrt(_fdiv(Sx, total))
        Sy = MathSqrt(_fdiv(Sy, total))
        Correlation.v = _fdiv(sign * cov, Sx * Sy)
        return False
    def CalcEquityDrawdown(self, finally_):
        global _s_CTradeStatistics_CalcEquityDrawdown_maxpeak, _s_CTradeStatistics_CalcEquityDrawdown_minpeak
        equity = AccountInfoDouble(ACCOUNT_EQUITY)
        if equity < self.m_equity_min:
            self.m_equity_min = equity
        if AccountInfoDouble(ACCOUNT_MARGIN_LEVEL) < self.m_min_margin_level:
            self.m_min_margin_level = AccountInfoDouble(ACCOUNT_MARGIN_LEVEL)
        if _s_CTradeStatistics_CalcEquityDrawdown_maxpeak == 0.0:
            _s_CTradeStatistics_CalcEquityDrawdown_maxpeak = equity
        if _s_CTradeStatistics_CalcEquityDrawdown_minpeak == 0.0:
            _s_CTradeStatistics_CalcEquityDrawdown_minpeak = equity
        if _s_CTradeStatistics_CalcEquityDrawdown_maxpeak < equity or finally_:
            drawdown = _s_CTradeStatistics_CalcEquityDrawdown_maxpeak - _s_CTradeStatistics_CalcEquityDrawdown_minpeak
            drawdown_percent = _fdiv(drawdown, _s_CTradeStatistics_CalcEquityDrawdown_maxpeak) * 100.0
            if self.m_equity_dd_relative_percent < drawdown_percent:
                self.m_equity_dd_relative_percent = drawdown_percent
                self.m_equity_dd_relative = drawdown
            if self.m_equity_dd < drawdown:
                self.m_equity_dd = drawdown
                self.m_equity_dd_percent = drawdown_percent
            _s_CTradeStatistics_CalcEquityDrawdown_maxpeak = equity
            _s_CTradeStatistics_CalcEquityDrawdown_minpeak = equity
        if _s_CTradeStatistics_CalcEquityDrawdown_minpeak > equity:
            _s_CTradeStatistics_CalcEquityDrawdown_minpeak = equity
    def CalcZScorePercent(self, z_score):
        total = ArrayRange(Laplas, 0)
        value = NormalizeDouble(MathAbs(z_score), 2)
        if value > Laplas[total - 2][0]:
            return Laplas[total - 1][1]
        for i in range(0, total):
            if Laplas[i][0] == value:
                return Laplas[i][1]
        return 0.0
    def InitialDeposit(self):
        return self.m_initial_deposit
    def Withdrawal(self):
        return self.m_withdrawal
    def Profit(self):
        return self.m_profit
    def GrossProfit(self):
        return self.m_gross_profit
    def GrossLoss(self):
        return self.m_gross_loss
    def LargestProfitTrade(self):
        return self.m_larg_profit_trade
    def LargestLossTrade(self):
        return self.m_larg_loss_trade
    def ConProfitMax(self):
        return self.m_con_profit_max
    def ConProfitMaxTrades(self):
        return self.m_con_profit_max_trades
    def MaxConWins(self):
        return self.m_max_con_wins
    def MaxConProfitTrades(self):
        return self.m_max_con_profit_trades
    def ConLossMax(self):
        return self.m_con_loss_max
    def ConLossMaxTrades(self):
        return self.m_con_loss_max_trades
    def MaxConLosses(self):
        return self.m_max_con_losses
    def MaxConLossTrades(self):
        return self.m_max_con_loss_trades
    def BalanceMin(self):
        return self.m_balance_min
    def BalanceDD(self):
        return self.m_balance_dd
    def BalanceDDPercent(self):
        return self.m_balance_dd_percent
    def BalanceDDRelative(self):
        return self.m_balance_dd_relative
    def BalanceDDRelativePercent(self):
        return self.m_balance_dd_relative_percent
    def EquityMin(self):
        return self.m_equity_min
    def EquityDD(self):
        return self.m_equity_dd
    def EquityDDPercent(self):
        return self.m_equity_dd_percent
    def EquityDDRelative(self):
        return self.m_equity_dd_relative
    def EquityDDRelativePercent(self):
        return self.m_equity_dd_relative_percent
    def ExpectedPayoff(self):
        return self.m_expected_payoff
    def ProfitFactor(self):
        return self.m_profit_factor
    def RecoveryFactor(self):
        return self.m_recovery_factor
    def SharpeRatio(self):
        return self.m_sharpe_ratio
    def MinMarginLevel(self):
        return self.m_min_margin_level
    def Deals(self):
        return self.m_deals
    def Trades(self):
        return self.m_trades
    def ProfitTrades(self):
        return self.m_profit_trades
    def LossTrades(self):
        return self.m_loss_trades
    def ShortTrades(self):
        return self.m_short_trades
    def LongTrades(self):
        return self.m_long_trades
    def ProfitShortTrades(self):
        return self.m_profit_short_trades
    def ProfitLongTrades(self):
        return self.m_profit_long_trades
    def ProfitTradesAvgCon(self):
        return self.m_profit_trades_avg_con
    def LossTradesAvgCon(self):
        return self.m_loss_trades_avg_con
    def AHPR(self):
        return self.m_ahpr
    def AHPRPercent(self):
        return self.m_ahpr_percent
    def GHPR(self):
        return self.m_ghpr
    def GHPRPercent(self):
        return self.m_ghpr_percent
    def ZScore(self):
        return self.m_z_score
    def ZScorePercent(self):
        return self.m_z_score_percent
    def LRCorrelation(self):
        return self.m_lr_correlation
    def LRStandardError(self):
        return self.m_lr_standard_error
    def Calculate(self, time_start=0, time_end=0, initial_deposit=0.0):
        self.m_err_msg = ''
        if time_end == 0:
            time_end = TimeTradeServer()
        self.m_initial_deposit = initial_deposit
        self.m_withdrawal = 0.0
        self.m_profit = 0.0
        self.m_gross_profit = 0.0
        self.m_gross_loss = 0.0
        self.m_short_trades = 0
        self.m_larg_profit_trade = 0.0
        self.m_long_trades = 0
        self.m_larg_loss_trade = 0.0
        self.m_profit_short_trades = 0
        self.m_profit_long_trades = 0
        self.m_larg_profit_trade = 0.0
        self.m_larg_loss_trade = 0.0
        self.m_con_profit_max = 0.0
        self.m_con_profit_max_trades = 0
        self.m_con_loss_max = 0.0
        self.m_con_loss_max_trades = 0
        self.m_max_con_losses = 0.0
        self.m_max_con_loss_trades = 0
        self.m_balance_min = 0.0
        self.m_balance_dd_absolute = 0.0
        self.m_balance_dd = 0.0
        self.m_balance_dd_percent = 0.0
        self.m_balance_dd_relative = 0.0
        self.m_balance_dd_relative_percent = 0.0
        self.m_expected_payoff = 0.0
        self.m_profit_factor = 0.0
        self.m_recovery_factor = 0.0
        self.m_sharpe_ratio = 0.0
        self.m_deals = 0
        self.m_trades = 0
        self.m_profit_trades = 0
        self.m_loss_trades = 0
        self.m_short_trades = 0
        self.m_long_trades = 0
        self.m_series_count = 0
        self.m_wins_series_count = 0
        self.m_loss_series_count = 0
        self.m_profit_trades_avg_con = 0
        self.m_loss_trades_avg_con = 0
        min_peak = 0.0
        max_peak = 0.0
        balance = 0.0
        sharp_balance = 0.0
        profit = 0.0
        sequential = 0.0
        profit_length = 0
        loss_length = 0
        result = NO_VALUE
        self.m_balance_data.Clear()
        self.m_profit_data.Clear()
        self.m_sharp_balance.Clear()
        try_ = 0
        res = HistorySelect(time_start, time_end)
        if (not res) and try_ < 20:
            Sleep(100)
            res = HistorySelect(time_start, time_end)
            try_ += 1
        if not res:
            self.m_err_msg = 'Unable to get the trade history'
            return False
        deals_total = HistoryDealsTotal()
        for i in range(0, deals_total):
            if not self.m_deal.SelectByIndex(i):
                self.m_err_msg = 'Error function SelectByIndex()'
                return False
            if self.m_deal.DealType() == DEAL_TYPE_BALANCE:
                profit = NormalizeDouble(self.m_deal.Profit() + self.m_deal.Swap(), 2)
                balance += profit
                self.m_balance_data.Add(balance)
                if min_peak == 0.0:
                    min_peak = balance
                else:
                    min_peak += profit
                if max_peak == 0.0:
                    max_peak = balance
                else:
                    max_peak += profit
                if profit >= 0.0:
                    if self.m_balance_min == 0.0:
                        self.m_balance_min = balance
                    else:
                        self.m_balance_min += profit
                    result = WIN
                    if initial_deposit == 0.0:
                        if self.m_initial_deposit == 0.0:
                            self.m_initial_deposit = self.m_deal.Profit()
                            sharp_balance += profit
                            self.m_sharp_balance.Add(sharp_balance)
                        else:
                            self.m_initial_deposit += self.m_deal.Profit()
                else:
                    self.m_withdrawal -= self.m_deal.Profit()
                    result = LOSS
            if self.m_deal.DealType() == DEAL_TYPE_BUY or self.m_deal.DealType() == DEAL_TYPE_SELL:
                self.m_deals += 1
                profit = NormalizeDouble(self.m_deal.Profit() + self.m_deal.Swap() + self.m_deal.Commission(), 2)
                self.m_profit_data.Add(profit)
                if profit >= 0.0:
                    self.m_gross_profit += profit
                else:
                    self.m_gross_loss += profit
                balance = balance + profit
                self.m_balance_data.Add(balance)
                if balance < self.m_balance_min:
                    self.m_balance_min = balance
                if min_peak == 0.0:
                    min_peak = balance
                if max_peak == 0.0:
                    max_peak = balance
                drawdown = max_peak - balance
                drawdown_percent = _fdiv(drawdown, max_peak) * 100.0
                if drawdown > self.m_balance_dd:
                    self.m_balance_dd = drawdown
                    self.m_balance_dd_percent = drawdown_percent
                if drawdown_percent > self.m_balance_dd_relative_percent:
                    self.m_balance_dd_relative_percent = drawdown_percent
                    self.m_balance_dd_relative = drawdown
                if max_peak < balance:
                    max_peak = balance
                if self.m_deal.Entry() == DEAL_ENTRY_OUT or self.m_deal.Entry() == DEAL_ENTRY_INOUT:
                    sharp_balance += profit
                    self.m_sharp_balance.Add(sharp_balance)
                    self.m_trades += 1
                    if profit >= 0.0:
                        self.m_profit_trades += 1
                    if profit < 0:
                        self.m_loss_trades += 1
                    if profit >= 0.0:
                        if profit > self.m_larg_profit_trade:
                            self.m_larg_profit_trade = profit
                        if result != WIN:
                            result = WIN
                            self.m_series_count += 1
                            self.m_wins_series_count += 1
                            profit_length = 0
                            sequential = 0.0
                        sequential += profit
                        profit_length += 1
                        if self.m_max_con_profit_trades < profit_length:
                            self.m_max_con_profit_trades = profit_length
                            self.m_max_con_wins = sequential
                        if self.m_con_profit_max < sequential:
                            self.m_con_profit_max = sequential
                            self.m_con_profit_max_trades = profit_length
                    else:
                        if profit < self.m_larg_loss_trade:
                            self.m_larg_loss_trade = profit
                        if result != LOSS:
                            result = LOSS
                            self.m_series_count += 1
                            self.m_loss_series_count += 1
                            loss_length = 0
                            sequential = 0.0
                        sequential += profit
                        loss_length += 1
                        if self.m_max_con_loss_trades < loss_length:
                            self.m_max_con_loss_trades = loss_length
                            self.m_max_con_losses = sequential
                        if self.m_con_loss_max > sequential:
                            self.m_con_loss_max = sequential
                            self.m_con_loss_max_trades = loss_length
                    if self.m_deal.DealType() == DEAL_TYPE_SELL:
                        if profit >= 0.0:
                            self.m_profit_long_trades += 1
                        self.m_long_trades += 1
                    if self.m_deal.DealType() == DEAL_TYPE_BUY:
                        if profit >= 0.0:
                            self.m_profit_short_trades += 1
                        self.m_short_trades += 1
        self.m_ahpr = 0.0
        self.m_ahpr_percent = 0.0
        self.m_ghpr = 0.0
        self.m_ghpr_percent = 0.0
        limit = self.m_sharp_balance.Total()
        if limit > 1:
            hpr = 0.0
            hpr2 = 0.0
            HPR = Arr(0, 0.0)
            ArrayResize(HPR, limit - 1)
            for i in range(1, limit):
                if self.m_sharp_balance.At(i) != 0.0:
                    HPR[i - 1] = _fdiv(self.m_sharp_balance.At(i), self.m_sharp_balance.At(i - 1))
                    self.m_ahpr += HPR[i - 1]
            self.m_ahpr = _fdiv(self.m_ahpr, limit - 1)
            self.m_ahpr_percent = (self.m_ahpr - 1) * 100
            self.m_ghpr = MathPow(_fdiv(self.m_sharp_balance.At(limit - 1), self.m_initial_deposit), _fdiv(1.0, limit - 1))
            self.m_ghpr_percent = (self.m_ghpr - 1) * 100
            self.m_sharpe_ratio = 0.0
            if limit > 2:
                Std = 0.0
                RiskFreeRate = 0.0
                for i in range(0, limit - 2):
                    Std += (self.m_ahpr - HPR[i]) * (self.m_ahpr - HPR[i])
                Std = MathPow(_fdiv(Std, limit - 2), 0.5)
                self.m_sharpe_ratio = _fdiv(self.m_ahpr - (1.0 + RiskFreeRate), Std)
        self.m_z_score = 0.0
        self.m_z_score_percent = 0.0
        N = self.m_profit_data.Total()
        if N > 2:
            W = 0
            L = 0
            R = 0
            outcome = NO_VALUE
            for i in range(0, N):
                if self.m_profit_data.At(i) >= 0.0:
                    if outcome != WIN:
                        outcome = WIN
                        R += 1
                    W += 1
                else:
                    if outcome != LOSS:
                        outcome = LOSS
                        R += 1
                    L += 1
            P = 2.0 * W * L
            if MathAbs(MathSqrt(_fdiv(P * (P - N), N - 1))) >= FLT_EPSILON:
                self.m_z_score = _fdiv((N * (R - 0.5)) - P, MathSqrt(_fdiv(P * (P - N), N - 1)))
                self.m_z_score_percent = self.CalcZScorePercent(self.m_z_score) * 100
        self.m_profit = self.m_gross_profit + self.m_gross_loss
        self.m_profit_factor = 0.0
        if MathAbs(self.m_gross_loss) > FLT_EPSILON:
            self.m_profit_factor = MathAbs(_fdiv(self.m_gross_profit, self.m_gross_loss))
        self.m_profit_trades_percent = 0.0
        self.m_loss_trades_percent = 0.0
        self.m_expected_payoff = 0.0
        if self.m_trades > 0:
            self.m_expected_payoff = _fdiv(self.m_profit, self.m_trades)
            self.m_profit_trades_percent = _fdiv(float(self.m_profit_trades), self.m_trades) * 100
            self.m_loss_trades_percent = _fdiv(float(self.m_loss_trades), self.m_trades) * 100
        self.m_profit_trades_avg_con = 0
        if self.m_wins_series_count > 0:
            self.m_profit_trades_avg_con = _int(MathRound(_fdiv(float(self.m_profit_trades), self.m_wins_series_count)))
        self.m_loss_trades_avg_con = 0
        if self.m_loss_series_count > 0:
            self.m_loss_trades_avg_con = _int(MathRound(_fdiv(float(self.m_loss_trades), self.m_loss_series_count)))
        if MathAbs(self.m_balance_dd) > FLT_EPSILON:
            self.m_recovery_factor = _fdiv(self.m_profit, self.m_balance_dd)
        self.CalculateRL(self.m_balance_data, self.m_balance_line, _AttrRef(self, 'm_lr_standard_error'), _AttrRef(self, 'm_lr_correlation'))
        return True
    def PrintStatistics(self):
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_INITIAL_DEPOSIT, ''), TesterStatistics(STAT_INITIAL_DEPOSIT), self.InitialDeposit())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_WITHDRAWAL, ''), TesterStatistics(STAT_WITHDRAWAL), self.Withdrawal())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_PROFIT, ''), TesterStatistics(STAT_PROFIT), self.Profit())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_GROSS_PROFIT, ''), TesterStatistics(STAT_GROSS_PROFIT), self.GrossProfit())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_GROSS_LOSS, ''), TesterStatistics(STAT_GROSS_LOSS), self.GrossLoss())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_MAX_PROFITTRADE, ''), TesterStatistics(STAT_MAX_PROFITTRADE), self.LargestProfitTrade())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_MAX_LOSSTRADE, ''), TesterStatistics(STAT_MAX_LOSSTRADE), self.LargestLossTrade())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_CONPROFITMAX, ''), TesterStatistics(STAT_CONPROFITMAX), self.ConProfitMax())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_CONPROFITMAX_TRADES, ''), TesterStatistics(STAT_CONPROFITMAX_TRADES), self.ConProfitMaxTrades())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_MAX_CONWINS, ''), TesterStatistics(STAT_MAX_CONWINS), self.MaxConWins())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_MAX_CONPROFIT_TRADES, ''), TesterStatistics(STAT_MAX_CONPROFIT_TRADES), self.MaxConProfitTrades())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_CONLOSSMAX, ''), TesterStatistics(STAT_CONLOSSMAX), self.ConLossMax())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_CONLOSSMAX_TRADES, ''), TesterStatistics(STAT_CONLOSSMAX_TRADES), self.ConLossMaxTrades())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_MAX_CONLOSSES, ''), TesterStatistics(STAT_MAX_CONLOSSES), self.MaxConLosses())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_MAX_CONLOSS_TRADES, ''), TesterStatistics(STAT_MAX_CONLOSS_TRADES), self.MaxConLossTrades())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_BALANCEMIN, ''), TesterStatistics(STAT_BALANCEMIN), self.BalanceMin())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_BALANCE_DD, ''), TesterStatistics(STAT_BALANCE_DD), self.BalanceDD())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_BALANCEDD_PERCENT, ''), TesterStatistics(STAT_BALANCEDD_PERCENT), self.BalanceDDPercent())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_BALANCE_DD_RELATIVE, ''), TesterStatistics(STAT_BALANCE_DD_RELATIVE), self.BalanceDDRelative())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_BALANCE_DDREL_PERCENT, ''), TesterStatistics(STAT_BALANCE_DDREL_PERCENT), self.BalanceDDRelativePercent())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_EQUITYMIN, ''), TesterStatistics(STAT_EQUITYMIN), self.EquityMin())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_EQUITY_DD, ''), TesterStatistics(STAT_EQUITY_DD), self.EquityDD())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_EQUITYDD_PERCENT, ''), TesterStatistics(STAT_EQUITYDD_PERCENT), self.EquityDDPercent())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_EQUITY_DD_RELATIVE, ''), TesterStatistics(STAT_EQUITY_DD_RELATIVE), self.EquityDDRelative())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_EQUITY_DDREL_PERCENT, ''), TesterStatistics(STAT_EQUITY_DDREL_PERCENT), self.EquityDDRelativePercent())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_EXPECTED_PAYOFF, ''), TesterStatistics(STAT_EXPECTED_PAYOFF), self.ExpectedPayoff())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_PROFIT_FACTOR, ''), TesterStatistics(STAT_PROFIT_FACTOR), self.ProfitFactor())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_RECOVERY_FACTOR, ''), TesterStatistics(STAT_RECOVERY_FACTOR), self.RecoveryFactor())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_SHARPE_RATIO, ''), TesterStatistics(STAT_SHARPE_RATIO), self.SharpeRatio())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_MIN_MARGINLEVEL, ''), TesterStatistics(STAT_MIN_MARGINLEVEL), self.MinMarginLevel())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_DEALS, ''), TesterStatistics(STAT_DEALS), self.Deals())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_TRADES, ''), TesterStatistics(STAT_TRADES), self.Trades())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_PROFIT_TRADES, ''), TesterStatistics(STAT_PROFIT_TRADES), self.ProfitTrades())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_LOSS_TRADES, ''), TesterStatistics(STAT_LOSS_TRADES), self.LossTrades())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_SHORT_TRADES, ''), TesterStatistics(STAT_SHORT_TRADES), self.ShortTrades())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_LONG_TRADES, ''), TesterStatistics(STAT_LONG_TRADES), self.LongTrades())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_PROFIT_SHORTTRADES, ''), TesterStatistics(STAT_PROFIT_SHORTTRADES), self.ProfitShortTrades())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_PROFIT_LONGTRADES, ''), TesterStatistics(STAT_PROFIT_LONGTRADES), self.ProfitLongTrades())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_PROFITTRADES_AVGCON, ''), TesterStatistics(STAT_PROFITTRADES_AVGCON), self.ProfitTradesAvgCon())
        PrintFormat('%s: %.0f - %.0f', EnumToString(STAT_LOSSTRADES_AVGCON, ''), TesterStatistics(STAT_LOSSTRADES_AVGCON), self.LossTradesAvgCon())
        PrintFormat('%s: %.4f(%.2f) - %.4f(%.2f)', EnumToString(STAT_GHPR, 'ENUM_STATISTICS_PLUS'), 0, 0, self.GHPR(), self.GHPRPercent())
        PrintFormat('%s: %.4f(%.2f) - %.4f(%.2f)', EnumToString(STAT_AHPR, 'ENUM_STATISTICS_PLUS'), 0, 0, self.AHPR(), self.AHPRPercent())
        PrintFormat('%s: %.2f(%.2f) - %.2f(%.2f)', EnumToString(STAT_Z_SCORE, 'ENUM_STATISTICS_PLUS'), 0, 0, self.ZScore(), self.ZScorePercent())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_LR_CORRELATION, 'ENUM_STATISTICS_PLUS'), 0, self.LRCorrelation())
        PrintFormat('%s: %.2f - %.2f', EnumToString(STAT_LR_STANDARD_ERROR, 'ENUM_STATISTICS_PLUS'), 0, self.LRStandardError())
    def GetLastErrorString(self):
        return self.m_err_msg
    def CalculateEquityDD(self, state):
        _sw8 = state
        if _sw8 == CALC_INIT:
            self.m_equity_min = AccountInfoDouble(ACCOUNT_EQUITY)
            self.m_equity_dd = 0.0
            self.m_equity_dd_percent = 0.0
            self.m_equity_dd_relative = 0.0
            self.m_equity_dd_relative_percent = 0.0
            self.m_min_margin_level = AccountInfoDouble(ACCOUNT_MARGIN_LEVEL)
        elif _sw8 == CALC_TICK:
            self.CalcEquityDrawdown(False)
        elif _sw8 == CALC_DEINIT:
            self.CalcEquityDrawdown(True)
        return True
    def Percent(self, value, divider):
        if MathAbs(value) <= FLT_EPSILON:
            return 0.0
        return _fdiv(100 * value, divider)
    def Divide(self, value, divider):
        if MathAbs(value) <= FLT_EPSILON:
            return 0.0
        return _fdiv(value, divider)

class Params(MqlObject):
    _q_fields = ('chart', 'subwin', 'name', 'x1', 'y1', 'x2', 'y2', 'font_name', 'font_size', 'font_color')
    def __init__(self, *args):
        self.chart = 0
        self.subwin = 0
        self.name = ""
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.font_name = ""
        self.font_size = 0
        self.font_color = 0

class CPanelDialog(CAppDialog):
    _q_fields = ('m_label', 'm_value', 'm_button', 'FontName', 'FontSize', 'FontColor', 'FontHeight')
    def __init__(self, *args):
        CAppDialog.__init__(self)
        self.m_label = Arr(3, 0, dyn=False, factory=CLabel, dims=(20,))
        self.m_value = Arr(3, 0, dyn=False, factory=CLabel, dims=(20,))
        self.m_button = Arr(1, 0, dyn=False, factory=CButton)
        self.FontName = ""
        self.FontSize = 0
        self.FontColor = 0
        self.FontHeight = 0
    def Create(self, p):
        if not CAppDialog.Create(self, p.chart, p.name, p.subwin, p.x1, p.y1, p.x2, p.y2):
            return False
        self.FontName = p.font_name
        self.FontSize = p.font_size
        self.FontColor = p.font_color
        self.FontHeight = self.FontSize * 2
        self.Caption_1(p.name)
        if not self.CreateButton(0):
            return False
        if not self.CreateLabel(0, 0, STAT_INITIAL_DEPOSIT):
            return False
        if not self.CreateLabel(1, 0, STAT_PROFIT):
            return False
        if not self.CreateLabel(2, 0, _int(STAT_GROSS_PROFIT)):
            return False
        if not self.CreateLabel(3, 0, _int(STAT_GROSS_LOSS)):
            return False
        if not self.CreateLabel(4, 0, _int(STAT_PROFIT_FACTOR)):
            return False
        if not self.CreateLabel(5, 0, _int(STAT_RECOVERY_FACTOR)):
            return False
        if not self.CreateLabel(6, 0, STAT_AHPR):
            return False
        if not self.CreateLabel(7, 0, STAT_GHPR):
            return False
        if not self.CreateLabel(8, 0, STAT_Z_SCORE):
            return False
        if not self.CreateLabel(10, 0, _int(STAT_TRADES)):
            return False
        if not self.CreateLabel(11, 0, _int(STAT_DEALS)):
            return False
        if not self.CreateLabel(0, 1, _int(STAT_EXPECTED_PAYOFF)):
            return False
        if not self.CreateLabel(1, 1, _int(STAT_SHARPE_RATIO)):
            return False
        if not self.CreateLabel(2, 1, STAT_LR_CORRELATION):
            return False
        if not self.CreateLabel(3, 1, STAT_LR_STANDARD_ERROR):
            return False
        if not self.CreateLabel(5, 1, _int(STAT_SHORT_TRADES)):
            return False
        if not self.CreateLabel(6, 1, _int(STAT_PROFIT_TRADES)):
            return False
        if not self.CreateLabel(7, 1, _int(STAT_MAX_PROFITTRADE)):
            return False
        if not self.CreateLabel(8, 1, STAT_AVG_PROFIT_TRADE):
            return False
        if not self.CreateLabel(9, 1, _int(STAT_MAX_CONWINS)):
            return False
        if not self.CreateLabel(10, 1, _int(STAT_CONPROFITMAX)):
            return False
        if not self.CreateLabel(11, 1, _int(STAT_PROFITTRADES_AVGCON)):
            return False
        if not self.CreateLabel(1, 2, STAT_BALANCE_DD_ABSOLUTE):
            return False
        if not self.CreateLabel(2, 2, _int(STAT_BALANCE_DD)):
            return False
        if not self.CreateLabel(3, 2, _int(STAT_BALANCE_DD_RELATIVE)):
            return False
        if not self.CreateLabel(5, 2, _int(STAT_LONG_TRADES)):
            return False
        if not self.CreateLabel(6, 2, _int(STAT_LOSS_TRADES)):
            return False
        if not self.CreateLabel(7, 2, _int(STAT_MAX_LOSSTRADE)):
            return False
        if not self.CreateLabel(8, 2, STAT_AVG_LOSS_TRADE):
            return False
        if not self.CreateLabel(9, 2, _int(STAT_MAX_CONLOSSES)):
            return False
        if not self.CreateLabel(10, 2, _int(STAT_CONLOSSMAX)):
            return False
        if not self.CreateLabel(11, 2, _int(STAT_LOSSTRADES_AVGCON)):
            return False
        return True
    def SetLabelParam(self, i, col, text):
        range1 = ArrayRange(self.m_value, 0)
        if col >= range1:
            col = range1 - 1
        range2 = ArrayRange(self.m_value, 1)
        if i >= range2:
            i = range2 - 1
        text_length = StringLen(text)
        if text_length < 16:
            temp = Box("")
            StringInit(temp, 16 - text_length, 32)
            text = temp.v + text
        self.m_value[col][i].Text_1(text)
        self.m_value[col][i].Color_1(self.FontColor)
    def GetButtonName(self, index):
        if index > 0:
            index = 0
        return self.m_button[index].Name()
    def OnResize(self):
        if not CWndContainer.OnResize(self):
            return False
        self.CreateButton(0, True)
        for c in range(0, 2 + 1):
            for i in range(0, 11 + 1):
                self.CreateLabel(i, c, 0, True)
        return True
    def CreateButton(self, index, only_move=False):
        delta = self.Height_0() - self.ClientAreaHeight()
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        caption = ""
        _sw9 = index
        if _sw9 == 0:
            x1 = self.ClientAreaWidth() - 120 - 70
            y1 = (-delta) + 3
            caption = 'Calculate'
        if only_move:
            return self.m_button[index].Move_2(x1, 1)
        x2 = x1 + 120
        y2 = y1 + 19
        if not self.m_button[index].Create(self.m_chart_id, self.m_name + 'Button_' + IntegerToString(index), self.m_subwin, x1, y1, x2, y2):
            return False
        self.m_button[index].FontSize_1(8)
        self.m_button[index].Text_1(caption)
        if not self.Add_1(self.m_button[index]):
            return False
        return True
    def CreateLabel(self, i, col, name, only_move=False):
        delta = self.Height_0() - self.ClientAreaHeight()
        range1 = MathMin(ArrayRange(self.m_label, 0), ArrayRange(self.m_value, 0))
        if col >= range1:
            col = range1 - 1
        range2 = MathMin(ArrayRange(self.m_label, 1), ArrayRange(self.m_value, 1))
        if i >= range2:
            i = range2 - 1
        width_3 = _idiv(self.ClientAreaWidth(), 3)
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        x11 = 0
        y11 = 0
        x22 = 0
        y22 = 0
        _sw10 = col
        if _sw10 == 1:
            x1 = 15 + width_3
            y1 = 30 + (self.FontHeight * i)
            x2 = x1
            y2 = y1 + self.FontHeight
            x11 = _int(width_3 * 1.5)
            y11 = 30 + (self.FontHeight * i)
            x22 = x11
            y22 = y1 + self.FontHeight
        elif _sw10 == 2:
            x1 = 15 + (width_3 * 2)
            y1 = 30 + (self.FontHeight * i)
            x2 = x1
            y2 = y1 + self.FontHeight
            x11 = _int(width_3 * 2.5)
            y11 = 30 + (self.FontHeight * i)
            x22 = x11
            y22 = y1 + self.FontHeight
        else:
            x1 = 15
            y1 = 30 + (self.FontHeight * i)
            x2 = x1
            y2 = y1 + self.FontHeight
            x11 = _idiv(width_3, 2)
            y11 = 30 + (self.FontHeight * i)
            x22 = x11
            y22 = y11 + self.FontHeight
        if only_move:
            self.m_label[col][i].Move_2(x1, y1)
            self.m_value[col][i].Move_2(x11, y11)
            return True
        if not self.m_label[col][i].Create(self.m_chart_id, self.m_name + 'Label_' + IntegerToString(i) + '_' + IntegerToString(col), self.m_subwin, x1, y1 - delta, x2, y2 - delta):
            return False
        if not self.Add_1(self.m_label[col][i]):
            return False
        self.m_label[col][i].Text_1(self.ParamCaption(name))
        self.m_label[col][i].Font_1(self.FontName)
        self.m_label[col][i].FontSize_1(self.FontSize)
        self.m_label[col][i].Color_1(self.FontColor)
        if not self.m_value[col][i].Create(self.m_chart_id, self.m_name + 'Value_' + IntegerToString(i) + '_' + IntegerToString(col), self.m_subwin, x11, y11 - delta, x22, y22 - delta):
            return False
        if not self.Add_1(self.m_value[col][i]):
            return False
        self.m_value[col][i].Font_1(self.FontName)
        self.m_value[col][i].FontSize_1(self.FontSize)
        self.m_value[col][i].Color_1(self.FontColor)
        self.m_value[col][i].Text_1('')
        return True
    def ParamCaption(self, index):
        _sw11 = index
        if _sw11 == STAT_INITIAL_DEPOSIT:
            return 'Initial Deposit'
        elif _sw11 == STAT_PROFIT:
            return 'Total Net Profit'
        elif _sw11 == STAT_BALANCE:
            return 'Balance'
        elif _sw11 == STAT_EQUITY:
            return 'Equity'
        elif _sw11 == STAT_GROSS_PROFIT:
            return 'Gross Profit'
        elif _sw11 == STAT_GROSS_LOSS:
            return 'Gross Loss'
        elif _sw11 == STAT_PROFIT_FACTOR:
            return 'Profit Factor'
        elif _sw11 == STAT_RECOVERY_FACTOR:
            return 'Recovery Factor'
        elif _sw11 == STAT_EXPECTED_PAYOFF:
            return 'Expected Payoff'
        elif _sw11 == STAT_BALANCE_DD_ABSOLUTE:
            return 'Balance Dr. Abs.'
        elif _sw11 == STAT_BALANCE_DD:
            return 'Balance Dr. Max.'
        elif _sw11 == STAT_BALANCE_DD_RELATIVE:
            return 'Balance Dr. Rel.'
        elif _sw11 == STAT_TRADES:
            return 'Total Trades'
        elif _sw11 == STAT_DEALS:
            return 'Total Deals'
        elif _sw11 == STAT_SHORT_TRADES:
            return 'Short Trades'
        elif _sw11 == STAT_LONG_TRADES:
            return 'Long Trades'
        elif _sw11 == STAT_PROFIT_TRADES:
            return 'Profit Trades'
        elif _sw11 == STAT_LOSS_TRADES:
            return 'Loss Trades'
        elif _sw11 == STAT_MAX_PROFITTRADE:
            return 'Largest Profit Trade'
        elif _sw11 == STAT_MAX_LOSSTRADE:
            return 'Largest Loss Trade'
        elif _sw11 == STAT_CONPROFITMAX:
            return 'Max. Cons. Profit'
        elif _sw11 == STAT_MAX_CONWINS:
            return 'Max. Cons. Wins'
        elif _sw11 == STAT_CONLOSSMAX:
            return 'Max. Cons. Loss'
        elif _sw11 == STAT_MAX_CONLOSSES:
            return 'Max. Cons. Losses'
        elif _sw11 == STAT_AVG_PROFIT_TRADE:
            return 'Avg. Profit Trade'
        elif _sw11 == STAT_AVG_LOSS_TRADE:
            return 'Avg. Loss Trade'
        elif _sw11 == STAT_PROFITTRADES_AVGCON:
            return 'Avg. Cons. Wins'
        elif _sw11 == STAT_LOSSTRADES_AVGCON:
            return 'Avg. Cons. Losses'
        elif _sw11 == STAT_GHPR:
            return 'GHPR'
        elif _sw11 == STAT_AHPR:
            return 'AHPR'
        elif _sw11 == STAT_SHARPE_RATIO:
            return 'Sharpe Ratio'
        elif _sw11 == STAT_Z_SCORE:
            return 'Z Score'
        elif _sw11 == STAT_LR_CORRELATION:
            return 'LR Correlation'
        elif _sw11 == STAT_LR_STANDARD_ERROR:
            return 'LR Standard Error'
        else:
            return '---'

def OnInit():
    param = Params()
    param.chart = 0
    param.name = ''
    param.subwin = 0
    param.x1 = 0
    param.y1 = 0
    param.x2 = _int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS))
    param.y2 = MathMin(15 * InpFontSize * 2, _int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)))
    param.font_name = InpFontName
    param.font_size = InpFontSize
    param.font_color = InpFontColor
    if not ExtDialog.Create(param):
        return -1
    if not ExtDialog.Run():
        return -2
    ClearData()
    if not TerminalInfoInteger(TERMINAL_CONNECTED):
        return 0
    if stat.Calculate():
        PrintData()
    else:
        PrintError()
    return 0

def OnDeinit(reason):
    ExtDialog.Destroy()
    ChartRedraw()

def OnTrade():
    global _s_OnTrade_time_on_trade
    if _s_OnTrade_time_on_trade == TimeCurrent():
        return
    _s_OnTrade_time_on_trade = TimeCurrent()
    ClearData()
    if stat.Calculate():
        PrintData()
    else:
        PrintError()
    ChartRedraw()

def OnChartEvent(id_, lparam, dparam, sparam):
    ExtDialog.ChartEvent(id_, lparam, dparam, sparam)
    if id_ == CHARTEVENT_OBJECT_CLICK:
        if ExtDialog.GetButtonName(0) == sparam:
            ClearData()
            if not TerminalInfoInteger(TERMINAL_CONNECTED):
                return
            if stat.Calculate():
                PrintData()
            else:
                PrintError()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if prev_calculated == 0:
        ClearData()
        if not TerminalInfoInteger(TERMINAL_CONNECTED):
            return 0
        if stat.Calculate():
            PrintData()
        else:
            PrintError()
    return rates_total

def PrintData():
    ExtDialog.Caption_1(IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)))
    ExtDialog.SetLabelParam(0, 0, StringFormat('%.2f', stat.InitialDeposit()))
    ExtDialog.SetLabelParam(1, 0, StringFormat('%.2f', stat.Profit()))
    ExtDialog.SetLabelParam(2, 0, StringFormat('%.2f', stat.GrossProfit()))
    ExtDialog.SetLabelParam(3, 0, StringFormat('%.2f', stat.GrossLoss()))
    ExtDialog.SetLabelParam(4, 0, StringFormat('%.2f', stat.ProfitFactor()))
    ExtDialog.SetLabelParam(5, 0, StringFormat('%.2f', stat.RecoveryFactor()))
    ExtDialog.SetLabelParam(6, 0, StringFormat('%.4f(%.2f%%)', stat.AHPR(), stat.AHPRPercent()))
    ExtDialog.SetLabelParam(7, 0, StringFormat('%.4f(%.2f%%)', stat.GHPR(), stat.GHPRPercent()))
    ExtDialog.SetLabelParam(8, 0, StringFormat('%.2f(%.2f%%)', stat.ZScore(), stat.ZScorePercent()))
    ExtDialog.SetLabelParam(10, 0, StringFormat('%d', stat.Trades()))
    ExtDialog.SetLabelParam(11, 0, StringFormat('%d', stat.Deals()))
    ExtDialog.SetLabelParam(0, 1, StringFormat('%.2f', stat.ExpectedPayoff()))
    ExtDialog.SetLabelParam(1, 1, StringFormat('%.2f', stat.SharpeRatio()))
    ExtDialog.SetLabelParam(2, 1, StringFormat('%.2f', stat.LRCorrelation()))
    ExtDialog.SetLabelParam(3, 1, StringFormat('%.2f', stat.LRStandardError()))
    ExtDialog.SetLabelParam(5, 1, StringFormat('%.d(%.2f%%)', stat.ShortTrades(), stat.Percent(stat.ProfitShortTrades(), stat.ShortTrades())))
    ExtDialog.SetLabelParam(6, 1, StringFormat('%.d(%.2f%%)', stat.ProfitTrades(), stat.Percent(stat.ProfitTrades(), stat.Trades())))
    ExtDialog.SetLabelParam(7, 1, StringFormat('%.2f', stat.LargestProfitTrade()))
    ExtDialog.SetLabelParam(8, 1, StringFormat('%.2f', stat.Divide(stat.GrossProfit(), stat.ProfitTrades())))
    ExtDialog.SetLabelParam(9, 1, StringFormat('%.d(%.2f)', stat.MaxConProfitTrades(), stat.MaxConWins()))
    ExtDialog.SetLabelParam(10, 1, StringFormat('%.2f(%.d)', stat.ConProfitMax(), stat.ConProfitMaxTrades()))
    ExtDialog.SetLabelParam(11, 1, StringFormat('%.d', stat.ProfitTradesAvgCon()))
    ExtDialog.SetLabelParam(1, 2, StringFormat('%.2f', stat.InitialDeposit() - stat.BalanceMin()))
    ExtDialog.SetLabelParam(2, 2, StringFormat('%.2f(%.2f%%)', stat.BalanceDD(), stat.BalanceDDPercent()))
    ExtDialog.SetLabelParam(3, 2, StringFormat('%.2f(%.2f%%)', stat.BalanceDDRelative(), stat.BalanceDDRelativePercent()))
    ExtDialog.SetLabelParam(5, 2, StringFormat('%.d(%.2f%%)', stat.LongTrades(), stat.Percent(stat.ProfitLongTrades(), stat.LongTrades())))
    ExtDialog.SetLabelParam(6, 2, StringFormat('%.d(%.2f%%)', stat.LossTrades(), stat.Percent(stat.LossTrades(), stat.Trades())))
    ExtDialog.SetLabelParam(7, 2, StringFormat('%.2f', stat.LargestLossTrade()))
    ExtDialog.SetLabelParam(8, 2, StringFormat('%.2f', stat.Divide(stat.GrossLoss(), stat.LossTrades())))
    ExtDialog.SetLabelParam(9, 2, StringFormat('%.d(%.2f)', stat.MaxConLossTrades(), stat.MaxConLosses()))
    ExtDialog.SetLabelParam(10, 2, StringFormat('%.2f(%.d)', stat.ConLossMax(), stat.ConLossMaxTrades()))
    ExtDialog.SetLabelParam(11, 2, StringFormat('%.d', stat.LossTradesAvgCon()))
    ChartRedraw()

def ClearData():
    ExtDialog.Caption_1('')
    for c in range(0, 2 + 1):
        for i in range(0, 11 + 1):
            ExtDialog.SetLabelParam(i, c, '')
    ChartRedraw()

def PrintError():
    msg = ' Error: ' + stat.GetLastErrorString()
    ExtDialog.Caption_1(msg)

# ---- global variables initialised from expressions
ExtDialog = _alloc(CPanelDialog)
ExtDialog.__init__()
stat = _alloc(CTradeStatistics)
stat.__init__()

# ---- static local variables
_s_CTradeStatistics_CalcEquityDrawdown_maxpeak = 0.0
_s_CTradeStatistics_CalcEquityDrawdown_minpeak = 0.0
_s_OnTrade_time_on_trade = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Tradestatisticspanel(_MQL5Indicator):
    name = 'tradestatisticspanel'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFontSize': 10,  # Font Size
    }

