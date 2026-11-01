"""EquiPeak Drawdown tracker ing — converted from MQL5: MQL5 Indicators/EquiPeak Drawdown Tracker/EquiPeak Drawdown tracker ing.mq5

Tracks current/historical drawdown, with logs and push notifications.
Copyright: (c) 2025 Enrique Enguix; Link: https://www.mql5.com/es/users/envex; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.object import *  # #include Object.mqh
from backtester.mql5.lib.stdliberr import *  # #include StdLibErr.mqh

MQL5_META = {'props': {'copyright': '(c) 2025 Enrique Enguix', 'link': 'https://www.mql5.com/es/users/envex', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Tracks current/historical drawdown, with logs and push notifications.'], 'name': 'EquiPeak Drawdown tracker ing', 'source': 'MQL5 Indicators/EquiPeak Drawdown Tracker/EquiPeak Drawdown tracker ing.mq5', 'folder': 'EquiPeak Drawdown Tracker', 'inputs': [{'mql': 'MagicNumbers', 'py': 'MagicNumbers', 'param': None, 'type': 'string', 'default': '-1', 'label': 'Magics to monitor (-1 tracks all)', 'sinput': False}, {'mql': 'InitialMaxDrawdown', 'py': 'InitialMaxDrawdown', 'param': 'InitialMaxDrawdown', 'type': 'double', 'default': 0.0, 'label': 'Initial Max DD (%)', 'sinput': False}, {'mql': 'RefreshInterval', 'py': 'RefreshInterval', 'param': 'RefreshInterval', 'type': 'uint', 'default': 60, 'label': 'Update frequency (seconds)', 'sinput': False}, {'mql': 'UpdateMaxDrawdown', 'py': 'UpdateMaxDrawdown', 'param': 'UpdateMaxDrawdown', 'type': 'int', 'default': 1, 'label': 'MaxDD update mode', 'sinput': False}, {'mql': 'SendPushNotifications', 'py': 'SendPushNotifications', 'param': 'SendPushNotifications', 'type': 'bool', 'default': True, 'label': 'Send push notifications?', 'sinput': False}, {'mql': 'ReferenceBalanceMode', 'py': 'ReferenceBalanceMode', 'param': 'ReferenceBalanceMode', 'type': 'int', 'default': 0, 'label': 'Fixed or peak reference?', 'sinput': False}, {'mql': 'InpFixedBalance', 'py': 'InpFixedBalance', 'param': 'InpFixedBalance', 'type': 'double', 'default': 0.0, 'label': 'Fixed balance (0 => current)', 'sinput': False}, {'mql': 'CurrentDrawdownTextColor', 'py': 'CurrentDrawdownTextColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Color for current DD text', 'sinput': False}, {'mql': 'MaxDrawdownTextColor', 'py': 'MaxDrawdownTextColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Color for max DD text', 'sinput': False}, {'mql': 'CurrentDrawdownFontSize', 'py': 'CurrentDrawdownFontSize', 'param': 'CurrentDrawdownFontSize', 'type': 'uint', 'default': 25, 'label': 'Font size (current DD)', 'sinput': False}, {'mql': 'MaxDrawdownFontSize', 'py': 'MaxDrawdownFontSize', 'param': 'MaxDrawdownFontSize', 'type': 'uint', 'default': 25, 'label': 'Font size (max DD)', 'sinput': False}, {'mql': 'DisplayLabelsInBackground', 'py': 'DisplayLabelsInBackground', 'param': 'DisplayLabelsInBackground', 'type': 'bool', 'default': True, 'label': 'Labels behind the chart?', 'sinput': False}, {'mql': 'LabelPosX', 'py': 'LabelPosX', 'param': 'LabelPosX', 'type': 'int', 'default': 200, 'label': 'Label X (pixels)', 'sinput': False}, {'mql': 'LabelPosY', 'py': 'LabelPosY', 'param': 'LabelPosY', 'type': 'int', 'default': 20, 'label': 'Label Y (pixels)', 'sinput': False}, {'mql': 'LabelSpacing', 'py': 'LabelSpacing', 'param': 'LabelSpacing', 'type': 'uint', 'default': 10, 'label': 'Vertical spacing', 'sinput': False}, {'mql': 'PrintDetailedLogs', 'py': 'PrintDetailedLogs', 'param': 'PrintDetailedLogs', 'type': 'bool', 'default': True, 'label': 'Print logs in Journal?', 'sinput': False}, {'mql': 'EnableFileLog', 'py': 'EnableFileLog', 'param': 'EnableFileLog', 'type': 'bool', 'default': True, 'label': 'Create a separate file to log current drawdown values', 'sinput': False}, {'mql': 'InpFileExtension', 'py': 'InpFileExtension', 'param': 'InpFileExtension', 'type': 'int', 'default': 1, 'label': 'File extension: CSV or TXT', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['Object.mqh', 'StdLibErr.mqh']}

POSITION_TIME_UPDATE_MSC = 0  # MQL5 constant unknown to the converter

# enum EBalanceMode
REF_FIXED_BALANCE = 0
REF_PEAK_BALANCE = 1
_enum('EBalanceMode', {0: 'REF_FIXED_BALANCE', 1: 'REF_PEAK_BALANCE'})

# enum EMaxDDUpdateMode
NO_UPDATE_MAX_DD = 0
UPDATE_MAX_DD_IF_BIGGER = 1
_enum('EMaxDDUpdateMode', {0: 'NO_UPDATE_MAX_DD', 1: 'UPDATE_MAX_DD_IF_BIGGER'})

# enum SFileExtension
UseCSV = 0
UseTXT = 1
_enum('SFileExtension', {0: 'UseCSV', 1: 'UseTXT'})

# ---- inputs and global variables
MagicNumbers = _input('MagicNumbers', '-1')  # Magics to monitor (-1 tracks all)
InitialMaxDrawdown = _input('InitialMaxDrawdown', 0.0)  # Initial Max DD (%)
RefreshInterval = _input('RefreshInterval', 60)  # Update frequency (seconds)
UpdateMaxDrawdown = _input('UpdateMaxDrawdown', UPDATE_MAX_DD_IF_BIGGER)  # MaxDD update mode
SendPushNotifications = _input('SendPushNotifications', True)  # Send push notifications?
ReferenceBalanceMode = _input('ReferenceBalanceMode', REF_FIXED_BALANCE)  # Fixed or peak reference?
InpFixedBalance = _input('InpFixedBalance', 0.0)  # Fixed balance (0 => current)
CurrentDrawdownTextColor = _input('CurrentDrawdownTextColor', clrGray)  # Color for current DD text
MaxDrawdownTextColor = _input('MaxDrawdownTextColor', clrGray)  # Color for max DD text
CurrentDrawdownFontSize = _input('CurrentDrawdownFontSize', 25)  # Font size (current DD)
MaxDrawdownFontSize = _input('MaxDrawdownFontSize', 25)  # Font size (max DD)
DisplayLabelsInBackground = _input('DisplayLabelsInBackground', True)  # Labels behind the chart?
LabelPosX = _input('LabelPosX', 200)  # Label X (pixels)
LabelPosY = _input('LabelPosY', 20)  # Label Y (pixels)
LabelSpacing = _input('LabelSpacing', 10)  # Vertical spacing
PrintDetailedLogs = _input('PrintDetailedLogs', True)  # Print logs in Journal?
EnableFileLog = _input('EnableFileLog', True)  # Create a separate file to log current drawdown values
InpFileExtension = _input('InpFileExtension', UseTXT)  # File extension: CSV or TXT
g_ReferenceBalance = 0.0  # Reference balance used for DD calculations
g_MaxDrawdown = 0.0  # Max historical drawdown (%), stored globally
g_PeakBalance = 0.0  # Peak balance (if using REF_PEAK_BALANCE)
g_PeakBalanceGVName = ""
g_MaxDrawdownGVName = ""
g_RefreshIntervalVar = 60
g_CurrentDrawdownFontSize = 35
g_MaxDrawdownFontSize = 35
g_FileExtension = '.csv'  # default value
g_currentDrawdownObjName = ""
g_maxDrawdownObjName = ""
g_LastPushTimeNOUPDATE = 0

class CPositionInfo(CObject):
    _q_fields = ('m_type', 'm_volume', 'm_price', 'm_stop_loss', 'm_take_profit')
    def __init__(self):
        CObject.__init__(self)
        self.m_type = 0
        self.m_volume = 0.0
        self.m_price = 0.0
        self.m_stop_loss = 0.0
        self.m_take_profit = 0.0
        self.m_type = WRONG_VALUE
        self.m_volume = 0.0
        self.m_price = 0.0
        self.m_stop_loss = 0.0
        self.m_take_profit = 0.0
    def _q_dtor(self):
        pass
    def Ticket(self):
        return _ulong(PositionGetInteger(POSITION_TICKET))
    def Time(self):
        return PositionGetInteger(POSITION_TIME)
    def TimeMsc(self):
        return _ulong(PositionGetInteger(POSITION_TIME_MSC))
    def TimeUpdate(self):
        return PositionGetInteger(POSITION_TIME_UPDATE)
    def TimeUpdateMsc(self):
        return _ulong(PositionGetInteger(POSITION_TIME_UPDATE_MSC))
    def PositionType(self):
        return PositionGetInteger(POSITION_TYPE)
    def TypeDescription(self):
        str_ = Box("")
        return self.FormatType(str_, self.PositionType())
    def Magic(self):
        return PositionGetInteger(POSITION_MAGIC)
    def Identifier(self):
        return PositionGetInteger(POSITION_IDENTIFIER)
    def Volume(self):
        return PositionGetDouble(POSITION_VOLUME)
    def PriceOpen(self):
        return PositionGetDouble(POSITION_PRICE_OPEN)
    def StopLoss(self):
        return PositionGetDouble(POSITION_SL)
    def TakeProfit(self):
        return PositionGetDouble(POSITION_TP)
    def PriceCurrent(self):
        return PositionGetDouble(POSITION_PRICE_CURRENT)
    def Commission(self):
        SetUserError(ERR_FUNCTION_NOT_ALLOWED)
        return 0.0
    def Swap(self):
        return PositionGetDouble(POSITION_SWAP)
    def Profit(self):
        return PositionGetDouble(POSITION_PROFIT)
    def Symbol(self):
        return PositionGetString(POSITION_SYMBOL)
    def Comment(self):
        return PositionGetString(POSITION_COMMENT)
    def InfoInteger(self, prop_id, var):
        return (PositionGetInteger(prop_id, var) != 0)
    def InfoDouble(self, prop_id, var):
        return (PositionGetDouble(prop_id, var) != 0)
    def InfoString(self, prop_id, var):
        return _bool(PositionGetString(prop_id, var))
    def FormatType(self, str_, type_):
        _sw1 = type_
        if _sw1 == POSITION_TYPE_BUY:
            str_.v = 'buy'
        elif _sw1 == POSITION_TYPE_SELL:
            str_.v = 'sell'
        else:
            str_.v = 'unknown position type ' + _str(type_)
        return str_.v
    def FormatPosition(self, str_):
        tmp = ""
        type_ = Box("")
        tmp_long = Box(0)
        margin_mode = AccountInfoInteger(ACCOUNT_MARGIN_MODE)
        symbol_name = self.Symbol()
        digits = Digits()
        if SymbolInfoInteger(symbol_name, SYMBOL_DIGITS, tmp_long):
            digits = _int(tmp_long.v)
        if margin_mode == ACCOUNT_MARGIN_MODE_RETAIL_HEDGING:
            str_.v = StringFormat('#%I64u %s %s %s %s', self.Ticket(), self.FormatType(type_, self.PositionType()), DoubleToString(self.Volume(), 2), symbol_name, DoubleToString(self.PriceOpen(), digits + 3))
        else:
            str_.v = StringFormat('%s %s %s %s', self.FormatType(type_, self.PositionType()), DoubleToString(self.Volume(), 2), symbol_name, DoubleToString(self.PriceOpen(), digits + 3))
        sl = self.StopLoss()
        tp = self.TakeProfit()
        if sl != 0.0:
            tmp = StringFormat(' sl: %s', DoubleToString(sl, digits))
            str_.v += tmp
        if tp != 0.0:
            tmp = StringFormat(' tp: %s', DoubleToString(tp, digits))
            str_.v += tmp
        return str_.v
    def Select(self, symbol):
        return PositionSelect(symbol)
    def SelectByMagic(self, symbol, magic):
        res = False
        total = PositionsTotal()
        for i in range(0, total):
            position_symbol = _str(PositionGetSymbol(i))
            if position_symbol == symbol and magic == PositionGetInteger(POSITION_MAGIC):
                res = True
                break
        return res
    def SelectByTicket(self, ticket):
        return PositionSelectByTicket(ticket)
    def SelectByIndex(self, index):
        ticket = PositionGetTicket(index)
        return ticket > 0
    def StoreState(self):
        self.m_type = self.PositionType()
        self.m_volume = self.Volume()
        self.m_price = self.PriceOpen()
        self.m_stop_loss = self.StopLoss()
        self.m_take_profit = self.TakeProfit()
    def CheckState(self):
        if (((self.m_type == self.PositionType() and self.m_volume == self.Volume()) and self.m_price == self.PriceOpen()) and self.m_stop_loss == self.StopLoss()) and self.m_take_profit == self.TakeProfit():
            return False
        return True

def OnInit():
    global g_CurrentDrawdownFontSize, g_FileExtension, g_MaxDrawdown, g_MaxDrawdownFontSize, g_MaxDrawdownGVName, g_PeakBalance, g_PeakBalanceGVName, g_ReferenceBalance, g_RefreshIntervalVar, g_currentDrawdownObjName, g_maxDrawdownObjName
    g_PeakBalanceGVName = 'EquiPeakDT_PeakBalance_' + _str(ChartID())
    g_MaxDrawdownGVName = 'EquiPeakDT_MaxDD_' + _str(ChartID())
    g_currentDrawdownObjName = 'current_drawdown_' + _str(ChartID())
    g_maxDrawdownObjName = 'max_drawdown_' + _str(ChartID())
    if RefreshInterval < 1:
        g_RefreshIntervalVar = 10
        if PrintDetailedLogs:
            Print('[WARNING] RefreshInterval < 1. Using 10 seconds as a minimum fallback.')
    elif RefreshInterval > 3600:
        g_RefreshIntervalVar = 3600
        if PrintDetailedLogs:
            Print('[WARNING] RefreshInterval > 3600. Using 3600 seconds (1 hour) as max.')
    else:
        g_RefreshIntervalVar = RefreshInterval
    if CurrentDrawdownFontSize < 1:
        g_CurrentDrawdownFontSize = 12
        if PrintDetailedLogs:
            Print('[WARNING] CurrentDrawdownFontSize <1. Using 12 as a fallback value.')
    else:
        g_CurrentDrawdownFontSize = CurrentDrawdownFontSize
    if MaxDrawdownFontSize < 1:
        g_MaxDrawdownFontSize = 12
        if PrintDetailedLogs:
            Print('[WARNING] MaxDrawdownFontSize <1. Using 12 as a fallback value.')
    else:
        g_MaxDrawdownFontSize = MaxDrawdownFontSize
    if InpFileExtension == UseCSV:
        g_FileExtension = '.csv'
    else:
        g_FileExtension = '.txt'
    EventSetTimer(g_RefreshIntervalVar)
    OnTimer()
    if ReferenceBalanceMode == REF_PEAK_BALANCE:
        if GlobalVariableCheck(g_PeakBalanceGVName):
            g_PeakBalance = GlobalVariableGet(g_PeakBalanceGVName)
            if PrintDetailedLogs:
                PrintFormat('[INFO] Loaded peak balance from global variable: %.2f', g_PeakBalance)
        else:
            g_PeakBalance = AccountInfoDouble(ACCOUNT_BALANCE)
            GlobalVariableSet(g_PeakBalanceGVName, g_PeakBalance)
            if PrintDetailedLogs:
                PrintFormat('[INFO] No global variable found. Created initial peak balance: %.2f', g_PeakBalance)
    if GlobalVariableCheck(g_MaxDrawdownGVName):
        g_MaxDrawdown = GlobalVariableGet(g_MaxDrawdownGVName)
        if PrintDetailedLogs:
            PrintFormat('[INFO] Loaded max historical DD from global variable: %.2f%%', g_MaxDrawdown)
    else:
        g_MaxDrawdown = InitialMaxDrawdown
        GlobalVariableSet(g_MaxDrawdownGVName, g_MaxDrawdown)
        if PrintDetailedLogs:
            PrintFormat('[INFO] No global variable found for max DD. Created initial with: %.2f%%', g_MaxDrawdown)
    if ReferenceBalanceMode == REF_FIXED_BALANCE:
        if InpFixedBalance <= 0.0:
            fallback = AccountInfoDouble(ACCOUNT_BALANCE)
            g_ReferenceBalance = fallback
            if PrintDetailedLogs:
                PrintFormat('[WARNING] InpFixedBalance <= 0. Using current account balance instead (%.2f).', fallback)
        else:
            g_ReferenceBalance = InpFixedBalance
            if PrintDetailedLogs:
                PrintFormat('[INFO] Using Fixed Balance mode. Reference = %.2f', g_ReferenceBalance)
    else:
        g_ReferenceBalance = g_PeakBalance
        if PrintDetailedLogs:
            PrintFormat('[INFO] Using Peak Balance mode. Reference = %.2f', g_ReferenceBalance)
    if g_ReferenceBalance < 1e-08:
        g_ReferenceBalance = 1e-08
        if PrintDetailedLogs:
            Print('[ERROR] Reference balance was 0 or invalid. Set to 1e-8 to avoid division by zero.')
    if PrintDetailedLogs:
        Print('[INFO] EquiPeakDrawdownTracker successfully initialized.')
        PrintConfigurationSummary()
    return INIT_SUCCEEDED

def OnTimer():
    global g_LastPushTimeNOUPDATE, g_MaxDrawdown, g_PeakBalance, g_ReferenceBalance
    realBalance = AccountInfoDouble(ACCOUNT_BALANCE)
    floatingProfit = GetFloatingProfit()
    accountEquity = realBalance + floatingProfit
    if ReferenceBalanceMode == REF_PEAK_BALANCE:
        if realBalance > g_PeakBalance:
            oldPeak = g_PeakBalance
            g_PeakBalance = realBalance
            GlobalVariableSet(g_PeakBalanceGVName, g_PeakBalance)
            g_ReferenceBalance = g_PeakBalance
            if PrintDetailedLogs:
                PrintFormat('[INFO] New peak balance detected: %.2f (old peak was %.2f)', g_PeakBalance, oldPeak)
    currentDrawdownPct = CalculateCurrentDrawdownPct(accountEquity, g_ReferenceBalance)
    if UpdateMaxDrawdown == UPDATE_MAX_DD_IF_BIGGER:
        if currentDrawdownPct > g_MaxDrawdown:
            oldMax = g_MaxDrawdown
            g_MaxDrawdown = currentDrawdownPct
            GlobalVariableSet(g_MaxDrawdownGVName, g_MaxDrawdown)
            if PrintDetailedLogs:
                PrintFormat('[INFO] New max drawdown reached: %.2f%% (old max was %.2f%%)', g_MaxDrawdown, oldMax)
            if SendPushNotifications:
                SendDetailedNotification(currentDrawdownPct, oldMax, True)
    else:
        if SendPushNotifications:
            if (TimeCurrent() - g_LastPushTimeNOUPDATE) >= 3600:
                SendDetailedNotification(currentDrawdownPct, g_MaxDrawdown, False)
                g_LastPushTimeNOUPDATE = TimeCurrent()
    currentDDText = StringFormat('Current Drawdown: %.2f%%', currentDrawdownPct)
    maxDDText = StringFormat('Max. Historical Drawdown: %.2f%%', g_MaxDrawdown)
    DrawLabel(g_currentDrawdownObjName, currentDDText, LabelPosX, LabelPosY, CurrentDrawdownTextColor, g_CurrentDrawdownFontSize)
    secondLabelY = LabelPosY + _int(g_CurrentDrawdownFontSize) + _int(LabelSpacing)
    DrawLabel(g_maxDrawdownObjName, maxDDText, LabelPosX, secondLabelY, MaxDrawdownTextColor, g_MaxDrawdownFontSize)
    if EnableFileLog:
        LogDrawdown(currentDrawdownPct)

def OnDeinit(reason):
    EventKillTimer()
    ObjectDelete(0, g_currentDrawdownObjName)
    ObjectDelete(0, g_maxDrawdownObjName)
    if PrintDetailedLogs:
        Print('[INFO] EquiPeakDrawdownTracker deinitialized.')

def OnCalculate(rates_total, prev_calculated, begin, price):
    return rates_total

def CalculateCurrentDrawdownPct(equity, referenceBalance):
    eps = 1e-10
    diff = referenceBalance - equity
    if diff <= eps:
        return 0.0
    return _fdiv(diff, referenceBalance) * 100.0

def GetFloatingProfit():
    totalProfit = 0.0
    for i in range(PositionsTotal() - 1, 0 - 1, -1):
        if not g_position.SelectByIndex(i):
            if PrintDetailedLogs:
                PrintFormat('[WARNING] Unable to select position at index %d', i)
            continue
        mNumber = g_position.Magic()
        if IsTrackedMagicNumber(mNumber):
            totalProfit += g_position.Profit()
    return totalProfit

def IsTrackedMagicNumber(magicNumber):
    magicList = Arr(0, "")
    count = StringSplit(MagicNumbers, 44, magicList)
    trackAll = False
    for i in range(0, count):
        magicStr = Box(magicList[i])
        StringReplace(magicStr, ' ', '')
        if magicStr.v == '-1':
            trackAll = True
            break
    if trackAll:
        return True
    for i in range(0, count):
        magicStr = Box(magicList[i])
        StringReplace(magicStr, ' ', '')
        parsed = StringToDouble(magicStr.v)
        if parsed == float(magicNumber):
            return True
    return False

def SendDetailedNotification(currentDD, oldMaxDD, isNewRecord):
    server = AccountInfoString(ACCOUNT_SERVER)
    login = AccountInfoInteger(ACCOUNT_LOGIN)
    timeStr = TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS)
    msg = StringFormat('EquiPeak Drawdown Tracker v1.00\nBroker/Server: %s\nAccount: %lld\nTime: %s\nCurrent DD: %.2f%%\nMax Historical DD: %.2f%%', server, login, timeStr, currentDD, g_MaxDrawdown)
    if isNewRecord:
        msg += StringFormat('\n[RECORD] New Max DD reached! (previous was %.2f%%)', oldMaxDD)
    sent = SendNotification(msg)
    if (not sent) and PrintDetailedLogs:
        PrintFormat('[WARNING] Failed to send push notification: %s', msg)

def PrintConfigurationSummary():
    if not PrintDetailedLogs:
        return
    Print('===== EquiPeak Drawdown Tracker Configuration Summary =====')
    PrintFormat(' > MagicNumbers to track: %s', MagicNumbers)
    if ReferenceBalanceMode == REF_FIXED_BALANCE:
        PrintFormat(' > Balance Mode: FIXED, reference balance = %.2f', g_ReferenceBalance)
    else:
        PrintFormat(' > Balance Mode: PEAK (loaded peak = %.2f)', g_PeakBalance)
    if UpdateMaxDrawdown == UPDATE_MAX_DD_IF_BIGGER:
        Print(' > MaxDD Update Mode: UPDATE IF BIGGER')
    else:
        Print(' > MaxDD Update Mode: DO NOT UPDATE (with limited notifications)')
    PrintFormat(' > Current stored Max DD = %.2f%%', g_MaxDrawdown)
    PrintFormat(' > Refresh interval (seconds): %u', g_RefreshIntervalVar)
    PrintFormat(' > Push Notifications: %s', ('ENABLED' if SendPushNotifications else 'DISABLED'))
    PrintFormat(' > Label Text Sizes (DD/MaxDD): %u / %u', g_CurrentDrawdownFontSize, g_MaxDrawdownFontSize)
    PrintFormat(' > Label Positions: X=%d, Y=%d, Spacing=%u', LabelPosX, LabelPosY, LabelSpacing)
    PrintFormat(' > File Logging: %s', ('ENABLED' if EnableFileLog else 'DISABLED'))
    if EnableFileLog:
        tf = PeriodToStringLowerCase(Period())
        fileName = 'DD_' + Symbol() + '_' + tf + '_Magic_' + MagicNumbers + g_FileExtension
        PrintFormat(' > File Extension: %s', g_FileExtension)
        PrintFormat(' > File Path (approx.): Common/Files/%s', fileName)
    Print('==========================================================')

def LogDrawdown(currentDrawdown):
    symbol = Symbol()
    tfString = PeriodToStringLowerCase(Period())
    fileName = 'DD_' + symbol + '_' + tfString + '_Magic_' + MagicNumbers + g_FileExtension
    flags = (FILE_READ | FILE_WRITE) | FILE_COMMON
    if g_FileExtension == '.csv':
        flags |= FILE_CSV
    handle = FileOpen(fileName, flags)
    if handle == INVALID_HANDLE:
        Print('[ERROR] Could not open/create log file: ', fileName)
        return
    FileSeek(handle, 0, SEEK_END)
    timeStr = TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS)
    realBalance = AccountInfoDouble(ACCOUNT_BALANCE)
    equity = realBalance + GetFloatingProfit()
    FileWrite(handle, timeStr, MagicNumbers, DoubleToString(currentDrawdown, 2), DoubleToString(realBalance, 2), DoubleToString(equity, 2))
    FileClose(handle)

def PeriodToStringLowerCase(period):
    _sw2 = period
    if _sw2 == PERIOD_M1:
        return 'm1'
    elif _sw2 == PERIOD_M2:
        return 'm2'
    elif _sw2 == PERIOD_M3:
        return 'm3'
    elif _sw2 == PERIOD_M4:
        return 'm4'
    elif _sw2 == PERIOD_M5:
        return 'm5'
    elif _sw2 == PERIOD_M6:
        return 'm6'
    elif _sw2 == PERIOD_M10:
        return 'm10'
    elif _sw2 == PERIOD_M12:
        return 'm12'
    elif _sw2 == PERIOD_M15:
        return 'm15'
    elif _sw2 == PERIOD_M20:
        return 'm20'
    elif _sw2 == PERIOD_M30:
        return 'm30'
    elif _sw2 == PERIOD_H1:
        return 'h1'
    elif _sw2 == PERIOD_H2:
        return 'h2'
    elif _sw2 == PERIOD_H3:
        return 'h3'
    elif _sw2 == PERIOD_H4:
        return 'h4'
    elif _sw2 == PERIOD_H6:
        return 'h6'
    elif _sw2 == PERIOD_H8:
        return 'h8'
    elif _sw2 == PERIOD_H12:
        return 'h12'
    elif _sw2 == PERIOD_D1:
        return 'd1'
    elif _sw2 == PERIOD_W1:
        return 'w1'
    elif _sw2 == PERIOD_MN1:
        return 'mn1'
    else:
        return 'unknown'

def DrawLabel(name, text, x, y, clr, fontSize):
    if ObjectFind(0, name) == -1:
        ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER)
        ObjectSetInteger(0, name, OBJPROP_BACK, DisplayLabelsInBackground)
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, fontSize)
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)

# ---- global variables initialised from expressions
g_position = _alloc(CPositionInfo)
g_position.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EquiPeakDrawdownTrackerIng(_MQL5Indicator):
    name = 'EquiPeak Drawdown tracker ing'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InitialMaxDrawdown': 0.0,  # Initial Max DD (%)
        'RefreshInterval': 60,  # Update frequency (seconds)
        'UpdateMaxDrawdown': _Choice({0: 'Do not update the historical Max DD', 1: 'Update if current DD exceeds the historical DD'}, default=1),  # MaxDD update mode
        'SendPushNotifications': True,  # Send push notifications?
        'ReferenceBalanceMode': _Choice({0: 'Use a fixed balance reference', 1: 'Use a peak balance reference (global variable)'}, default=0),  # Fixed or peak reference?
        'InpFixedBalance': 0.0,  # Fixed balance (0 => current)
        'CurrentDrawdownFontSize': 25,  # Font size (current DD)
        'MaxDrawdownFontSize': 25,  # Font size (max DD)
        'DisplayLabelsInBackground': True,  # Labels behind the chart?
        'LabelPosX': 200,  # Label X (pixels)
        'LabelPosY': 20,  # Label Y (pixels)
        'LabelSpacing': 10,  # Vertical spacing
        'PrintDetailedLogs': True,  # Print logs in Journal?
        'EnableFileLog': True,  # Create a separate file to log current drawdown values
        'InpFileExtension': _Choice({0: 'Use CSV format (Excel-friendly)', 1: 'Use TXT format (plain text)'}, default=1),  # File extension: CSV or TXT
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

