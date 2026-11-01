"""ModifiedStdDev — converted from MQL5: MQL5 Indicators/Modified Standard Deviation.mq5/ModifiedStdDev.mq5

Modified Standard Deviation
Copyright: 2017, stanilevych.com; Link: http://www.stanilevych.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2017, stanilevych.com', 'link': 'http://www.stanilevych.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [255, 32768, 65535]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['Modified Standard Deviation'], 'name': 'ModifiedStdDev', 'source': 'MQL5 Indicators/Modified Standard Deviation.mq5/ModifiedStdDev.mq5', 'folder': 'Modified Standard Deviation.mq5', 'inputs': [{'mql': 'InpStdDevPeriod', 'py': 'InpStdDevPeriod', 'param': 'InpStdDevPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpStdDevShift', 'py': 'InpStdDevShift', 'param': 'InpStdDevShift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpDigits', 'py': 'InpDigits', 'param': 'InpDigits', 'type': 'int', 'default': 5, 'label': 'Accuracy', 'sinput': False}, {'mql': 'InpMessageType', 'py': 'InpMessageType', 'param': 'InpMessageType', 'type': 'int', 'default': 1, 'label': 'Type of messages', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

Green = 0x008000  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# enum MessageType
PushMessage = 0
AlertMessage = 1
LogMessage = 2
_enum('MessageType', {0: 'PushMessage', 1: 'AlertMessage', 2: 'LogMessage'})

# ---- inputs and global variables
InpStdDevPeriod = _input('InpStdDevPeriod', 20)  # Period
InpStdDevShift = _input('InpStdDevShift', 0)  # Shift
InpMAMethod = _input('InpMAMethod', MODE_SMA)  # Method
InpDigits = _input('InpDigits', 5)  # Accuracy
InpMessageType = _input('InpMessageType', AlertMessage)  # Type of messages
ExtStdDevBuffer = Arr(0, 0.0)
ExtMABuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
ExtStdDevPeriod = 0
ExtStdDevShift = 0
rates = 0

def OnInit():
    global ExtStdDevPeriod, ExtStdDevShift
    if InpStdDevPeriod <= 1:
        ExtStdDevPeriod = 20
        printf('Incorrect value for input variable InpStdDevPeriod=%d. Indicator will use value=%d for calculations.', InpStdDevPeriod, ExtStdDevPeriod)
    else:
        ExtStdDevPeriod = InpStdDevPeriod
    if InpStdDevShift < 0:
        ExtStdDevShift = 0
        printf('Incorrect value for input variable InpStdDevShift=%d. Indicator will use value=%d for calculations.', InpStdDevShift, ExtStdDevShift)
    else:
        ExtStdDevShift = InpStdDevShift
    IndicatorSetString(INDICATOR_SHORTNAME, 'StdDev(' + _str(ExtStdDevPeriod) + ')')
    SetIndexBuffer(0, ExtStdDevBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtMABuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetString(0, PLOT_LABEL, 'StdDev(' + _str(ExtStdDevPeriod) + ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, ExtStdDevShift)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, Red)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, Yellow)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, Green)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global rates
    if rates == 0:
        rates = rates_total
    pos = 0
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtStdDevPeriod - 1 + begin)
    if rates_total < ExtStdDevPeriod:
        return 0
    pos = prev_calculated - 1
    if pos < ExtStdDevPeriod:
        pos = ExtStdDevPeriod - 1
        ArrayInitialize(ExtStdDevBuffer, 0.0)
        ArrayInitialize(ColorBuffer, 0.0)
        ArrayInitialize(ExtMABuffer, 0.0)
    _sw1 = InpMAMethod
    if _sw1 == MODE_EMA:
        for i in range(pos, rates_total):
            if i == (InpStdDevPeriod - 1):
                ExtMABuffer[i] = SimpleMA(i, InpStdDevPeriod, price)
            else:
                ExtMABuffer[i] = ExponentialMA(i, InpStdDevPeriod, ExtMABuffer[i - 1], price)
            ExtStdDevBuffer[i] = StdDevFunc(price, ExtMABuffer, i)
            SetColor(i)
    elif _sw1 == MODE_SMMA:
        for i in range(pos, rates_total):
            if i == (InpStdDevPeriod - 1):
                ExtMABuffer[i] = SimpleMA(i, InpStdDevPeriod, price)
            else:
                ExtMABuffer[i] = SmoothedMA(i, InpStdDevPeriod, ExtMABuffer[i - 1], price)
            ExtStdDevBuffer[i] = StdDevFunc(price, ExtMABuffer, i)
            SetColor(i)
    elif _sw1 == MODE_LWMA:
        for i in range(pos, rates_total):
            ExtMABuffer[i] = LinearWeightedMA(i, InpStdDevPeriod, price)
            ExtStdDevBuffer[i] = StdDevFunc(price, ExtMABuffer, i)
            SetColor(i)
    else:
        for i in range(pos, rates_total):
            ExtMABuffer[i] = SimpleMA(i, InpStdDevPeriod, price)
            ExtStdDevBuffer[i] = StdDevFunc(price, ExtMABuffer, i)
            if rates != rates_total:
                Signal(i)
                rates = rates_total
            SetColor(i)
    return rates_total - 1

def StdDevFunc(price, MAprice, position):
    dTmp = 0.0
    for i in range(0, ExtStdDevPeriod):
        dTmp += MathPow(price[position - i] - MAprice[position], 2)
    dTmp = NormalizeDouble(MathSqrt(_fdiv(dTmp, ExtStdDevPeriod)), InpDigits)
    return dTmp

def SetColor(i):
    if ExtStdDevBuffer[i] < ExtStdDevBuffer[i - 1]:
        ColorBuffer[i] = 0.0
    elif ExtStdDevBuffer[i] > ExtStdDevBuffer[i - 1]:
        ColorBuffer[i] = 2.0
    else:
        ColorBuffer[i] = 1.0

def Signal(i):
    message = ''
    if ColorBuffer[i - 1] == 0 and ColorBuffer[i - 2] > 0:
        message = 'Начало падения.'
    elif ColorBuffer[i - 1] == 2 and ColorBuffer[i - 2] < 2:
        message = 'Начало роста.'
    if message != '':
        if InpMessageType == AlertMessage:
            Alert(message)
        if InpMessageType == PushMessage:
            SendNotification(message)
        if InpMessageType == LogMessage:
            Print(message)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ModifiedStdDev(_MQL5Indicator):
    name = 'ModifiedStdDev'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpStdDevPeriod': 20,  # Period
        'InpStdDevShift': 0,  # Shift
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpDigits': 5,  # Accuracy
        'InpMessageType': _Choice({0: 'PushMessage', 1: 'AlertMessage', 2: 'LogMessage'}, default=1),  # Type of messages
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

