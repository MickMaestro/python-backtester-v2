"""Corr volume weighted MA — converted from MQL5: MQL5 Indicators/Corrected volume weighted moving average/Corr volume weighted MA.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 8, 4: 8}, 'colors': {1: [15132390], 2: [8421504], 3: [12632256, 7451452, 17919], 4: [12632256, 7451452, 17919]}, 'widths': {4: 3}, 'styles': {2: 2}, 'labels': {1: 'Corrected average zone', 2: 'Corrected average middle', 3: 'Corrected average original', 4: 'Corrected average '}, 'levels': [], 'description': [], 'name': 'Corr volume weighted MA', 'source': 'MQL5 Indicators/Corrected volume weighted moving average/Corr volume weighted MA.mq5', 'folder': 'Corrected volume weighted moving average', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'VWMA period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpVolume', 'py': 'inpVolume', 'param': 'inpVolume', 'type': 'int', 'default': 0, 'label': 'Volume to use', 'sinput': False}, {'mql': 'inpCorrectionPeriod', 'py': 'inpCorrectionPeriod', 'param': 'inpCorrectionPeriod', 'type': 'int', 'default': 0, 'label': '"Correction" period (<0 no correction,0 or 1 same as average)', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on :', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlUp', 'py': 'inpFlUp', 'param': 'inpFlUp', 'type': 'double', 'default': 90.0, 'label': 'Upper level %', 'sinput': False}, {'mql': 'inpFlDown', 'py': 'inpFlDown', 'param': 'inpFlDown', 'type': 'double', 'default': 10.0, 'label': 'Lower level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum chgColor
chg_onSlope = 0
chg_onLevel = 1
chg_onMiddle = 2
chg_onOrig = 3
_enum('chgColor', {0: 'chg_onSlope', 1: 'chg_onLevel', 2: 'chg_onMiddle', 3: 'chg_onOrig'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # VWMA period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpVolume = _input('inpVolume', VOLUME_TICK)  # Volume to use
inpCorrectionPeriod = _input('inpCorrectionPeriod', 0)  # "Correction" period (<0 no correction,0 or 1 same as average)
inpColorOn = _input('inpColorOn', chg_onLevel)  # Color change on :
inpFlPeriod = _input('inpFlPeriod', 25)  # Floating levels period
inpFlUp = _input('inpFlUp', 90.0)  # Upper level %
inpFlDown = _input('inpFlDown', 10.0)  # Lower level %
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
mid = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
avg = Arr(0, 0.0)
avgc = Arr(0, 0.0)
ª_corrPeriod = 0
ª_colorOn = 0

class sCorrMaStruct(MqlObject):
    _q_fields = ('corrected', 'price', 'price2', 'summ', 'summ2')
    def __init__(self, *args):
        self.corrected = 0.0
        self.price = 0.0
        self.price2 = 0.0
        self.summ = 0.0
        self.summ2 = 0.0

class sVwmaArrayStruct(MqlObject):
    _q_fields = ('price', 'volume', 'sump', 'sumv')
    def __init__(self, *args):
        self.price = 0.0
        self.volume = 0.0
        self.sump = 0.0
        self.sumv = 0.0

def OnInit():
    global ª_colorOn, ª_corrPeriod
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, mid, INDICATOR_DATA)
    SetIndexBuffer(3, avg, INDICATOR_DATA)
    SetIndexBuffer(4, avgc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, val, INDICATOR_DATA)
    SetIndexBuffer(6, valc, INDICATOR_COLOR_INDEX)
    ª_corrPeriod = (inpCorrectionPeriod if (inpCorrectionPeriod > 0) else 0 if (inpCorrectionPeriod < 0) else inpPeriod)
    ª_colorOn = (inpColorOn if (inpFlPeriod > 1 and ª_corrPeriod > 1) else inpColorOn if (inpColorOn != chg_onOrig) else chg_onSlope)
    IndicatorSetString(INDICATOR_SHORTNAME, '"Corrected" VWMA (' + _str(inpPeriod) + ',' + _str(inpCorrectionPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        avg[i] = iVwma(_price, (tick_volume[i] if (inpVolume == VOLUME_TICK) else volume[i]), inpPeriod, i, rates_total)
        val[i] = (iCorrMa(_price, avg[i], ª_corrPeriod, i, rates_total) if (ª_corrPeriod > 1) else avg[i])
        start = i - inpFlPeriod + 1
        if start < 0:
            start = 0
        min_ = val[ArrayMinimum(val, start, inpFlPeriod)]
        range_ = (val[ArrayMaximum(val, start, inpFlPeriod)] - min_) / 100.0
        fup[i] = min_ + (inpFlUp * range_)
        fdn[i] = min_ + (inpFlDown * range_)
        mid[i] = (fup[i] + fdn[i]) / 2.0
        avgc[i] = (1 if (avg[i] > val[i]) else 2 if (avg[i] < val[i]) else 0)
        _sw2 = ª_colorOn
        if _sw2 == chg_onOrig:
            valc[i] = avgc[i]
        elif _sw2 == chg_onLevel:
            valc[i] = (1 if (val[i] > fup[i]) else 2 if (val[i] < fdn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        elif _sw2 == chg_onMiddle:
            valc[i] = (1 if (val[i] > mid[i]) else 2 if (val[i] < mid[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        else:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iCorrMa(price, average, period, i, bars, instance=0):
    global _s_iCorrMa_m_arraySize
    if _s_iCorrMa_m_arraySize < bars:
        _res = ArrayResize(_s_iCorrMa_m_array, bars + 500)
        if _res <= bars:
            return 0.0
        _s_iCorrMa_m_arraySize = _res
    _s_iCorrMa_m_array[i][instance].price = price
    _s_iCorrMa_m_array[i][instance].price2 = price * price
    if i > period:
        _s_iCorrMa_m_array[i][instance].summ = _s_iCorrMa_m_array[i - 1][instance].summ + price - _s_iCorrMa_m_array[i - period][instance].price
        _s_iCorrMa_m_array[i][instance].summ2 = _s_iCorrMa_m_array[i - 1][instance].summ2 + _s_iCorrMa_m_array[i][instance].price2 - _s_iCorrMa_m_array[i - period][instance].price2
    else:
        _s_iCorrMa_m_array[i][instance].summ = _s_iCorrMa_m_array[i][instance].price
        _s_iCorrMa_m_array[i][instance].summ2 = _s_iCorrMa_m_array[i][instance].price2
        k = 1
        while k < period and i >= k:
            _s_iCorrMa_m_array[i][instance].summ += _s_iCorrMa_m_array[i - k][instance].price
            _s_iCorrMa_m_array[i][instance].summ2 += _s_iCorrMa_m_array[i - k][instance].price2
            k += 1
    v1 = _fdiv(_s_iCorrMa_m_array[i][instance].summ2 - _fdiv(_s_iCorrMa_m_array[i][instance].summ * _s_iCorrMa_m_array[i][instance].summ, float(period)), float(period))
    v2 = (((_s_iCorrMa_m_array[i - 1][instance].corrected - average) * (_s_iCorrMa_m_array[i - 1][instance].corrected - average)) if (i > 0) else 0)
    c = (0 if (v2 < v1 or v2 == 0) else (1.0 - _fdiv(v1, v2)))
    _s_iCorrMa_m_array[i][instance].corrected = ((_s_iCorrMa_m_array[i - 1][instance].corrected + (c * (average - _s_iCorrMa_m_array[i - 1][instance].corrected))) if (i > 0) else average)
    return _s_iCorrMa_m_array[i][instance].corrected

def iVwma(price, volume, period, i, bars, instance=0):
    global _s_iVwma_m_arraySize
    if _s_iVwma_m_arraySize < bars:
        _res = ArrayResize(_s_iVwma_m_array, bars + 500)
        if _res <= bars:
            return 0.0
        _s_iVwma_m_arraySize = _res
    if volume == 0:
        volume = 1.0
    _s_iVwma_m_array[i][instance].price = volume * price
    _s_iVwma_m_array[i][instance].volume = volume
    if i > period:
        _s_iVwma_m_array[i][instance].sump = _s_iVwma_m_array[i - 1][instance].sump + _s_iVwma_m_array[i][instance].price - _s_iVwma_m_array[i - period][instance].price
        _s_iVwma_m_array[i][instance].sumv = _s_iVwma_m_array[i - 1][instance].sumv + volume - _s_iVwma_m_array[i - period][instance].volume
    else:
        _s_iVwma_m_array[i][instance].sump = _s_iVwma_m_array[i][instance].price
        _s_iVwma_m_array[i][instance].sumv = _s_iVwma_m_array[i][instance].volume
        k = 1
        while k < period and i >= k:
            _s_iVwma_m_array[i][instance].sump += _s_iVwma_m_array[i - k][instance].price
            _s_iVwma_m_array[i][instance].sumv += _s_iVwma_m_array[i - k][instance].volume
            k += 1
    return _fdiv(_s_iVwma_m_array[i][instance].sump, _s_iVwma_m_array[i][instance].sumv)

# ---- static local variables
_s_iCorrMa_m_array = Arr(0, 0, factory=sCorrMaStruct, dims=(1,))
_s_iCorrMa_m_arraySize = 0
_s_iVwma_m_array = Arr(0, 0, factory=sVwmaArrayStruct, dims=(1,))
_s_iVwma_m_arraySize = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrVolumeWeightedMA(_MQL5Indicator):
    name = 'Corr volume weighted MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # VWMA period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume to use
        'inpCorrectionPeriod': 0,  # "Correction" period (<0 no correction,0 or 1 same as average)
        'inpColorOn': _Choice({0: 'change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross', 3: 'Change color on average value cross'}, default=1),  # Color change on :
        'inpFlPeriod': 25,  # Floating levels period
        'inpFlUp': 90.0,  # Upper level %
        'inpFlDown': 10.0,  # Lower level %
    }

