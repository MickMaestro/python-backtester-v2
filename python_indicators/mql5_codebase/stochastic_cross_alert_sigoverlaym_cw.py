"""stochastic_cross_alert_sigoverlaym_cw — converted from MQL5: MQL5 Indicators/Stochastic_Cross_Alert_SigOverlayM_cw/stochastic_cross_alert_sigoverlaym_cw.mq5

Copyright: Copyright © 2006, Robert Hill; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Robert Hill', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Sell', 2: 'Buy'}, 'levels': [], 'description': [], 'name': 'stochastic_cross_alert_sigoverlaym_cw', 'source': 'MQL5 Indicators/Stochastic_Cross_Alert_SigOverlayM_cw/stochastic_cross_alert_sigoverlaym_cw.mq5', 'folder': 'Stochastic_Cross_Alert_SigOverlayM_cw', 'inputs': [{'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EmailON', 'py': 'EmailON', 'param': 'EmailON', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'OverBoughtLevel', 'py': 'OverBoughtLevel', 'param': 'OverBoughtLevel', 'type': 'int', 'default': 80, 'label': '', 'sinput': False}, {'mql': 'OverSoldLevel', 'py': 'OverSoldLevel', 'param': 'OverSoldLevel', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'show_KD_cross', 'py': 'show_KD_cross', 'param': 'show_KD_cross', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'show_K_OBOScross', 'py': 'show_K_OBOScross', 'param': 'show_K_OBOScross', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'show_D_OBOScross', 'py': 'show_D_OBOScross', 'param': 'show_D_OBOScross', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SoundON = _input('SoundON', False)
EmailON = _input('EmailON', False)
KPeriod = _input('KPeriod', 5)
DPeriod = _input('DPeriod', 3)
Slowing = _input('Slowing', 3)
MA_Method = _input('MA_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
OverBoughtLevel = _input('OverBoughtLevel', 80)
OverSoldLevel = _input('OverSoldLevel', 20)
show_KD_cross = _input('show_KD_cross', False)
show_K_OBOScross = _input('show_K_OBOScross', True)
show_D_OBOScross = _input('show_D_OBOScross', False)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
StartBars = 0
STO_Handle = 0
flagval1_ = False
flagval2_ = False

def OnInit():
    global STO_Handle, StartBars
    StartBars = KPeriod + DPeriod
    if StartBars < 9:
        StartBars = 9
    STO_Handle = iStochastic(None, 0, KPeriod, DPeriod, Slowing, MA_Method, Price_field)
    if STO_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic1 indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Stochastic_Cross_Alert'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global flagval1_, flagval2_
    if BarsCalculated(STO_Handle) < rates_total or rates_total < StartBars:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    fastMAnow = 0.0
    slowMAnow = 0.0
    fastMAprevious = 0.0
    slowMAprevious = 0.0
    Range = 0.0
    AvgRange = 0.0
    STOM = Arr(0, 0.0)
    STOS = Arr(0, 0.0)
    Bid = 0.0
    Ask = 0.0
    sTimeCur = ""
    sAsk = ""
    sBid = ""
    sTimeHour = ""
    sTimeMinute = ""
    sPeriod = ""
    flagval1 = False
    flagval2 = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - StartBars - 1
        flagval1_ = False
        flagval2_ = False
    else:
        to_copy = rates_total - prev_calculated + 2
        limit = rates_total - prev_calculated
    if CopyBuffer(STO_Handle, 0, 0, to_copy, STOM) <= 0:
        return 0
    if CopyBuffer(STO_Handle, 1, 0, to_copy, STOS) <= 0:
        return 0
    ArraySetAsSeries(STOM, True)
    ArraySetAsSeries(STOS, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    flagval1 = flagval1_
    flagval2 = flagval2_
    bar = limit
    for bar in range(bar, 0, -1):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            flagval1_ = flagval1
            flagval2_ = flagval2
        AvgRange = 0.0
        for iii in range(bar, bar + 10):
            AvgRange += MathAbs(high[iii] - low[iii])
        Range = AvgRange / 10
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        fastMAnow = STOM[bar]
        fastMAprevious = STOM[bar + 1]
        slowMAnow = STOS[bar]
        slowMAprevious = STOS[bar + 1]
        if (((show_KD_cross and fastMAnow > slowMAnow) and fastMAprevious < slowMAprevious) or ((show_K_OBOScross and fastMAnow > OverSoldLevel) and fastMAprevious < OverSoldLevel)) or ((show_D_OBOScross and slowMAnow > OverSoldLevel) and slowMAprevious < OverSoldLevel):
            if bar == 1 and (not flagval1):
                flagval1 = True
                flagval2 = False
                if SoundON or EmailON:
                    Bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
                    Ask = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
                    sTimeCur = TimeToString(TimeCurrent(), TIME_DATE)
                    sAsk = DoubleToString(Ask, Digits())
                    sBid = DoubleToString(Bid, Digits())
                    tm = MqlDateTime()
                    TimeToStruct(TimeCurrent(), tm)
                    sTimeHour = IntegerToString(tm.hour)
                    sTimeMinute = IntegerToString(tm.min)
                    sPeriod = EnumToString(Period(), '')
                if SoundON:
                    Alert('BUY signal at Ask=', sAsk, '\n Bid=', sBid, '\n Time=', sTimeCur, ' ', sTimeHour, ':', sTimeMinute, '\n Symbol=', Symbol(), ' Period=', sPeriod)
                if EmailON:
                    SendMail('BUY signal alert', 'BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + sTimeCur + ' ' + sTimeHour + ':' + sTimeMinute + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
            BuyBuffer[bar] = low[bar] - (Range * 0.5)
            SellBuffer[bar] = 0.0
        elif (((show_KD_cross and fastMAnow < slowMAnow) and fastMAprevious > slowMAprevious) or ((show_K_OBOScross and fastMAnow < OverBoughtLevel) and fastMAprevious > OverBoughtLevel)) or ((show_D_OBOScross and slowMAnow < OverBoughtLevel) and slowMAprevious > OverBoughtLevel):
            if bar == 1 and (not flagval2):
                flagval2 = True
                flagval1 = False
                if SoundON or EmailON:
                    Bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
                    Ask = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
                    sTimeCur = TimeToString(TimeCurrent(), TIME_DATE)
                    sAsk = DoubleToString(Ask, Digits())
                    sBid = DoubleToString(Bid, Digits())
                    tm = MqlDateTime()
                    TimeToStruct(TimeCurrent(), tm)
                    sTimeHour = IntegerToString(tm.hour)
                    sTimeMinute = IntegerToString(tm.min)
                    sPeriod = EnumToString(Period(), '')
                if SoundON:
                    Alert('SELL signal at Ask=', sAsk, '\n Bid=', sBid, '\n Date=', sTimeCur, ' ', sTimeHour, ':', sTimeMinute, '\n Symbol=', Symbol(), ' Period=', sPeriod)
                if EmailON:
                    SendMail('SELL signal alert', 'SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + sTimeCur + ' ' + sTimeHour + ':' + sTimeMinute + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
            SellBuffer[bar] = high[bar] + (Range * 0.5)
            BuyBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0, -1)
    SellBuffer[0] = 0.0
    BuyBuffer[0] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticCrossAlertSigoverlaymCw(_MQL5Indicator):
    name = 'stochastic_cross_alert_sigoverlaym_cw'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SoundON': False,
        'EmailON': False,
        'KPeriod': 5,
        'DPeriod': 3,
        'Slowing': 3,
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'OverBoughtLevel': 80,
        'OverSoldLevel': 20,
        'show_KD_cross': False,
        'show_K_OBOScross': True,
        'show_D_OBOScross': False,
    }

