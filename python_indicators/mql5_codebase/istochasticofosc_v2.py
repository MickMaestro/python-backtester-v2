"""istochasticofosc_v2 — converted from MQL5: MQL5 Indicators/iStochasticOfOsc/istochasticofosc_v2.mq5

Copyright: Integer; Link: http://dmffx.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'http://dmffx.com', 'version': '1.00', 'window': 'separate', 'indicator_minimum': -3.0, 'indicator_maximum': 103.0, 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Main', 2: 'Signal'}, 'levels': [0.0, 100.0, 50.0, 20.0, 80.0], 'description': [], 'name': 'istochasticofosc_v2', 'source': 'MQL5 Indicators/iStochasticOfOsc/istochasticofosc_v2.mq5', 'folder': 'iStochasticOfOsc', 'inputs': [{'mql': 'Indicator', 'py': 'Indicator', 'param': 'Indicator', 'type': 'int', 'default': 29, 'label': '', 'sinput': False}, {'mql': 'Volume', 'py': 'Volume', 'param': 'Volume', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Period_1', 'py': 'Period_1', 'param': 'Period_1', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Period_2', 'py': 'Period_2', 'param': 'Period_2', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Period_3', 'py': 'Period_3', 'param': 'Period_3', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Method', 'py': 'Method', 'param': 'Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Shift_1', 'py': 'Shift_1', 'param': 'Shift_1', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Shift_2', 'py': 'Shift_2', 'param': 'Shift_2', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Shift_3', 'py': 'Shift_3', 'param': 'Shift_3', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Line', 'py': 'Line', 'param': 'Line', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'StPeriod_K', 'py': 'StPeriod_K', 'param': 'StPeriod_K', 'type': 'int', 'default': 200, 'label': '', 'sinput': False}, {'mql': 'StPeriod_D', 'py': 'StPeriod_D', 'param': 'StPeriod_D', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'StPeriod_S', 'py': 'StPeriod_S', 'param': 'StPeriod_S', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'StMethod', 'py': 'StMethod', 'param': 'StMethod', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum eOscType
AC = 0
AD = 1
ADX = 2
ADXW = 3
AO = 6
ATR = 7
BEARS = 9
BULLS = 10
BWMFI = 11
CCI = 12
CHAIKIN = 13
DEMARKER = 16
FORCE = 18
GATOR = 21
MACD = 24
MFI = 25
MOMENTUM = 26
OBV = 27
OSMA = 28
RSI = 29
RVI = 30
STDDEV = 32
STOCHASTIC = 33
TRIX = 35
VOLUMES = 37
WPR = 38
_enum('eOscType', {0: 'AC', 1: 'AD', 2: 'ADX', 3: 'ADXW', 6: 'AO', 7: 'ATR', 9: 'BEARS', 10: 'BULLS', 11: 'BWMFI', 12: 'CCI', 13: 'CHAIKIN', 16: 'DEMARKER', 18: 'FORCE', 21: 'GATOR', 24: 'MACD', 25: 'MFI', 26: 'MOMENTUM', 27: 'OBV', 28: 'OSMA', 29: 'RSI', 30: 'RVI', 32: 'STDDEV', 33: 'STOCHASTIC', 35: 'TRIX', 37: 'VOLUMES', 38: 'WPR'})

# enum ePrice
CLOSECLOSE = 1
LOWHIGH = 0
CLOSE = 1
HIGH = 3
LOW = 4
MEDIAN = 5
OPEN = 2
TYPICAL = 6
WEIGHTED = 7
_enum('ePrice', {1: 'CLOSECLOSE', 0: 'LOWHIGH', 1: 'CLOSE', 3: 'HIGH', 4: 'LOW', 5: 'MEDIAN', 2: 'OPEN', 6: 'TYPICAL', 7: 'WEIGHTED'})

# enum eInLine
GATOR_UPPER_HISTOGRAM = 0
GATOR_LOWER_HISTOGRAM = 2
ADX_ADX = 0
ADX_PDI = 1
ADX_MDI = 2
MAIN = 0
SIGNAL = 1
_enum('eInLine', {0: 'GATOR_UPPER_HISTOGRAM', 2: 'GATOR_LOWER_HISTOGRAM', 0: 'ADX_ADX', 1: 'ADX_PDI', 2: 'ADX_MDI', 0: 'MAIN', 1: 'SIGNAL'})

# ---- inputs and global variables
Indicator = _input('Indicator', RSI)
Volume = _input('Volume', VOLUME_TICK)
Period_1 = _input('Period_1', 14)
Period_2 = _input('Period_2', 10)
Period_3 = _input('Period_3', 10)
Price = _input('Price', CLOSE)
Method = _input('Method', MODE_SMA)
Shift_1 = _input('Shift_1', 8)
Shift_2 = _input('Shift_2', 5)
Shift_3 = _input('Shift_3', 3)
Line = _input('Line', MAIN)
StPeriod_K = _input('StPeriod_K', 200)
StPeriod_D = _input('StPeriod_D', 5)
StPeriod_S = _input('StPeriod_S', 7)
StMethod = _input('StMethod', MODE_SMA)
HandleX = 0
Handle_v = 0
MainBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
IndBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
LowestBuffer = Arr(0, 0.0)
SumVBuffer = Arr(0, 0.0)
SumRBuffer = Arr(0, 0.0)

def OnInit():
    global HandleX
    SetIndexBuffer(0, MainBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, IndBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, HighestBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, LowestBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, SumVBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, SumRBuffer, INDICATOR_CALCULATIONS)
    _sw1 = Indicator
    if _sw1 == AC:
        HandleX = iAC(Symbol(), PERIOD_CURRENT)
    elif _sw1 == AD:
        HandleX = iAD(Symbol(), PERIOD_CURRENT, Volume)
    elif _sw1 == ADX:
        HandleX = iADX(Symbol(), PERIOD_CURRENT, Period_1)
    elif _sw1 == ADXW:
        HandleX = iADXWilder(Symbol(), PERIOD_CURRENT, Period_1)
    elif _sw1 == AO:
        HandleX = iAO(Symbol(), PERIOD_CURRENT)
    elif _sw1 == ATR:
        HandleX = iATR(Symbol(), PERIOD_CURRENT, Period_1)
    elif _sw1 == BEARS:
        HandleX = iBearsPower(Symbol(), PERIOD_CURRENT, Period_1)
    elif _sw1 == BULLS:
        HandleX = iBullsPower(Symbol(), PERIOD_CURRENT, Period_1)
    elif _sw1 == BWMFI:
        HandleX = iBWMFI(Symbol(), PERIOD_CURRENT, Volume)
    elif _sw1 == CCI:
        HandleX = iCCI(Symbol(), PERIOD_CURRENT, Period_1, Price)
    elif _sw1 == CHAIKIN:
        HandleX = iChaikin(Symbol(), PERIOD_CURRENT, Period_1, Period_2, Method, Volume)
    elif _sw1 == DEMARKER:
        HandleX = iDeMarker(Symbol(), PERIOD_CURRENT, Period_1)
    elif _sw1 == FORCE:
        HandleX = iForce(Symbol(), PERIOD_CURRENT, Period_1, Method, Volume)
    elif _sw1 == GATOR:
        HandleX = iGator(Symbol(), PERIOD_CURRENT, Period_1, Shift_1, Period_2, Shift_2, Period_3, Shift_3, Method, Price)
    elif _sw1 == MACD:
        HandleX = iMACD(Symbol(), PERIOD_CURRENT, Period_1, Period_2, Period_3, Price)
    elif _sw1 == MFI:
        HandleX = iMFI(Symbol(), PERIOD_CURRENT, Period_1, Volume)
    elif _sw1 == MOMENTUM:
        HandleX = iMomentum(Symbol(), PERIOD_CURRENT, Period_1, Price)
    elif _sw1 == OBV:
        HandleX = iOBV(Symbol(), PERIOD_CURRENT, Volume)
    elif _sw1 == OSMA:
        HandleX = iOsMA(Symbol(), PERIOD_CURRENT, Period_1, Period_2, Period_3, Price)
    elif _sw1 == RSI:
        HandleX = iRSI(Symbol(), PERIOD_CURRENT, Period_1, Price)
    elif _sw1 == RVI:
        HandleX = iRVI(Symbol(), PERIOD_CURRENT, Period_1)
    elif _sw1 == STDDEV:
        HandleX = iStdDev(Symbol(), PERIOD_CURRENT, Period_1, 0, Method, Price)
    elif _sw1 == STOCHASTIC:
        HandleX = iStochastic(Symbol(), PERIOD_CURRENT, Period_1, Period_2, Period_3, Method, Price)
    elif _sw1 == TRIX:
        HandleX = iTriX(Symbol(), PERIOD_CURRENT, Period_1, Price)
    elif _sw1 == VOLUMES:
        HandleX = iVolumes(Symbol(), PERIOD_CURRENT, Volume)
    elif _sw1 == WPR:
        HandleX = iWPR(Symbol(), PERIOD_CURRENT, Period_1)
    Label = ""
    _sw2 = Indicator
    if _sw2 == AC:
        Label = 'AC'
    elif _sw2 == AD:
        Label = 'AD(' + fNameVolume(Volume) + ')'
    elif _sw2 == ADX:
        Label = 'ADX-' + fNameADXLine(Line) + '(' + ITS(Period_1) + ')'
    elif _sw2 == ADXW:
        Label = 'ADXW-' + fNameADXLine(Line) + '(' + ITS(Period_1) + ')'
    elif _sw2 == AO:
        Label = 'AO'
    elif _sw2 == ATR:
        Label = 'ATR(' + ITS(Period_1) + ')'
    elif _sw2 == BEARS:
        Label = 'BEARS(' + ITS(Period_1) + ')'
    elif _sw2 == BULLS:
        Label = 'BULLS(' + ITS(Period_1) + ')'
    elif _sw2 == BWMFI:
        Label = 'BWMFI(' + fNameVolume(Volume) + ')'
    elif _sw2 == CCI:
        Label = 'CCI(' + ITS(Period_1) + ',' + fNamePriceShort(Price) + ')'
    elif _sw2 == CHAIKIN:
        Label = 'CHAIKIN(' + ITS(Period_1) + ',' + ITS(Period_2) + ',' + fMethodName(Method) + ',' + fNameVolume(Volume) + ')'
    elif _sw2 == DEMARKER:
        Label = 'DEMARKER(' + ITS(Period_1) + ')'
    elif _sw2 == FORCE:
        Label = 'FORCE(' + ITS(Period_1) + ',' + fMethodName(Method) + ',' + fNameVolume(Volume) + ')'
    elif _sw2 == GATOR:
        Label = 'GATOR(' + ITS(Period_1) + ',' + ITS(Shift_1) + ',' + ITS(Period_2) + ',' + ITS(Shift_2) + ',' + ITS(Period_3) + ',' + ITS(Shift_3) + ',' + fMethodName(Method) + ',' + fNameVolume(Volume) + ')'
    elif _sw2 == MACD:
        Label = 'MACD(' + ITS(Period_1) + ',' + ITS(Period_2) + ITS(Period_3) + ',' + fNamePriceShort(Price) + ')'
    elif _sw2 == MFI:
        Label = 'MFI(' + ITS(Period_1) + ',' + fNameVolume(Volume) + ')'
    elif _sw2 == MOMENTUM:
        Label = 'MOMENTUM(' + ITS(Period_1) + ',' + fNamePriceShort(Price) + ')'
    elif _sw2 == OBV:
        Label = 'OBV(' + fNameVolume(Volume) + ')'
    elif _sw2 == OSMA:
        Label = 'OSMA(' + ITS(Period_1) + ',' + ITS(Period_2) + ITS(Period_3) + ',' + fNamePriceShort(Price) + ')'
    elif _sw2 == RSI:
        Label = 'RSI(' + ITS(Period_1) + ',' + fNamePriceShort(Price) + ')'
    elif _sw2 == RVI:
        Label = 'RVI-' + fNameMainSignal(Line) + '(' + ITS(Period_1) + ')'
    elif _sw2 == STDDEV:
        Label = 'STDDEV(' + ITS(Period_1) + ',' + fMethodName(Method) + ',' + fNamePriceShort(Price) + ')'
    elif _sw2 == STOCHASTIC:
        Label = 'STOCHASTIC-' + fNameMainSignal(Line) + '(' + ITS(Period_1) + ',' + ITS(Period_2) + ITS(Period_3) + ',' + fMethodName(Method) + ',' + fNameStoPriceShort(Price) + ')'
    elif _sw2 == TRIX:
        Label = 'TRIX(' + ITS(Period_1) + ',' + fNamePriceShort(Price) + ')'
    elif _sw2 == VOLUMES:
        Label = 'VOLUMES(' + fNameVolume(Volume) + ')'
    elif _sw2 == WPR:
        Label = 'WPR(' + ITS(Period_1) + ')'
    PlotIndexSetString(0, PLOT_LABEL, 'ST OF ' + Label)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ST OF ' + Label)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return 0

def OnDeinit(reason):
    IndicatorRelease(HandleX)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_begin, _s_OnCalculate_error
    start = 0
    start2 = 0
    start3 = 0
    start4 = 0
    prev_calc = prev_calculated
    if prev_calculated == 0:
        _s_OnCalculate_error = True
    if _s_OnCalculate_error:
        start = 0
        prev_calc = 0
    else:
        start = prev_calculated - 1
    if CopyBuffer(HandleX, Line, 0, rates_total - start, IndBuffer) == -1:
        _s_OnCalculate_error = True
        return rates_total
    if _s_OnCalculate_error:
        for i in range(0, rates_total):
            if IndBuffer[i] != EMPTY_VALUE and IndBuffer[i] != 0:
                _s_OnCalculate_begin = i
                break
        start2 = start + StPeriod_K
        start3 = start2 + StPeriod_K + StPeriod_S
        start4 = start3
        _s_OnCalculate_begin = start4
        ArrayInitialize(MainBuffer, EMPTY_VALUE)
        ArrayInitialize(SignalBuffer, EMPTY_VALUE)
        PlotIndexGetInteger(0, PLOT_DRAW_BEGIN, _s_OnCalculate_begin)
        PlotIndexGetInteger(1, PLOT_DRAW_BEGIN, _s_OnCalculate_begin + fMADrawBegin(StPeriod_D, StMethod))
        _s_OnCalculate_error = False
    else:
        start2 = start
        start3 = start
        start4 = start
    for i in range(start2, rates_total):
        HighestBuffer[i] = IndBuffer[i]
        LowestBuffer[i] = IndBuffer[i]
        for j in range(i, i - StPeriod_K, -1):
            HighestBuffer[i] = MathMax(HighestBuffer[i], IndBuffer[j])
            LowestBuffer[i] = MathMin(LowestBuffer[i], IndBuffer[j])
    for i in range(start3, rates_total):
        SumVBuffer[i] = 0.0
        SumRBuffer[i] = 0.0
        for j in range(i, i - StPeriod_S, -1):
            SumVBuffer[i] += IndBuffer[j] - LowestBuffer[j]
            SumRBuffer[i] += HighestBuffer[j] - LowestBuffer[j]
        SumRBuffer[i] = ND8(SumRBuffer[i])
        if SumRBuffer[i] == 0:
            MainBuffer[i] = 100.0
        else:
            MainBuffer[i] = _fdiv(100.0 * SumVBuffer[i], SumRBuffer[i])
    fMAOnArray2(MainBuffer, SignalBuffer, StPeriod_D, StMethod, _s_OnCalculate_begin, start4, rates_total)
    return rates_total

def fMAOnArray2(aData, aMA, aPeriod, aMethod, aBegin, aStart, aRatesTotal):
    p1 = 0.0
    p2 = 0.0
    tWS = 0.0
    _sw3 = aMethod
    if _sw3 == MODE_SMA:
        aStart = MathMax(aStart, aBegin + aPeriod)
        for i in range(aStart, aRatesTotal):
            if i == (aBegin + aPeriod):
                aMA[i] = 0.0
                for j in range(0, aPeriod):
                    aMA[i] += aData[i - j]
                aMA[i] = _fdiv(aMA[i], aPeriod)
            else:
                aMA[i] = aMA[i - 1] - _fdiv(aData[i - aPeriod] - aData[i], aPeriod)
    elif _sw3 == MODE_EMA:
        if aStart == aBegin:
            aMA[aBegin] = aData[aBegin]
            aStart += 1
        p1 = _fdiv(2.0, 1.0 + aPeriod)
        p2 = 1.0 - p1
        for i in range(aStart, aRatesTotal):
            aMA[i] = (p1 * aData[i]) + (p2 * aMA[i - 1])
    elif _sw3 == MODE_LWMA:
        aStart = MathMax(aStart, aBegin + aPeriod)
        tWS = ((1.0 + aPeriod) / 2.0) * aPeriod
        for i in range(aStart, aRatesTotal):
            aMA[i] = 0.0
            for j in range(0, aPeriod):
                aMA[i] += aData[i - j] * (aPeriod - j)
            aMA[i] = _fdiv(aMA[i], tWS)
    elif _sw3 == MODE_SMMA:
        if aStart == aBegin:
            aMA[aBegin] = aData[aBegin]
            aStart += 1
        p1 = _fdiv(1.0, aPeriod)
        p2 = 1.0 - p1
        for i in range(aStart, aRatesTotal):
            aMA[i] = (p1 * aData[i]) + (p2 * aMA[i - 1])

def ND8(aValue):
    return NormalizeDouble(aValue, 8)

def fMADrawBegin(aPeriod, aMethod):
    _sw4 = aMethod
    if _sw4 == 1:
        return 10 * aPeriod
    elif _sw4 == 2:
        return 20 * aPeriod
    return aPeriod

def fNameVolume(aVolume):
    _sw5 = aVolume
    if _sw5 == VOLUME_REAL:
        return 'R'
    elif _sw5 == VOLUME_TICK:
        return 'T'
    return '?'

def ITS(aValue):
    return IntegerToString(aValue)

def fNameADXLine(aLine):
    _sw6 = aLine
    if _sw6 == MAIN_LINE:
        return 'MAIN'
    elif _sw6 == PLUSDI_LINE:
        return 'PDI'
    elif _sw6 == MINUSDI_LINE:
        return 'MDI'
    return '?'

def fNameMainSignal(aLine):
    _sw7 = aLine
    if _sw7 == MAIN_LINE:
        return 'MAIN'
    elif _sw7 == SIGNAL_LINE:
        return 'SIGNAL'
    return '?'

def fNamePriceShort(aPrice):
    _sw8 = aPrice
    if _sw8 == PRICE_CLOSE:
        return 'C'
    elif _sw8 == PRICE_HIGH:
        return 'H'
    elif _sw8 == PRICE_LOW:
        return 'L'
    elif _sw8 == PRICE_MEDIAN:
        return 'M'
    elif _sw8 == PRICE_OPEN:
        return 'O'
    elif _sw8 == PRICE_TYPICAL:
        return 'T'
    elif _sw8 == PRICE_WEIGHTED:
        return 'W'
    return '?'

def fNameStoPriceShort(aPrice):
    _sw9 = aPrice
    if _sw9 == STO_CLOSECLOSE:
        return 'CC'
    elif _sw9 == STO_LOWHIGH:
        return 'LH'
    return '?'

def fMethodName(aMethod):
    _sw10 = aMethod
    if _sw10 == MODE_EMA:
        return 'E'
    elif _sw10 == MODE_LWMA:
        return 'L'
    elif _sw10 == MODE_SMA:
        return 'S'
    elif _sw10 == MODE_SMMA:
        return 'SM'
    return '?'

# ---- static local variables
_s_OnCalculate_error = True
_s_OnCalculate_begin = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IstochasticofoscV2(_MQL5Indicator):
    name = 'istochasticofosc_v2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Indicator': _Choice({0: 'AC', 1: 'AD', 2: 'ADX', 3: 'ADXW', 6: 'AO', 7: 'ATR', 9: 'BEARS', 10: 'BULLS', 11: 'BWMFI', 12: 'CCI', 13: 'CHAIKIN', 16: 'DEMARKER', 18: 'FORCE', 21: 'GATOR', 24: 'MACD', 25: 'MFI', 26: 'MOMENTUM', 27: 'OBV', 28: 'OSMA', 29: 'RSI', 30: 'RVI', 32: 'STDDEV', 33: 'STOCHASTIC', 35: 'TRIX', 37: 'VOLUMES', 38: 'WPR'}, default=29),
        'Volume': _Choice({0: 'Tick', 1: 'Real'}, default=0),
        'Period_1': 14,
        'Period_2': 10,
        'Period_3': 10,
        'Price': _Choice({1: 'CLOSECLOSE', 0: 'LOWHIGH', 3: 'HIGH', 4: 'LOW', 5: 'MEDIAN', 2: 'OPEN', 6: 'TYPICAL', 7: 'WEIGHTED'}, default=1),
        'Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Shift_1': 8,
        'Shift_2': 5,
        'Shift_3': 3,
        'Line': _Choice({0: 'GATOR_UPPER_HISTOGRAM', 2: 'GATOR_LOWER_HISTOGRAM', 1: 'ADX_PDI'}, default=0),
        'StPeriod_K': 200,
        'StPeriod_D': 5,
        'StPeriod_S': 7,
        'StMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
    }
    y_range = (-3.0, 103.0)

