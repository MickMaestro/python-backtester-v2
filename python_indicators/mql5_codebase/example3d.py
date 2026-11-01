"""example3D — converted from MQL5: MQL5 Indicators/3D Moving Average Indicator/example3D.mq5

Демонстрация 3D индикатора Moving Average
Copyright: Copyright 2016, DC2008; Link: http://www.mql5.com/ru/users/dc2008; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.m_3d_usc import *  # #include USC.mqh
from backtester.mql5.lib.m_3d_igo import *  # #include IGO.mqh
from backtester.mql5.lib.m_3d_gm import *  # #include GM.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2016, DC2008', 'link': 'http://www.mql5.com/ru/users/dc2008', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Демонстрация 3D индикатора Moving Average'], 'name': 'example3D', 'source': 'MQL5 Indicators/3D Moving Average Indicator/example3D.mq5', 'folder': '3D Moving Average Indicator', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['USC.mqh', 'IGO.mqh', 'GM.mqh']}

# ---- inputs and global variables
fun = Arr(50, 0.0, dyn=False, dims=(20,))  # 3D функция
MA = Arr(0, 0.0)
iMA_handle = Arr(20, 0, dyn=False)
period = Arr.of([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200], fill=0, dyn=False, size=20)

def OnInit():
    USC.Create('3D')
    ArraySetAsSeries(MA, True)
    for i in range(0, 20):
        iMA_handle[i] = iMA(Symbol(), Period(), period[i], 0, MODE_SMA, PRICE_CLOSE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(0, 50):
        for j in range(0, 20):
            CopyBuffer(iMA_handle[j], 0, i * 10, 1, MA)
            fun[i][j] = MA[0]
    for i in range(1, 50):
        for j in range(0, 20):
            p0 = USC.Z(fun[i - 1][j], (i - 1) * 10, (-j) * 10)
            p1 = USC.Z(fun[i][j], i * 10, (-j) * 10)
            name = 'MA(' + _str(period[j]) + ') x' + _str(i) + 'y' + _str(j)
            ObjectCreate(0, name, OBJ_TREND, 0, p0.time, p0.price, p1.time, p1.price)
            if fun[i][j] > USC.m_price and fun[i - 1][j] > USC.m_price:
                ObjectSetInteger(0, name, OBJPROP_COLOR, clrRed)
            else:
                ObjectSetInteger(0, name, OBJPROP_COLOR, clrBlue)
            ObjectSetInteger(0, name, OBJPROP_WIDTH, 1)
            if j == 0 or j == (20 - 1):
                ObjectSetInteger(0, name, OBJPROP_WIDTH, 3)
            ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID)
            ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, False)
            ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, False)
            ObjectSetInteger(0, name, OBJPROP_BACK, True)
            ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    for i in range(0, 50):
        for j in range(1, 20):
            p0 = USC.Z(fun[i][j - 1], i * 10, (-(j - 1)) * 10)
            p1 = USC.Z(fun[i][j], i * 10, (-j) * 10)
            name = 'line yz ' + 'x' + _str(i) + 'y' + _str(j)
            ObjectCreate(0, name, OBJ_TREND, 0, p0.time, p0.price, p1.time, p1.price)
            ObjectSetInteger(0, name, OBJPROP_COLOR, clrGreen)
            ObjectSetInteger(0, name, OBJPROP_WIDTH, 1)
            ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID)
            ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, False)
            ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, False)
            ObjectSetInteger(0, name, OBJPROP_BACK, True)
            ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    USC.OnEvent(id_, lparam, dparam, sparam)

# ---- global variables initialised from expressions
USC = _alloc(CUSC)
USC.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Example3D(_MQL5Indicator):
    name = 'example3D'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

