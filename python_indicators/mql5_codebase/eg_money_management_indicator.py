"""EG-Money-Management-Indicator — converted from MQL5: MQL5 Indicators/Position Size Calculator/EG-Money-Management-Indicator.mq5

Copyright: Copyright 2021, ErangaG; Link: http://www.simply.trade; Version: 21.11

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, ErangaG', 'link': 'http://www.simply.trade', 'version': '21.11', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 0, 2: 0, 3: 0}, 'colors': {1: [4294967295], 2: [4294967295], 3: [4294967295]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'EG-Money-Management-Indicator', 'source': 'MQL5 Indicators/Position Size Calculator/EG-Money-Management-Indicator.mq5', 'folder': 'Position Size Calculator', 'inputs': [{'mql': 'iRisk_AvailableCapital', 'py': 'iRisk_AvailableCapital', 'param': 'iRisk_AvailableCapital', 'type': 'int', 'default': 4, 'label': 'Capital calculation mechanism', 'sinput': False}, {'mql': 'iRisk_FractionOfCapital', 'py': 'iRisk_FractionOfCapital', 'param': 'iRisk_FractionOfCapital', 'type': 'double', 'default': 0.01, 'label': 'Risk fraction of the capital ,ex: 0.01 = 1%', 'sinput': False}, {'mql': 'iRisk_RiskMode', 'py': 'iRisk_RiskMode', 'param': 'iRisk_RiskMode', 'type': 'int', 'default': 3, 'label': 'Stop-Loss points calculation mechanism', 'sinput': False}, {'mql': 'iCommon_ATRLength', 'py': 'iCommon_ATRLength', 'param': 'iCommon_ATRLength', 'type': 'int', 'default': 14, 'label': 'ATR length for ATR based Stop-Loss', 'sinput': False}, {'mql': 'iCommon_ATRMultiplier', 'py': 'iCommon_ATRMultiplier', 'param': 'iCommon_ATRMultiplier', 'type': 'double', 'default': 1.5, 'label': 'ATR value multiplier', 'sinput': False}, {'mql': 'iCommon_FixedStoplossPoints', 'py': 'iCommon_FixedStoplossPoints', 'param': 'iCommon_FixedStoplossPoints', 'type': 'int', 'default': 1000, 'label': 'Fixed size Stop-Loss point count', 'sinput': False}, {'mql': 'iCommon_CurrencyPairAppendix', 'py': 'iCommon_CurrencyPairAppendix', 'param': None, 'type': 'string', 'default': '', 'label': 'Currency Pair Appendix', 'sinput': False}, {'mql': 'iCommon_ColorParameters', 'py': 'iCommon_ColorParameters', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Colour for Parameters', 'sinput': False}, {'mql': 'iCommon_ColorLotsize', 'py': 'iCommon_ColorLotsize', 'param': None, 'type': 'color', 'default': 16760576, 'label': 'Colour for calculaed Lots', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum EMyCapitalCalculation
FREEMARGIN = 2
BALANCE = 4
EQUITY = 8
_enum('EMyCapitalCalculation', {2: 'FREEMARGIN', 4: 'BALANCE', 8: 'EQUITY'})

# enum EMyRiskCalculation
ATR_POINTS = 3
FIXED_POINTS = 9
_enum('EMyRiskCalculation', {3: 'ATR_POINTS', 9: 'FIXED_POINTS'})

# ---- inputs and global variables
iRisk_AvailableCapital = _input('iRisk_AvailableCapital', BALANCE)  # Capital calculation mechanism
iRisk_FractionOfCapital = _input('iRisk_FractionOfCapital', 0.01)  # Risk fraction of the capital ,ex: 0.01 = 1%
iRisk_RiskMode = _input('iRisk_RiskMode', ATR_POINTS)  # Stop-Loss points calculation mechanism
iCommon_ATRLength = _input('iCommon_ATRLength', 14)  # ATR length for ATR based Stop-Loss
iCommon_ATRMultiplier = _input('iCommon_ATRMultiplier', 1.5)  # ATR value multiplier
iCommon_FixedStoplossPoints = _input('iCommon_FixedStoplossPoints', 1000)  # Fixed size Stop-Loss point count
iCommon_CurrencyPairAppendix = _input('iCommon_CurrencyPairAppendix', '')  # Currency Pair Appendix
iCommon_ColorParameters = _input('iCommon_ColorParameters', clrOrange)  # Colour for Parameters
iCommon_ColorLotsize = _input('iCommon_ColorLotsize', clrDeepSkyBlue)  # Colour for calculaed Lots
mDisplay_Corner = CORNER_LEFT_LOWER
mMaxPeriod = 0
mHandleATR = 0
mBuffer_lotsize = Arr(0, 0.0)
mBuffer_stoplossPoints = Arr(0, 0.0)
mBuffer_atrPoints = Arr(0, 0.0)
mBuffer_atr = Arr(0, 0.0)

class CMyToolkit(MqlObject):
    _q_fields = ()
    def __init__(self, *args):
        pass
    def _Name(self):
        pass
    @staticmethod
    def NormalizeLots(pSymbol, pLots):
        uvolumeStep = SymbolInfoDouble(pSymbol, SYMBOL_VOLUME_STEP)
        ulots = MathRound(_fdiv(pLots, uvolumeStep)) * uvolumeStep
        return ulots
    @staticmethod
    def ToPointDecimal(pSymbol, pPointsCount):
        udigits = _int(SymbolInfoInteger(pSymbol, SYMBOL_DIGITS))
        upointDecimal = SymbolInfoDouble(pSymbol, SYMBOL_POINT)
        return NormalizeDouble(upointDecimal * pPointsCount, udigits)
    @staticmethod
    def ToPointsCount(pSymbol, pDecimalValue):
        upointDecimal = SymbolInfoDouble(pSymbol, SYMBOL_POINT)
        return _int(_fdiv(1, upointDecimal) * pDecimalValue)
    @staticmethod
    def ToTicksCount(pSymbol, pPointsCount):
        uticksize = SymbolInfoDouble(pSymbol, SYMBOL_TRADE_TICK_SIZE)
        utickscount = _int(_fdiv(pPointsCount, uticksize) * uticksize)
        return utickscount
    @staticmethod
    def _CurrencyMultiplicator(pCurrencyPairAppendix=''):
        _multiplicator = 1.0
        xCurrency = Box(AccountInfoString(ACCOUNT_CURRENCY))
        StringToUpper(xCurrency)
        if xCurrency.v == 'USD':
            return _multiplicator
        if xCurrency.v == 'EUR':
            _multiplicator = _fdiv(1.0, SymbolInfoDouble('EURUSD' + pCurrencyPairAppendix, SYMBOL_BID))
        if xCurrency.v == 'GBP':
            _multiplicator = _fdiv(1.0, SymbolInfoDouble('GBPUSD' + pCurrencyPairAppendix, SYMBOL_BID))
        if xCurrency.v == 'AUD':
            _multiplicator = _fdiv(1.0, SymbolInfoDouble('AUDUSD' + pCurrencyPairAppendix, SYMBOL_BID))
        if xCurrency.v == 'NZD':
            _multiplicator = _fdiv(1.0, SymbolInfoDouble('NZDUSD' + pCurrencyPairAppendix, SYMBOL_BID))
        if xCurrency.v == 'CHF':
            _multiplicator = SymbolInfoDouble('USDCHF' + pCurrencyPairAppendix, SYMBOL_BID)
        if xCurrency.v == 'JPY':
            _multiplicator = SymbolInfoDouble('USDJPY' + pCurrencyPairAppendix, SYMBOL_BID)
        if xCurrency.v == 'CAD':
            _multiplicator = SymbolInfoDouble('USDCAD' + pCurrencyPairAppendix, SYMBOL_BID)
        if _multiplicator == 0:
            _multiplicator = 1.0
        return _multiplicator
    @staticmethod
    def CalculateLotSize(pSymbol, pMoneyCapital, pRiskDecimal, pStoplossPoints, pExtraPriceGapPoints, pAllowedMaxLotSize, pCurrencyPairAppendix=''):
        _moneyRisk = 0.0
        _lotsByRequiredMargin = 0.0
        _lotsByRisk = 0.0
        _lotSize = 0.0
        _lotdigit = 2
        _totalSLPoints = 0
        _totalTickCount = 0
        _marginForOneLot = 0.0
        if OrderCalcMargin(ORDER_TYPE_BUY, pSymbol, 1, SymbolInfoDouble(pSymbol, SYMBOL_ASK), _marginForOneLot):
            _lotsByRequiredMargin = _fdiv(pMoneyCapital * 0.98, _marginForOneLot)
            _lotsByRequiredMargin = MathMin(_lotsByRequiredMargin, MathMin(pAllowedMaxLotSize, SymbolInfoDouble(pSymbol, SYMBOL_VOLUME_MAX)))
            _lotsByRequiredMargin = CMyToolkit.NormalizeLots(pSymbol, _lotsByRequiredMargin)
        else:
            _lotsByRequiredMargin = SymbolInfoDouble(pSymbol, SYMBOL_VOLUME_MAX)
        _lotStep = SymbolInfoDouble(pSymbol, SYMBOL_VOLUME_STEP)
        _oneTickValue = SymbolInfoDouble(pSymbol, SYMBOL_TRADE_TICK_VALUE)
        if _lotStep == 1:
            _lotdigit = 0
        if _lotStep == 0.1:
            _lotdigit = 1
        if _lotStep == 0.01:
            _lotdigit = 2
        _moneyRisk = pRiskDecimal * pMoneyCapital
        _totalSLPoints = pStoplossPoints + pExtraPriceGapPoints
        _totalTickCount = CMyToolkit.ToTicksCount(pSymbol, _totalSLPoints)
        _lotsByRisk = _fdiv(_moneyRisk, _totalTickCount * _oneTickValue)
        _lotsByRisk = _lotsByRisk * CMyToolkit._CurrencyMultiplicator(pCurrencyPairAppendix)
        _lotsByRisk = CMyToolkit.NormalizeLots(pSymbol, _lotsByRisk)
        _lotSize = MathMax(MathMin(_lotsByRisk, _lotsByRequiredMargin), SymbolInfoDouble(pSymbol, SYMBOL_VOLUME_MIN))
        _lotSize = NormalizeDouble(_lotSize, _lotdigit)
        return _lotSize
    @staticmethod
    def DisplayText(objname, objtext, clr, x, y, corner):
        if ObjectFind(ChartID(), objname) == -1:
            ObjectCreate(ChartID(), objname, OBJ_LABEL, 0, 0, 0)
            ObjectSetInteger(ChartID(), objname, OBJPROP_CORNER, corner)
            ObjectSetInteger(ChartID(), objname, OBJPROP_XDISTANCE, x)
            ObjectSetInteger(ChartID(), objname, OBJPROP_YDISTANCE, y)
            ObjectSetInteger(ChartID(), objname, OBJPROP_FONTSIZE, 13)
            ObjectSetString(ChartID(), objname, OBJPROP_FONT, 'Arial')
        ObjectSetString(ChartID(), objname, OBJPROP_TEXT, objtext)
        ObjectSetInteger(ChartID(), objname, OBJPROP_COLOR, clr)

def myIndicatorCreate():
    global mHandleATR
    mHandleATR = iATR(None, PERIOD_CURRENT, iCommon_ATRLength)
    if mHandleATR == INVALID_HANDLE:
        return False
    return True

def myIndicatorRelease():
    if mHandleATR != INVALID_HANDLE:
        IndicatorRelease(mHandleATR)

def OnInit():
    global mMaxPeriod
    SetIndexBuffer(0, mBuffer_lotsize, INDICATOR_DATA)
    SetIndexBuffer(1, mBuffer_stoplossPoints, INDICATOR_DATA)
    SetIndexBuffer(2, mBuffer_atrPoints, INDICATOR_DATA)
    SetIndexBuffer(3, mBuffer_atr, INDICATOR_CALCULATIONS)
    PlotIndexSetString(0, PLOT_LABEL, 'EG_Lots')
    PlotIndexSetString(1, PLOT_LABEL, 'EG_Stoploss_Points')
    PlotIndexSetString(2, PLOT_LABEL, 'EG_ATR_Points')
    mMaxPeriod = iCommon_ATRLength
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, mMaxPeriod)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, mMaxPeriod)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, mMaxPeriod)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetString(INDICATOR_SHORTNAME, MQLInfoString(MQL_PROGRAM_NAME))
    str_ = Box("")
    if myIndicatorCreate() == False:
        StringConcatenate(str_, 'Failed to create indicator handle(s) , Error: ', GetLastError())
        MessageBox(str_.v, 'Error')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(ChartID(), '@MM-ATR')
    ObjectDelete(ChartID(), '@MM-LotText')
    ObjectDelete(ChartID(), '@MM-LotSize')
    myIndicatorRelease()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if False:
        return 0
    if rates_total < mMaxPeriod:
        return 0
    if BarsCalculated(mHandleATR) < rates_total:
        return 0
    startBar = 0
    copyLength = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        copyLength = rates_total
        startBar = mMaxPeriod
    else:
        copyLength = rates_total - prev_calculated
        if prev_calculated > 0:
            copyLength += 1
        startBar = prev_calculated - 1
    if CopyBuffer(mHandleATR, 0, 0, copyLength, mBuffer_atr) <= 0:
        return 0
    availableMoney = 0.0
    lotsize = 0.0
    atrPoints = 0
    slPoints = 0
    extraPoints = 0
    str_ = Box("")
    _sw1 = iRisk_AvailableCapital
    if _sw1 == FREEMARGIN:
        availableMoney = AccountInfoDouble(ACCOUNT_MARGIN_FREE)
    elif _sw1 == BALANCE:
        availableMoney = AccountInfoDouble(ACCOUNT_BALANCE)
    elif _sw1 == EQUITY:
        availableMoney = AccountInfoDouble(ACCOUNT_EQUITY)
    else:
        availableMoney = AccountInfoDouble(ACCOUNT_MARGIN_FREE)
    for i in range(startBar, rates_total):
        atrPoints = _int(mBuffer_atr[i] * MathPow(10, SymbolInfoInteger(None, SYMBOL_DIGITS)))
        slPoints = _int(MathCeil(iCommon_ATRMultiplier * atrPoints))
        if iRisk_RiskMode == FIXED_POINTS:
            slPoints = iCommon_FixedStoplossPoints
        else:
            slPoints = (slPoints if (slPoints > 0) else iCommon_FixedStoplossPoints)
        extraPoints = _int(SymbolInfoInteger(None, SYMBOL_SPREAD))
        lotsize = CMyToolkit.CalculateLotSize("", availableMoney, iRisk_FractionOfCapital, slPoints, 0, SymbolInfoDouble(None, SYMBOL_VOLUME_MAX), iCommon_CurrencyPairAppendix)
        mBuffer_atrPoints[i] = StringToDouble(DoubleToString(atrPoints, 0))
        mBuffer_stoplossPoints[i] = StringToDouble(DoubleToString(slPoints, 0))
        mBuffer_lotsize[i] = StringToDouble(DoubleToString(lotsize, 2))
    if iRisk_RiskMode == ATR_POINTS:
        str_.v = ''
        StringConcatenate(str_, 'ATR (', iCommon_ATRLength, ') : ', mBuffer_atrPoints[rates_total - 1], ' points')
        CMyToolkit.DisplayText('@MM-ATR', str_.v, iCommon_ColorParameters, 30, 110, mDisplay_Corner)
    str_.v = ''
    StringConcatenate(str_, 'Risk : ', DoubleToString(iRisk_FractionOfCapital * 100, 2), '% , Stop-Loss : ', mBuffer_stoplossPoints[rates_total - 1], ' points')
    CMyToolkit.DisplayText('@MM-LotText', str_.v, iCommon_ColorParameters, 30, 80, mDisplay_Corner)
    str_.v = ''
    StringConcatenate(str_, 'Lots : ', mBuffer_lotsize[rates_total - 1])
    CMyToolkit.DisplayText('@MM-LotSize', str_.v, iCommon_ColorLotsize, 30, 50, mDisplay_Corner)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EGMoneyManagementIndicator(_MQL5Indicator):
    name = 'EG-Money-Management-Indicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iRisk_AvailableCapital': _Choice({2: 'FREEMARGIN', 4: 'BALANCE', 8: 'EQUITY'}, default=4),  # Capital calculation mechanism
        'iRisk_FractionOfCapital': 0.01,  # Risk fraction of the capital ,ex: 0.01 = 1%
        'iRisk_RiskMode': _Choice({3: 'ATR_POINTS', 9: 'FIXED_POINTS'}, default=3),  # Stop-Loss points calculation mechanism
        'iCommon_ATRLength': 14,  # ATR length for ATR based Stop-Loss
        'iCommon_ATRMultiplier': 1.5,  # ATR value multiplier
        'iCommon_FixedStoplossPoints': 1000,  # Fixed size Stop-Loss point count
    }

