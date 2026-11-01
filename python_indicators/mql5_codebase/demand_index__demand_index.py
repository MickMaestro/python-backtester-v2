"""Demand_Index — converted from MQL5: MQL5 Indicators/Demand_Index/Demand_Index.mq5

Demand Index by James Sibbet
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2263842]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Demand Idx'}, 'levels': [], 'description': ['Demand Index by James Sibbet'], 'name': 'Demand_Index', 'source': 'MQL5 Indicators/Demand_Index/Demand_Index.mq5', 'folder': 'Demand_Index', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 5, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 5)  # Period
BufferDI = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferBuyPres = Arr(0, 0.0)
BufferSellPres = Arr(0, 0.0)
BufferTR = Arr(0, 0.0)
BufferVolAvg = Arr(0, 0.0)
BufferWghtClose = Arr(0, 0.0)
period_ind = 0

def OnInit():
    global period_ind
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferDI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferBuyPres, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSellPres, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferTR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferVolAvg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferWghtClose, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Demand Index (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDI, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferBuyPres, True)
    ArraySetAsSeries(BufferSellPres, True)
    ArraySetAsSeries(BufferTR, True)
    ArraySetAsSeries(BufferVolAvg, True)
    ArraySetAsSeries(BufferWghtClose, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_ind, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ind - 2
        ArrayInitialize(BufferDI, EMPTY_VALUE)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferBuyPres, 0)
        ArrayInitialize(BufferSellPres, 0)
        ArrayInitialize(BufferTR, 0)
        ArrayInitialize(BufferVolAvg, 0)
        ArrayInitialize(BufferWghtClose, 0)
    for i in range(limit, 0 - 1, -1):
        BufferVol[i] = float(tick_volume[i])
        BufferWghtClose[i] = ((2.0 * close[i]) + high[i] + low[i]) / 4.0
        BufferTR[i] = fmax(high[i], high[i + 1]) - fmin(low[i], low[i + 1])
    for i in range(limit, 0 - 1, -1):
        BufferVolAvg[i] = (GetSMA(rates_total, i, period_ind, BufferVol) if (i == (rates_total - period_ind - 2)) else _fdiv((BufferVolAvg[i + 1] * (period_ind - 1.0)) + tick_volume[i], period_ind))
        AvgTR = GetSMA(rates_total, i, period_ind, BufferTR)
        if ((BufferWghtClose[i] != 0 and BufferWghtClose[i + 1] != 0) and AvgTR != 0) and BufferVolAvg[i] != 0:
            WtCRatio = _fdiv(BufferWghtClose[i] - BufferWghtClose[i + 1], fmin(BufferWghtClose[i], BufferWghtClose[i + 1]))
            VolRatio = _fdiv(tick_volume[i], BufferVolAvg[i])
            Constant = _fdiv(VolRatio, exp(fmin(_fdiv(3.0 * fabs(WtCRatio) * BufferWghtClose[i], AvgTR), 88.0)))
            BuyP = 0.0
            SellP = 0.0
            if WtCRatio > 0:
                BuyP = VolRatio
                SellP = Constant
            else:
                BuyP = Constant
                SellP = VolRatio
            BufferBuyPres[i] = _fdiv((BufferBuyPres[i + 1] * (period_ind - 1.0)) + BuyP, period_ind)
            BufferSellPres[i] = _fdiv((BufferSellPres[i + 1] * (period_ind - 1.0)) + SellP, period_ind)
            TempDI = 1.0
            Sign = 0.0
            if BufferSellPres[i] > BufferBuyPres[i]:
                Sign = -1.0
                if BufferSellPres[i] != 0:
                    TempDI = _fdiv(BufferBuyPres[i], BufferSellPres[i])
            else:
                Sign = 1.0
                if BufferBuyPres[i] != 0:
                    TempDI = _fdiv(BufferSellPres[i], BufferBuyPres[i])
            TempDI *= Sign
            BufferDI[i] = _fdiv(((-1.0 - TempDI) if (TempDI < 0) else (1.0 - TempDI)), Point())
        else:
            BufferDI[i] = 0.0
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DemandIndex(_MQL5Indicator):
    name = 'Demand_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 5,  # Period
    }

