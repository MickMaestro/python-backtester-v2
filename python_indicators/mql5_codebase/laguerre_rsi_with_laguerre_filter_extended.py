"""Laguerre RSI with Laguerre filter extended — converted from MQL5: MQL5 Indicators/Laguerre RSi with Laguerre filter - extended/Laguerre RSI with Laguerre filter extended.mq5

Laguerre RSI with Laguerre filter - extended
Copyright: © mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 1}, 'colors': {1: [13823743, 13823743], 2: [11119017, 16748574, 9662683], 3: [6908265]}, 'widths': {2: 2}, 'styles': {3: 4}, 'labels': {1: 'No trade zone', 2: 'Laguerre RSI', 3: 'Laguerre filter signal'}, 'levels': [], 'description': ['Laguerre RSI with Laguerre filter - extended'], 'name': 'Laguerre RSI with Laguerre filter extended', 'source': 'MQL5 Indicators/Laguerre RSi with Laguerre filter - extended/Laguerre RSI with Laguerre filter extended.mq5', 'folder': 'Laguerre RSi with Laguerre filter - extended', 'inputs': [{'mql': 'RsiGamma', 'py': 'RsiGamma', 'param': 'RsiGamma', 'type': 'double', 'default': 0.8, 'label': 'Laguerre RSI gamma', 'sinput': False}, {'mql': 'RsiPrice', 'py': 'RsiPrice', 'param': 'RsiPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'RsiSmoothGamma', 'py': 'RsiSmoothGamma', 'param': 'RsiSmoothGamma', 'type': 'double', 'default': 0.001, 'label': 'Laguerre RSI smooth gamma', 'sinput': False}, {'mql': 'RsiSmoothSpeed', 'py': 'RsiSmoothSpeed', 'param': 'RsiSmoothSpeed', 'type': 'int', 'default': 2, 'label': 'Laguerre RSI smooth speed (min 0, max 6)', 'sinput': False}, {'mql': 'FilterGamma', 'py': 'FilterGamma', 'param': 'FilterGamma', 'type': 'double', 'default': 0.6, 'label': 'Laguerre filter gamma', 'sinput': False}, {'mql': 'FilterSpeed', 'py': 'FilterSpeed', 'param': 'FilterSpeed', 'type': 'int', 'default': 2, 'label': 'Laguerre filter speed (min 0, max 6)', 'sinput': False}, {'mql': 'LevelUp', 'py': 'LevelUp', 'param': 'LevelUp', 'type': 'double', 'default': 0.85, 'label': 'Level up', 'sinput': False}, {'mql': 'LevelDown', 'py': 'LevelDown', 'param': 'LevelDown', 'type': 'double', 'default': 0.15, 'label': 'Level down', 'sinput': False}, {'mql': 'NoTradeZoneUp', 'py': 'NoTradeZoneUp', 'param': 'NoTradeZoneUp', 'type': 'double', 'default': 0.65, 'label': 'No trade zone up', 'sinput': False}, {'mql': 'NoTradeZoneDown', 'py': 'NoTradeZoneDown', 'param': 'NoTradeZoneDown', 'type': 'double', 'default': 0.35, 'label': 'No trade zone down', 'sinput': False}, {'mql': 'inpColorDisplay', 'py': 'inpColorDisplay', 'param': 'inpColorDisplay', 'type': 'int', 'default': 1, 'label': 'Color change mode :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorDisplay
change_onNoTrade = 0
change_onOuter = 1
change_onSlope = 2
change_onSignal = 3
_enum('enColorDisplay', {0: 'change_onNoTrade', 1: 'change_onOuter', 2: 'change_onSlope', 3: 'change_onSignal'})

# ---- inputs and global variables
RsiGamma = _input('RsiGamma', 0.8)  # Laguerre RSI gamma
RsiPrice = _input('RsiPrice', PRICE_CLOSE)  # Price
RsiSmoothGamma = _input('RsiSmoothGamma', 0.001)  # Laguerre RSI smooth gamma
RsiSmoothSpeed = _input('RsiSmoothSpeed', 2)  # Laguerre RSI smooth speed (min 0, max 6)
FilterGamma = _input('FilterGamma', 0.6)  # Laguerre filter gamma
FilterSpeed = _input('FilterSpeed', 2)  # Laguerre filter speed (min 0, max 6)
LevelUp = _input('LevelUp', 0.85)  # Level up
LevelDown = _input('LevelDown', 0.15)  # Level down
NoTradeZoneUp = _input('NoTradeZoneUp', 0.65)  # No trade zone up
NoTradeZoneDown = _input('NoTradeZoneDown', 0.35)  # No trade zone down
inpColorDisplay = _input('inpColorDisplay', change_onOuter)  # Color change mode :
osc = Arr(0, 0.0)
oscc = Arr(0, 0.0)
oscs = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
workLagRsi = Arr(5, 0.0, dyn=False, dims=(5,))
workLagFil = Arr(5, 0.0, dyn=False, dims=(8,))

def OnInit():
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levd, INDICATOR_DATA)
    SetIndexBuffer(2, osc, INDICATOR_DATA)
    SetIndexBuffer(3, oscc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, oscs, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, LevelUp)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, LevelDown)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Laguerre RSI with Laguerre filter (' + _str(RsiGamma) + ',' + _str(FilterGamma) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        osc[i] = iLaGuerreRsi(getPrice(RsiPrice, open, close, high, low, i, rates_total), RsiGamma, RsiSmoothGamma, RsiSmoothSpeed, i)
        oscs[i] = iLaGuerreFil(osc[i], FilterGamma, FilterSpeed, i)
        levu[i] = NoTradeZoneUp
        levd[i] = NoTradeZoneDown
        _sw1 = inpColorDisplay
        if _sw1 == change_onNoTrade:
            oscc[i] = (1 if (osc[i] > NoTradeZoneUp) else 2 if (osc[i] < NoTradeZoneDown) else 0)
        elif _sw1 == change_onOuter:
            oscc[i] = (1 if (osc[i] > LevelUp) else 2 if (osc[i] < LevelDown) else 0)
        elif _sw1 == change_onSlope:
            oscc[i] = ((1 if (osc[i] > osc[i - 1]) else 2 if (osc[i] < osc[i - 1]) else oscc[i - 1]) if (i > 0) else 0)
        else:
            oscc[i] = (1 if (osc[i] > oscs[i]) else 2 if (osc[i] < oscs[i]) else 0)
        i += 1
    return i

def iLaGuerreRsi(price, gamma, smooth, smoothSpeed, i, instance=0):
    _indP = _imod(i - 1, 5)
    _indC = _imod(i, 5)
    _inst = instance * 5
    workLagRsi[_indC][_inst] = ((((1.0 - gamma) * price) + (gamma * workLagRsi[_indP][_inst])) if (i > 0) else price)
    workLagRsi[_indC][_inst + 1] = ((((-gamma) * workLagRsi[_indC][_inst]) + workLagRsi[_indP][_inst] + (gamma * workLagRsi[_indP][_inst + 1])) if (i > 0) else price)
    workLagRsi[_indC][_inst + 2] = ((((-gamma) * workLagRsi[_indC][_inst + 1]) + workLagRsi[_indP][_inst + 1] + (gamma * workLagRsi[_indP][_inst + 2])) if (i > 0) else price)
    workLagRsi[_indC][_inst + 3] = ((((-gamma) * workLagRsi[_indC][_inst + 2]) + workLagRsi[_indP][_inst + 2] + (gamma * workLagRsi[_indP][_inst + 3])) if (i > 0) else price)
    CU = 0.0
    CD = 0.0
    if i > 0:
        if workLagRsi[_indC][_inst] >= workLagRsi[_indC][_inst + 1]:
            CU = workLagRsi[_indC][_inst] - workLagRsi[_indC][_inst + 1]
        else:
            CD = workLagRsi[_indC][_inst + 1] - workLagRsi[_indC][_inst]
        if workLagRsi[_indC][_inst + 1] >= workLagRsi[_indC][_inst + 2]:
            CU = CU + workLagRsi[_indC][_inst + 1] - workLagRsi[_indC][_inst + 2]
        else:
            CD = CD + workLagRsi[_indC][_inst + 2] - workLagRsi[_indC][_inst + 1]
        if workLagRsi[_indC][_inst + 2] >= workLagRsi[_indC][_inst + 3]:
            CU = CU + workLagRsi[_indC][_inst + 2] - workLagRsi[_indC][_inst + 3]
        else:
            CD = CD + workLagRsi[_indC][_inst + 3] - workLagRsi[_indC][_inst + 2]
    workLagRsi[_indC][_inst + 4] = (_fdiv(CU, CU + CD) if ((CU + CD) != 0) else 0)
    return iLaGuerreFil(workLagRsi[_indC][_inst + 4], smooth, _int(smoothSpeed), i, 1)

def iLaGuerreFil(price, gamma, smoothSpeed, i, instance=0):
    if gamma <= 0:
        return price
    _indP = _imod(i - 1, 5)
    _indC = _imod(i, 5)
    _inst = instance * 4
    workLagFil[_indC][_inst] = ((((1.0 - gamma) * price) + (gamma * workLagFil[_indP][_inst])) if (i > 0) else price)
    workLagFil[_indC][_inst + 1] = ((((-gamma) * workLagFil[_indC][_inst]) + workLagFil[_indP][_inst] + (gamma * workLagFil[_indP][_inst + 1])) if (i > 0) else price)
    workLagFil[_indC][_inst + 2] = ((((-gamma) * workLagFil[_indC][_inst + 1]) + workLagFil[_indP][_inst + 1] + (gamma * workLagFil[_indP][_inst + 2])) if (i > 0) else price)
    workLagFil[_indC][_inst + 3] = ((((-gamma) * workLagFil[_indC][_inst + 2]) + workLagFil[_indP][_inst + 2] + (gamma * workLagFil[_indP][_inst + 3])) if (i > 0) else price)
    if _s_iLaGuerreFil_coeffs[0] == -1:
        smoothSpeed = MathMax(MathMin(smoothSpeed, 6), 0)
        _sw2 = smoothSpeed
        if _sw2 == 0:
            _s_iLaGuerreFil_coeffs[0] = 1.0
            _s_iLaGuerreFil_coeffs[1] = 1.0
            _s_iLaGuerreFil_coeffs[2] = 1.0
            _s_iLaGuerreFil_coeffs[3] = 1.0
        elif _sw2 == 1:
            _s_iLaGuerreFil_coeffs[0] = 1.0
            _s_iLaGuerreFil_coeffs[1] = 1.0
            _s_iLaGuerreFil_coeffs[2] = 2.0
            _s_iLaGuerreFil_coeffs[3] = 1.0
        elif _sw2 == 2:
            _s_iLaGuerreFil_coeffs[0] = 1.0
            _s_iLaGuerreFil_coeffs[1] = 2.0
            _s_iLaGuerreFil_coeffs[2] = 2.0
            _s_iLaGuerreFil_coeffs[3] = 1.0
        elif _sw2 == 3:
            _s_iLaGuerreFil_coeffs[0] = 2.0
            _s_iLaGuerreFil_coeffs[1] = 2.0
            _s_iLaGuerreFil_coeffs[2] = 2.0
            _s_iLaGuerreFil_coeffs[3] = 1.0
        elif _sw2 == 4:
            _s_iLaGuerreFil_coeffs[0] = 2.0
            _s_iLaGuerreFil_coeffs[1] = 3.0
            _s_iLaGuerreFil_coeffs[2] = 2.0
            _s_iLaGuerreFil_coeffs[3] = 1.0
        elif _sw2 == 5:
            _s_iLaGuerreFil_coeffs[0] = 3.0
            _s_iLaGuerreFil_coeffs[1] = 3.0
            _s_iLaGuerreFil_coeffs[2] = 2.0
            _s_iLaGuerreFil_coeffs[3] = 1.0
        elif _sw2 == 6:
            _s_iLaGuerreFil_coeffs[0] = 4.0
            _s_iLaGuerreFil_coeffs[1] = 3.0
            _s_iLaGuerreFil_coeffs[2] = 2.0
            _s_iLaGuerreFil_coeffs[3] = 1.0
    sumc = 0.0
    for k in range(0, 4):
        sumc += _s_iLaGuerreFil_coeffs[k]
    return _fdiv((_s_iLaGuerreFil_coeffs[0] * workLagFil[_indC][_inst + 0]) + (_s_iLaGuerreFil_coeffs[1] * workLagFil[_indC][_inst + 1]) + (_s_iLaGuerreFil_coeffs[2] * workLagFil[_indC][_inst + 2]) + (_s_iLaGuerreFil_coeffs[3] * workLagFil[_indC][_inst + 3]), sumc)

def getPrice(tprice, open, close, high, low, i, _bars):
    _sw3 = tprice
    if _sw3 == PRICE_CLOSE:
        return close[i]
    elif _sw3 == PRICE_OPEN:
        return open[i]
    elif _sw3 == PRICE_HIGH:
        return high[i]
    elif _sw3 == PRICE_LOW:
        return low[i]
    elif _sw3 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw3 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw3 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

# ---- static local variables
_s_iLaGuerreFil_coeffs = Arr.of([-1.0, 0.0, 0.0, 0.0], fill=0.0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LaguerreRSIWithLaguerreFilterExtended(_MQL5Indicator):
    name = 'Laguerre RSI with Laguerre filter extended'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RsiGamma': 0.8,  # Laguerre RSI gamma
        'RsiPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'RsiSmoothGamma': 0.001,  # Laguerre RSI smooth gamma
        'RsiSmoothSpeed': 2,  # Laguerre RSI smooth speed (min 0, max 6)
        'FilterGamma': 0.6,  # Laguerre filter gamma
        'FilterSpeed': 2,  # Laguerre filter speed (min 0, max 6)
        'LevelUp': 0.85,  # Level up
        'LevelDown': 0.15,  # Level down
        'NoTradeZoneUp': 0.65,  # No trade zone up
        'NoTradeZoneDown': 0.35,  # No trade zone down
        'inpColorDisplay': _Choice({0: 'Change colors on no trade zones crossing', 1: 'Change colors on outer levels crossing', 2: 'Change colors on Laguerre RSI slope', 3: 'Change colors on signal line crossing'}, default=1),  # Color change mode :
    }

