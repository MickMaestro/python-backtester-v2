"""PS_Magicas — converted from MQL5: MQL5 Indicators/PS Magicas - Three moving averages/PS_Magicas.mq5

PS Magicas - Three moving averages that give target and possible entries
Copyright: PS - psmarqu3s@outlook.com; Link: https://www.mql5.com; Version: 1.07

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'PS - psmarqu3s@outlook.com', 'link': 'https://www.mql5.com', 'version': '1.07', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [36095], 2: [16776960], 3: [11186720, 32768, 65535, 255]}, 'widths': {1: 4, 2: 3, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Slow', 2: 'Medium', 3: 'Fast'}, 'levels': [], 'description': ['PS Magicas - Three moving averages that give target and possible entries'], 'name': 'PS_Magicas', 'source': 'MQL5 Indicators/PS Magicas - Three moving averages/PS_Magicas.mq5', 'folder': 'PS Magicas - Three moving averages', 'inputs': [{'mql': 'Rapida', 'py': 'Rapida', 'param': 'Rapida', 'type': 'int', 'default': 20, 'label': 'Fast - Usualy 20 ou 21', 'sinput': False}, {'mql': 'RapidaTipo', 'py': 'RapidaTipo', 'param': 'RapidaTipo', 'type': 'int', 'default': 2, 'label': 'Fast MA Type - SMMA Default', 'sinput': False}, {'mql': 'Media', 'py': 'Media', 'param': 'Media', 'type': 'int', 'default': 90, 'label': 'Medium - Usualy 90', 'sinput': False}, {'mql': 'MediaTipo', 'py': 'MediaTipo', 'param': 'MediaTipo', 'type': 'int', 'default': 2, 'label': 'Medium MA Type - SMMA Default', 'sinput': False}, {'mql': 'Lenta', 'py': 'Lenta', 'param': 'Lenta', 'type': 'int', 'default': 200, 'label': 'Slow - Usualy 200', 'sinput': False}, {'mql': 'LentaTipo', 'py': 'LentaTipo', 'param': 'LentaTipo', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'HabilitarSinais', 'py': 'HabilitarSinais', 'param': 'HabilitarSinais', 'type': 'bool', 'default': False, 'label': 'Enable Buy or Sell Suggestion(Beta)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Rapida = _input('Rapida', 20)  # Fast - Usualy 20 ou 21
RapidaTipo = _input('RapidaTipo', MODE_SMMA)  # Fast MA Type - SMMA Default
Media = _input('Media', 90)  # Medium - Usualy 90
MediaTipo = _input('MediaTipo', MODE_SMMA)  # Medium MA Type - SMMA Default
Lenta = _input('Lenta', 200)  # Slow - Usualy 200
LentaTipo = _input('LentaTipo', MODE_SMMA)
HabilitarSinais = _input('HabilitarSinais', False)  # Enable Buy or Sell Suggestion(Beta)
pLentaBuffer = Arr(0, 0.0)
pMediaBuffer = Arr(0, 0.0)
pRapidaBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
ma_rapida = 0
ma_media = 0
ma_lenta = 0
lastsignal = 0

def OnInit():
    global ma_lenta, ma_media, ma_rapida
    SetIndexBuffer(0, pLentaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, pMediaBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, pRapidaBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorBuffer, INDICATOR_COLOR_INDEX)
    ma_rapida = iMA(Symbol(), 0, Rapida, 0, RapidaTipo, PRICE_CLOSE)
    ma_media = iMA(Symbol(), 0, Media, 0, MediaTipo, PRICE_CLOSE)
    ma_lenta = iMA(Symbol(), 0, Lenta, 0, LentaTipo, PRICE_CLOSE)
    PlotIndexSetInteger(0, 0, PLOT_DRAW_BEGIN, Lenta)
    PlotIndexSetInteger(1, 0, PLOT_DRAW_BEGIN, Media)
    PlotIndexSetInteger(2, 0, PLOT_DRAW_BEGIN, Rapida)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = (0 if (prev_calculated == 0) else (prev_calculated - 1))
    preco = 0.0
    timeSeries = Arr(1, 0.0, dyn=False)
    CopyBuffer(ma_lenta, 0, 0, rates_total - start, pLentaBuffer)
    CopyBuffer(ma_media, 0, 0, rates_total - start, pMediaBuffer)
    CopyBuffer(ma_rapida, 0, 0, rates_total - start, pRapidaBuffer)
    CopyClose(Symbol(), Period(), 0, 1, timeSeries)
    preco = timeSeries[0]
    priceLenta = pLentaBuffer[start]
    priceLenta1 = pLentaBuffer[(0 if (start == 0) else (start - 1))]
    priceMedia = pMediaBuffer[start]
    priceMedia1 = pMediaBuffer[(0 if (start == 0) else (start - 1))]
    priceRapida = pRapidaBuffer[start]
    priceRapida1 = pRapidaBuffer[(0 if (start == 0) else (start - 1))]
    ColorMediaTick(rates_total, start, high, low)
    if start > 17:
        if (priceRapida > priceLenta and priceMedia > priceLenta) and (((priceRapida > priceMedia and priceRapida1 < priceMedia) or (priceLenta > priceMedia and priceLenta1 < priceMedia)) or (((priceMedia > priceLenta and priceMedia1 < priceLenta) and priceRapida > priceMedia) and close[start] > priceRapida)):
            if HabilitarSinais:
                DrawSignal(0, low[start])
        elif (priceRapida < priceLenta and priceMedia < priceLenta) and (((priceRapida < priceMedia and priceRapida1 > priceMedia) or (priceLenta < priceMedia and priceLenta1 > priceMedia)) or (((priceMedia < priceLenta and priceMedia1 > priceLenta) and priceRapida < priceMedia) and close[start] < priceRapida)):
            if HabilitarSinais:
                DrawSignal(0, high[start])
    return rates_total

def OnTimer():
    pass

def DrawSignal(tipo, price):
    global lastsignal
    dt = TimeTradeServer()
    name = 'signal_s' + IntegerToString(dt)
    ResetLastError()
    if (dt - lastsignal) < 240:
        return
    tp = ('compra' if (tipo == 0) else 'venda')
    ObjectCreate(0, 'signal_' + tp + DoubleToString(price, 0), (OBJ_ARROW_UP if (tipo == 0) else OBJ_ARROW_DOWN), 0, dt, price)
    ObjectSetInteger(0, 'signal_' + tp + IntegerToString(tipo) + DoubleToString(price, 0), OBJPROP_ANCHOR, (ANCHOR_TOP if (tipo == 0) else ANCHOR_BOTTOM))
    ObjectSetInteger(0, 'signal_' + tp + IntegerToString(tipo) + DoubleToString(price, 0), OBJPROP_WIDTH, 3)
    ObjectSetInteger(0, 'signal_' + tp + IntegerToString(tipo) + DoubleToString(price, 0), OBJPROP_COLOR, (clrBlue if (tipo == 0) else clrRed))
    ObjectSetInteger(0, 'signal_' + tp + IntegerToString(tipo) + DoubleToString(price, 0), OBJPROP_STYLE, STYLE_SOLID)
    lastsignal = dt

def ColorMediaTick(rates_total, prev_calculated, high, low):
    limit = ((prev_calculated + Rapida + 1) if (prev_calculated == 0) else (prev_calculated - 1))
    for i in range(limit, rates_total):
        precoL = low[i]
        precoH = high[i]
        precoRapida = pRapidaBuffer[i]
        if precoL > precoRapida:
            ColorBuffer[i] = 1.0
        elif precoH < precoRapida:
            ColorBuffer[i] = 3.0
        else:
            ColorBuffer[i] = 2.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PSMagicas(_MQL5Indicator):
    name = 'PS_Magicas'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Rapida': 20,  # Fast - Usualy 20 ou 21
        'RapidaTipo': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Fast MA Type - SMMA Default
        'Media': 90,  # Medium - Usualy 90
        'MediaTipo': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Medium MA Type - SMMA Default
        'Lenta': 200,  # Slow - Usualy 200
        'LentaTipo': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),
        'HabilitarSinais': False,  # Enable Buy or Sell Suggestion(Beta)
    }

