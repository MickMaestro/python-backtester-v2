"""T3 velocity tape — converted from MQL5: MQL5 Indicators/T3 veocity tape/T3 velocity tape.mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 11, 2: 8, 3: 8}, 'colors': {1: [3329330, 42495], 2: [3329330, 42495], 3: [3329330, 42495]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'T3 velocity histo', 2: 'T3 velocity', 3: 'T3 velocity signal'}, 'levels': [], 'description': [], 'name': 'T3 velocity tape', 'source': 'MQL5 Indicators/T3 veocity tape/T3 velocity tape.mq5', 'folder': 'T3 veocity tape', 'inputs': [{'mql': 'T3Period', 'py': 'T3Period', 'param': 'T3Period', 'type': 'double', 'default': 14.0, 'label': 'T3 velocity calculation period', 'sinput': False}, {'mql': 'T3Hot', 'py': 'T3Hot', 'param': 'T3Hot', 'type': 'double', 'default': 1.0, 'label': 'T3 hot value', 'sinput': False}, {'mql': 'T3Original', 'py': 'T3Original', 'param': 'T3Original', 'type': 'bool', 'default': False, 'label': 'T3 original Tillson calculation?', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'ColorNorm', 'py': 'ColorNorm', 'param': 'ColorNorm', 'type': 'int', 'default': 20, 'label': 'Colors normalization period', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 6333684, 'label': 'Color down', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 16760576, 'label': 'Color Up', 'sinput': False}, {'mql': 'ColorSteps', 'py': 'ColorSteps', 'param': 'ColorSteps', 'type': 'int', 'default': 20, 'label': 'Color steps for drawing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
pr_medianb = 8
pr_tbiased = 9
pr_haclose = 10
pr_haopen = 11
pr_hahigh = 12
pr_halow = 13
pr_hamedian = 14
pr_hatypical = 15
pr_haweighted = 16
pr_haaverage = 17
pr_hamedianb = 18
pr_hatbiased = 19
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_medianb', 9: 'pr_tbiased', 10: 'pr_haclose', 11: 'pr_haopen', 12: 'pr_hahigh', 13: 'pr_halow', 14: 'pr_hamedian', 15: 'pr_hatypical', 16: 'pr_haweighted', 17: 'pr_haaverage', 18: 'pr_hamedianb', 19: 'pr_hatbiased'})

# ---- inputs and global variables
T3Period = _input('T3Period', 14.0)  # T3 velocity calculation period
T3Hot = _input('T3Hot', 1.0)  # T3 hot value
T3Original = _input('T3Original', False)  # T3 original Tillson calculation?
Price = _input('Price', pr_close)  # Price to use
ColorNorm = _input('ColorNorm', 20)  # Colors normalization period
ColorFrom = _input('ColorFrom', clrSandyBrown)  # Color down
ColorTo = _input('ColorTo', clrDeepSkyBlue)  # Color Up
ColorSteps = _input('ColorSteps', 20)  # Color steps for drawing
vel = Arr(0, 0.0)
vel2 = Arr(0, 0.0)
velh = Arr(0, 0.0)
velh2 = Arr(0, 0.0)
colorBuffer = Arr(0, 0.0)
colorBuffer2 = Arr(0, 0.0)
colorBufferh = Arr(0, 0.0)
cSteps = 0
workHa = Arr(0, 0.0, dims=(4,))

class cT3CoeffStruct(MqlObject):
    _q_fields = ('OriginalPeriod', 'OriginalVolume', 'Volume', 'CalcPeriod', 'VolumePlus', 'Alpha')
    def __init__(self):
        self.OriginalPeriod = 0.0
        self.OriginalVolume = 0.0
        self.Volume = 0.0
        self.CalcPeriod = 0.0
        self.VolumePlus = 0.0
        self.Alpha = 0.0
        self.OriginalPeriod = DBL_EPSILON
        self.OriginalVolume = DBL_EPSILON
    def _q_dtor(self):
        pass

def OnInit():
    global cSteps
    SetIndexBuffer(0, velh, INDICATOR_DATA)
    SetIndexBuffer(1, velh2, INDICATOR_DATA)
    SetIndexBuffer(2, colorBufferh, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, vel, INDICATOR_DATA)
    SetIndexBuffer(4, colorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, vel2, INDICATOR_DATA)
    SetIndexBuffer(6, colorBuffer2, INDICATOR_COLOR_INDEX)
    cSteps = (ColorSteps if (ColorSteps > 1) else 2)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, cSteps + 1)
    PlotIndexSetInteger(1, PLOT_COLOR_INDEXES, cSteps + 1)
    PlotIndexSetInteger(2, PLOT_COLOR_INDEXES, cSteps + 1)
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(1, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    i = 0
    while i < (cSteps + 1):
        PlotIndexSetInteger(2, PLOT_LINE_COLOR, i, gradientColor(i, cSteps + 1, ColorFrom, ColorTo))
        i += 1
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        price = getPrice(Price, open, close, high, low, i, rates_total)
        vel[i] = iT3(price, T3Period, T3Hot, T3Original, i, rates_total, 0) - iT3(price, T3Period, T3Hot / 2.0, T3Original, i, rates_total, 1)
        velh[i] = vel[i]
        if i > 0:
            velh2[i] = vel[i - 1]
            vel2[i] = vel[i - 1]
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - ColorNorm + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = vel[ArrayMaximum(vel, start, ColorNorm - 1)]
            _s_OnCalculate_prev_min = vel[ArrayMinimum(vel, start, ColorNorm - 1)]
        max_ = (vel[i] if (vel[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (vel[i] if (vel[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        sto = (_fdiv(100 * (vel[i] - min_), max_ - min_) if (max_ != min_) else 50)
        colorBuffer[i] = _int((sto * cSteps) / 100.0)
        colorBuffer2[i] = colorBuffer[i]
        colorBufferh[i] = colorBuffer[i]
        i += 1
    return i

def iT3(price, period, volumeFactor, original, i, bars, instance=0):
    global _s_iT3_m_arraySize
    if _s_iT3_m_arraySize < bars:
        _s_iT3_m_arraySize = ArrayResize(_s_iT3_m_array, bars + 500)
        if _s_iT3_m_arraySize < bars:
            return 0.0
    if _s_iT3_m_coeff[instance].OriginalPeriod != period or _s_iT3_m_coeff[instance].OriginalVolume != volumeFactor:
        _s_iT3_m_coeff[instance].OriginalPeriod = period
        _s_iT3_m_coeff[instance].OriginalVolume = volumeFactor
        _s_iT3_m_coeff[instance].Volume = ((1 if (volumeFactor > 1) else volumeFactor) if (volumeFactor > 0) else DBL_MIN)
        _s_iT3_m_coeff[instance].VolumePlus = _s_iT3_m_coeff[instance].Volume + 1
        _s_iT3_m_coeff[instance].CalcPeriod = (period if (period > 1) else 1)
        _s_iT3_m_coeff[instance].Alpha = (_fdiv(2.0, 1.0 + _s_iT3_m_coeff[instance].CalcPeriod) if original else _fdiv(2.0, 2.0 + ((_s_iT3_m_coeff[instance].CalcPeriod - 1.0) / 2.0)))
    if i > 0 and _s_iT3_m_coeff[instance].CalcPeriod > 1:
        _s_iT3_m_array[i][instance][0] = _s_iT3_m_array[i - 1][instance][0] + (_s_iT3_m_coeff[instance].Alpha * (price - _s_iT3_m_array[i - 1][instance][0]))
        _s_iT3_m_array[i][instance][1] = _s_iT3_m_array[i - 1][instance][1] + (_s_iT3_m_coeff[instance].Alpha * (_s_iT3_m_array[i][instance][0] - _s_iT3_m_array[i - 1][instance][1]))
        _s_iT3_m_array[i][instance][2] = _s_iT3_m_array[i - 1][instance][2] + (_s_iT3_m_coeff[instance].Alpha * ((_s_iT3_m_array[i][instance][0] * _s_iT3_m_coeff[instance].VolumePlus) - (_s_iT3_m_array[i][instance][1] * _s_iT3_m_coeff[instance].Volume) - _s_iT3_m_array[i - 1][instance][2]))
        _s_iT3_m_array[i][instance][3] = _s_iT3_m_array[i - 1][instance][3] + (_s_iT3_m_coeff[instance].Alpha * (_s_iT3_m_array[i][instance][2] - _s_iT3_m_array[i - 1][instance][3]))
        _s_iT3_m_array[i][instance][4] = _s_iT3_m_array[i - 1][instance][4] + (_s_iT3_m_coeff[instance].Alpha * ((_s_iT3_m_array[i][instance][2] * _s_iT3_m_coeff[instance].VolumePlus) - (_s_iT3_m_array[i][instance][3] * _s_iT3_m_coeff[instance].Volume) - _s_iT3_m_array[i - 1][instance][4]))
        _s_iT3_m_array[i][instance][5] = _s_iT3_m_array[i - 1][instance][5] + (_s_iT3_m_coeff[instance].Alpha * (_s_iT3_m_array[i][instance][4] - _s_iT3_m_array[i - 1][instance][5]))
        _s_iT3_m_array[i][instance][6] = (_s_iT3_m_array[i][instance][4] * _s_iT3_m_coeff[instance].VolumePlus) - (_s_iT3_m_array[i][instance][5] * _s_iT3_m_coeff[instance].Volume)
    else:
        for k in range(0, 7):
            _s_iT3_m_array[i][instance][k] = price
    return _s_iT3_m_array[i][instance][6]

def getPrice(price, open, close, high, low, i, bars):
    if price >= pr_haclose:
        if ArrayRange(workHa, 0) <= bars:
            ArrayResize(workHa, bars + 500)
        haOpen = 0.0
        if i > 0:
            haOpen = (workHa[i - 1][2] + workHa[i - 1][3]) / 2.0
        else:
            haOpen = (open[i] + close[i]) / 2
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        if haOpen < haClose:
            workHa[i][0] = haLow
            workHa[i][1] = haHigh
        else:
            workHa[i][0] = haHigh
            workHa[i][1] = haLow
        workHa[i][2] = haOpen
        workHa[i][3] = haClose
        _sw1 = price
        if _sw1 == pr_haclose:
            return haClose
        elif _sw1 == pr_haopen:
            return haOpen
        elif _sw1 == pr_hahigh:
            return haHigh
        elif _sw1 == pr_halow:
            return haLow
        elif _sw1 == pr_hamedian:
            return (haHigh + haLow) / 2.0
        elif _sw1 == pr_hamedianb:
            return (haOpen + haClose) / 2.0
        elif _sw1 == pr_hatypical:
            return (haHigh + haLow + haClose) / 3.0
        elif _sw1 == pr_haweighted:
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw1 == pr_haaverage:
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw1 == pr_hatbiased:
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
    _sw2 = price
    if _sw2 == pr_close:
        return close[i]
    elif _sw2 == pr_open:
        return open[i]
    elif _sw2 == pr_high:
        return high[i]
    elif _sw2 == pr_low:
        return low[i]
    elif _sw2 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw2 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw2 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw2 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    return 0.0

def getColor(stepNo, totalSteps, from_, to):
    stes = float(totalSteps) - 1.0
    step = _fdiv(from_ - to, stes)
    return _uint(round(from_ - (step * stepNo)))

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0
_s_iT3_m_coeff = Arr(2, 0, dyn=False, factory=cT3CoeffStruct)
_s_iT3_m_array = Arr(0, 0.0, dims=(2, 7,))
_s_iT3_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3VelocityTape(_MQL5Indicator):
    name = 'T3 velocity tape'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'T3Period': 14.0,  # T3 velocity calculation period
        'T3Hot': 1.0,  # T3 hot value
        'T3Original': False,  # T3 original Tillson calculation?
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Heiken ashi close', 11: 'Heiken ashi open', 12: 'Heiken ashi high', 13: 'Heiken ashi low', 14: 'Heiken ashi median', 15: 'Heiken ashi typical', 16: 'Heiken ashi weighted', 17: 'Heiken ashi average', 18: 'Heiken ashi median body', 19: 'Heiken ashi trend biased price'}, default=0),  # Price to use
        'ColorNorm': 20,  # Colors normalization period
        'ColorSteps': 20,  # Color steps for drawing
    }

