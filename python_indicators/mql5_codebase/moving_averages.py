"""moving_averages — converted from MQL5: MQL5 Indicators/Moving Averages with Colors/moving_averages.mq5

Copyright: Mladen; Link: http://www.forex-tsd.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Mladen', 'link': 'http://www.forex-tsd.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Moving average'}, 'levels': [], 'description': [], 'name': 'moving_averages', 'source': 'MQL5 Indicators/Moving Averages with Colors/moving_averages.mq5', 'folder': 'Moving Averages with Colors', 'inputs': [{'mql': 'inpLength', 'py': 'inpLength', 'param': 'inpLength', 'type': 'int', 'default': 14, 'label': 'Moving average period (length)', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'Method', 'py': 'Method', 'param': 'Method', 'type': 'int', 'default': 1, 'label': 'Moving average method', 'sinput': False}, {'mql': 'ColorFrom', 'py': 'ColorFrom', 'param': None, 'type': 'color', 'default': 0, 'label': '"Fast up" color', 'sinput': False}, {'mql': 'ColorTo', 'py': 'ColorTo', 'param': None, 'type': 'color', 'default': 0, 'label': '"Fast down" color', 'sinput': False}, {'mql': 'MaxAngle', 'py': 'MaxAngle', 'param': 'MaxAngle', 'type': 'int', 'default': 20, 'label': 'Angle threshhold for color steps', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DeepPink = 0x9314FF  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name

# ---- inputs and global variables
inpLength = _input('inpLength', 14)  # Moving average period (length)
Price = _input('Price', PRICE_CLOSE)  # Applied price
Method = _input('Method', MODE_EMA)  # Moving average method
MaxAngle = _input('MaxAngle', 20)  # Angle threshhold for color steps
maBuffer = Arr(0, 0.0)
maColors = Arr(0, 0.0)
atrBuffer = Arr(0, 0.0)
maHandle = 0
atrHandle = 0

def OnInit():
    global atrHandle, maHandle
    SetIndexBuffer(0, maBuffer, INDICATOR_DATA)
    ArraySetAsSeries(maBuffer, True)
    SetIndexBuffer(1, maColors, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(maColors, True)
    SetIndexBuffer(2, atrBuffer, INDICATOR_DATA)
    ArraySetAsSeries(atrBuffer, True)
    iLength = (inpLength if (inpLength > 0) else 1)
    maHandle = iMA(None, 0, iLength, 0, Method, Price)
    atrHandle = iATR(None, 0, 100)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 20)
    for i in range(0, 20):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, gradientColor(i, 20, ColorTo, ColorFrom))
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = rates_total - prev_calculated
    if prev_calculated > 0:
        limit += 1
    if prev_calculated == 0:
        limit -= 6 + 1
    if not checkCalculated(maHandle, rates_total, 'averages'):
        return prev_calculated
    if not checkCalculated(atrHandle, rates_total, 'ATR'):
        return prev_calculated
    if not doCopy(maHandle, maBuffer, 0, limit, 'averages'):
        return prev_calculated
    if not doCopy(atrHandle, atrBuffer, 0, limit, 'ATR'):
        return prev_calculated
    for i in range(limit, 0 - 1, -1):
        maColors[i] = slopeColor(i)
    return rates_total

def slopeColor(i):
    range_ = atrBuffer[i]
    angle = 0.0
    change = maBuffer[i] - maBuffer[i + 6]
    if range_ != 0:
        angle = (MathArctan(_fdiv(change, range_ * 6)) * 180.0) / 3.141592653589793
    theColor = _int(round((angle + MaxAngle) / (MaxAngle / 10.0)))
    theColor = ((theColor if (theColor < 20) else 19) if (theColor >= 0) else 0)
    return theColor

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed

def getColor(stepNo, totalSteps, from_, to):
    step = _fdiv(from_ - to, totalSteps - 1.0)
    return _uint(round(from_ - (step * stepNo)))

def checkCalculated(bufferHandle, total, checkDescription):
    calculated = BarsCalculated(bufferHandle)
    if calculated < total:
        Print('Not all data of ' + checkDescription + ' calculated (', _str(total - calculated), ' un-calculated bars )')
        return False
    return True

def doCopy(bufferHandle, buffer, buffNum, copyCount, copyDescription):
    if CopyBuffer(bufferHandle, buffNum, 0, copyCount, buffer) <= 0:
        Print('Getting ' + copyDescription + ' failed! Error', GetLastError())
        return False
    return True

# ---- global variables initialised from expressions
ColorFrom = _input('ColorFrom', _uint(Lime))  # "Fast up" color
ColorTo = _input('ColorTo', _uint(DeepPink))  # "Fast down" color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MovingAverages(_MQL5Indicator):
    name = 'moving_averages'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpLength': 14,  # Moving average period (length)
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Moving average method
        'MaxAngle': 20,  # Angle threshhold for color steps
    }

