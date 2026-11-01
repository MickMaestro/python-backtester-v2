"""Traders_Dynamic_Index — converted from MQL5: MQL5 Indicators/Traders_Dynamic_Index/Traders_Dynamic_Index.mq5

Traders Dynamic Index oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [32768], 2: [255], 3: [16760576], 4: [14053594], 5: [16760576]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'RSI Price', 2: 'Trade Signal', 3: 'VolBand High', 4: 'Market Base', 5: 'VolBand Low'}, 'levels': [], 'description': ['Traders Dynamic Index oscillator'], 'name': 'Traders_Dynamic_Index', 'source': 'MQL5 Indicators/Traders_Dynamic_Index/Traders_Dynamic_Index.mq5', 'folder': 'Traders_Dynamic_Index', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 13, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpAppliedPriceRSI', 'py': 'InpAppliedPriceRSI', 'param': 'InpAppliedPriceRSI', 'type': 'int', 'default': 1, 'label': 'RSI applied price', 'sinput': False}, {'mql': 'InpPeriodVolBand', 'py': 'InpPeriodVolBand', 'param': 'InpPeriodVolBand', 'type': 'uint', 'default': 34, 'label': 'Volatility band period', 'sinput': False}, {'mql': 'InpPeriodSmRSI', 'py': 'InpPeriodSmRSI', 'param': 'InpPeriodSmRSI', 'type': 'uint', 'default': 2, 'label': 'RSI smoothing period', 'sinput': False}, {'mql': 'InpMethodSmRSI', 'py': 'InpMethodSmRSI', 'param': 'InpMethodSmRSI', 'type': 'int', 'default': 0, 'label': 'RSI smoothing method', 'sinput': False}, {'mql': 'InpPeriodSmSig', 'py': 'InpPeriodSmSig', 'param': 'InpPeriodSmSig', 'type': 'uint', 'default': 7, 'label': 'Signal smoothing period', 'sinput': False}, {'mql': 'InpMethodSmSig', 'py': 'InpMethodSmSig', 'param': 'InpMethodSmSig', 'type': 'int', 'default': 0, 'label': 'Signal smoothing method', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 68.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 32.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpShowBase', 'py': 'InpShowBase', 'param': 'InpShowBase', 'type': 'int', 'default': 0, 'label': 'Show Market Base line', 'sinput': False}, {'mql': 'InpShowVBL', 'py': 'InpShowVBL', 'param': 'InpShowVBL', 'type': 'int', 'default': 0, 'label': 'Show Volatility band lines', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 13)  # RSI period
InpAppliedPriceRSI = _input('InpAppliedPriceRSI', PRICE_CLOSE)  # RSI applied price
InpPeriodVolBand = _input('InpPeriodVolBand', 34)  # Volatility band period
InpPeriodSmRSI = _input('InpPeriodSmRSI', 2)  # RSI smoothing period
InpMethodSmRSI = _input('InpMethodSmRSI', MODE_SMA)  # RSI smoothing method
InpPeriodSmSig = _input('InpPeriodSmSig', 7)  # Signal smoothing period
InpMethodSmSig = _input('InpMethodSmSig', MODE_SMA)  # Signal smoothing method
InpOverbought = _input('InpOverbought', 68.0)  # Overbought
InpOversold = _input('InpOversold', 32.0)  # Oversold
InpShowBase = _input('InpShowBase', INPUT_NO)  # Show Market Base line
InpShowVBL = _input('InpShowVBL', INPUT_NO)  # Show Volatility band lines
BufferTRSI = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferUpZone = Arr(0, 0.0)
BufferMdZone = Arr(0, 0.0)
BufferDnZone = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferTmpRSI = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_rsi = 0
period_vb = 0
period_sm_rsi = 0
period_sm_sig = 0
handle_rsi = 0
weight_sumR = 0
weight_sumS = 0

def OnInit():
    global handle_rsi, overbought, oversold, period_rsi, period_sm_rsi, period_sm_sig, period_vb
    period_rsi = (2 if (InpPeriodRSI < 2) else InpPeriodRSI)
    period_vb = (1 if (InpPeriodVolBand < 1) else InpPeriodVolBand)
    period_sm_rsi = (2 if (InpPeriodSmRSI < 2) else InpPeriodSmRSI)
    period_sm_sig = ((period_sm_rsi + 1) if (InpPeriodSmSig == period_sm_rsi) else 2 if (InpPeriodSmSig < 2) else InpPeriodSmSig)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferTRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferUpZone, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMdZone, INDICATOR_DATA)
    SetIndexBuffer(4, BufferDnZone, INDICATOR_DATA)
    SetIndexBuffer(5, BufferRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferTmpRSI, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TDI (' + _str(period_rsi) + ',' + _str(period_vb) + ',' + _str(period_sm_rsi) + ',' + _str(period_sm_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, InpShowVBL)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, InpShowBase)
    PlotIndexSetInteger(4, PLOT_DRAW_TYPE, InpShowVBL)
    ArraySetAsSeries(BufferTRSI, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferUpZone, True)
    ArraySetAsSeries(BufferMdZone, True)
    ArraySetAsSeries(BufferDnZone, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferTmpRSI, True)
    ResetLastError()
    handle_rsi = iRSI(None, PERIOD_CURRENT, period_rsi, InpAppliedPriceRSI)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI(', _str(period_rsi), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_vb, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_vb - 2
        ArrayInitialize(BufferTRSI, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferUpZone, EMPTY_VALUE)
        ArrayInitialize(BufferMdZone, EMPTY_VALUE)
        ArrayInitialize(BufferDnZone, EMPTY_VALUE)
        ArrayInitialize(BufferRSI, 0)
        ArrayInitialize(BufferTmpRSI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
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
    _sw1 = InpMethodSmRSI
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_rsi, period_sm_rsi, BufferRSI, BufferTRSI) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_rsi, period_sm_rsi, BufferRSI, BufferTRSI) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_rsi, period_sm_rsi, BufferRSI, BufferTRSI, _GlobRef(globals(), 'weight_sumR')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_rsi, period_sm_rsi, BufferRSI, BufferTRSI) == 0:
            return 0
    _sw2 = InpMethodSmSig
    if _sw2 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_rsi, period_sm_sig, BufferRSI, BufferSignal) == 0:
            return 0
    elif _sw2 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_rsi, period_sm_sig, BufferRSI, BufferSignal) == 0:
            return 0
    elif _sw2 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_rsi, period_sm_sig, BufferRSI, BufferSignal, _GlobRef(globals(), 'weight_sumS')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_rsi, period_sm_sig, BufferRSI, BufferSignal) == 0:
            return 0
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TradersDynamicIndex(_MQL5Indicator):
    name = 'Traders_Dynamic_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 13,  # RSI period
        'InpAppliedPriceRSI': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSI applied price
        'InpPeriodVolBand': 34,  # Volatility band period
        'InpPeriodSmRSI': 2,  # RSI smoothing period
        'InpMethodSmRSI': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # RSI smoothing method
        'InpPeriodSmSig': 7,  # Signal smoothing period
        'InpMethodSmSig': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal smoothing method
        'InpOverbought': 68.0,  # Overbought
        'InpOversold': 32.0,  # Oversold
        'InpShowBase': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show Market Base line
        'InpShowVBL': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show Volatility band lines
    }

