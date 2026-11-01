"""Tarzan — converted from MQL5: MQL5 Indicators/Tarzan/Tarzan.mq5

\\"Tarzan\\" Indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 6}, 'types': {1: 1, 2: 8, 3: 1, 4: 1, 5: 5, 6: 5}, 'colors': {1: [10526303], 2: [16748574, 32768, 42495, 255, 13882323], 3: [13422920], 4: [13422920], 5: [255], 6: [16711680]}, 'widths': {1: 1, 2: 3, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'RSI', 2: 'Central', 3: 'Top', 4: 'Bottom', 5: 'Sell', 6: 'Buy'}, 'levels': [], 'description': ['\\"Tarzan\\" Indicator'], 'name': 'Tarzan', 'source': 'MQL5 Indicators/Tarzan/Tarzan.mq5', 'folder': 'Tarzan', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 5, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'RSI Applied price', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 50, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA Method', 'sinput': False}, {'mql': 'InpChannelTop', 'py': 'InpChannelTop', 'param': 'InpChannelTop', 'type': 'uint', 'default': 20, 'label': 'Channel top size', 'sinput': False}, {'mql': 'InpChannelBottom', 'py': 'InpChannelBottom', 'param': 'InpChannelBottom', 'type': 'uint', 'default': 20, 'label': 'Channel bottom size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 5)  # RSI period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # RSI Applied price
InpPeriodMA = _input('InpPeriodMA', 50)  # MA period
InpMethod = _input('InpMethod', MODE_SMA)  # MA Method
InpChannelTop = _input('InpChannelTop', 20)  # Channel top size
InpChannelBottom = _input('InpChannelBottom', 20)  # Channel bottom size
BufferRSI = Arr(0, 0.0)
BufferCentral = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferArrowUP = Arr(0, 0.0)
BufferArrowDN = Arr(0, 0.0)
period_rsi = 0
period_ma = 0
handle_rsi = 0
weight_sum = 0

def OnInit():
    global handle_rsi, period_ma, period_rsi
    period_rsi = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    period_ma = (2 if (InpPeriodMA < 2) else InpPeriodMA)
    SetIndexBuffer(0, BufferRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCentral, INDICATOR_DATA)
    SetIndexBuffer(2, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(4, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(5, BufferArrowUP, INDICATOR_DATA)
    SetIndexBuffer(6, BufferArrowDN, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_ARROW, 242)
    PlotIndexSetInteger(5, PLOT_ARROW, 241)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Tarzan (' + _str(period_rsi) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferCentral, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferArrowUP, True)
    ArraySetAsSeries(BufferArrowDN, True)
    ResetLastError()
    handle_rsi = iRSI(None, PERIOD_CURRENT, period_rsi, InpAppliedPrice)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI(', _str(period_rsi), ')object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferRSI, EMPTY_VALUE)
        ArrayInitialize(BufferCentral, EMPTY_VALUE)
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferArrowUP, EMPTY_VALUE)
        ArrayInitialize(BufferArrowDN, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_rsi, period_ma, BufferRSI, BufferCentral)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_rsi, period_ma, BufferRSI, BufferCentral)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_rsi, period_ma, BufferRSI, BufferCentral, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_rsi, period_ma, BufferRSI, BufferCentral)
    for i in range(limit, 0 - 1, -1):
        MA = BufferCentral[i]
        UP = (100 if ((MA + InpChannelTop) > 100) else (MA + InpChannelTop))
        DN = (0 if ((MA - InpChannelBottom) < 0) else (MA - InpChannelBottom))
        BufferTop[i] = UP
        BufferBottom[i] = DN
        RSI_0 = BufferRSI[i]
        RSI_1 = BufferRSI[i + 1]
        cross_to_up = False
        cross_to_dn = False
        if RSI_0 > DN and RSI_1 <= DN:
            cross_to_up = True
            BufferArrowDN[i] = DN
        else:
            BufferArrowDN[i] = EMPTY_VALUE
        if RSI_0 < UP and RSI_1 >= UP:
            cross_to_dn = True
            BufferArrowUP[i] = UP
        else:
            BufferArrowUP[i] = EMPTY_VALUE
        BufferColors[i] = (1 if cross_to_up else 3 if cross_to_dn else 0 if (RSI_0 > MA and RSI_0 <= UP) else 2 if (RSI_0 < MA and RSI_0 >= DN) else 4)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Tarzan(_MQL5Indicator):
    name = 'Tarzan'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 5,  # RSI period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSI Applied price
        'InpPeriodMA': 50,  # MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Method
        'InpChannelTop': 20,  # Channel top size
        'InpChannelBottom': 20,  # Channel bottom size
    }

