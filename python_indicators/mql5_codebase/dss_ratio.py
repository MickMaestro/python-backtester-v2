"""DSS ratio — converted from MQL5: MQL5 Indicators/Double smoothed stochastic of ratio/DSS ratio.mq5

Double Smoothed Stochastic - of \\"ratio\\"
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3, 'indicator_minimum': -5.0, 'indicator_maximum': 105.0}, 'types': {1: 7, 2: 8, 3: 1}, 'colors': {1: [16769505, 14803455], 2: [16760576, 36095], 3: [12632256]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Fill area', 2: 'DSS', 3: 'DSS signal'}, 'levels': [0.0, 100.0], 'description': ['Double Smoothed Stochastic - of \\"ratio\\"'], 'name': 'DSS ratio', 'source': 'MQL5 Indicators/Double smoothed stochastic of ratio/DSS ratio.mq5', 'folder': 'Double smoothed stochastic of ratio', 'inputs': [{'mql': 'inpStoPeriod', 'py': 'inpStoPeriod', 'param': 'inpStoPeriod', 'type': 'int', 'default': 55, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpSmtPeriod', 'py': 'inpSmtPeriod', 'param': 'inpSmtPeriod', 'type': 'int', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpSigPeriod', 'py': 'inpSigPeriod', 'param': 'inpSigPeriod', 'type': 'int', 'default': 5, 'label': 'Signal/trigger period', 'sinput': False}, {'mql': 'inpRafPeriod', 'py': 'inpRafPeriod', 'param': 'inpRafPeriod', 'type': 'int', 'default': 5, 'label': 'Fast ratio period', 'sinput': False}, {'mql': 'inpRasPeriod', 'py': 'inpRasPeriod', 'param': 'inpRasPeriod', 'type': 'int', 'default': 20, 'label': 'Slow ratio period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpStoPeriod = _input('inpStoPeriod', 55)  # Stochastic period
inpSmtPeriod = _input('inpSmtPeriod', 5)  # Smoothing period
inpSigPeriod = _input('inpSigPeriod', 5)  # Signal/trigger period
inpRafPeriod = _input('inpRafPeriod', 5)  # Fast ratio period
inpRasPeriod = _input('inpRasPeriod', 20)  # Slow ratio period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
stc = Arr(0, 0.0)
stcc = Arr(0, 0.0)
sig = Arr(0, 0.0)
ratiof = Arr(0, 0.0)
ratios = Arr(0, 0.0)
ª_sigAlpha = 0.0
ª_rafAlpha = 0.0
ª_rasAlpha = 0.0
ª_sigPeriod = 0
ª_rafPeriod = 0
ª_rasPeriod = 0

class cDssStochasticWork(MqlObject):
    _q_fields = ('originalPeriod', 'period', 'alpha', 'ema1', 'ema2', 'maxArray', 'minArray', 'workArray')
    def __init__(self):
        self.originalPeriod = 0
        self.period = 0
        self.alpha = 0.0
        self.ema1 = Arr(32, 0.0, dyn=False)
        self.ema2 = Arr(32, 0.0, dyn=False)
        self.maxArray = Arr(0, 0.0)
        self.minArray = Arr(0, 0.0)
        self.workArray = Arr(0, 0.0)
        self.originalPeriod = -1
        return
    def _q_dtor(self):
        ArrayFree(self.maxArray)
        ArrayFree(self.minArray)
        ArrayFree(self.workArray)
        return

def OnInit():
    global ª_rafAlpha, ª_rafPeriod, ª_rasAlpha, ª_rasPeriod, ª_sigAlpha, ª_sigPeriod
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, stc, INDICATOR_DATA)
    SetIndexBuffer(3, stcc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, sig, INDICATOR_DATA)
    SetIndexBuffer(5, ratiof, INDICATOR_DATA)
    SetIndexBuffer(6, ratios, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ª_rafPeriod = (inpRafPeriod if (inpRafPeriod > 1) else 1)
    ª_rasPeriod = (inpRasPeriod if (inpRasPeriod > 1) else 1)
    if ª_rafPeriod == ª_rasPeriod:
        Alert('Fast and slow ratio period can not be the same')
        return INIT_FAILED
    ª_sigPeriod = (inpSigPeriod if (inpSigPeriod > 1) else 1)
    ª_sigAlpha = _fdiv(2.0, 1.0 + ª_sigPeriod)
    ª_rafAlpha = _fdiv(2.0, 1.0 + MathMin(ª_rafPeriod, ª_rasPeriod))
    ª_rasAlpha = _fdiv(2.0, 1.0 + MathMax(ª_rafPeriod, ª_rasPeriod))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dss of "ratio" (' + _str(inpStoPeriod) + ',' + _str(inpSmtPeriod) + ',' + _str(ª_sigPeriod) + ')(' + _str(ª_rafPeriod) + ',' + _str(ª_rasPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _rawPrice = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _rawPrice = close[i]
        elif _sw1 == PRICE_OPEN:
            _rawPrice = open[i]
        elif _sw1 == PRICE_HIGH:
            _rawPrice = high[i]
        elif _sw1 == PRICE_LOW:
            _rawPrice = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _rawPrice = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _rawPrice = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _rawPrice = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _rawPrice = 0.0
        ratiof[i] = ((ratiof[i - 1] + (ª_rafAlpha * (_rawPrice - ratiof[i - 1]))) if (i > 0) else close[i])
        ratios[i] = ((ratios[i - 1] + (ª_rasAlpha * (_rawPrice - ratios[i - 1]))) if (i > 0) else close[i])
        _price = _fdiv(ratiof[i], ratios[i])
        stc[i] = iDssStoch(_price, _price, _price, inpStoPeriod, inpSmtPeriod, i)
        fillu[i] = stc[i]
        sig[i] = ((sig[i - 1] + (ª_sigAlpha * (stc[i] - sig[i - 1]))) if (i > 0) else 0)
        filld[i] = sig[i]
        stcc[i] = (0 if (stc[i] > sig[i]) else 1)
        i += 1
    return i

def iDssStoch(price, priceHigh, priceLow, period, smoothing, i, instance=0):
    if _s_iDssStoch_m_work[instance].originalPeriod != period:
        _s_iDssStoch_m_work[instance].originalPeriod = period
        _s_iDssStoch_m_work[instance].period = (period if (period > 0) else 1)
        _s_iDssStoch_m_work[instance].alpha = _fdiv(2.0, 1.0 + (smoothing if (smoothing > 1) else 1))
        ArrayResize(_s_iDssStoch_m_work[instance].maxArray, _s_iDssStoch_m_work[instance].period)
        ArrayInitialize(_s_iDssStoch_m_work[instance].maxArray, priceHigh)
        ArrayResize(_s_iDssStoch_m_work[instance].minArray, _s_iDssStoch_m_work[instance].period)
        ArrayInitialize(_s_iDssStoch_m_work[instance].minArray, priceLow)
        ArrayResize(_s_iDssStoch_m_work[instance].workArray, _s_iDssStoch_m_work[instance].period)
        ArrayInitialize(_s_iDssStoch_m_work[instance].workArray, 0.5)
    _poe = _imod(i, 32)
    _pos = _imod(i, _s_iDssStoch_m_work[instance].period)
    _s_iDssStoch_m_work[instance].minArray[_pos] = priceLow
    _s_iDssStoch_m_work[instance].maxArray[_pos] = priceHigh
    if i > 0:
        _pop = _imod(i - 1, 32)
        min_ = _s_iDssStoch_m_work[instance].minArray[ArrayMinimum(_s_iDssStoch_m_work[instance].minArray)]
        div = _s_iDssStoch_m_work[instance].maxArray[ArrayMaximum(_s_iDssStoch_m_work[instance].maxArray)] - min_
        _s_iDssStoch_m_work[instance].ema1[_poe] = _s_iDssStoch_m_work[instance].ema1[_pop] + (_s_iDssStoch_m_work[instance].alpha * ((_fdiv(price - min_, div) if div else 0) - _s_iDssStoch_m_work[instance].ema1[_pop]))
        _s_iDssStoch_m_work[instance].workArray[_pos] = _s_iDssStoch_m_work[instance].ema1[_poe]
        min_ = _s_iDssStoch_m_work[instance].workArray[ArrayMinimum(_s_iDssStoch_m_work[instance].workArray)]
        div = _s_iDssStoch_m_work[instance].workArray[ArrayMaximum(_s_iDssStoch_m_work[instance].workArray)] - min_
        _s_iDssStoch_m_work[instance].ema2[_poe] = _s_iDssStoch_m_work[instance].ema2[_pop] + (_s_iDssStoch_m_work[instance].alpha * ((_fdiv(_s_iDssStoch_m_work[instance].ema1[_poe] - min_, div) if div else _s_iDssStoch_m_work[instance].ema1[_poe]) - _s_iDssStoch_m_work[instance].ema2[_pop]))
    else:
        _s_iDssStoch_m_work[instance].ema1[_poe] = 0.0
        _s_iDssStoch_m_work[instance].ema2[_poe] = _s_iDssStoch_m_work[instance].ema1[_poe]
    return 100 * _s_iDssStoch_m_work[instance].ema2[_poe]

# ---- static local variables
_s_iDssStoch_m_work = Arr(1, 0, dyn=False, factory=cDssStochasticWork)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DSSRatio(_MQL5Indicator):
    name = 'DSS ratio'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpStoPeriod': 55,  # Stochastic period
        'inpSmtPeriod': 5,  # Smoothing period
        'inpSigPeriod': 5,  # Signal/trigger period
        'inpRafPeriod': 5,  # Fast ratio period
        'inpRasPeriod': 20,  # Slow ratio period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }
    y_range = (-5.0, 105.0)

