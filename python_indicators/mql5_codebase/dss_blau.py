"""DSS Blau — converted from MQL5: MQL5 Indicators/Double smoothed stochastic Blau/DSS Blau.mq5

Double Smoothed Stochastic Blau
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3, 'indicator_minimum': -5.0, 'indicator_maximum': 105.0}, 'types': {1: 7, 2: 8, 3: 1}, 'colors': {1: [16769505, 14803455], 2: [8421504, 16760576, 36095], 3: [12632256]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Fill area', 2: 'DSS', 3: 'DSS signal'}, 'levels': [0.0, 100.0], 'description': ['Double Smoothed Stochastic Blau'], 'name': 'DSS Blau', 'source': 'MQL5 Indicators/Double smoothed stochastic Blau/DSS Blau.mq5', 'folder': 'Double smoothed stochastic Blau', 'inputs': [{'mql': 'inpStoPeriod', 'py': 'inpStoPeriod', 'param': 'inpStoPeriod', 'type': 'int', 'default': 55, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpSmtPeriod1', 'py': 'inpSmtPeriod1', 'param': 'inpSmtPeriod1', 'type': 'int', 'default': 5, 'label': 'Smoothing period 1', 'sinput': False}, {'mql': 'inpSmtPeriod2', 'py': 'inpSmtPeriod2', 'param': 'inpSmtPeriod2', 'type': 'int', 'default': 5, 'label': 'Smoothing period 2', 'sinput': False}, {'mql': 'inpSigPeriod', 'py': 'inpSigPeriod', 'param': 'inpSigPeriod', 'type': 'int', 'default': 5, 'label': 'Signal/trigger period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': -99, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 1
pr_open = 2
pr_high = 3
pr_low = 4
pr_median = 5
pr_typical = 6
pr_weighted = 7
pr_lowhigh = -99
_enum('enPrices', {1: 'pr_close', 2: 'pr_open', 3: 'pr_high', 4: 'pr_low', 5: 'pr_median', 6: 'pr_typical', 7: 'pr_weighted', -99: 'pr_lowhigh'})

# ---- inputs and global variables
inpStoPeriod = _input('inpStoPeriod', 55)  # Stochastic period
inpSmtPeriod1 = _input('inpSmtPeriod1', 5)  # Smoothing period 1
inpSmtPeriod2 = _input('inpSmtPeriod2', 5)  # Smoothing period 2
inpSigPeriod = _input('inpSigPeriod', 5)  # Signal/trigger period
inpPrice = _input('inpPrice', pr_lowhigh)  # Price
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
stc = Arr(0, 0.0)
stcc = Arr(0, 0.0)
sig = Arr(0, 0.0)
ª_sigAlpha = 0.0
ª_sigPeriod = 0

class cDssStochasticBlauWork(MqlObject):
    _q_fields = ('originalPeriod', 'period', 'alpha1', 'alpha2', 'emamaxmin1', 'emamaxmin2', 'emaprcmin1', 'emaprcmin2', 'maxArray', 'minArray')
    def __init__(self):
        self.originalPeriod = 0
        self.period = 0
        self.alpha1 = 0.0
        self.alpha2 = 0.0
        self.emamaxmin1 = Arr(32, 0.0, dyn=False)
        self.emamaxmin2 = Arr(32, 0.0, dyn=False)
        self.emaprcmin1 = Arr(32, 0.0, dyn=False)
        self.emaprcmin2 = Arr(32, 0.0, dyn=False)
        self.maxArray = Arr(0, 0.0)
        self.minArray = Arr(0, 0.0)
        self.originalPeriod = -1
        return
    def _q_dtor(self):
        ArrayFree(self.maxArray)
        ArrayFree(self.minArray)
        return

def OnInit():
    global ª_sigAlpha, ª_sigPeriod
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, stc, INDICATOR_DATA)
    SetIndexBuffer(3, stcc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, sig, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ª_sigPeriod = (inpSigPeriod if (inpSigPeriod > 1) else 1)
    ª_sigAlpha = _fdiv(2.0, 1.0 + ª_sigPeriod)
    _priceType = StringSubstr(EnumToString(inpPrice, 'enPrices'), 3)
    _priceType = ((_priceType + '/' + _priceType) if (_priceType != 'lowhigh') else 'low/high')
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dss Blau ' + _priceType + ' (' + _str(inpStoPeriod) + ',' + _str(inpSmtPeriod1) + ',' + _str(inpSmtPeriod2) + ',' + _str(ª_sigPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = 0.0
        _priceh = 0.0
        _pricel = 0.0
        _sw1 = inpPrice
        if _sw1 == pr_close:
            _pricel = close[i]
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_open:
            _pricel = open[i]
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_high:
            _pricel = high[i]
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_low:
            _pricel = low[i]
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_median:
            _pricel = (high[i] + low[i]) / 2.0
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_typical:
            _pricel = (high[i] + low[i] + close[i]) / 3.0
            _priceh = _pricel
            _price = _priceh
        elif _sw1 == pr_weighted:
            _pricel = (high[i] + low[i] + close[i] + close[i]) / 4.0
            _priceh = _pricel
            _price = _priceh
        else:
            _price = close[i]
            _priceh = high[i]
            _pricel = low[i]
        stc[i] = iDssStochBlau(_price, _priceh, _pricel, inpStoPeriod, inpSmtPeriod1, inpSmtPeriod2, i)
        fillu[i] = stc[i]
        sig[i] = ((sig[i - 1] + (ª_sigAlpha * (stc[i] - sig[i - 1]))) if (i > 0) else 0)
        filld[i] = sig[i]
        stcc[i] = (1 if (stc[i] > sig[i]) else 2)
        i += 1
    return i

def iDssStochBlau(price, priceHigh, priceLow, period, smoothing1, smoothing2, i, instance=0):
    if _s_iDssStochBlau_m_work[instance].originalPeriod != period:
        _s_iDssStochBlau_m_work[instance].originalPeriod = period
        _s_iDssStochBlau_m_work[instance].period = (period if (period > 0) else 1)
        _s_iDssStochBlau_m_work[instance].alpha1 = _fdiv(2.0, 1.0 + (smoothing1 if (smoothing1 > 1) else 1))
        _s_iDssStochBlau_m_work[instance].alpha2 = _fdiv(2.0, 1.0 + (smoothing2 if (smoothing2 > 1) else 1))
        ArrayResize(_s_iDssStochBlau_m_work[instance].maxArray, _s_iDssStochBlau_m_work[instance].period)
        ArrayInitialize(_s_iDssStochBlau_m_work[instance].maxArray, priceHigh)
        ArrayResize(_s_iDssStochBlau_m_work[instance].minArray, _s_iDssStochBlau_m_work[instance].period)
        ArrayInitialize(_s_iDssStochBlau_m_work[instance].minArray, priceLow)
    _poe = _imod(i, 32)
    _pos = _imod(i, _s_iDssStochBlau_m_work[instance].period)
    _s_iDssStochBlau_m_work[instance].minArray[_pos] = priceLow
    _s_iDssStochBlau_m_work[instance].maxArray[_pos] = priceHigh
    if i > 0:
        _pop = _imod(i - 1, 32)
        min_ = _s_iDssStochBlau_m_work[instance].minArray[ArrayMinimum(_s_iDssStochBlau_m_work[instance].minArray)]
        div = _s_iDssStochBlau_m_work[instance].maxArray[ArrayMaximum(_s_iDssStochBlau_m_work[instance].maxArray)] - min_
        _s_iDssStochBlau_m_work[instance].emaprcmin1[_poe] = _s_iDssStochBlau_m_work[instance].emaprcmin1[_pop] + (_s_iDssStochBlau_m_work[instance].alpha1 * (price - min_ - _s_iDssStochBlau_m_work[instance].emaprcmin1[_pop]))
        _s_iDssStochBlau_m_work[instance].emaprcmin2[_poe] = _s_iDssStochBlau_m_work[instance].emaprcmin2[_pop] + (_s_iDssStochBlau_m_work[instance].alpha2 * (_s_iDssStochBlau_m_work[instance].emaprcmin1[_poe] - _s_iDssStochBlau_m_work[instance].emaprcmin2[_pop]))
        _s_iDssStochBlau_m_work[instance].emamaxmin1[_poe] = _s_iDssStochBlau_m_work[instance].emamaxmin1[_pop] + (_s_iDssStochBlau_m_work[instance].alpha1 * (div - _s_iDssStochBlau_m_work[instance].emamaxmin1[_pop]))
        _s_iDssStochBlau_m_work[instance].emamaxmin2[_poe] = _s_iDssStochBlau_m_work[instance].emamaxmin2[_pop] + (_s_iDssStochBlau_m_work[instance].alpha2 * (_s_iDssStochBlau_m_work[instance].emamaxmin1[_poe] - _s_iDssStochBlau_m_work[instance].emamaxmin2[_pop]))
    else:
        _s_iDssStochBlau_m_work[instance].emamaxmin2[_poe] = 0.0
        _s_iDssStochBlau_m_work[instance].emamaxmin1[_poe] = _s_iDssStochBlau_m_work[instance].emamaxmin2[_poe]
        _s_iDssStochBlau_m_work[instance].emaprcmin2[_poe] = _s_iDssStochBlau_m_work[instance].emamaxmin1[_poe]
        _s_iDssStochBlau_m_work[instance].emaprcmin1[_poe] = _s_iDssStochBlau_m_work[instance].emaprcmin2[_poe]
    return (_fdiv(100 * _s_iDssStochBlau_m_work[instance].emaprcmin2[_poe], _s_iDssStochBlau_m_work[instance].emamaxmin2[_poe]) if _s_iDssStochBlau_m_work[instance].emamaxmin2[_poe] else 0)

# ---- static local variables
_s_iDssStochBlau_m_work = Arr(1, 0, dyn=False, factory=cDssStochasticBlauWork)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DSSBlau(_MQL5Indicator):
    name = 'DSS Blau'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpStoPeriod': 55,  # Stochastic period
        'inpSmtPeriod1': 5,  # Smoothing period 1
        'inpSmtPeriod2': 5,  # Smoothing period 2
        'inpSigPeriod': 5,  # Signal/trigger period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted', -99: 'Low/High'}, default=-99),  # Price
    }
    y_range = (-5.0, 105.0)

