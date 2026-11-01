"""demo_filereaddatetime — converted from MQL5: MQL5 Indicators/Demo_FileReadDatetime/demo_filereaddatetime.mq5

Copyright: Copyright 2013, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [255]}, 'widths': {1: 4, 2: 4}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'UpSignal', 2: 'DownSignal'}, 'levels': [], 'description': [], 'name': 'demo_filereaddatetime', 'source': 'MQL5 Indicators/Demo_FileReadDatetime/demo_filereaddatetime.mq5', 'folder': 'Demo_FileReadDatetime', 'inputs': [{'mql': 'InpFileName', 'py': 'InpFileName', 'param': None, 'type': 'string', 'default': 'MACD.csv', 'label': 'file name', 'sinput': False}, {'mql': 'InpDirectoryName', 'py': 'InpDirectoryName', 'param': None, 'type': 'string', 'default': 'Data', 'label': 'directory name', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFileName = _input('InpFileName', 'MACD.csv')  # file name
InpDirectoryName = _input('InpDirectoryName', 'Data')  # directory name
ind = 0  # index
upbuff = Arr(0, 0.0)  # indicator buffers of up arrows
downbuff = Arr(0, 0.0)  # indicator buffer of down arrows
sign_buff = Arr(0, False)  # signal array (true - buy, false - sell)
time_buff = Arr(0, 0)  # array of signals' arrival time
size = 0  # size of signal arrays

def OnInit():
    global size
    ResetLastError()
    file_handle = FileOpen(InpDirectoryName + '//' + InpFileName, FILE_READ | FILE_CSV)
    if file_handle != INVALID_HANDLE:
        PrintFormat('%s file is open for reading', InpFileName)
        size = _int(FileReadNumber(file_handle))
        ArrayResize(sign_buff, size)
        ArrayResize(time_buff, size)
        for i in range(0, size):
            time_buff[i] = FileReadDatetime(file_handle)
            sign_buff[i] = FileReadBool(file_handle)
        FileClose(file_handle)
    else:
        PrintFormat('Failed to open %s file, Error code = %d', InpFileName, GetLastError())
        return INIT_FAILED
    SetIndexBuffer(0, upbuff, INDICATOR_DATA)
    SetIndexBuffer(1, downbuff, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 241)
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global ind
    ArraySetAsSeries(time, False)
    ArraySetAsSeries(low, False)
    ArraySetAsSeries(high, False)
    for i in range(prev_calculated, rates_total):
        upbuff[i] = 0.0
        downbuff[i] = 0.0
        if ind < size:
            for j in range(ind, size):
                if time[i] == time_buff[j]:
                    if sign_buff[j]:
                        upbuff[i] = high[i]
                    else:
                        downbuff[i] = low[i]
                    ind = j + 1
                    break
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DemoFilereaddatetime(_MQL5Indicator):
    name = 'demo_filereaddatetime'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

