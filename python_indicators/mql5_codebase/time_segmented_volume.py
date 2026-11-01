"""Time Segmented Volume — converted from MQL5: MQL5 Indicators/Time Segmented Volume (TSV)/Time Segmented Volume.mq5

MName
MetaTrader Indicator (Build 
Copyright: MCopyright; Link: MProfile; Version: MVersion

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': 'MVersion', 'copyright': 'MCopyright', 'link': 'MProfile', 'window': 'separate', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 10, 2: 1, 3: 1}, 'colors': {1: [], 2: [], 3: []}, 'widths': {1: 5, 2: 2, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Summation', 2: 'Averaging (simple)', 3: 'Averaging (exponential)'}, 'levels': [], 'description': ['MName', 'MetaTrader Indicator (Build '], 'name': 'Time Segmented Volume', 'source': 'MQL5 Indicators/Time Segmented Volume (TSV)/Time Segmented Volume.mq5', 'folder': 'Time Segmented Volume (TSV)', 'inputs': [{'mql': 'i_nSummationPeriod', 'py': 'i_nSummationPeriod', 'param': 'i_nSummationPeriod', 'type': 'uint', 'default': 13, 'label': 'Summation period', 'sinput': False}, {'mql': 'i_nAveragingPeriod', 'py': 'i_nAveragingPeriod', 'param': 'i_nAveragingPeriod', 'type': 'uint', 'default': 7, 'label': 'Averaging period', 'sinput': False}, {'mql': 'i_ePriceApplied', 'py': 'i_ePriceApplied', 'param': 'i_ePriceApplied', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'i_eVolumeWeight', 'py': 'i_eVolumeWeight', 'param': 'i_eVolumeWeight', 'type': 'int', 'default': 1, 'label': 'Applied volume', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum EVolumeWeight
EVW_None = 0
EVW_TickVolume = 1
EVW_RealVolume = 2
EVW_PriceRange = 3
_enum('EVolumeWeight', {0: 'EVW_None', 1: 'EVW_TickVolume', 2: 'EVW_RealVolume', 3: 'EVW_PriceRange'})

# ---- inputs and global variables
i_nSummationPeriod = _input('i_nSummationPeriod', 13)  # Summation period
i_nAveragingPeriod = _input('i_nAveragingPeriod', 7)  # Averaging period
i_ePriceApplied = _input('i_ePriceApplied', PRICE_CLOSE)  # Applied price
i_eVolumeWeight = _input('i_eVolumeWeight', EVW_TickVolume)  # Applied volume
g_adbPriceApplied = Arr(0, 0.0)  # Buffer for applied price
g_adbVolumePriceDelta = Arr(0, 0.0)  # Buffer for volume weight price delta change
g_adbSummation = Arr(0, 0.0)  # Buffer for summation of volume weighte price change
g_adbSummationSimple = Arr(0, 0.0)  # Buffer for summation of summation for simple averaging
g_adbAveragingSimple = Arr(0, 0.0)  # Buffer for simple averaging
g_adbAveragingExponential = Arr(0, 0.0)  # Buffer for exponential averaging
g_adbSummationColour = Arr(0, 0.0)  # Buffer for summation colourisation
g_dbEmaWeight = 0.0  # Weight to be used for exponential moving averages

def OnInit():
    global g_dbEmaWeight
    if i_nSummationPeriod < 1:
        Print('Error: Invalid ', 'summation period')
        return INIT_PARAMETERS_INCORRECT
    if i_nAveragingPeriod < 1 or i_nAveragingPeriod > i_nSummationPeriod:
        Print('Error: Invalid ', 'averaging period')
        return INIT_PARAMETERS_INCORRECT
    g_dbEmaWeight = _fdiv(2.0, i_nAveragingPeriod + 1.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    iBuffer = 0
    SetIndexBuffer(((iBuffer := iBuffer + 1) - 1), g_adbSummation, INDICATOR_DATA)
    SetIndexBuffer(((iBuffer := iBuffer + 1) - 1), g_adbSummationColour, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(((iBuffer := iBuffer + 1) - 1), g_adbAveragingSimple, INDICATOR_DATA)
    SetIndexBuffer(((iBuffer := iBuffer + 1) - 1), g_adbAveragingExponential, INDICATOR_DATA)
    SetIndexBuffer(((iBuffer := iBuffer + 1) - 1), g_adbPriceApplied, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((iBuffer := iBuffer + 1) - 1), g_adbVolumePriceDelta, INDICATOR_CALCULATIONS)
    SetIndexBuffer(((iBuffer := iBuffer + 1) - 1), g_adbSummationSimple, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Time Segmented Volume (TSV) ( %d, %d )', i_nSummationPeriod, i_nAveragingPeriod))
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    iCur = (0 if (prev_calculated < 1 or prev_calculated > rates_total) else (prev_calculated - 1))
    iPrev = iCur - 1
    iSumPrev = iCur - _int(i_nSummationPeriod)
    iAvgPrev = iCur - _int(i_nAveragingPeriod)
    while True and iCur < rates_total:
        dbVolume = 1.0
        _sw1 = i_eVolumeWeight
        if _sw1 == EVW_RealVolume:
            dbVolume = float(volume[iCur])
        elif _sw1 == EVW_TickVolume:
            dbVolume = float(tick_volume[iCur])
        elif _sw1 == EVW_PriceRange:
            if iPrev >= 0:
                dbClosePrev = close[iPrev]
                dbVolume = fmax(high[iCur], dbClosePrev) - fmin(low[iCur], dbClosePrev)
            else:
                dbVolume = high[iCur] - low[iCur]
        dbPriceCur = 0.0
        _sw2 = i_ePriceApplied
        if _sw2 == PRICE_WEIGHTED:
            dbPriceCur = (high[iCur] + low[iCur] + close[iCur] + close[iCur]) * 0.25
        elif _sw2 == PRICE_TYPICAL:
            dbPriceCur = (high[iCur] + low[iCur] + close[iCur]) / 3.0
        elif _sw2 == PRICE_MEDIAN:
            dbPriceCur = (high[iCur] + low[iCur]) * 0.5
        elif _sw2 == PRICE_HIGH:
            dbPriceCur = high[iCur]
        elif _sw2 == PRICE_LOW:
            dbPriceCur = low[iCur]
        elif _sw2 == PRICE_OPEN:
            dbPriceCur = open[iCur]
        else:
            dbPriceCur = close[iCur]
        dbPricePrev = (g_adbPriceApplied[iPrev] if (iPrev >= 0) else open[iCur])
        dbPriceDelta = dbPriceCur - dbPricePrev
        dbVolumePriceDelta = dbPriceDelta * dbVolume
        dbSummation = dbVolumePriceDelta + (g_adbSummation[iPrev] if (iPrev >= 0) else 0.0) - (g_adbVolumePriceDelta[iSumPrev] if (iSumPrev >= 0) else 0.0)
        dbSummationColour = (1.0 if (dbSummation > 0.0) else 2.0 if (dbSummation < 0.0) else 0.0)
        dbSumSimpleCur = dbSummation + (g_adbSummationSimple[iPrev] if (iPrev >= 0) else 0.0) - (g_adbSummation[iAvgPrev] if (iAvgPrev >= 0) else 0.0)
        dbAverageSimpleCur = dbSumSimpleCur / i_nAveragingPeriod
        dbAverageExponentialPrev = (g_adbAveragingExponential[iPrev] if (iPrev >= 0) else dbSummation)
        dbAverageExponentialCur = dbAverageExponentialPrev + ((dbSummation - dbAverageExponentialPrev) * g_dbEmaWeight)
        g_adbPriceApplied[iCur] = dbPriceCur
        g_adbVolumePriceDelta[iCur] = dbVolumePriceDelta
        g_adbSummation[iCur] = dbSummation
        g_adbSummationSimple[iCur] = dbSumSimpleCur
        g_adbAveragingSimple[iCur] = dbAverageSimpleCur
        g_adbAveragingExponential[iCur] = dbAverageExponentialCur
        g_adbSummationColour[iCur] = dbSummationColour
        iCur += 1
        iPrev += 1
        iSumPrev += 1
        iAvgPrev += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TimeSegmentedVolume(_MQL5Indicator):
    name = 'Time Segmented Volume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'i_nSummationPeriod': 13,  # Summation period
        'i_nAveragingPeriod': 7,  # Averaging period
        'i_ePriceApplied': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'i_eVolumeWeight': _Choice({0: 'No volume weighting', 1: 'Tick volume', 2: 'Real volume', 3: 'True price range (pseudo volume)'}, default=1),  # Applied volume
    }

