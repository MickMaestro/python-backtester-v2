"""alexstal_zigzagprof — converted from MQL5: MQL5 Indicators/Professional ZigZag/alexstal_zigzagprof.mq5

Copyright: Copyright 2011, AlexSTAL; Link: http://www.alexstal.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.alexstal_outsidebar import *  # #include AlexSTAL_OutsideBar.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2011, AlexSTAL', 'link': 'http://www.alexstal.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 6, 2: 6}, 'colors': {1: [255], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Zigzag', 2: 'Zigzag'}, 'levels': [], 'description': [], 'name': 'alexstal_zigzagprof', 'source': 'MQL5 Indicators/Professional ZigZag/alexstal_zigzagprof.mq5', 'folder': 'Professional ZigZag', 'inputs': [{'mql': 'iExtPeriod', 'py': 'iExtPeriod', 'param': 'iExtPeriod', 'type': 'uchar', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'iMinAmplitude', 'py': 'iMinAmplitude', 'param': 'iMinAmplitude', 'type': 'uchar', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'iMinMotion', 'py': 'iMinMotion', 'param': 'iMinMotion', 'type': 'uchar', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'iUseSmallerTFforEB', 'py': 'iUseSmallerTFforEB', 'param': 'iUseSmallerTFforEB', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['AlexSTAL_OutsideBar.mqh']}

# ---- inputs and global variables
iExtPeriod = _input('iExtPeriod', 12)
iMinAmplitude = _input('iMinAmplitude', 10)
iMinMotion = _input('iMinMotion', 0)
iUseSmallerTFforEB = _input('iUseSmallerTFforEB', True)
ExtPeriod = 0
MinAmplitude = 0
MinMotion = 0
UP = Arr(0, 0.0)
DN = Arr(0, 0.0)
OB = Arr(0, 0.0)
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
    MinAmplitude = iMinAmplitude
    MP = NormalizeDouble(MinAmplitude * Point(), Digits())
    if iMinMotion >= 1:
        MinMotion = iMinMotion
    else:
        MinMotion = 1
    MM = NormalizeDouble(MinMotion * Point(), Digits())
    SetIndexBuffer(0, UP, INDICATOR_DATA)
    SetIndexBuffer(1, DN, INDICATOR_DATA)
    SetIndexBuffer(2, OB, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(UP, True)
    ArraySetAsSeries(DN, True)
    ArraySetAsSeries(OB, True)
    PlotIndexSetString(0, PLOT_LABEL, 'ZigZag(' + _str(ExtPeriod) + ',' + _str(MinAmplitude) + ',' + _str(MinMotion) + ',' + _str(iUseSmallerTFforEB) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'ZigZag(' + _str(ExtPeriod) + ',' + _str(MinAmplitude) + ',' + _str(MinMotion) + ',' + _str(iUseSmallerTFforEB) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
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
        UP[i] = EMPTY_VALUE
        DN[i] = EMPTY_VALUE
        OB[i] = EMPTY_VALUE
    else:
        i = _range_end(i, 0 - 1, -1)
    counted_bars = prev_calculated
    if counted_bars == 0:
        DownloadHistory = True
    if DownloadHistory:
        ArrayInitialize(UP, EMPTY_VALUE)
        ArrayInitialize(DN, EMPTY_VALUE)
        ArrayInitialize(OB, EMPTY_VALUE)
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
    lastUPbar = 0
    lastDNbar = 0
    lastUP = 0.0
    lastDN = 0.0
    m = 0
    n = 0
    i = BarsForRecalculation
    for i in range(i, 0 - 1, -1):
        lastUP = 0.0
        lastDN = 0.0
        lastUPbar = i
        lastDNbar = i
        LET = 0
        m = 0
        n = 0
        while UP[lastUPbar] == EMPTY_VALUE:
            if lastUPbar > (rates_total - ExtPeriod):
                break
            lastUPbar += 1
        lastUP = UP[lastUPbar]
        while DN[lastDNbar] == EMPTY_VALUE:
            if lastDNbar > (rates_total - ExtPeriod):
                break
            lastDNbar += 1
        lastDN = DN[lastDNbar]
        if lastUPbar < lastDNbar:
            LET = 1
        if lastUPbar > lastDNbar:
            LET = -1
        if lastUPbar == lastDNbar:
            m = lastUPbar
            n = m
            while m == n:
                m += 1
                n += 1
                while UP[m] == EMPTY_VALUE:
                    if m > (rates_total - ExtPeriod):
                        break
                    m += 1
                while DN[n] == EMPTY_VALUE:
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
                if lastUP < Fup:
                    UP[lastUPbar] = EMPTY_VALUE
                    UP[i] = Fup
            elif _sw2 == -1:
                if (Fup - lastDN) > MP:
                    UP[i] = Fup
            else:
                UP[i] = Fup
                TimeFirstExtBar = time[i]
        elif _sw1 == -1:
            _sw3 = LET
            if _sw3 == 1:
                if (lastUP - Fdn) > MP:
                    DN[i] = Fdn
            elif _sw3 == -1:
                if lastDN > Fdn:
                    DN[lastDNbar] = EMPTY_VALUE
                    DN[i] = Fdn
            else:
                DN[i] = Fdn
                TimeFirstExtBar = time[i]
        elif _sw1 == 2:
            _sw4 = LET
            if _sw4 == 1:
                if (Fup - Fdn) > MP:
                    if (lastUP - Fdn) > MP:
                        UP[i] = Fup
                        DN[i] = Fdn
                    else:
                        if lastUP < Fup:
                            UP[lastUPbar] = EMPTY_VALUE
                            UP[i] = Fup
                else:
                    if (lastUP - Fdn) > MP:
                        DN[i] = Fdn
                    else:
                        if lastUP < Fup:
                            UP[lastUPbar] = EMPTY_VALUE
                            UP[i] = Fup
            elif _sw4 == -1:
                if (Fup - Fdn) > MP:
                    UP[i] = Fup
                    if Fdn < lastDN and time[lastDNbar] > TimeFirstExtBar:
                        DN[lastDNbar] = EMPTY_VALUE
                        DN[i] = Fdn
                else:
                    if (Fup - lastDN) > MP:
                        UP[i] = Fup
                    else:
                        if lastDN > Fdn:
                            DN[lastDNbar] = EMPTY_VALUE
                            DN[i] = Fdn
            else:
                pass
        elif _sw1 == -2:
            _sw5 = LET
            if _sw5 == 1:
                if (Fup - Fdn) > MP:
                    DN[i] = Fdn
                    if lastUP < Fup and time[lastUPbar] > TimeFirstExtBar:
                        UP[lastUPbar] = EMPTY_VALUE
                        UP[i] = Fup
                else:
                    if (lastUP - Fdn) > MP:
                        DN[i] = Fdn
                    else:
                        if lastUP < Fup:
                            UP[lastUPbar] = EMPTY_VALUE
                            UP[i] = Fup
            elif _sw5 == -1:
                if (Fup - Fdn) > MP:
                    if (Fup - lastDN) > MP:
                        UP[i] = Fup
                        DN[i] = Fdn
                    else:
                        if lastDN > Fdn:
                            DN[lastDNbar] = EMPTY_VALUE
                            DN[i] = Fdn
                else:
                    if (Fup - lastDN) > MP:
                        UP[i] = Fup
                    else:
                        if lastDN > Fdn:
                            DN[lastDNbar] = EMPTY_VALUE
                            DN[i] = Fdn
            else:
                pass
        else:
            pass
    else:
        i = _range_end(i, 0 - 1, -1)
    return rates_total

def Comb(i, H, L, Fup, Fdn):
    if Fup == H and (Fdn == 0 or (Fdn > 0 and Fdn > L)):
        return 1
    if Fdn == L and (Fup == 0 or (Fup > 0 and Fup < H)):
        return -1
    if Fdn == L and Fup == H:
        OrderFormationHL = OFBError
        if OB[i] == EMPTY_VALUE:
            OrderFormationHL = GetOrderFormationBarHighLow(Symbol(), Period(), i, iUseSmallerTFforEB)
        if OrderFormationHL != OFBError:
            OB[i] = OrderFormationHL
        else:
            OrderFormationHL = _int(OB[i])
        _sw6 = OrderFormationHL
        if _sw6 == OFBLowHigh:
            return 2
        elif _sw6 == OFBHighLow:
            return -2
    return 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AlexstalZigzagprof(_MQL5Indicator):
    name = 'alexstal_zigzagprof'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'iExtPeriod': 12,
        'iMinAmplitude': 10,
        'iMinMotion': 0,
        'iUseSmallerTFforEB': True,
    }

