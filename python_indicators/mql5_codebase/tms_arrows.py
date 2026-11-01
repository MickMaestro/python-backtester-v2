"""TMS_Arrows — converted from MQL5: MQL5 Indicators/TMS_Arrows/TMS_Arrows.mq5

TMS Arrows indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'TMS Bullish', 2: 'TMS Bearish'}, 'levels': [], 'description': ['TMS Arrows indicator'], 'name': 'TMS_Arrows', 'source': 'MQL5 Indicators/TMS_Arrows/TMS_Arrows.mq5', 'folder': 'TMS_Arrows', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 13, 'label': 'TDI RSI period', 'sinput': False}, {'mql': 'InpAppliedPriceRSI', 'py': 'InpAppliedPriceRSI', 'param': 'InpAppliedPriceRSI', 'type': 'int', 'default': 1, 'label': 'TDI RSI applied price', 'sinput': False}, {'mql': 'InpPeriodVolBand', 'py': 'InpPeriodVolBand', 'param': 'InpPeriodVolBand', 'type': 'uint', 'default': 34, 'label': 'TDI Volatility band period', 'sinput': False}, {'mql': 'InpPeriodSmRSI', 'py': 'InpPeriodSmRSI', 'param': 'InpPeriodSmRSI', 'type': 'uint', 'default': 2, 'label': 'TDI RSI smoothing period', 'sinput': False}, {'mql': 'InpMethodSmRSI', 'py': 'InpMethodSmRSI', 'param': 'InpMethodSmRSI', 'type': 'int', 'default': 0, 'label': 'TDI RSI smoothing method', 'sinput': False}, {'mql': 'InpPeriodSmSig', 'py': 'InpPeriodSmSig', 'param': 'InpPeriodSmSig', 'type': 'uint', 'default': 7, 'label': 'TDI Signal smoothing period', 'sinput': False}, {'mql': 'InpMethodSmSig', 'py': 'InpMethodSmSig', 'param': 'InpMethodSmSig', 'type': 'int', 'default': 0, 'label': 'TDI Signal smoothing method', 'sinput': False}, {'mql': 'InpAnchorBuffer', 'py': 'InpAnchorBuffer', 'param': 'InpAnchorBuffer', 'type': 'int', 'default': 0, 'label': 'Signal point anchor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_SIGNAL_POINT_ANCHOR
ANCHOR_HL = 0
ANCHOR_OPEN = 1
_enum('ENUM_SIGNAL_POINT_ANCHOR', {0: 'ANCHOR_HL', 1: 'ANCHOR_OPEN'})

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 13)  # TDI RSI period
InpAppliedPriceRSI = _input('InpAppliedPriceRSI', PRICE_CLOSE)  # TDI RSI applied price
InpPeriodVolBand = _input('InpPeriodVolBand', 34)  # TDI Volatility band period
InpPeriodSmRSI = _input('InpPeriodSmRSI', 2)  # TDI RSI smoothing period
InpMethodSmRSI = _input('InpMethodSmRSI', MODE_SMA)  # TDI RSI smoothing method
InpPeriodSmSig = _input('InpPeriodSmSig', 7)  # TDI Signal smoothing period
InpMethodSmSig = _input('InpMethodSmSig', MODE_SMA)  # TDI Signal smoothing method
InpAnchorBuffer = _input('InpAnchorBuffer', ANCHOR_HL)  # Signal point anchor
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferTmpRSI = Arr(0, 0.0)
BufferHAOpen = Arr(0, 0.0)
BufferHAClose = Arr(0, 0.0)
BufferStoM = Arr(0, 0.0)
BufferStoS = Arr(0, 0.0)
BufferUpZone = Arr(0, 0.0)
BufferMdZone = Arr(0, 0.0)
BufferDnZone = Arr(0, 0.0)
BufferMa = Arr(0, 0.0)
BufferMb = Arr(0, 0.0)
period_rsi = 0
period_vb = 0
period_sm_rsi = 0
period_sm_sig = 0
handle_rsi = 0
handle_sto = 0
weight_sumR = 0
weight_sumS = 0

def OnInit():
    global handle_rsi, handle_sto, period_rsi, period_sm_rsi, period_sm_sig, period_vb
    period_rsi = (2 if (InpPeriodRSI < 2) else InpPeriodRSI)
    period_vb = (1 if (InpPeriodVolBand < 1) else InpPeriodVolBand)
    period_sm_rsi = (2 if (InpPeriodSmRSI < 2) else InpPeriodSmRSI)
    period_sm_sig = ((period_sm_rsi + 1) if (InpPeriodSmSig == period_sm_rsi) else 2 if (InpPeriodSmSig < 2) else InpPeriodSmSig)
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferTmpRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferHAOpen, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferHAClose, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferStoM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferStoS, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferUpZone, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferMdZone, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferDnZone, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferMa, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferMb, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TMS (' + _str(period_rsi) + ',' + _str(period_vb) + ',' + _str(period_sm_rsi) + ',' + _str(period_sm_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferTmpRSI, True)
    ArraySetAsSeries(BufferHAOpen, True)
    ArraySetAsSeries(BufferHAClose, True)
    ArraySetAsSeries(BufferStoM, True)
    ArraySetAsSeries(BufferStoS, True)
    ArraySetAsSeries(BufferUpZone, True)
    ArraySetAsSeries(BufferMdZone, True)
    ArraySetAsSeries(BufferDnZone, True)
    ArraySetAsSeries(BufferMa, True)
    ArraySetAsSeries(BufferMb, True)
    ResetLastError()
    handle_rsi = iRSI(None, PERIOD_CURRENT, period_rsi, InpAppliedPriceRSI)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI(', _str(period_rsi), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sto = iStochastic(None, PERIOD_CURRENT, 8, 3, 3, MODE_SMA, STO_LOWHIGH)
    if handle_sto == INVALID_HANDLE:
        Print('The iRSI(', 8, ',', 3, ',', 3, ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_alert
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < fmax(period_vb, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_vb - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferRSI, 0)
        ArrayInitialize(BufferTmpRSI, 0)
        ArrayInitialize(BufferHAOpen, 0)
        ArrayInitialize(BufferHAClose, 0)
        ArrayInitialize(BufferStoM, 0)
        ArrayInitialize(BufferStoS, 0)
        ArrayInitialize(BufferUpZone, 0)
        ArrayInitialize(BufferMdZone, 0)
        ArrayInitialize(BufferDnZone, 0)
        ArrayInitialize(BufferMa, 0)
        ArrayInitialize(BufferMb, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto, MAIN_LINE, 0, count, BufferStoM)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto, SIGNAL_LINE, 0, count, BufferStoS)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        MA = 0.0
        for j in range(i, i + period_vb):
            BufferTmpRSI[j - i] = BufferRSI[j]
            MA += _fdiv(BufferRSI[j], period_vb)
        BufferUpZone[i] = MA + (1.6185 * StDev(BufferTmpRSI, period_vb))
        BufferDnZone[i] = MA - (1.6185 * StDev(BufferTmpRSI, period_vb))
        BufferMdZone[i] = (BufferUpZone[i] + BufferDnZone[i]) / 2
        BufferHAOpen[i] = (BufferHAOpen[i + 1] + BufferHAClose[i + 1]) / 2.0
        BufferHAClose[i] = (open[i] + high[i] + low[i] + close[i]) / 4.0
    _sw1 = InpMethodSmRSI
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_rsi, period_sm_rsi, BufferRSI, BufferMa) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_rsi, period_sm_rsi, BufferRSI, BufferMa) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_rsi, period_sm_rsi, BufferRSI, BufferMa, _GlobRef(globals(), 'weight_sumR')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_rsi, period_sm_rsi, BufferRSI, BufferMa) == 0:
            return 0
    _sw2 = InpMethodSmSig
    if _sw2 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_rsi, period_sm_sig, BufferRSI, BufferMb) == 0:
            return 0
    elif _sw2 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_rsi, period_sm_sig, BufferRSI, BufferMb) == 0:
            return 0
    elif _sw2 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_rsi, period_sm_sig, BufferRSI, BufferMb, _GlobRef(globals(), 'weight_sumS')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_rsi, period_sm_sig, BufferRSI, BufferMb) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        if (((BufferMa[i] > BufferMb[i] and BufferMa[i + 1] < BufferMb[i + 1]) and BufferStoM[i] > BufferStoS[i]) and BufferHAOpen[i] < BufferHAClose[i]) and (BufferHAOpen[i + 1] > BufferHAClose[i + 1] or (BufferHAOpen[i + 1] < BufferHAClose[i + 1] and BufferHAOpen[i + 2] > BufferHAClose[i + 2])):
            BufferUP[i] = (low[i] if (InpAnchorBuffer == ANCHOR_HL) else open[i])
            if i == 0 and time[0] > _s_OnCalculate_last_alert:
                Alert(Symbol() + ',' + TimeframeToString(Period()) + ': TMS Bullish Signal')
                _s_OnCalculate_last_alert = TimeCurrent()
        if (((BufferMa[i] < BufferMb[i] and BufferMa[i + 1] > BufferMb[i + 1]) and BufferStoM[i] < BufferStoS[i]) and BufferHAOpen[i] > BufferHAClose[i]) and (BufferHAOpen[i + 1] < BufferHAClose[i + 1] or (BufferHAOpen[i + 1] > BufferHAClose[i + 1] and BufferHAOpen[i + 2] < BufferHAClose[i + 2])):
            BufferDN[i] = (high[i] if (InpAnchorBuffer == ANCHOR_HL) else open[i])
            if i == 0 and time[0] > _s_OnCalculate_last_alert:
                Alert(Symbol() + ',' + TimeframeToString(Period()) + ': TMS Bearish Signal')
                _s_OnCalculate_last_alert = TimeCurrent()
    return rates_total

def StDev(Data, period):
    return sqrt(Variance(Data, period))

def Variance(Data, period):
    sum_ = 0.0
    ssum = 0.0
    for i in range(0, period):
        sum_ += Data[i]
        ssum += pow(Data[i], 2)
    return _fdiv((ssum * period) - (sum_ * sum_), period * (period - 1))

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

# ---- static local variables
_s_OnCalculate_last_alert = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TMSArrows(_MQL5Indicator):
    name = 'TMS_Arrows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 13,  # TDI RSI period
        'InpAppliedPriceRSI': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # TDI RSI applied price
        'InpPeriodVolBand': 34,  # TDI Volatility band period
        'InpPeriodSmRSI': 2,  # TDI RSI smoothing period
        'InpMethodSmRSI': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # TDI RSI smoothing method
        'InpPeriodSmSig': 7,  # TDI Signal smoothing period
        'InpMethodSmSig': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # TDI Signal smoothing method
        'InpAnchorBuffer': _Choice({0: 'High/Low', 1: 'Open'}, default=0),  # Signal point anchor
    }

