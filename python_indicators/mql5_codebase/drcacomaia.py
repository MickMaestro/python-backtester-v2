"""DRCacoMaia — converted from MQL5: MQL5 Indicators/DR Caco Maia/DRCacoMaia.mq5

MA_DR = Double breaking of averages with a candle
As described by Caco Maia
buffer 0 - value > 0 - buy
buffer 1 - value > 0 - sell
Copyright: Copyright © 2021, Ronei Toporcov; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2021, Ronei Toporcov', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [32768], 2: [2763429]}, 'widths': {1: 4, 2: 4}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Compra', 2: 'Venda'}, 'levels': [], 'description': ['MA_DR = Double breaking of averages with a candle', 'As described by Caco Maia', 'buffer 0 - value > 0 - buy', 'buffer 1 - value > 0 - sell'], 'name': 'DRCacoMaia', 'source': 'MQL5 Indicators/DR Caco Maia/DRCacoMaia.mq5', 'folder': 'DR Caco Maia', 'inputs': [{'mql': 'InpFastMA', 'py': 'InpFastMA', 'param': 'InpFastMA', 'type': 'int', 'default': 8, 'label': 'Periodo da MA rápida', 'sinput': False}, {'mql': 'InpSlowMA', 'py': 'InpSlowMA', 'param': 'InpSlowMA', 'type': 'int', 'default': 20, 'label': 'Periodo da MA lenta', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpFastMA = _input('InpFastMA', 8)  # Periodo da MA rápida
InpSlowMA = _input('InpSlowMA', 20)  # Periodo da MA lenta
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
ExtBufferCompra = Arr(0, 0.0)
ExtBufferVenda = Arr(0, 0.0)
ExtFastMaBuffer = Arr(0, 0.0)
ExtSlowMaBuffer = Arr(0, 0.0)
ExtTrixSinal = Arr(0, 0.0)
ExtTrixMedia = Arr(0, 0.0)
ExtEstSinal = Arr(0, 0.0)
ExtEstMedia = Arr(0, 0.0)
ExtFastMaHandle = 0
ExtSlowMaHandle = 0
ExtTrixHandle = 0
ExtMaTrixHandle = 0
ExtEstHandle = 0
point = 0.0

def OnInit():
    global ExtEstHandle, ExtFastMaHandle, ExtMaTrixHandle, ExtSlowMaHandle, ExtTrixHandle, point
    SetIndexBuffer(0, ExtBufferCompra, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBufferVenda, INDICATOR_DATA)
    SetIndexBuffer(2, ExtFastMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtSlowMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtTrixSinal, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtTrixMedia, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ExtEstSinal, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, ExtEstMedia, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MA_DR')
    ExtFastMaHandle = iMA(None, 0, InpFastMA, 0, MODE_SMA, InpAppliedPrice)
    ExtSlowMaHandle = iMA(None, 0, InpSlowMA, 0, MODE_SMA, InpAppliedPrice)
    ExtEstHandle = iStochastic(None, 0, 14, 3, 3, MODE_SMA, STO_LOWHIGH)
    ExtTrixHandle = iTriX(None, 0, 7, InpAppliedPrice)
    ExtMaTrixHandle = iMA(None, 0, 4, 0, MODE_SMA, ExtTrixHandle)
    point = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_SIZE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < InpSlowMA:
        return 0
    calculated = BarsCalculated(ExtFastMaHandle)
    if calculated < rates_total:
        Print('ExtFastMaHandle data is not all calculated (', calculated, ' bar ). Erro', GetLastError())
        return 0
    calculated = BarsCalculated(ExtSlowMaHandle)
    if calculated < rates_total:
        Print('ExtSlowMaHandle data is not all calculated (', calculated, ' bar ). Erro', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(ExtFastMaHandle, 0, 0, to_copy, ExtFastMaBuffer) <= 0:
        Print('Copy fast MA fail! Erro', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtSlowMaHandle, 0, 0, to_copy, ExtSlowMaBuffer) <= 0:
        Print('Copy slow MA fail! Erro', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtEstHandle, 0, 0, to_copy, ExtEstSinal) <= 0:
        Print('Copy main Estocastic fail! Erro', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtEstHandle, 1, 0, to_copy, ExtEstMedia) <= 0:
        Print('Copy signal Estocastic fail! Erro', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtTrixHandle, 0, 0, to_copy, ExtTrixSinal) <= 0:
        Print('Copy signnal Trix fail! Erro', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtMaTrixHandle, 0, 0, to_copy, ExtTrixMedia) <= 0:
        Print('Copy average Trix fail! Erro', GetLastError())
        return 0
    limit = 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    for i in range(MathMax(prev_calculated - 1, 1), rates_total):
        if open[i] < close[i]:
            if low[i] <= ExtSlowMaBuffer[i] and low[i] <= ExtFastMaBuffer[i]:
                if ((close[i] >= ExtSlowMaBuffer[i] and close[i] >= ExtFastMaBuffer[i]) and ExtEstSinal[i] > ExtEstMedia[i]) and ExtTrixSinal[i] > ExtTrixMedia[i]:
                    ExtBufferCompra[i] = high[i] + point
                else:
                    ExtBufferCompra[i] = 0.0
            else:
                ExtBufferCompra[i] = 0.0
            ExtBufferVenda[i] = 0.0
        else:
            if open[i] > close[i]:
                if high[i] >= ExtSlowMaBuffer[i] and high[i] >= ExtFastMaBuffer[i]:
                    if ((close[i] <= ExtSlowMaBuffer[i] and close[i] <= ExtFastMaBuffer[i]) and ExtEstSinal[i] < ExtEstMedia[i]) and ExtTrixSinal[i] < ExtTrixMedia[i]:
                        ExtBufferVenda[i] = low[i] - point
                    else:
                        ExtBufferVenda[i] = 0.0
                else:
                    ExtBufferVenda[i] = 0.0
                ExtBufferCompra[i] = 0.0
            else:
                ExtBufferCompra[i] = 0.0
                ExtBufferVenda[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DRCacoMaia(_MQL5Indicator):
    name = 'DRCacoMaia'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastMA': 8,  # Periodo da MA rápida
        'InpSlowMA': 20,  # Periodo da MA lenta
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

