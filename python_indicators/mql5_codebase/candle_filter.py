"""Candle_Filter — converted from MQL5: MQL5 Indicators/Candle Filter/Candle_Filter.mq5

Copyright: Copyright 2019-2025, Virologista Kerntopf Corp.; Link: https://www.mql5.com/pt/users/virologustavo/news; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2019-2025, Virologista Kerntopf Corp.', 'link': 'https://www.mql5.com/pt/users/virologustavo/news', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [2263842, 139, 55295, 0]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Candle Filter'}, 'levels': [], 'description': [], 'name': 'Candle_Filter', 'source': 'MQL5 Indicators/Candle Filter/Candle_Filter.mq5', 'folder': 'Candle Filter', 'inputs': [{'mql': 'InpCandleShow', 'py': 'InpCandleShow', 'param': 'InpCandleShow', 'type': 'int', 'default': 0, 'label': 'Tipo de candle a exibir', 'sinput': False}, {'mql': 'InpBullishColor', 'py': 'InpBullishColor', 'param': None, 'type': 'color', 'default': 2263842, 'label': 'Cor dos candles de alta', 'sinput': False}, {'mql': 'InpBearishColor', 'py': 'InpBearishColor', 'param': None, 'type': 'color', 'default': 139, 'label': 'Cor dos candles de baixa', 'sinput': False}, {'mql': 'InpDojiColor', 'py': 'InpDojiColor', 'param': None, 'type': 'color', 'default': 55295, 'label': 'Cor dos candles tipo Doji', 'sinput': False}, {'mql': 'InpBackgroundColor', 'py': 'InpBackgroundColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Cor de fundo no gráfico', 'sinput': False}, {'mql': 'InpDojiThreshold', 'py': 'InpDojiThreshold', 'param': 'InpDojiThreshold', 'type': 'double', 'default': 0.1, 'label': 'Limite para detecção de candles Doji (em %)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum DisplayCandle
ShowBullish = 0
ShowBearish = 1
ShowDoji = 2
ShowAllCandle = 3
_enum('DisplayCandle', {0: 'ShowBullish', 1: 'ShowBearish', 2: 'ShowDoji', 3: 'ShowAllCandle'})

# ---- inputs and global variables
InpCandleShow = _input('InpCandleShow', ShowBullish)  # Tipo de candle a exibir
InpBullishColor = _input('InpBullishColor', clrForestGreen)  # Cor dos candles de alta
InpBearishColor = _input('InpBearishColor', clrDarkRed)  # Cor dos candles de baixa
InpDojiColor = _input('InpDojiColor', clrGold)  # Cor dos candles tipo Doji
InpBackgroundColor = _input('InpBackgroundColor', clrBlack)  # Cor de fundo no gráfico
InpDojiThreshold = _input('InpDojiThreshold', 0.1)  # Limite para detecção de candles Doji (em %)
ExtOpenBuffer = Arr(0, 0.0)  # Buffer para valores de abertura
ExtHighBuffer = Arr(0, 0.0)  # Buffer para valores de máxima
ExtLowBuffer = Arr(0, 0.0)  # Buffer para valores de mínima
ExtCloseBuffer = Arr(0, 0.0)  # Buffer para valores de fechamento
ExtFilterColors = Arr(0, 0.0)  # Buffer para cores

def OnInit():
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtFilterColors, INDICATOR_COLOR_INDEX)
    short_name = StringFormat('Candle Filter', InpBackgroundColor)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 4)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, InpBullishColor)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, InpBearishColor)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, InpDojiColor)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 3, InpBackgroundColor)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    to_copy = 0
    to_copy = (1 if (prev_calculated < 1) else prev_calculated if (rates_total != prev_calculated) else (prev_calculated - 1))
    for i in range(to_copy, rates_total):
        current_open = open[i]
        current_close = close[i]
        current_high = high[i]
        current_low = low[i]
        point_value = SymbolInfoDouble(Symbol(), SYMBOL_POINT)
        is_doji = False
        candle_body = MathAbs(current_close - current_open)
        candle_range = current_high - current_low
        if candle_range > 0:
            is_doji = _fdiv(candle_body, candle_range) <= (InpDojiThreshold / 100.0)
        is_bullish = current_close > current_open
        is_bearish = current_close < current_open
        ExtOpenBuffer[i] = EMPTY_VALUE
        ExtHighBuffer[i] = EMPTY_VALUE
        ExtLowBuffer[i] = EMPTY_VALUE
        ExtCloseBuffer[i] = EMPTY_VALUE
        ExtFilterColors[i] = EMPTY_VALUE
        _sw1 = InpCandleShow
        if _sw1 == ShowBullish:
            if is_bullish:
                ExtOpenBuffer[i] = current_open
                ExtHighBuffer[i] = current_high
                ExtLowBuffer[i] = current_low
                ExtCloseBuffer[i] = current_close
                ExtFilterColors[i] = 0.0
            else:
                ExtOpenBuffer[i] = current_open
                ExtHighBuffer[i] = current_high
                ExtLowBuffer[i] = current_low
                ExtCloseBuffer[i] = current_close
                ExtFilterColors[i] = 3.0
        elif _sw1 == ShowBearish:
            if is_bearish:
                ExtOpenBuffer[i] = current_open
                ExtHighBuffer[i] = current_high
                ExtLowBuffer[i] = current_low
                ExtCloseBuffer[i] = current_close
                ExtFilterColors[i] = 1.0
            else:
                ExtOpenBuffer[i] = current_open
                ExtHighBuffer[i] = current_high
                ExtLowBuffer[i] = current_low
                ExtCloseBuffer[i] = current_close
                ExtFilterColors[i] = 3.0
        elif _sw1 == ShowDoji:
            if is_doji:
                ExtOpenBuffer[i] = current_open
                ExtHighBuffer[i] = current_high
                ExtLowBuffer[i] = current_low
                ExtCloseBuffer[i] = current_close
                ExtFilterColors[i] = 2.0
            else:
                ExtOpenBuffer[i] = current_open
                ExtHighBuffer[i] = current_high
                ExtLowBuffer[i] = current_low
                ExtCloseBuffer[i] = current_close
                ExtFilterColors[i] = 3.0
        elif _sw1 == ShowAllCandle:
            if is_bullish:
                ExtFilterColors[i] = 0.0
            elif is_bearish:
                ExtFilterColors[i] = 1.0
            elif is_doji:
                ExtFilterColors[i] = 2.0
            ExtOpenBuffer[i] = current_open
            ExtHighBuffer[i] = current_high
            ExtLowBuffer[i] = current_low
            ExtCloseBuffer[i] = current_close
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleFilter(_MQL5Indicator):
    name = 'Candle_Filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpCandleShow': _Choice({0: 'Exibir apenas os candles de alta', 1: 'Exibir apenas os candles de baixa', 2: 'Exibir apenas os candles tipo doji', 3: 'Exibir todos os candles'}, default=0),  # Tipo de candle a exibir
        'InpDojiThreshold': 0.1,  # Limite para detecção de candles Doji (em %)
    }

