"""AlexSTAL_ZigZagProf_channel — converted from MQL5: MQL5 Indicators/AlexSTAL_ZigZagProf_channel/AlexSTAL_ZigZagProf_channel.mq5

Copyright: Copyright 2011, AlexSTAL; Link: http://www.alexstal.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.alexstal_outsidebar import *  # #include AlexSTAL_OutsideBar.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2011, AlexSTAL', 'link': 'http://www.alexstal.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 7, 2: 8, 3: 8, 4: 5, 5: 5}, 'colors': {1: [16443110], 2: [10156544, 42495], 3: [10156544, 42495], 4: [16711680], 5: [9639167]}, 'widths': {2: 2, 3: 2, 4: 2, 5: 2}, 'styles': {}, 'labels': {1: ' AlexSTAL_ZigZagProf Cloud', 2: 'Up  AlexSTAL_ZigZagProf', 3: 'Down  AlexSTAL_ZigZagProf', 4: 'Up AlexSTAL_ZigZagProf_Arrows', 5: 'Down AlexSTAL_ZigZagProf_Arrows'}, 'levels': [], 'description': [], 'name': 'AlexSTAL_ZigZagProf_channel', 'source': 'MQL5 Indicators/AlexSTAL_ZigZagProf_channel/AlexSTAL_ZigZagProf_channel.mq5', 'folder': 'AlexSTAL_ZigZagProf_channel', 'inputs': [{'mql': 'iExtPeriod', 'py': 'iExtPeriod', 'param': 'iExtPeriod', 'type': 'uchar', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'iMinAmplitude', 'py': 'iMinAmplitude', 'param': 'iMinAmplitude', 'type': 'uchar', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'iMinMotion', 'py': 'iMinMotion', 'param': 'iMinMotion', 'type': 'uchar', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'iUseSmallerTFforEB', 'py': 'iUseSmallerTFforEB', 'param': 'iUseSmallerTFforEB', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'uint', 'default': 159, 'label': 'лейба верхнего фрактала', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'uint', 'default': 159, 'label': 'лейба нижнего фрактала', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['AlexSTAL_OutsideBar.mqh']}

# ---- inputs and global variables
iExtPeriod = _input('iExtPeriod', 12)
iMinAmplitude = _input('iMinAmplitude', 10)
iMinMotion = _input('iMinMotion', 0)
iUseSmallerTFforEB = _input('iUseSmallerTFforEB', True)
UpLable = _input('UpLable', 159)  # лейба верхнего фрактала
DnLable = _input('DnLable', 159)  # лейба нижнего фрактала
ExtPeriod = 0
MinAmplitude = 0
MinMotion = 0
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
ColorUpperBuffer = Arr(0, 0.0)
ColorLowerBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
LowestBuffer = Arr(0, 0.0)
OBBuffer = Arr(0, 0.0)
LastBarTime = 0
LastBarLastHigh = 0.0
LastBarLastLow = 0.0
TimeFirstExtBar = 0
MP = 0.0
MM = 0.0
DownloadHistory = False

def OnInit():
    global DownloadHistory, ExtPeriod, MM, MP, MinAmplitude, MinMotion
    if iExtPeriod >= 2:
        ExtPeriod = iExtPeriod
    else:
        ExtPeriod = 2
    if iMinAmplitude >= 0:
        MinAmplitude = iMinAmplitude
    else:
        MinAmplitude = 0
    MP = NormalizeDouble(MinAmplitude * Point(), Digits())
    if iMinMotion >= 1:
        MinMotion = iMinMotion
    else:
        MinMotion = 1
    MM = NormalizeDouble(MinMotion * Point(), Digits())
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, UpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorUpperBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, LowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ColorLowerBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, HighestBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, OBBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpBuffer, True)
    ArraySetAsSeries(DnBuffer, True)
    ArraySetAsSeries(UpperBuffer, True)
    ArraySetAsSeries(LowerBuffer, True)
    ArraySetAsSeries(ColorUpperBuffer, True)
    ArraySetAsSeries(ColorLowerBuffer, True)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    ArraySetAsSeries(OBBuffer, True)
    PlotIndexSetInteger(3, PLOT_ARROW, DnLable)
    PlotIndexSetInteger(4, PLOT_ARROW, UpLable)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, 'ZigZag(' + _str(ExtPeriod) + ',' + _str(MinAmplitude) + ',' + _str(MinMotion) + ',' + _str(iUseSmallerTFforEB) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    DownloadHistory = True
    return 0

def iHighest_u(array, depth, startPos):
    index = startPos
    MaxBar = ArraySize(array) - 1
    if startPos < 0 or startPos > MaxBar:
        Print('Invalid parameter in the function iHighest, startPos =', startPos)
        return -1
    max_ = array[startPos]
    for i in range(MathMin(startPos + depth - 1, MaxBar), startPos - 1, -1):
        if array[i] > max_:
            index = i
            max_ = array[i]
    return index

def iLowest_u(array, depth, startPos):
    index = startPos
    MaxBar = ArraySize(array) - 1
    if startPos < 0 or startPos > MaxBar:
        Print('Invalid parameter in the function iLowest, startPos =', startPos)
        return -1
    min_ = array[startPos]
    for i in range(MathMin(startPos + depth - 1, MaxBar), startPos - 1, -1):
        if array[i] < min_:
            index = i
            min_ = array[i]
    return index

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global DownloadHistory, LastBarLastHigh, LastBarLastLow, LastBarTime, TimeFirstExtBar
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    i = 0
    i = rates_total - prev_calculated - 1
    for i in range(i, 0 - 1, -1):
        HighestBuffer[i] = EMPTY_VALUE
        LowestBuffer[i] = EMPTY_VALUE
        OBBuffer[i] = EMPTY_VALUE
    else:
        i = _range_end(i, 0 - 1, -1)
    counted_bars = prev_calculated
    if counted_bars == 0:
        DownloadHistory = True
    if DownloadHistory:
        ArrayInitialize(HighestBuffer, EMPTY_VALUE)
        ArrayInitialize(LowestBuffer, EMPTY_VALUE)
        ArrayInitialize(OBBuffer, EMPTY_VALUE)
        TimeFirstExtBar = 0
        counted_bars = 0
        LastBarTime = 0
        DownloadHistory = False
    NewBar = False
    if LastBarTime != time[0]:
        NewBar = True
        LastBarTime = time[0]
        LastBarLastHigh = high[0]
        LastBarLastLow = low[0]
    BarsForRecalculation = 0
    if counted_bars != 0:
        BarsForRecalculation = rates_total - counted_bars
        if not NewBar:
            if NormalizeDouble(high[0] - LastBarLastHigh, Digits()) >= MM or NormalizeDouble(LastBarLastLow - low[0], Digits()) >= MM:
                LastBarLastHigh = high[0]
                LastBarLastLow = low[0]
            else:
                return rates_total
    else:
        BarsForRecalculation = rates_total - ExtPeriod
    LET = 0
    H = 0.0
    L = 0.0
    Fup = 0.0
    Fdn = 0.0
    lastHighestBufferbar = 0
    lastLowestBufferbar = 0
    lastHighestBuffer = 0.0
    lastLowestBuffer = 0.0
    m = 0
    n = 0
    i = BarsForRecalculation
    for i in range(i, 0 - 1, -1):
        lastHighestBuffer = 0.0
        lastLowestBuffer = 0.0
        lastHighestBufferbar = i
        lastLowestBufferbar = i
        LET = 0
        m = 0
        n = 0
        while HighestBuffer[lastHighestBufferbar] == EMPTY_VALUE:
            if lastHighestBufferbar > (rates_total - ExtPeriod):
                break
            lastHighestBufferbar += 1
        lastHighestBuffer = HighestBuffer[lastHighestBufferbar]
        while LowestBuffer[lastLowestBufferbar] == EMPTY_VALUE:
            if lastLowestBufferbar > (rates_total - ExtPeriod):
                break
            lastLowestBufferbar += 1
        lastLowestBuffer = LowestBuffer[lastLowestBufferbar]
        if lastHighestBufferbar < lastLowestBufferbar:
            LET = 1
        if lastHighestBufferbar > lastLowestBufferbar:
            LET = -1
        if lastHighestBufferbar == lastLowestBufferbar:
            m = lastHighestBufferbar
            n = m
            while m == n:
                m += 1
                n += 1
                while HighestBuffer[m] == EMPTY_VALUE:
                    if m > (rates_total - ExtPeriod):
                        break
                    m += 1
                while LowestBuffer[n] == EMPTY_VALUE:
                    if n > (rates_total - ExtPeriod):
                        break
                    n += 1
                if MathMax(m, n) > (rates_total - ExtPeriod):
                    break
            if m < n:
                LET = 1
            elif m > n:
                LET = -1
        H = high[iHighest_u(high, ExtPeriod, i)]
        L = low[iLowest_u(low, ExtPeriod, i)]
        Fup = high[i]
        Fdn = low[i]
        _sw1 = Comb(i, H, L, Fup, Fdn)
        if _sw1 == 1:
            _sw2 = LET
            if _sw2 == 1:
                if lastHighestBuffer < Fup:
                    HighestBuffer[lastHighestBufferbar] = EMPTY_VALUE
                    HighestBuffer[i] = Fup
            elif _sw2 == -1:
                if (Fup - lastLowestBuffer) > MP:
                    HighestBuffer[i] = Fup
            else:
                HighestBuffer[i] = Fup
                TimeFirstExtBar = time[i]
        elif _sw1 == -1:
            _sw3 = LET
            if _sw3 == 1:
                if (lastHighestBuffer - Fdn) > MP:
                    LowestBuffer[i] = Fdn
            elif _sw3 == -1:
                if lastLowestBuffer > Fdn:
                    LowestBuffer[lastLowestBufferbar] = EMPTY_VALUE
                    LowestBuffer[i] = Fdn
            else:
                LowestBuffer[i] = Fdn
                TimeFirstExtBar = time[i]
        elif _sw1 == 2:
            _sw4 = LET
            if _sw4 == 1:
                if (Fup - Fdn) > MP:
                    if (lastHighestBuffer - Fdn) > MP:
                        HighestBuffer[i] = Fup
                        LowestBuffer[i] = Fdn
                    else:
                        if lastHighestBuffer < Fup:
                            HighestBuffer[lastHighestBufferbar] = EMPTY_VALUE
                            HighestBuffer[i] = Fup
                else:
                    if (lastHighestBuffer - Fdn) > MP:
                        LowestBuffer[i] = Fdn
                    else:
                        if lastHighestBuffer < Fup:
                            HighestBuffer[lastHighestBufferbar] = EMPTY_VALUE
                            HighestBuffer[i] = Fup
            elif _sw4 == -1:
                if (Fup - Fdn) > MP:
                    HighestBuffer[i] = Fup
                    if Fdn < lastLowestBuffer and time[lastLowestBufferbar] > TimeFirstExtBar:
                        LowestBuffer[lastLowestBufferbar] = EMPTY_VALUE
                        LowestBuffer[i] = Fdn
                else:
                    if (Fup - lastLowestBuffer) > MP:
                        HighestBuffer[i] = Fup
                    else:
                        if lastLowestBuffer > Fdn:
                            LowestBuffer[lastLowestBufferbar] = EMPTY_VALUE
                            LowestBuffer[i] = Fdn
            else:
                pass
        elif _sw1 == -2:
            _sw5 = LET
            if _sw5 == 1:
                if (Fup - Fdn) > MP:
                    LowestBuffer[i] = Fdn
                    if lastHighestBuffer < Fup and time[lastHighestBufferbar] > TimeFirstExtBar:
                        HighestBuffer[lastHighestBufferbar] = EMPTY_VALUE
                        HighestBuffer[i] = Fup
                else:
                    if (lastHighestBuffer - Fdn) > MP:
                        LowestBuffer[i] = Fdn
                    else:
                        if lastHighestBuffer < Fup:
                            HighestBuffer[lastHighestBufferbar] = EMPTY_VALUE
                            HighestBuffer[i] = Fup
            elif _sw5 == -1:
                if (Fup - Fdn) > MP:
                    if (Fup - lastLowestBuffer) > MP:
                        HighestBuffer[i] = Fup
                        LowestBuffer[i] = Fdn
                    else:
                        if lastLowestBuffer > Fdn:
                            LowestBuffer[lastLowestBufferbar] = EMPTY_VALUE
                            LowestBuffer[i] = Fdn
                else:
                    if (Fup - lastLowestBuffer) > MP:
                        HighestBuffer[i] = Fup
                    else:
                        if lastLowestBuffer > Fdn:
                            LowestBuffer[lastLowestBufferbar] = EMPTY_VALUE
                            LowestBuffer[i] = Fdn
            else:
                pass
        else:
            pass
    else:
        i = _range_end(i, 0 - 1, -1)
    limit = 0
    bar = 0
    barHH = 0
    barHH1 = 0
    barLL = 0
    barLL1 = 0
    HH = Box(0.0)
    LL = Box(0.0)
    HH1 = Box(0.0)
    LL1 = Box(0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
        for index in range(rates_total - 1, 0 - 1, -1):
            UpBuffer[index] = 0.0
            UpperBuffer[index] = 0.0
            DnBuffer[index] = 0.0
            LowerBuffer[index] = 0.0
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        barHH = FindFirstExtremum(bar, rates_total, HighestBuffer, HH)
        barHH1 = FindFirstExtremum(barHH + 1, rates_total, HighestBuffer, HH1)
        if barHH >= 0 and barHH1 >= 0:
            for index in range(barHH1 - 1, barHH, -1):
                UpBuffer[index] = HH1.v
                UpperBuffer[index] = HH1.v
                ColorUpperBuffer[index] = ColorUpperBuffer[index + 1]
            for index in range(barHH, bar - 1, -1):
                UpBuffer[index] = HH.v
                UpperBuffer[index] = HH.v
                if HH.v > HH1.v:
                    ColorUpperBuffer[index] = 0.0
                elif HH.v < HH1.v:
                    ColorUpperBuffer[index] = 1.0
                else:
                    ColorUpperBuffer[index] = ColorUpperBuffer[index + 1]
        barLL = FindFirstExtremum(bar, rates_total, LowestBuffer, LL)
        barLL1 = FindFirstExtremum(barLL + 1, rates_total, LowestBuffer, LL1)
        if barLL >= 0 and barLL1 >= 0:
            for index in range(barLL1 - 1, barLL, -1):
                DnBuffer[index] = LL1.v
                LowerBuffer[index] = LL1.v
                ColorLowerBuffer[index] = ColorLowerBuffer[index + 1]
            for index in range(barLL, bar - 1, -1):
                DnBuffer[index] = LL.v
                LowerBuffer[index] = LL.v
                if LL.v > LL1.v:
                    ColorLowerBuffer[index] = 0.0
                elif LL.v < LL1.v:
                    ColorLowerBuffer[index] = 1.0
                else:
                    ColorLowerBuffer[index] = ColorLowerBuffer[index + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def Comb(i, H, L, Fup, Fdn):
    if Fup == H and (Fdn == 0 or (Fdn > 0 and Fdn > L)):
        return 1
    if Fdn == L and (Fup == 0 or (Fup > 0 and Fup < H)):
        return -1
    if Fdn == L and Fup == H:
        OrderFormationHL = OFBError
        if OBBuffer[i] == EMPTY_VALUE:
            OrderFormationHL = GetOrderFormationBarHighLow(Symbol(), Period(), i, iUseSmallerTFforEB)
        if OrderFormationHL != OFBError:
            OBBuffer[i] = OrderFormationHL
        else:
            OrderFormationHL = _int(OBBuffer[i])
        _sw6 = OrderFormationHL
        if _sw6 == OFBLowHigh:
            return 2
        elif _sw6 == OFBHighLow:
            return -2
    return 0

def FindFirstExtremum(StartPos, Rates_total, Array, Extremum):
    for bar in range(StartPos, Rates_total):
        if Array[bar] and Array[bar] != EMPTY_VALUE:
            Extremum.v = Array[bar]
            return bar
            break
    Extremum.v = 0.0
    return -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AlexSTALZigZagProfChannel(_MQL5Indicator):
    name = 'AlexSTAL_ZigZagProf_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'iExtPeriod': 12,
        'iMinAmplitude': 10,
        'iMinMotion': 0,
        'iUseSmallerTFforEB': True,
        'UpLable': 159,  # лейба верхнего фрактала
        'DnLable': 159,  # лейба нижнего фрактала
    }

