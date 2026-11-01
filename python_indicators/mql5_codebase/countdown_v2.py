"""Countdown_v2 — converted from MQL5: MQL5 Indicators/Countdown 2.0/Countdown_v2.mq5

Copyright: Copyright 2019-2025, Virologista Kerntopf Corp.; Link: https://www.mql5.com/pt/users/virologustavo/news; Version: 2.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2019-2025, Virologista Kerntopf Corp.', 'link': 'https://www.mql5.com/pt/users/virologustavo/news', 'version': '2.0', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Countdown_v2', 'source': 'MQL5 Indicators/Countdown 2.0/Countdown_v2.mq5', 'folder': 'Countdown 2.0', 'inputs': [{'mql': 'InpTimerPosition', 'py': 'InpTimerPosition', 'param': 'InpTimerPosition', 'type': 'int', 'default': 2, 'label': 'Posição do temporizador', 'sinput': False}, {'mql': 'InpTextColor', 'py': 'InpTextColor', 'param': None, 'type': 'color', 'default': 2139610, 'label': 'Cor do texto', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'int', 'default': 8, 'label': 'Tamanho da fonte', 'sinput': False}, {'mql': 'InpAnchorPoint', 'py': 'InpAnchorPoint', 'param': 'InpAnchorPoint', 'type': 'int', 'default': 2, 'label': 'Ponto de ancoragem', 'sinput': False}, {'mql': 'InpCornerPosition', 'py': 'InpCornerPosition', 'param': 'InpCornerPosition', 'type': 'int', 'default': 1, 'label': 'Canto de posicionamento', 'sinput': False}, {'mql': 'InpOpenMarket', 'py': 'InpOpenMarket', 'param': None, 'type': 'string', 'default': '09:00', 'label': 'Hora de abertura', 'sinput': False}, {'mql': 'InpCloseMarket', 'py': 'InpCloseMarket', 'param': None, 'type': 'string', 'default': '18:30', 'label': 'Hora de fechamento', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum DisplayPosition
CommentDisplay = 0
ChartCorner = 1
NearPrice = 2
_enum('DisplayPosition', {0: 'CommentDisplay', 1: 'ChartCorner', 2: 'NearPrice'})

# ---- inputs and global variables
InpTimerPosition = _input('InpTimerPosition', NearPrice)  # Posição do temporizador
InpTextColor = _input('InpTextColor', clrGoldenrod)  # Cor do texto
InpFontSize = _input('InpFontSize', 8)  # Tamanho da fonte
InpAnchorPoint = _input('InpAnchorPoint', ANCHOR_LEFT_LOWER)  # Ponto de ancoragem
InpCornerPosition = _input('InpCornerPosition', CORNER_LEFT_LOWER)  # Canto de posicionamento
InpOpenMarket = _input('InpOpenMarket', '09:00')  # Hora de abertura
InpCloseMarket = _input('InpCloseMarket', '18:30')  # Hora de fechamento
countdownLabel = 'lblNextCandle'
openMarketHour = 0
openingMinute = 0
closeMarketHour = 0
closingMinute = 0
nextMarketOpen = 0  # Armazena o próximo horário de abertura

def GetBrasiliaTime():
    gmtTime = TimeCurrent()
    brasiliaOffset = -3 * 3600
    currentOffset = TimeGMTOffset()
    return gmtTime + brasiliaOffset + currentOffset

def OnInit():
    ResetLastError()
    if not ParseTime(InpOpenMarket, _GlobRef(globals(), 'openMarketHour'), _GlobRef(globals(), 'openingMinute')):
        Print('Erro: Formato de horário de abertura inválido. Use HH:MM (ex.: 09:00).')
        return INIT_FAILED
    if not ParseTime(InpCloseMarket, _GlobRef(globals(), 'closeMarketHour'), _GlobRef(globals(), 'closingMinute')):
        Print('Erro: Formato de horário de fechamento inválido. Use HH:MM (ex.: 18:30).')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ResetLastError()
    Comment('')
    if ObjectFind(0, countdownLabel) != -1:
        ObjectDelete(0, countdownLabel)

def ParseTime(timeStr, hour, minute):
    colonIndex = StringFind(timeStr, ':')
    if colonIndex == -1 or StringLen(timeStr) != 5:
        Print('Erro: Formato de hora inválido. Use HH:MM (ex.: 09:00).')
        return False
    hour.v = StringToInteger(StringSubstr(timeStr, 0, colonIndex))
    minute.v = StringToInteger(StringSubstr(timeStr, colonIndex + 1))
    if ((hour.v < 0 or hour.v > 23) or minute.v < 0) or minute.v > 59:
        Print('Erro: Horário fora do intervalo válido. Use 00:00 a 23:59.')
        return False
    return True

def IsMarketOpen(openHour, openMinute, closeHour, closeMinute):
    currentTime = GetBrasiliaTime()
    rawDay = _int(MathMod(_idiv(currentTime, 86400), 7))
    currentDay = _int(MathMod(rawDay + 3, 7))
    if currentDay >= 0 and currentDay <= 4:
        marketOpenTime = StringToTime(TimeToString(currentTime, TIME_DATE) + ' ' + IntegerToString(openHour, 2, 48) + ':' + IntegerToString(openMinute, 2, 48))
        marketCloseTime = StringToTime(TimeToString(currentTime, TIME_DATE) + ' ' + IntegerToString(closeHour, 2, 48) + ':' + IntegerToString(closeMinute, 2, 48))
        if currentDay == 4 and currentTime > marketCloseTime:
            return False
        if currentTime >= marketOpenTime and currentTime < marketCloseTime:
            return True
    return False

def CalculateNextMarketOpen(currentTime, openHour, openMinute):
    rawDay = _int(MathMod(_idiv(currentTime, 86400), 7))
    currentDay = _int(MathMod(rawDay + 3, 7))
    nextMarketOpen_ = StringToTime(TimeToString(currentTime, TIME_DATE) + ' ' + IntegerToString(openHour, 2, 48) + ':' + IntegerToString(openMinute, 2, 48))
    if currentDay == 5 or currentDay == 6:
        daysUntilMonday = _imod(7 - currentDay, 7)
        nextMarketOpen_ += daysUntilMonday * 24 * 3600
        nextMarketOpen_ = StringToTime(TimeToString(nextMarketOpen_, TIME_DATE) + ' ' + IntegerToString(openHour, 2, 48) + ':' + IntegerToString(openMinute, 2, 48))
    else:
        while True:
            if currentDay >= 0 and currentDay <= 4:
                if currentTime < nextMarketOpen_:
                    break
                nextMarketOpen_ += 24 * 3600
            else:
                nextMarketOpen_ += 24 * 3600
            currentDay = _int(MathMod(_idiv(nextMarketOpen_, 86400) + 3, 7))
    return nextMarketOpen_

def CreateLabel(text, x, y, isLabel=True, textColor=clrGoldenrod):
    ResetLastError()
    if ObjectFind(0, countdownLabel) == -1:
        if isLabel:
            ObjectCreate(0, countdownLabel, OBJ_LABEL, 0, 0, 0)
        else:
            ObjectCreate(0, countdownLabel, OBJ_TEXT, 0, x, y)
    ObjectSetInteger(0, countdownLabel, OBJPROP_COLOR, textColor)
    ObjectSetString(0, countdownLabel, OBJPROP_TEXT, text)
    ObjectSetInteger(0, countdownLabel, OBJPROP_FONTSIZE, InpFontSize)
    ObjectSetString(0, countdownLabel, OBJPROP_FONT, 'Arial')
    ObjectSetInteger(0, countdownLabel, OBJPROP_ANCHOR, InpAnchorPoint)
    ObjectSetInteger(0, countdownLabel, OBJPROP_CORNER, InpCornerPosition)
    ObjectSetInteger(0, countdownLabel, OBJPROP_SELECTABLE, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global nextMarketOpen
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(close, True)
    ResetLastError()
    currentTime = GetBrasiliaTime()
    if not IsMarketOpen(openMarketHour, openingMinute, closeMarketHour, closingMinute):
        if nextMarketOpen == 0 or currentTime >= nextMarketOpen:
            nextMarketOpen = CalculateNextMarketOpen(currentTime, openMarketHour, openingMinute)
        timeRemainingInSeconds = MathMax(0, nextMarketOpen - currentTime)
        days = _int(_idiv(timeRemainingInSeconds, 86400))
        hours = _int(_idiv(_imod(timeRemainingInSeconds, 86400), 3600))
        minutes = _int(_idiv(_imod(_imod(timeRemainingInSeconds, 86400), 3600), 60))
        seconds = _int(_imod(_imod(_imod(timeRemainingInSeconds, 86400), 3600), 60))
        message = ""
        if days > 0:
            message = StringFormat('Falta %d dia(s), %02d:%02d:%02d', days, hours, minutes, seconds)
        else:
            message = StringFormat('Próxima Abertura: %02d:%02d:%02d', hours, minutes, seconds)
        _sw1 = InpTimerPosition
        if _sw1 == CommentDisplay:
            Comment(message)
        elif _sw1 == ChartCorner:
            CreateLabel(message, 0, 0, True, InpTextColor)
        elif _sw1 == NearPrice:
            if ObjectFind(0, countdownLabel) == -1:
                ObjectCreate(0, countdownLabel, OBJ_TEXT, 0, time[0] + (PeriodSeconds() * 2), close[0])
            ObjectSetInteger(0, countdownLabel, OBJPROP_COLOR, InpTextColor)
            ObjectSetString(0, countdownLabel, OBJPROP_TEXT, message)
            ObjectSetInteger(0, countdownLabel, OBJPROP_FONTSIZE, InpFontSize)
            ObjectSetString(0, countdownLabel, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(0, countdownLabel, OBJPROP_ANCHOR, InpAnchorPoint)
            ObjectMove(0, countdownLabel, 0, time[0] + (PeriodSeconds() * 2), close[0])
        return rates_total
    nextCandleTime = iTime(Symbol(), Period(), 0) + PeriodSeconds()
    timeRemainingInSeconds = MathMax(0, nextCandleTime - currentTime)
    iH = _int(_idiv(timeRemainingInSeconds, 3600))
    iM = _int(_imod(_idiv(timeRemainingInSeconds, 60), 60))
    iS = _int(_imod(timeRemainingInSeconds, 60))
    countdown = StringFormat('%02d:%02d:%02d', iH, iM, iS)
    _sw2 = InpTimerPosition
    if _sw2 == CommentDisplay:
        Comment('Contagem Regressiva: ' + countdown)
    elif _sw2 == ChartCorner:
        CreateLabel(countdown, 0, 0, True, InpTextColor)
    elif _sw2 == NearPrice:
        if ObjectFind(0, countdownLabel) == -1:
            ObjectCreate(0, countdownLabel, OBJ_TEXT, 0, time[0] + (PeriodSeconds() * 2), close[0])
        ObjectSetInteger(0, countdownLabel, OBJPROP_COLOR, InpTextColor)
        ObjectSetString(0, countdownLabel, OBJPROP_TEXT, countdown)
        ObjectSetInteger(0, countdownLabel, OBJPROP_FONTSIZE, InpFontSize)
        ObjectSetString(0, countdownLabel, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, countdownLabel, OBJPROP_ANCHOR, InpAnchorPoint)
        ObjectMove(0, countdownLabel, 0, time[0] + (PeriodSeconds() * 2), close[0])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CountdownV2(_MQL5Indicator):
    name = 'Countdown_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimerPosition': _Choice({0: 'Exibir no comentário', 1: 'Exibir nas bordas do gráfico', 2: 'Exibir próximo ao preço'}, default=2),  # Posição do temporizador
        'InpFontSize': 8,  # Tamanho da fonte
        'InpAnchorPoint': _Choice({0: 'ANCHOR_LEFT_UPPER', 1: 'ANCHOR_LEFT', 2: 'ANCHOR_LEFT_LOWER', 3: 'ANCHOR_LOWER', 4: 'ANCHOR_RIGHT_LOWER', 5: 'ANCHOR_RIGHT', 6: 'ANCHOR_RIGHT_UPPER', 7: 'ANCHOR_UPPER', 8: 'ANCHOR_CENTER'}, default=2),  # Ponto de ancoragem
        'InpCornerPosition': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # Canto de posicionamento
    }

