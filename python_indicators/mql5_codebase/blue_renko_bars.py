"""Blue Renko Bars — converted from MQL5: MQL5 Indicators/Blue Renko Bars/Blue Renko Bars.mq5

Simplest Renko Chart Indicator for MetaTrader 5
Copyright: © SharmuttaDJ, 2018; Link: https://www.mql5.com/ru/users/sharmuttadj/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© SharmuttaDJ, 2018', 'link': 'https://www.mql5.com/ru/users/sharmuttadj/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 15}, 'colors': {1: [16748574, 16760576, 0]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': ['Simplest Renko Chart Indicator for MetaTrader 5'], 'name': 'Blue Renko Bars', 'source': 'MQL5 Indicators/Blue Renko Bars/Blue Renko Bars.mq5', 'folder': 'Blue Renko Bars', 'inputs': [{'mql': 'BrickSize', 'py': 'BrickSize', 'param': 'BrickSize', 'type': 'int', 'default': 10, 'label': 'Brick Size', 'sinput': False}, {'mql': 'ShowWicks', 'py': 'ShowWicks', 'param': 'ShowWicks', 'type': 'bool', 'default': True, 'label': 'Show Wicks', 'sinput': False}, {'mql': 'TotalBars', 'py': 'TotalBars', 'param': 'TotalBars', 'type': 'bool', 'default': False, 'label': 'Use full history', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BrickSize = _input('BrickSize', 10)  # Brick Size
ShowWicks = _input('ShowWicks', True)  # Show Wicks
TotalBars = _input('TotalBars', False)  # Use full history
RedrawChart = 1  # Redraw Renko Chart Bars
BarsCount = 500  # Bars Count
OpenBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
brickColors = Arr(0, 0.0)
brickSize = 0.0
upWick = 0.0
downWick = 0.0

def OnInit():
    global BarsCount, brickSize
    brickSize = BrickSize * Point()
    if brickSize < (Point() * 1):
        brickSize = Point() * 1
        Print('Brick size must be a minimum value of ', brickSize)
    if TotalBars == True:
        BarsCount = total
    elif brickSize > 1:
        BarsCount = BarsCount * _int(brickSize)
    brickSize = NormalizeDouble(brickSize, Digits())
    SetIndexBuffer(0, OpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, CloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, brickColors, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(OpenBuffer, True)
    ArraySetAsSeries(HighBuffer, True)
    ArraySetAsSeries(LowBuffer, True)
    ArraySetAsSeries(CloseBuffer, True)
    ArraySetAsSeries(brickColors, True)
    ArraySetAsSeries(renkoBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    title = '-=BLUErenkoBARS=- ('
    title += '[' + _str(BrickSize) + ' Pips])'
    IndicatorSetString(INDICATOR_SHORTNAME, title)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global total
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    size = ArraySize(renkoBuffer)
    if size == 0:
        m1Buffer = Arr(0, 0, factory=MqlRates)
        ArraySetAsSeries(m1Buffer, True)
        total = CopyRates(Symbol(), PERIOD_M1, 0, BarsCount, m1Buffer)
        if total < 0:
            Comment('Failed to copy history data for the M1 time frame. Error #', GetLastError(), '. Retry...')
            return 0
        Comment('Reading history... 0% [0 of ', total, ']')
        gap = 0.0
        up = 0.0
        down = 0.0
        progress = 0.0
        for i in range(total - 2, 0 - 1, -1):
            gap = MathAbs(m1Buffer[i].open - m1Buffer[i + 1].close)
            up = m1Buffer[i].high - MathMax(m1Buffer[i].open, m1Buffer[i].close)
            down = MathMin(m1Buffer[i].open, m1Buffer[i].close) - m1Buffer[i].low
            if gap > brickSize:
                Renko(m1Buffer[i].open)
            if m1Buffer[i].open < m1Buffer[i].close:
                if down > brickSize:
                    Renko(m1Buffer[i].low)
                if up > brickSize:
                    Renko(m1Buffer[i].high)
            else:
                if up > brickSize:
                    Renko(m1Buffer[i].high)
                if down > brickSize:
                    Renko(m1Buffer[i].low)
            Renko(m1Buffer[i].close)
            progress = 100 - _idiv(i * 100, total)
            if _imod(i, 50) == 0:
                Comment('Reading history... ', progress, '% [', total - i, ' of ', total, ']')
        Comment('')
    Renko(close[0])
    size = ArraySize(renkoBuffer)
    first = 0
    if prev_calculated == 0:
        first = (size if (rates_total > size) else rates_total)
    else:
        first = _int(MathMax(RedrawChart, ChartGetInteger(0, CHART_VISIBLE_BARS, 0)))
    for i in range(first - 2, 0 - 1, -1):
        OpenBuffer[i + 1] = renkoBuffer[i].open
        HighBuffer[i + 1] = renkoBuffer[i].high
        LowBuffer[i + 1] = renkoBuffer[i].low
        CloseBuffer[i + 1] = renkoBuffer[i].close
        brickColors[i + 1] = (1 if (renkoBuffer[i].close > renkoBuffer[i + 1].close) else 0)
        if i == 0:
            OpenBuffer[i] = renkoBuffer[i].close
            HighBuffer[i] = upWick
            LowBuffer[i] = downWick
            CloseBuffer[i] = close[i]
            brickColors[i] = brickColors[i + 1]
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, close[0])
    return rates_total

def RenkoAdd():
    size = ArraySize(renkoBuffer)
    ArrayResize(renkoBuffer, size + 1, 10000)
    ArrayCopy(renkoBuffer, renkoBuffer, 1, 0, size)

def RenkoUp(points):
    global downWick, upWick
    RenkoAdd()
    renkoBuffer[0].open = renkoBuffer[1].close + points - brickSize
    renkoBuffer[0].high = renkoBuffer[1].close + points
    renkoBuffer[0].low = renkoBuffer[1].close
    if ShowWicks and downWick < renkoBuffer[1].close:
        renkoBuffer[0].low = downWick
    else:
        renkoBuffer[0].low = renkoBuffer[0].open
    renkoBuffer[0].close = renkoBuffer[1].close + points
    downWick = renkoBuffer[0].close
    upWick = downWick

def RenkoDown(points):
    global downWick, upWick
    RenkoAdd()
    renkoBuffer[0].open = renkoBuffer[1].close - points + brickSize
    if ShowWicks and upWick > renkoBuffer[1].close:
        renkoBuffer[0].high = upWick
    else:
        renkoBuffer[0].high = renkoBuffer[0].open
    renkoBuffer[0].low = renkoBuffer[1].close - points
    renkoBuffer[0].close = renkoBuffer[1].close - points
    downWick = renkoBuffer[0].close
    upWick = downWick

def Renko(price):
    global downWick, upWick
    size = ArraySize(renkoBuffer)
    upWick = MathMax(upWick, price)
    downWick = MathMin(downWick, price)
    if size == 0:
        RenkoAdd()
        renkoBuffer[0].close = NormalizeDouble(MathFloor(_fdiv(price, brickSize)) * brickSize, Digits())
        renkoBuffer[0].high = renkoBuffer[0].close
        renkoBuffer[0].low = renkoBuffer[0].close - brickSize
        renkoBuffer[0].open = renkoBuffer[0].low
    elif size < 2:
        while price > (renkoBuffer[0].close + brickSize):
            RenkoUp(brickSize)
        while price < (renkoBuffer[0].close - brickSize):
            RenkoDown(brickSize)
    else:
        if renkoBuffer[0].close > renkoBuffer[1].close:
            if price > (renkoBuffer[0].close + brickSize):
                while price > (renkoBuffer[0].close + brickSize):
                    RenkoUp(brickSize)
            elif price < (renkoBuffer[0].close - (2 * brickSize)):
                RenkoDown(2 * brickSize)
                while price < (renkoBuffer[1].close - brickSize):
                    RenkoDown(brickSize)
        if renkoBuffer[0].close < renkoBuffer[1].close:
            if price < (renkoBuffer[0].close - brickSize):
                while price < (renkoBuffer[0].close - brickSize):
                    RenkoDown(brickSize)
            elif price > (renkoBuffer[0].close + (2 * brickSize)):
                RenkoUp(2 * brickSize)
                while price > (renkoBuffer[0].close + brickSize):
                    RenkoUp(brickSize)
    return

# ---- global variables initialised from expressions
renkoBuffer = Arr(0, 0, factory=MqlRates)
total = Bars(Symbol(), PERIOD_M1)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlueRenkoBars(_MQL5Indicator):
    name = 'Blue Renko Bars'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BrickSize': 10,  # Brick Size
        'ShowWicks': True,  # Show Wicks
        'TotalBars': False,  # Use full history
    }

