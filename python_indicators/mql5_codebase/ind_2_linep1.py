"""ind_2_linep1 — converted from MQL5: MQL5 Indicators/Ind_2 Line+1/ind_2_linep1.mq5

Indicator of arbitration situations for the spread, which consists of two instruments.
The main idea is belong to traders leonid553 & Son_Of_Earth
A huge THANK YOU to them for that!!!
 
Holes in the history of the instruments for the current chart filled with previous values. This calculation conception is explained by the assumption that if the exchange of one instrument is not working that the price is frozen. Similar to the rate of the dollar on the Russian exchange.
Copyright: Copyright 2012, Evgeniy Trofimov; Link: https://login.mql5.com/ru/users/EvgeTrofi; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Evgeniy Trofimov', 'link': 'https://login.mql5.com/ru/users/EvgeTrofi', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [65280], 2: [16748574], 3: [255, 13749760]}, 'widths': {1: 2, 2: 2, 3: 1}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Indicator of arbitration situations for the spread, which consists of two instruments.', 'The main idea is belong to traders leonid553 & Son_Of_Earth', 'A huge THANK YOU to them for that!!!', ' ', 'Holes in the history of the instruments for the current chart filled with previous values. This calculation conception is explained by the assumption that if the exchange of one instrument is not working that the price is frozen. Similar to the rate of the dollar on the Russian exchange.'], 'name': 'ind_2_linep1', 'source': 'MQL5 Indicators/Ind_2 Line+1/ind_2_linep1.mq5', 'folder': 'Ind_2 Line+1', 'inputs': [{'mql': 'Symbol1_Name', 'py': 'Symbol1_Name', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'Main instrument', 'sinput': False}, {'mql': 'Symbol1_Reverse', 'py': 'Symbol1_Reverse', 'param': 'Symbol1_Reverse', 'type': 'bool', 'default': False, 'label': 'Reverse correlation', 'sinput': False}, {'mql': 'Symbol2_Name', 'py': 'Symbol2_Name', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'Indirect instrument', 'sinput': False}, {'mql': 'Symbol2_Reverse', 'py': 'Symbol2_Reverse', 'param': 'Symbol2_Reverse', 'type': 'bool', 'default': False, 'label': 'Reverse correlation', 'sinput': False}, {'mql': 'UseVolatility', 'py': 'UseVolatility', 'param': 'UseVolatility', 'type': 'bool', 'default': True, 'label': 'Draw considering volatility', 'sinput': False}, {'mql': 'VOL_Mode', 'py': 'VOL_Mode', 'param': 'VOL_Mode', 'type': 'int', 'default': 3, 'label': 'Mode to calculate the volumes of trade', 'sinput': False}, {'mql': 'VOL_PeriodATR', 'py': 'VOL_PeriodATR', 'param': 'VOL_PeriodATR', 'type': 'int', 'default': 144, 'label': 'ATR averaging period', 'sinput': False}, {'mql': 'MA_Slow', 'py': 'MA_Slow', 'param': 'MA_Slow', 'type': 'int', 'default': 21, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'MA_Fast', 'py': 'MA_Fast', 'param': 'MA_Fast', 'type': 'int', 'default': 8, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 2, 'label': 'method of approximation', 'sinput': False}, {'mql': 'MA_Price', 'py': 'MA_Price', 'param': 'MA_Price', 'type': 'int', 'default': 7, 'label': 'Calculated price', 'sinput': False}, {'mql': 'Label_Color', 'py': 'Label_Color', 'param': None, 'type': 'color', 'default': 8421376, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

ACCOUNT_FREEMARGIN = 0  # MQL5 constant unknown to the converter
MQL5_OPTIMIZATION = 0  # MQL5 constant unknown to the converter
SYMBOL_MARGIN_LONG = 0  # MQL5 constant unknown to the converter
SYMBOL_MARGIN_SHORT = 0  # MQL5 constant unknown to the converter

# enum TYPE_LOT
LOT_FIXED = 0
LOT_RISK = 1
LOT_CURRENCY = 2
_enum('TYPE_LOT', {0: 'LOT_FIXED', 1: 'LOT_RISK', 2: 'LOT_CURRENCY'})

# enum ENUM_VOL_TYPE
VOL_PRICE_OPEN = 1
VOL_VOL_OR_PRICE = 2
VOL_VOL_AND_PRICE = 3
_enum('ENUM_VOL_TYPE', {1: 'VOL_PRICE_OPEN', 2: 'VOL_VOL_OR_PRICE', 3: 'VOL_VOL_AND_PRICE'})

# ---- inputs and global variables
Symbol1_Name = _input('Symbol1_Name', 'EURUSD')  # Main instrument
Symbol1_Reverse = _input('Symbol1_Reverse', False)  # Reverse correlation
Symbol2_Name = _input('Symbol2_Name', 'GBPUSD')  # Indirect instrument
Symbol2_Reverse = _input('Symbol2_Reverse', False)  # Reverse correlation
UseVolatility = _input('UseVolatility', True)  # Draw considering volatility
VOL_Mode = _input('VOL_Mode', 3)  # Mode to calculate the volumes of trade
VOL_PeriodATR = _input('VOL_PeriodATR', 144)  # ATR averaging period
MA_Slow = _input('MA_Slow', 21)  # Slow MA period
MA_Fast = _input('MA_Fast', 8)  # Fast MA period
MA_Method = _input('MA_Method', MODE_SMMA)  # method of approximation
MA_Price = _input('MA_Price', PRICE_WEIGHTED)  # Calculated price
Buf1 = Arr(0, 0.0)  # First instrument
Buf2 = Arr(0, 0.0)  # Second instrument
BufW = Arr(0, 0.0)  # Channel width
BufW_Clr = Arr(0, 0.0)  # Channel color
bufPrice1 = Arr(0, 0.0)
bufPrice2 = Arr(0, 0.0)
curTime = Arr(0, 0)
MAFastSym1 = Arr(0, 0.0)
MAFastSym2 = Arr(0, 0.0)
MASlowSym1 = Arr(0, 0.0)
MASlowSym2 = Arr(0, 0.0)
EMPTY_v = -1
InpSymbol1 = ""  # Instruments names without register
InpSymbol2 = ""  # Instruments names without register
kPrice1 = 0.0  # Weight coefficients of the price charts
kPrice2 = 0.0  # Weight coefficients of the price charts
kVol1 = 0.0  # Balance is changed if the instrument price is changed
kVol2 = 0.0  # Balance is changed if the instrument price is changed
hATR1 = 0  # ATR indicator handle for the instrument 1
hATR2 = 0  # ATR indicator handle for the instrument 2
Label_Name = 'label'
Indic_Name = 'Ind_2 Line+1'
Label_Color = _input('Label_Color', clrTeal)
wndNum = 0  # number of indicator subwindow
wndName = ""  # window name

class CMoneyManagment(MqlObject):
    _q_fields = ()
    def __init__(self, *args):
        pass
    def PrCur(self, inSymbol='', inType=-1):
        if inSymbol == '':
            inSymbol = Symbol()
        tick = MqlTick()
        if not SymbolInfoTick(inSymbol, tick):
            Print('CMoneyManagment::PrCur', ' Failed to get the instrument price ' + inSymbol)
            return -1.0
        if inType == 0:
            return tick.ask
        elif inType == 1:
            return tick.bid
        else:
            return (tick.bid + tick.ask) / 2
        return 0.0
    def Currency_Transfer(self, Value, CurrentCurrency='EUR', NeedCurrency='USD', inType=-1):
        i = 0
        res = Value
        name = ""
        USD = 'USD'
        FndCurrency = ''
        if CurrentCurrency == NeedCurrency:
            return Value
        i = 0
        while i < SymbolsTotal(True):
            name = SymbolName(i, True)
            if SymbolInfoString(name, SYMBOL_CURRENCY_PROFIT) == CurrentCurrency and SymbolInfoString(name, SYMBOL_CURRENCY_BASE) == NeedCurrency:
                res = _fdiv(res, self.PrCur(name, inType))
                return res
            elif SymbolInfoString(name, SYMBOL_CURRENCY_PROFIT) == NeedCurrency and SymbolInfoString(name, SYMBOL_CURRENCY_BASE) == CurrentCurrency:
                res = res * self.PrCur(name, inType)
                return res
            i += 1
        if CurrentCurrency != USD:
            i = 0
            while i < SymbolsTotal(True):
                name = SymbolName(i, True)
                if SymbolInfoString(name, SYMBOL_CURRENCY_PROFIT) == CurrentCurrency and SymbolInfoString(name, SYMBOL_CURRENCY_BASE) == USD:
                    res = _fdiv(res, self.PrCur(name, inType))
                    FndCurrency = USD
                    break
                elif SymbolInfoString(name, SYMBOL_CURRENCY_PROFIT) == USD and SymbolInfoString(name, SYMBOL_CURRENCY_BASE) == CurrentCurrency:
                    res = res * self.PrCur(name, inType)
                    FndCurrency = USD
                    break
                i += 1
            if FndCurrency != USD:
                Print('CMoneyManagment::Currency_Transfer', '  Failed to find the currency pair for calculation ' + CurrentCurrency)
                Print("Necessary to have In 'Market Watch' a currency pair which includes the " + CurrentCurrency + ' and ' + USD + '.')
                return -1.0
        if NeedCurrency == USD:
            return res
        i = 0
        while i < SymbolsTotal(True):
            name = SymbolName(i, True)
            if SymbolInfoString(name, SYMBOL_CURRENCY_PROFIT) == USD and SymbolInfoString(name, SYMBOL_CURRENCY_BASE) == NeedCurrency:
                res = _fdiv(res, self.PrCur(name, inType))
                FndCurrency = NeedCurrency
                break
            elif SymbolInfoString(name, SYMBOL_CURRENCY_PROFIT) == NeedCurrency and SymbolInfoString(name, SYMBOL_CURRENCY_BASE) == USD:
                res = res * self.PrCur(name, inType)
                FndCurrency = NeedCurrency
                break
            i += 1
        if FndCurrency == NeedCurrency:
            return res
        Print('CMoneyManagment::Currency_Transfer', '  Failed to find the currency pair for calculation ' + NeedCurrency)
        Print("Necessary to have In 'Market Watch' a currency pair which includes the " + NeedCurrency + ' и ' + USD + '.')
        return -1.0
    def GetMargin(self, inSymbol='', inType=-1):
        if inSymbol == '':
            inSymbol = Symbol()
        res = 0.0
        if inType == 0:
            res = SymbolInfoDouble(inSymbol, SYMBOL_MARGIN_LONG)
        else:
            res = SymbolInfoDouble(inSymbol, SYMBOL_MARGIN_SHORT)
        res = res * SymbolInfoDouble(inSymbol, SYMBOL_TRADE_CONTRACT_SIZE)
        Mode = SymbolInfoInteger(inSymbol, SYMBOL_TRADE_CALC_MODE)
        _sw1 = Mode
        if _sw1 == SYMBOL_CALC_MODE_FOREX:
            res = self.Currency_Transfer(res, SymbolInfoString(inSymbol, SYMBOL_CURRENCY_MARGIN), AccountInfoString(ACCOUNT_CURRENCY), inType)
            return _fdiv(res, AccountInfoInteger(ACCOUNT_LEVERAGE))
        elif _sw1 == SYMBOL_CALC_MODE_FUTURES:
            Print('CMoneyManagment::GetMargin', ' The FUTURES method of margin calculation has not been studied!')
            return -1.0
        elif _sw1 == SYMBOL_CALC_MODE_CFD:
            res = self.Currency_Transfer(res, SymbolInfoString(inSymbol, SYMBOL_CURRENCY_MARGIN), AccountInfoString(ACCOUNT_CURRENCY), inType)
            return res * self.PrCur(inSymbol, inType)
        else:
            Print('CMoneyManagment::GetMargin', ' the ', StringSubstr(EnumToString(Mode, 'ENUM_SYMBOL_CALC_MODE'), 17), ' method of margin calculation has not been studied!')
            return -1.0
        return res
    def TickValue(self, inSymbol='', inType=-1):
        res = 0.0
        if inSymbol == '':
            inSymbol = Symbol()
        Mode = SymbolInfoInteger(inSymbol, SYMBOL_TRADE_CALC_MODE)
        _sw2 = Mode
        if _sw2 == SYMBOL_CALC_MODE_FOREX:
            res = SymbolInfoDouble(inSymbol, SYMBOL_TRADE_TICK_VALUE)
            return res
        elif _sw2 == SYMBOL_CALC_MODE_FUTURES:
            Print('CMoneyManagment::TickValue', ' The FUTURES method of profit calculation has not been studied!')
            return -1.0
        elif _sw2 == SYMBOL_CALC_MODE_CFD:
            res = SymbolInfoDouble(inSymbol, SYMBOL_TRADE_TICK_VALUE) * SymbolInfoDouble(inSymbol, SYMBOL_TRADE_TICK_SIZE) * SymbolInfoDouble(inSymbol, SYMBOL_TRADE_CONTRACT_SIZE) * AccountInfoInteger(ACCOUNT_LEVERAGE)
            res = self.Currency_Transfer(res, SymbolInfoString(inSymbol, SYMBOL_CURRENCY_PROFIT), AccountInfoString(ACCOUNT_CURRENCY), inType)
            return res
        else:
            Print('CMoneyManagment::TickValue', ' the ', StringSubstr(EnumToString(Mode, 'ENUM_SYMBOL_CALC_MODE'), 17), ' method of profit calculation has not been studied!')
            return -1.0
        return res
    def Lot(self, inValue, inTypeLot=0, inSymbol='', inType=-1):
        if inSymbol == '':
            inSymbol = Symbol()
        res = inValue
        calc_margin = 0.0
        if inTypeLot > 0:
            calc_margin = self.GetMargin(inSymbol, inType)
            if calc_margin <= 0:
                Print('CMoneyManagment::Lot', ' Failed to calculate margin!')
                return -1.0
            if inTypeLot == LOT_RISK:
                res = _fdiv(AccountInfoDouble(ACCOUNT_EQUITY) * res, calc_margin) / 100
            if inTypeLot == LOT_CURRENCY:
                res = _fdiv(res, calc_margin)
        return self.LotNormalize(res, inSymbol, inType)
    def LotNormalize(self, inValue, inSymbol='', inType=-1):
        if inSymbol == '':
            inSymbol = Symbol()
        free_margin = AccountInfoDouble(ACCOUNT_FREEMARGIN)
        calc_margin = self.GetMargin(inSymbol, inType)
        if calc_margin <= 0:
            return -1.0
        res = inValue
        if free_margin < (calc_margin * res):
            if (calc_margin * res) > (0.5 * AccountInfoDouble(ACCOUNT_EQUITY)):
                Alert('You are trying to make a deal, the deposit on which exceeds the size of funds more than 50%!!!')
                return -1.0
            res = _fdiv(free_margin * 0.9, calc_margin)
            Print('CMoneyManagment::LotNormalize', ' The lot value is adjusted: ', DoubleToString(inValue, 2), ' -> ', DoubleToString(res, 2))
        res = MathMax(res, SymbolInfoDouble(inSymbol, SYMBOL_VOLUME_MIN))
        res = MathMin(res, SymbolInfoDouble(inSymbol, SYMBOL_VOLUME_MAX))
        lot_step = SymbolInfoDouble(inSymbol, SYMBOL_VOLUME_STEP)
        norm = _int(MathRound(NormalizeDouble(MathCeil(MathAbs(_fdiv(MathLog(lot_step), MathLog(10.0)))), 0)))
        return NormalizeDouble(res, norm)
    def LotSL(self, inValue, inSL, inTypeLot=0, inSymbol='', inType=-1):
        if inSymbol == '':
            inSymbol = Symbol()
        res = inValue
        calc_tv = 0.0
        if inTypeLot > 0:
            if inSL <= 0:
                Print('CMoneyManagment::LotSL', ' It is really necessary set the Stop Loss boundary to calculate the lot')
                return -1.0
            calc_tv = self.TickValue(inSymbol, inType) * inSL
            if calc_tv <= 0:
                Print('CMoneyManagment::LotSL', ' Failed to calculate price of point!')
                return -1.0
            if inTypeLot == LOT_RISK:
                res = _fdiv(AccountInfoDouble(ACCOUNT_EQUITY) * res, calc_tv) / 100
            if inTypeLot == LOT_CURRENCY:
                res = _fdiv(res, calc_tv)
        return self.LotNormalize(res, inSymbol, inType)
    def GetCurrentLot(self, inSymbol='', inMagic=0):
        if inSymbol == '':
            inSymbol = Symbol()
        if not PositionSelect(inSymbol):
            return 0.0
        t = 0
        lot = 0.0
        trend = 0
        HistorySelectByPosition(PositionGetInteger(POSITION_IDENTIFIER))
        i = 0
        while i < HistoryDealsTotal():
            t = HistoryDealGetTicket(i)
            if inMagic > 0:
                if HistoryDealGetInteger(t, DEAL_MAGIC) != inMagic:
                    i += 1
                    continue
            trend = HistoryDealGetInteger(t, DEAL_TYPE)
            if trend == DEAL_TYPE_BUY:
                lot = lot + HistoryDealGetDouble(t, DEAL_VOLUME)
            elif trend == DEAL_TYPE_SELL:
                lot = lot - HistoryDealGetDouble(t, DEAL_VOLUME)
            i += 1
        return lot
    def GetCurrentProfit(self, inSymbol='', inMagic=0):
        return 0.0
    def LotIsKiller(self, inLot, inSymbol, inType):
        if not PositionSelect(inSymbol):
            return False
        if PositionGetInteger(POSITION_TYPE) == inType:
            return False
        if PositionGetDouble(POSITION_VOLUME) == inLot:
            return True
        return False

def OnInit():
    global InpSymbol1, InpSymbol2, hATR1, hATR2, kVol1, kVol2
    MM = CMoneyManagment()
    InpSymbol1 = StringUpper(Symbol1_Name)
    InpSymbol2 = StringUpper(Symbol2_Name)
    if SymbolInfoDouble(InpSymbol1, SYMBOL_TRADE_TICK_SIZE) == 0:
        Print('The zero TICK_SIZE value for the instrument ', InpSymbol1, '. Perhaps the instrument is specified incorrectly!')
        return -1
    kVol1 = _fdiv(MM.TickValue(InpSymbol1), SymbolInfoDouble(InpSymbol1, SYMBOL_TRADE_TICK_SIZE))
    if SymbolInfoDouble(InpSymbol2, SYMBOL_TRADE_TICK_SIZE) == 0:
        Print('The zero TICK_SIZE value for the instrument ', InpSymbol2, '. Perhaps the instrument is specified incorrectly!')
        return -1
    kVol2 = _fdiv(MM.TickValue(InpSymbol2), SymbolInfoDouble(InpSymbol2, SYMBOL_TRADE_TICK_SIZE))
    SetIndexBuffer(0, Buf1, INDICATOR_DATA)
    SetIndexBuffer(1, Buf2, INDICATOR_DATA)
    SetIndexBuffer(2, BufW, INDICATOR_DATA)
    SetIndexBuffer(3, BufW_Clr, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, bufPrice1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, bufPrice2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, MAFastSym1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, MAFastSym2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, MASlowSym1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, MASlowSym2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, Indic_Name)
    PlotIndexSetString(0, PLOT_LABEL, InpSymbol1)
    PlotIndexSetString(1, PLOT_LABEL, InpSymbol2)
    PlotIndexSetString(2, PLOT_LABEL, 'Width')
    hATR1 = iATR(InpSymbol1, Period(), VOL_PeriodATR)
    hATR2 = iATR(InpSymbol2, Period(), VOL_PeriodATR)
    return 0

def OnDeinit(reason):
    DeleteObject(InpSymbol1)
    DeleteObject(InpSymbol2)
    DeleteObject(Label_Name)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global kPrice1, kPrice2, wndName, wndNum
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if CopyTime(Symbol(), Period(), 0, to_copy, curTime) <= 0:
        Print('Getting Time ' + Symbol() + ' is failed! Error ', GetLastError())
        return 0
    if False:
        return 0
    i = ArraySize(curTime) - 1
    if CopyRates(InpSymbol1, Period(), _DT(curTime[0]), _DT(curTime[i]), tmpSymbol1) <= 0:
        Print('Getting Rates ' + InpSymbol1 + ' is failed! Error ', GetLastError())
        return 0
    if False:
        return 0
    if CopyRates(InpSymbol2, Period(), _DT(curTime[0]), _DT(curTime[i]), tmpSymbol2) <= 0:
        Print('Getting Rates ' + InpSymbol2 + ' is failed! Error ', GetLastError())
        return 0
    if False:
        return 0
    ATR1 = Arr(0, 0.0)
    ATR2 = Arr(0, 0.0)
    if CopyBuffer(hATR1, 0, 1, 1, ATR1) <= 0:
        Print('Failed to load the ATR indicator for the symbol ' + InpSymbol1)
        return 0
    if False:
        return 0
    if CopyBuffer(hATR2, 0, 1, 1, ATR2) <= 0:
        Print('Failed to load the ATR indicator for the symbol ' + InpSymbol2)
        return 0
    if False:
        return 0
    limit = 0
    j = 0
    k = 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    j = limit
    k = limit
    i = limit
    for i in range(i, rates_total):
        if j >= ArraySize(tmpSymbol1):
            break
        while (curTime[i] > tmpSymbol1[j].time and True) and j < (ArraySize(tmpSymbol1) - 1):
            j += 1
        if k >= ArraySize(tmpSymbol2):
            break
        while (curTime[i] > tmpSymbol2[k].time and True) and k < (ArraySize(tmpSymbol2) - 1):
            k += 1
        if curTime[i] < tmpSymbol1[j].time:
            if i > 0:
                bufPrice1[i] = bufPrice1[i - 1]
            else:
                bufPrice1[i] = 0.0
        else:
            bufPrice1[i] = CalcPrice(MA_Price, tmpSymbol1[j].open, tmpSymbol1[j].close, tmpSymbol1[j].high, tmpSymbol1[j].low)
        if curTime[i] < tmpSymbol2[k].time:
            if i > 0:
                bufPrice2[i] = bufPrice2[i - 1]
            else:
                bufPrice2[i] = 0.0
        else:
            bufPrice2[i] = CalcPrice(MA_Price, tmpSymbol2[k].open, tmpSymbol2[k].close, tmpSymbol2[k].high, tmpSymbol2[k].low)
    else:
        i = _range_end(i, rates_total, 1)
    j = ArraySize(tmpSymbol1) - 1
    k = ArraySize(tmpSymbol2) - 1
    bufPrice1[rates_total - 1] = CalcPrice(MA_Price, tmpSymbol1[j].open, tmpSymbol1[j].close, tmpSymbol1[j].high, tmpSymbol1[j].low)
    bufPrice2[rates_total - 1] = CalcPrice(MA_Price, tmpSymbol2[k].open, tmpSymbol2[k].close, tmpSymbol2[k].high, tmpSymbol2[k].low)
    wndNum = ChartWindowFind(0, Indic_Name)
    wndName = Indic_Name + IntegerToString(wndNum)
    kPrice1 = 100.0
    kPrice2 = _fdiv(kPrice1, tmpSymbol2[k].open) * tmpSymbol1[j].open
    kP1 = 1
    kP2 = 1
    if Symbol1_Reverse:
        kP1 = -1
    if Symbol2_Reverse:
        kP2 = -1
    kPrice1 = kP1 * kPrice1
    kPrice2 = kP2 * kPrice2
    volA1 = 1.0
    volA2 = EMPTY_v
    volP1 = 1.0
    volP2 = EMPTY_v
    var1 = 0.0
    if (kVol2 == 0 or ATR2[0] == 0) or tmpSymbol2[k].open == 0:
        return 0
    if ((VOL_Mode == VOL_VOL_OR_PRICE or VOL_Mode == VOL_VOL_AND_PRICE) and Bars(InpSymbol1, Period()) > VOL_PeriodATR) and Bars(InpSymbol2, Period()) > VOL_PeriodATR:
        var1 = volA1 * kVol1 * ATR1[0]
        volA2 = _fdiv(_fdiv(var1, kVol2), ATR2[0])
    if (VOL_Mode == VOL_PRICE_OPEN or VOL_Mode == VOL_VOL_AND_PRICE) or volA2 == EMPTY_v:
        var1 = volP1 * kVol1 * tmpSymbol1[j].open
        volP2 = _fdiv(_fdiv(var1, kVol2), tmpSymbol2[k].open)
    if False:
        return 0
    AverageOnArray(MA_Method, rates_total, prev_calculated, 0, MA_Fast, bufPrice1, MAFastSym1, _GlobRef(globals(), '_s_OnCalculate_weightfast1'))
    AverageOnArray(MA_Method, rates_total, prev_calculated, 0, MA_Slow, bufPrice1, MASlowSym1, _GlobRef(globals(), '_s_OnCalculate_weightslow1'))
    AverageOnArray(MA_Method, rates_total, prev_calculated, 0, MA_Fast, bufPrice2, MAFastSym2, _GlobRef(globals(), '_s_OnCalculate_weightfast2'))
    AverageOnArray(MA_Method, rates_total, prev_calculated, 0, MA_Slow, bufPrice2, MASlowSym2, _GlobRef(globals(), '_s_OnCalculate_weightslow2'))
    i = limit
    for i in range(i, rates_total):
        Buf1[i] = kPrice1 * (MAFastSym1[i] - MASlowSym1[i])
        if not UseVolatility:
            Buf2[i] = kPrice2 * (MAFastSym2[i] - MASlowSym2[i])
        elif volA2 != EMPTY_v:
            Buf2[i] = kPrice2 * volA2 * (MAFastSym2[i] - MASlowSym2[i])
        BufW[i] = Buf1[i] - Buf2[i]
        if i > 0:
            if MathAbs(BufW[i]) > MathAbs(BufW[i - 1]):
                BufW_Clr[i] = 1.0
            else:
                BufW_Clr[i] = 0.0
    else:
        i = _range_end(i, rates_total, 1)
    if MQL5InfoInteger(MQL5_OPTIMIZATION):
        return rates_total
    i = rates_total - 1
    sVolA1 = ''
    sVolA2 = ''
    sVolP1 = ''
    sVolP2 = ''
    if volP2 != EMPTY_v:
        sVolP1 = DoubleToString(volP1, 2) + '= '
        sVolP2 = DoubleToString(volP2, 2) + '= '
    if volA2 != EMPTY_v:
        sVolA1 = ' =' + DoubleToString(volA1, 2)
        sVolA2 = ' =' + DoubleToString(volA2, 2)
    DrawLabel(InpSymbol1, sVolP1 + InpSymbol1 + sVolA1, 10, PlotIndexGetInteger(0, PLOT_LINE_COLOR), 5)
    DrawLabel(InpSymbol2, sVolP2 + InpSymbol2 + sVolA2, 10, PlotIndexGetInteger(1, PLOT_LINE_COLOR), 18)
    label = ""
    if MathAbs(BufW[i - 2]) > MathAbs(BufW[i - 1]) and MathAbs(BufW[i - 3]) > MathAbs(BufW[i - 2]):
        label = 'Convergence'
    elif MathAbs(BufW[i - 2]) < MathAbs(BufW[i - 1]) and MathAbs(BufW[i - 3]) < MathAbs(BufW[i - 2]):
        label = 'Divergence'
    else:
        label = 'Flat'
    DrawLabel(Label_Name, label, 9, Label_Color, 31)
    return rates_total

def StringUpper(s):
    s = Box(s)
    i = 0
    k = StringLen(s.v)
    c = 0
    n = 0
    i = 0
    for i in range(i, k):
        n = 0
        c = StringGetCharacter(s.v, i)
        if c > 96 and c < 123:
            n = c - 32
        if c > 223 and c < 256:
            n = c - 32
        if c == 184:
            n = 168
        if n > 0:
            StringSetCharacter(s, i, n)
    else:
        i = _range_end(i, k, 1)
    return s.v

def CalcPrice(inType, inOpen=0.0, inClose=0.0, inHigh=0.0, inLow=0.0):
    _sw3 = inType
    if _sw3 == PRICE_CLOSE:
        return inClose
    elif _sw3 == PRICE_HIGH:
        return inHigh
    elif _sw3 == PRICE_OPEN:
        return inOpen
    elif _sw3 == PRICE_LOW:
        return inLow
    elif _sw3 == PRICE_MEDIAN:
        return (inHigh + inLow) / 2
    elif _sw3 == PRICE_TYPICAL:
        return (inHigh + inLow + inClose) / 3
    elif _sw3 == PRICE_WEIGHTED:
        return (inHigh + inLow + inOpen + inClose) / 4
    else:
        return 0.0

def DrawLabel(aName, aText, aFontSize, aColor, aValue):
    objName = aName + wndName
    if ObjectFind(0, objName) < 0:
        ObjectCreate(0, objName, OBJ_LABEL, wndNum, 0, 0)
        ObjectSetString(0, objName, OBJPROP_FONT, 'Verdana')
        ObjectSetInteger(0, objName, OBJPROP_CORNER, CORNER_RIGHT_UPPER)
        ObjectSetInteger(0, objName, OBJPROP_XDISTANCE, 150)
    ObjectSetString(0, objName, OBJPROP_TEXT, aText)
    ObjectSetInteger(0, objName, OBJPROP_FONTSIZE, aFontSize)
    ObjectSetInteger(0, objName, OBJPROP_COLOR, aColor)
    ObjectSetInteger(0, objName, OBJPROP_YDISTANCE, aValue)

def DeleteObject(name):
    ObjectDelete(0, name + wndName)

def AverageOnArray(mode, rates_total, prev_calculated, begin, period, source, destination, weightsum):
    _sw4 = mode
    if _sw4 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, begin, period, source, destination)
    elif _sw4 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, begin, period, source, destination)
    elif _sw4 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, begin, period, source, destination, weightsum)
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, begin, period, source, destination)

# ---- global variables initialised from expressions
tmpSymbol1 = Arr(0, 0, factory=MqlRates)
tmpSymbol2 = Arr(0, 0, factory=MqlRates)

# ---- static local variables
_s_OnCalculate_weightfast1 = 0
_s_OnCalculate_weightfast2 = 0
_s_OnCalculate_weightslow1 = 0
_s_OnCalculate_weightslow2 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind2Linep1(_MQL5Indicator):
    name = 'ind_2_linep1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Symbol1_Reverse': False,  # Reverse correlation
        'Symbol2_Reverse': False,  # Reverse correlation
        'UseVolatility': True,  # Draw considering volatility
        'VOL_Mode': _Choice({1: 'by open prices', 2: 'by volatility, and if it is impossible - by open prices', 3: 'by volatility (if it is possible) and open prices'}, default=3),  # Mode to calculate the volumes of trade
        'VOL_PeriodATR': 144,  # ATR averaging period
        'MA_Slow': 21,  # Slow MA period
        'MA_Fast': 8,  # Fast MA period
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # method of approximation
        'MA_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),  # Calculated price
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

