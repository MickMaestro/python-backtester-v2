"""Cumulative candle subwindow — converted from MQL5: MQL5 Indicators/Cumulative candle subwindow/Cumulative candle subwindow.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [16443110, 3329330]}, 'widths': {1: 5}, 'styles': {1: 0}, 'labels': {1: 'Cumulative'}, 'levels': [], 'description': [], 'name': 'Cumulative candle subwindow', 'source': 'MQL5 Indicators/Cumulative candle subwindow/Cumulative candle subwindow.mq5', 'folder': 'Cumulative candle subwindow', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
ColorColors = Arr(0, 0.0)
m_high = 0.0
m_low = 0.0
m_type = 0

def OnInit():
    SetIndexBuffer(0, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LowBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ColorColors, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global m_high, m_low, m_type
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
        m_high = high[limit]
        m_low = low[limit]
        m_type = (1 if (open[limit] < close[limit]) else -1)
    for i in range(limit, rates_total):
        current_type = (1 if (open[i] < close[i]) else -1)
        if m_type != current_type:
            m_high = high[i]
            m_low = low[i]
            m_type = current_type
        else:
            if high[i] > m_high:
                m_high = high[i]
            if low[i] < m_low:
                m_low = low[i]
            m_type = current_type
        HighBuffer[i] = m_high
        LowBuffer[i] = m_low
        if m_type == 1:
            ColorColors[i] = 0.0
        else:
            ColorColors[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CumulativeCandleSubwindow(_MQL5Indicator):
    name = 'Cumulative candle subwindow'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

