"""cambiar el color de velas y mecha — converted from MQL5: MQL5 Indicators/Change the colour of candles and wick/cambiar el color de velas y mecha.mq5

Copyright: Copyright 2022, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 3}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'cambiar el color de velas y mecha', 'source': 'MQL5 Indicators/Change the colour of candles and wick/cambiar el color de velas y mecha.mq5', 'folder': 'Change the colour of candles and wick', 'inputs': [{'mql': '____________CONFIGURACIÓN___________________', 'py': '____________CONFIGURACIÓN___________________', 'param': None, 'type': 'string', 'default': '========= CAMBIAR COLOR DE VELAS Y MECHA =========', 'label': '', 'sinput': False}, {'mql': 'APAGAR_MECHA_DE_LA_VELA', 'py': 'APAGAR_MECHA_DE_LA_VELA', 'param': 'APAGAR_MECHA_DE_LA_VELA', 'type': 'int', 'default': 0, 'label': 'Encender/apagar la mecha', 'sinput': False}, {'mql': 'ANCHO_DE_LA_MECHA', 'py': 'ANCHO_DE_LA_MECHA', 'param': 'ANCHO_DE_LA_MECHA', 'type': 'int', 'default': 1, 'label': 'Grosor de la línea de la mecha', 'sinput': False}, {'mql': 'COLOR_DEL_CUERPO_DE_LA_VELA_ALCISTA', 'py': 'COLOR_DEL_CUERPO_DE_LA_VELA_ALCISTA', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Color vela alcista', 'sinput': False}, {'mql': 'COLOR_DEL_CUERPO_DE_LA_VELA_BAJISTA', 'py': 'COLOR_DEL_CUERPO_DE_LA_VELA_BAJISTA', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color vela bajista', 'sinput': False}, {'mql': 'COLOR_DE_LA_MECHA', 'py': 'COLOR_DE_LA_MECHA', 'param': None, 'type': 'color', 'default': 16777215, 'label': 'Color de la mecha (wick)', 'sinput': False}, {'mql': 'FONDO_DE_COLOR_EN_EL_PRIMER_PLANO_DEL_GRAFICO', 'py': 'FONDO_DE_COLOR_EN_EL_PRIMER_PLANO_DEL_GRAFICO', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color texto', 'sinput': False}, {'mql': 'FONDO_DE_COLOR_EN_EL_GRAFICO', 'py': 'FONDO_DE_COLOR_EN_EL_GRAFICO', 'param': None, 'type': 'color', 'default': 0, 'label': 'Fondo del gráfico', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum APAGAR
ENCIENDE = 0
APAGA = 1
_enum('APAGAR', {0: 'ENCIENDE', 1: 'APAGA'})

# ---- inputs and global variables
BUFFER_WICK_TOP = Arr(0, 0.0)  # Puntero a la mecha superior
BUFFER_WICK_BOTTOM = Arr(0, 0.0)  # Puntero a la mecha inferior
BUFFER_ALCISTA_OPEN = Arr(0, 0.0)  # Precio de apertura
BUFFER_ALCISTA_HIGH = Arr(0, 0.0)  # Precio máximo
BUFFER_ALCISTA_LOW = Arr(0, 0.0)  # Precio mínimo
BUFFER_ALCISTA_CLOSE = Arr(0, 0.0)  # Precio de cierre
BUFFER_BAJISTA_OPEN = Arr(0, 0.0)
BUFFER_BAJISTA_HIGH = Arr(0, 0.0)
BUFFER_BAJISTA_LOW = Arr(0, 0.0)
BUFFER_BAJISTA_CLOSE = Arr(0, 0.0)
____________CONFIGURACIÓN___________________ = _input('____________CONFIGURACIÓN___________________', '========= CAMBIAR COLOR DE VELAS Y MECHA =========')
APAGAR_MECHA_DE_LA_VELA = _input('APAGAR_MECHA_DE_LA_VELA', ENCIENDE)  # Encender/apagar la mecha
ANCHO_DE_LA_MECHA = _input('ANCHO_DE_LA_MECHA', 1)  # Grosor de la línea de la mecha
COLOR_DEL_CUERPO_DE_LA_VELA_ALCISTA = _input('COLOR_DEL_CUERPO_DE_LA_VELA_ALCISTA', clrGreen)  # Color vela alcista
COLOR_DEL_CUERPO_DE_LA_VELA_BAJISTA = _input('COLOR_DEL_CUERPO_DE_LA_VELA_BAJISTA', clrRed)  # Color vela bajista
COLOR_DE_LA_MECHA = _input('COLOR_DE_LA_MECHA', clrWhite)  # Color de la mecha (wick)
FONDO_DE_COLOR_EN_EL_PRIMER_PLANO_DEL_GRAFICO = _input('FONDO_DE_COLOR_EN_EL_PRIMER_PLANO_DEL_GRAFICO', clrRed)  # Color texto
FONDO_DE_COLOR_EN_EL_GRAFICO = _input('FONDO_DE_COLOR_EN_EL_GRAFICO', clrBlack)  # Fondo del gráfico

def OnInit():
    SetIndexBuffer(0, BUFFER_WICK_TOP, INDICATOR_DATA)
    SetIndexBuffer(1, BUFFER_WICK_BOTTOM, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_HISTOGRAM2)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, COLOR_DE_LA_MECHA)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, ANCHO_DE_LA_MECHA)
    PlotIndexSetString(0, PLOT_LABEL, 'Wicks')
    SetIndexBuffer(2, BUFFER_ALCISTA_OPEN, INDICATOR_DATA)
    SetIndexBuffer(3, BUFFER_ALCISTA_HIGH, INDICATOR_DATA)
    SetIndexBuffer(4, BUFFER_ALCISTA_LOW, INDICATOR_DATA)
    SetIndexBuffer(5, BUFFER_ALCISTA_CLOSE, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_CANDLES)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, COLOR_DEL_CUERPO_DE_LA_VELA_ALCISTA)
    PlotIndexSetString(1, PLOT_LABEL, 'Bullish Candles')
    SetIndexBuffer(6, BUFFER_BAJISTA_OPEN, INDICATOR_DATA)
    SetIndexBuffer(7, BUFFER_BAJISTA_HIGH, INDICATOR_DATA)
    SetIndexBuffer(8, BUFFER_BAJISTA_LOW, INDICATOR_DATA)
    SetIndexBuffer(9, BUFFER_BAJISTA_CLOSE, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_CANDLES)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, COLOR_DEL_CUERPO_DE_LA_VELA_BAJISTA)
    PlotIndexSetString(2, PLOT_LABEL, 'Bearish Candles')
    ChartSetInteger(ChartID(), CHART_MODE, CHART_CANDLES)
    ChartSetInteger(ChartID(), CHART_FOREGROUND, APAGAR_MECHA_DE_LA_VELA)
    ChartSetInteger(ChartID(), CHART_COLOR_BACKGROUND, FONDO_DE_COLOR_EN_EL_GRAFICO)
    ChartSetInteger(ChartID(), CHART_COLOR_FOREGROUND, FONDO_DE_COLOR_EN_EL_PRIMER_PLANO_DEL_GRAFICO)
    ChartSetInteger(ChartID(), CHART_COLOR_CANDLE_BULL, COLOR_DEL_CUERPO_DE_LA_VELA_ALCISTA)
    ChartSetInteger(ChartID(), CHART_COLOR_CANDLE_BEAR, COLOR_DEL_CUERPO_DE_LA_VELA_BAJISTA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 10:
        return 0
    start = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(start, rates_total):
        o = open[i]
        h = high[i]
        l = low[i]
        c = close[i]
        BUFFER_WICK_TOP[i] = EMPTY_VALUE
        BUFFER_WICK_BOTTOM[i] = EMPTY_VALUE
        BUFFER_ALCISTA_OPEN[i] = EMPTY_VALUE
        BUFFER_ALCISTA_HIGH[i] = EMPTY_VALUE
        BUFFER_ALCISTA_LOW[i] = EMPTY_VALUE
        BUFFER_ALCISTA_CLOSE[i] = EMPTY_VALUE
        BUFFER_BAJISTA_OPEN[i] = EMPTY_VALUE
        BUFFER_BAJISTA_HIGH[i] = EMPTY_VALUE
        BUFFER_BAJISTA_LOW[i] = EMPTY_VALUE
        BUFFER_BAJISTA_CLOSE[i] = EMPTY_VALUE
        cuerpo_alto = MathMax(o, c)
        cuerpo_bajo = MathMin(o, c)
        BUFFER_WICK_TOP[i] = h
        BUFFER_WICK_BOTTOM[i] = l
        if c > o:
            BUFFER_ALCISTA_OPEN[i] = o
            BUFFER_ALCISTA_HIGH[i] = cuerpo_alto
            BUFFER_ALCISTA_LOW[i] = cuerpo_bajo
            BUFFER_ALCISTA_CLOSE[i] = c
        elif c < o:
            BUFFER_BAJISTA_OPEN[i] = o
            BUFFER_BAJISTA_HIGH[i] = cuerpo_alto
            BUFFER_BAJISTA_LOW[i] = cuerpo_bajo
            BUFFER_BAJISTA_CLOSE[i] = c
        else:
            BUFFER_ALCISTA_OPEN[i] = o
            BUFFER_ALCISTA_HIGH[i] = o
            BUFFER_ALCISTA_LOW[i] = o
            BUFFER_ALCISTA_CLOSE[i] = o
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CambiarElColorDeVelasYMecha(_MQL5Indicator):
    name = 'cambiar el color de velas y mecha'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'APAGAR_MECHA_DE_LA_VELA': _Choice({0: 'Valor 0 = No se apaga (activa)', 1: 'Valor 1 = Se apaga (desactiva)'}, default=0),  # Encender/apagar la mecha
        'ANCHO_DE_LA_MECHA': 1,  # Grosor de la línea de la mecha
    }

