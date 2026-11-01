"""Consensus_of_Five — converted from MQL5: MQL5 Indicators/Consensus_of_Five/Consensus_of_Five.mq5

Consensus of Five indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 5}, 'colors': {1: [16711680], 2: [255], 3: [11119017]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Up', 2: 'Down', 3: 'Neutral'}, 'levels': [], 'description': ['Consensus of Five indicator'], 'name': 'Consensus_of_Five', 'source': 'MQL5 Indicators/Consensus_of_Five/Consensus_of_Five.mq5', 'folder': 'Consensus_of_Five', 'inputs': [{'mql': 'InpUseADX', 'py': 'InpUseADX', 'param': 'InpUseADX', 'type': 'int', 'default': 1, 'label': 'Use ADX as trend filter', 'sinput': False}, {'mql': 'InpUseDMI', 'py': 'InpUseDMI', 'param': 'InpUseDMI', 'type': 'int', 'default': 1, 'label': 'Use DMI', 'sinput': False}, {'mql': 'InpUseCCI', 'py': 'InpUseCCI', 'param': 'InpUseCCI', 'type': 'int', 'default': 1, 'label': 'Use CCI', 'sinput': False}, {'mql': 'InpUseMACD', 'py': 'InpUseMACD', 'param': 'InpUseMACD', 'type': 'int', 'default': 1, 'label': 'Use MACD', 'sinput': False}, {'mql': 'InpUseSto', 'py': 'InpUseSto', 'param': 'InpUseSto', 'type': 'int', 'default': 1, 'label': 'Use Stochastic', 'sinput': False}, {'mql': 'InpPeriodADX', 'py': 'InpPeriodADX', 'param': 'InpPeriodADX', 'type': 'uint', 'default': 14, 'label': 'ADX period', 'sinput': False}, {'mql': 'InpEntryADX', 'py': 'InpEntryADX', 'param': 'InpEntryADX', 'type': 'double', 'default': 20.0, 'label': 'ADX entry level', 'sinput': False}, {'mql': 'InpExitADX', 'py': 'InpExitADX', 'param': 'InpExitADX', 'type': 'double', 'default': 40.0, 'label': 'ADX exit level', 'sinput': False}, {'mql': 'InpPeriodDMI', 'py': 'InpPeriodDMI', 'param': 'InpPeriodDMI', 'type': 'uint', 'default': 14, 'label': 'DMI period', 'sinput': False}, {'mql': 'InpPeriodCCI', 'py': 'InpPeriodCCI', 'param': 'InpPeriodCCI', 'type': 'uint', 'default': 14, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpBuyCCI', 'py': 'InpBuyCCI', 'param': 'InpBuyCCI', 'type': 'double', 'default': 0.0, 'label': 'CCI Buy level', 'sinput': False}, {'mql': 'InpSellCCI', 'py': 'InpSellCCI', 'param': 'InpSellCCI', 'type': 'double', 'default': 0.0, 'label': 'CCI Sell level', 'sinput': False}, {'mql': 'InpPeriodFastMACD', 'py': 'InpPeriodFastMACD', 'param': 'InpPeriodFastMACD', 'type': 'uint', 'default': 12, 'label': 'MACD fast EMA period', 'sinput': False}, {'mql': 'InpPeriodSlowMACD', 'py': 'InpPeriodSlowMACD', 'param': 'InpPeriodSlowMACD', 'type': 'uint', 'default': 26, 'label': 'MACD slow EMA period', 'sinput': False}, {'mql': 'InpBuyMACD', 'py': 'InpBuyMACD', 'param': 'InpBuyMACD', 'type': 'double', 'default': 0.0, 'label': 'MACD Buy level', 'sinput': False}, {'mql': 'InpSellMACD', 'py': 'InpSellMACD', 'param': 'InpSellMACD', 'type': 'double', 'default': 0.0, 'label': 'MACD Sell level', 'sinput': False}, {'mql': 'InpPeriodStoK', 'py': 'InpPeriodStoK', 'param': 'InpPeriodStoK', 'type': 'uint', 'default': 5, 'label': 'Stochastic %K period', 'sinput': False}, {'mql': 'InpPeriodStoD', 'py': 'InpPeriodStoD', 'param': 'InpPeriodStoD', 'type': 'uint', 'default': 3, 'label': 'Stochastic %D period', 'sinput': False}, {'mql': 'InpSlowingSto', 'py': 'InpSlowingSto', 'param': 'InpSlowingSto', 'type': 'uint', 'default': 3, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'InpOverboughtSto', 'py': 'InpOverboughtSto', 'param': 'InpOverboughtSto', 'type': 'double', 'default': 80.0, 'label': 'Stochastic overbought', 'sinput': False}, {'mql': 'InpOversoldSto', 'py': 'InpOversoldSto', 'param': 'InpOversoldSto', 'type': 'double', 'default': 20.0, 'label': 'Stochastic oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpUseADX = _input('InpUseADX', INPUT_YES)  # Use ADX as trend filter
InpUseDMI = _input('InpUseDMI', INPUT_YES)  # Use DMI
InpUseCCI = _input('InpUseCCI', INPUT_YES)  # Use CCI
InpUseMACD = _input('InpUseMACD', INPUT_YES)  # Use MACD
InpUseSto = _input('InpUseSto', INPUT_YES)  # Use Stochastic
InpPeriodADX = _input('InpPeriodADX', 14)  # ADX period
InpEntryADX = _input('InpEntryADX', 20.0)  # ADX entry level
InpExitADX = _input('InpExitADX', 40.0)  # ADX exit level
InpPeriodDMI = _input('InpPeriodDMI', 14)  # DMI period
InpPeriodCCI = _input('InpPeriodCCI', 14)  # CCI period
InpBuyCCI = _input('InpBuyCCI', 0.0)  # CCI Buy level
InpSellCCI = _input('InpSellCCI', 0.0)  # CCI Sell level
InpPeriodFastMACD = _input('InpPeriodFastMACD', 12)  # MACD fast EMA period
InpPeriodSlowMACD = _input('InpPeriodSlowMACD', 26)  # MACD slow EMA period
InpBuyMACD = _input('InpBuyMACD', 0.0)  # MACD Buy level
InpSellMACD = _input('InpSellMACD', 0.0)  # MACD Sell level
InpPeriodStoK = _input('InpPeriodStoK', 5)  # Stochastic %K period
InpPeriodStoD = _input('InpPeriodStoD', 3)  # Stochastic %D period
InpSlowingSto = _input('InpSlowingSto', 3)  # Stochastic slowing
InpOverboughtSto = _input('InpOverboughtSto', 80.0)  # Stochastic overbought
InpOversoldSto = _input('InpOversoldSto', 20.0)  # Stochastic oversold
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferNL = Arr(0, 0.0)
BufferDMIP = Arr(0, 0.0)
BufferDMIM = Arr(0, 0.0)
BufferADX = Arr(0, 0.0)
BufferCCI = Arr(0, 0.0)
BufferMACD = Arr(0, 0.0)
BufferSTOK = Arr(0, 0.0)
BufferSTOS = Arr(0, 0.0)
prefix = ""
wnd = 0
UpFr = 0
DnFr = 0
lev_entry_adx = 0.0
lev_exit_adx = 0.0
lev_buy_cci = 0.0
lev_sell_cci = 0.0
lev_buy_macd = 0.0
lev_sell_macd = 0.0
overbought_sto = 0.0
oversold_sto = 0.0
period_adx = 0
period_dmi = 0
period_cci = 0
period_fast = 0
period_slow = 0
period_k = 0
period_d = 0
period_s = 0
handle_adx = 0
handle_dmi = 0
handle_cci = 0
handle_macd = 0
handle_sto = 0

class SDataUsed(MqlObject):
    _q_fields = ('name', 'used')
    def __init__(self, *args):
        self.name = ""
        self.used = False

def OnInit():
    global handle_adx, handle_cci, handle_dmi, handle_macd, handle_sto, lev_buy_cci, lev_buy_macd, lev_entry_adx, lev_exit_adx, lev_sell_cci, lev_sell_macd, overbought_sto, oversold_sto, period_adx, period_cci, period_d, period_dmi, period_fast, period_k, period_s, period_slow, prefix, wnd
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    wnd = ChartWindowFind()
    ArrayResize(array_used, 5)
    array_used[0].name = 'ADX'
    array_used[0].used = (InpUseADX != 0)
    array_used[1].name = 'DMI'
    array_used[1].used = (InpUseDMI != 0)
    array_used[2].name = 'CCI'
    array_used[2].used = (InpUseCCI != 0)
    array_used[3].name = 'MACD'
    array_used[3].used = (InpUseMACD != 0)
    array_used[4].name = 'Stoch'
    array_used[4].used = (InpUseSto != 0)
    SizeByScale()
    Descriptions()
    period_adx = (1 if (InpPeriodADX < 1) else InpPeriodADX)
    period_dmi = (1 if (InpPeriodDMI < 1) else InpPeriodDMI)
    period_cci = (1 if (InpPeriodCCI < 1) else InpPeriodCCI)
    period_fast = (1 if (InpPeriodFastMACD < 1) else InpPeriodFastMACD)
    period_slow = ((period_fast + 1) if (InpPeriodSlowMACD == period_fast) else 1 if (InpPeriodSlowMACD < 1) else InpPeriodSlowMACD)
    period_k = (1 if (InpPeriodStoK < 1) else InpPeriodStoK)
    period_d = (1 if (InpPeriodStoD < 1) else InpPeriodStoD)
    period_s = (1 if (InpSlowingSto < 1) else InpSlowingSto)
    lev_entry_adx = (0 if (InpEntryADX < 0) else InpEntryADX)
    lev_exit_adx = (0 if (InpExitADX < 0) else InpExitADX)
    lev_buy_cci = InpBuyCCI
    lev_sell_cci = InpSellCCI
    lev_buy_macd = InpBuyMACD
    lev_sell_macd = InpSellMACD
    overbought_sto = (100 if (InpOverboughtSto > 100) else 0.1 if (InpOverboughtSto < 0.1) else InpOverboughtSto)
    oversold_sto = (0 if (InpOversoldSto < 0) else (overbought_sto - 0.1) if (InpOversoldSto >= overbought_sto) else InpOversoldSto)
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferNL, INDICATOR_DATA)
    SetIndexBuffer(3, BufferDMIP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDMIM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferADX, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferCCI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferMACD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferSTOK, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferSTOS, INDICATOR_CALCULATIONS)
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_ARROW, 167)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Consensus of Five')
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    IndicatorSetInteger(INDICATOR_HEIGHT, 60)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 1)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferNL, True)
    ArraySetAsSeries(BufferDMIP, True)
    ArraySetAsSeries(BufferDMIM, True)
    ArraySetAsSeries(BufferADX, True)
    ArraySetAsSeries(BufferCCI, True)
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferSTOK, True)
    ArraySetAsSeries(BufferSTOS, True)
    ResetLastError()
    handle_adx = iADX(None, PERIOD_CURRENT, period_adx)
    if handle_adx == INVALID_HANDLE:
        Print(176, ': The iADX(', _str(period_adx), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_dmi = iADX(None, PERIOD_CURRENT, period_dmi)
    if handle_dmi == INVALID_HANDLE:
        Print(182, ': The ADX(', _str(period_dmi), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_cci = iCCI(None, PERIOD_CURRENT, period_cci, PRICE_CLOSE)
    if handle_cci == INVALID_HANDLE:
        Print('The iCCI(', _str(period_cci), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_macd = iMACD(None, PERIOD_CURRENT, period_fast, period_slow, 1, PRICE_CLOSE)
    if handle_macd == INVALID_HANDLE:
        Print('The iMACD(', _str(period_fast), ',', _str(period_slow), ',2) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sto = iStochastic(None, PERIOD_CURRENT, period_k, period_d, period_s, MODE_SMA, STO_LOWHIGH)
    if handle_sto == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k), ',', _str(period_d), ',', _str(period_s), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferNL, EMPTY_VALUE)
        ArrayInitialize(BufferDMIP, 0)
        ArrayInitialize(BufferDMIM, 0)
        ArrayInitialize(BufferADX, 0)
        ArrayInitialize(BufferCCI, 0)
        ArrayInitialize(BufferMACD, 0)
        ArrayInitialize(BufferSTOK, 0)
        ArrayInitialize(BufferSTOS, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_adx, MAIN_LINE, 0, count, BufferADX)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_dmi, PLUSDI_LINE, 0, count, BufferDMIP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_dmi, MINUSDI_LINE, 0, count, BufferDMIM)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_macd, MAIN_LINE, 0, count, BufferMACD)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto, MAIN_LINE, 0, count, BufferSTOK)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto, SIGNAL_LINE, 0, count, BufferSTOS)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        ADX = ((1 if ((BufferADX[i] > lev_entry_adx and BufferADX[i] < lev_exit_adx) and BufferADX[i] > BufferADX[i + 1]) else -1) if InpUseADX else 0)
        DMI = ((1 if (BufferDMIP[i] > BufferDMIM[i]) else -1) if InpUseDMI else 0)
        CCI_BUY = ((1 if (BufferCCI[i] > lev_buy_cci) else -1) if InpUseCCI else 0)
        CCI_SELL = ((-1 if (BufferCCI[i] < lev_sell_cci) else 1) if InpUseCCI else 0)
        MACD_BUY = ((1 if (BufferMACD[i] > lev_buy_macd) else -1) if InpUseMACD else 0)
        MACD_SELL = ((-1 if (BufferMACD[i] < lev_sell_macd) else 1) if InpUseMACD else 0)
        STO_BUY = ((1 if (BufferSTOK[i] > BufferSTOS[i] and BufferSTOS[i] < overbought_sto) else -1) if InpUseSto else 0)
        STO_SELL = ((-1 if (BufferSTOK[i] < BufferSTOS[i] and BufferSTOS[i] > oversold_sto) else 1) if InpUseSto else 0)
        if (((((DMI == 0 and CCI_BUY == 0) and CCI_SELL == 0) and MACD_BUY == 0) and MACD_SELL == 0) and STO_BUY == 0) and STO_SELL == 0:
            SettingBufferValues(0, i)
        else:
            SettingBufferValues(0, i)
            if ((((ADX == 1 or ADX == 0) and (DMI == 1 or DMI == 0)) and (CCI_BUY == 1 or CCI_BUY == 0)) and (MACD_BUY == 1 or MACD_BUY == 0)) and (STO_BUY == 1 or STO_BUY == 0):
                SettingBufferValues(1, i)
            if ((((ADX == 1 or ADX == 0) and (DMI == -1 or DMI == 0)) and (CCI_SELL == -1 or CCI_SELL == 0)) and (MACD_SELL == -1 or MACD_SELL == 0)) and (STO_SELL == -1 or STO_SELL == 0):
                SettingBufferValues(-1, i)
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        for i in range(0, 3):
            PlotIndexSetInteger(i, PLOT_LINE_WIDTH, SizeByScale())
        Descriptions()
        ChartRedraw()

def SettingBufferValues(direction, shift):
    _sw1 = direction
    if _sw1 == 1:
        BufferUP[shift] = 0.5
        BufferNL[shift] = EMPTY_VALUE
        BufferDN[shift] = BufferNL[shift]
    elif _sw1 == -1:
        BufferDN[shift] = 0.5
        BufferUP[shift] = EMPTY_VALUE
        BufferNL[shift] = BufferUP[shift]
    else:
        BufferNL[shift] = 0.5
        BufferUP[shift] = EMPTY_VALUE
        BufferDN[shift] = BufferUP[shift]

def SizeByScale():
    scale = _uchar(ChartGetInteger(0, CHART_SCALE))
    size = (1 if (scale < 3) else 2 if (scale == 3) else 5 if (scale == 4) else 8)
    return size

def Descriptions():
    x = 0
    y = 1
    arr_texts = Arr.of(['Up', 'Down', 'Neutral'], fill="")
    for i in range(0, 3 + 5):
        if i < 3:
            x = (45 * i) + 6
            name = prefix + 'label' + _str(i)
            clr = _uint(PlotIndexGetInteger(i, PLOT_LINE_COLOR))
            Label(name, x, y, CharToString(167), 16, clr, 'Wingdings')
            Label(name + '_txt', x + 10, y + 5, arr_texts[i], 10, clrGray, 'Calibri')
        else:
            shift = (33 if ((i - 3) > 3) else 30) * (i - 3)
            x1 = x + 80 + shift
            Label(prefix + array_used[i - 3].name, x1, y + 5, array_used[i - 3].name, 10, (clrGreen if array_used[i - 3].used else clrSilver), 'Calibri')

def Label(name, x, y, text, size, clr, font):
    if ObjectFind(0, name) != wnd:
        ObjectCreate(0, name, OBJ_LABEL, wnd, 0, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_LOWER)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, size)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
    ObjectSetString(0, name, OBJPROP_FONT, font)
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetString(0, name, OBJPROP_TOOLTIP, '\n')

# ---- global variables initialised from expressions
array_used = Arr(0, 0, factory=SDataUsed)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ConsensusOfFive(_MQL5Indicator):
    name = 'Consensus_of_Five'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpUseADX': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use ADX as trend filter
        'InpUseDMI': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use DMI
        'InpUseCCI': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use CCI
        'InpUseMACD': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use MACD
        'InpUseSto': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use Stochastic
        'InpPeriodADX': 14,  # ADX period
        'InpEntryADX': 20.0,  # ADX entry level
        'InpExitADX': 40.0,  # ADX exit level
        'InpPeriodDMI': 14,  # DMI period
        'InpPeriodCCI': 14,  # CCI period
        'InpBuyCCI': 0.0,  # CCI Buy level
        'InpSellCCI': 0.0,  # CCI Sell level
        'InpPeriodFastMACD': 12,  # MACD fast EMA period
        'InpPeriodSlowMACD': 26,  # MACD slow EMA period
        'InpBuyMACD': 0.0,  # MACD Buy level
        'InpSellMACD': 0.0,  # MACD Sell level
        'InpPeriodStoK': 5,  # Stochastic %K period
        'InpPeriodStoD': 3,  # Stochastic %D period
        'InpSlowingSto': 3,  # Stochastic slowing
        'InpOverboughtSto': 80.0,  # Stochastic overbought
        'InpOversoldSto': 20.0,  # Stochastic oversold
    }

