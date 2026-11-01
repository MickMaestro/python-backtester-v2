"""CompoundPercent For Trader — converted from MQL5: MQL5 Indicators/Advanced compound interest calculator for the trader/CompoundPercent For Trader.mq5

Расширенный калькулятор для трейдера с риск-менеджментом
Copyright: Copyright 2025; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['Расширенный калькулятор для трейдера с риск-менеджментом'], 'name': 'CompoundPercent For Trader', 'source': 'MQL5 Indicators/Advanced compound interest calculator for the trader/CompoundPercent For Trader.mq5', 'folder': 'Advanced compound interest calculator for the trader', 'inputs': [{'mql': 'InitialCapital', 'py': 'InitialCapital', 'param': 'InitialCapital', 'type': 'double', 'default': 1000.0, 'label': 'Начальный капитал', 'sinput': False}, {'mql': 'Years', 'py': 'Years', 'param': 'Years', 'type': 'int', 'default': 10, 'label': 'Количество лет', 'sinput': False}, {'mql': 'MonthlyDeposit', 'py': 'MonthlyDeposit', 'param': 'MonthlyDeposit', 'type': 'double', 'default': 100.0, 'label': 'Ежемесячное пополнение', 'sinput': False}, {'mql': 'TradesPerDay', 'py': 'TradesPerDay', 'param': 'TradesPerDay', 'type': 'int', 'default': 3, 'label': 'Количество сделок в день', 'sinput': False}, {'mql': 'WinRate', 'py': 'WinRate', 'param': 'WinRate', 'type': 'double', 'default': 55.0, 'label': 'Вероятность прибыльной сделки (%)', 'sinput': False}, {'mql': 'RiskRewardRatio', 'py': 'RiskRewardRatio', 'param': 'RiskRewardRatio', 'type': 'double', 'default': 1.5, 'label': 'Отношение риска к прибыли (1:X)', 'sinput': False}, {'mql': 'MaxDrawdownLimit', 'py': 'MaxDrawdownLimit', 'param': 'MaxDrawdownLimit', 'type': 'double', 'default': 20.0, 'label': 'Психологический барьер просадки (%)', 'sinput': False}, {'mql': 'RefreshInterval', 'py': 'RefreshInterval', 'param': 'RefreshInterval', 'type': 'int', 'default': 1, 'label': 'Интервал обновления (в секундах)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InitialCapital = _input('InitialCapital', 1000.0)  # Начальный капитал
Years = _input('Years', 10)  # Количество лет
MonthlyDeposit = _input('MonthlyDeposit', 100.0)  # Ежемесячное пополнение
TradesPerDay = _input('TradesPerDay', 3)  # Количество сделок в день
WinRate = _input('WinRate', 55.0)  # Вероятность прибыльной сделки (%)
RiskRewardRatio = _input('RiskRewardRatio', 1.5)  # Отношение риска к прибыли (1:X)
MaxDrawdownLimit = _input('MaxDrawdownLimit', 20.0)  # Психологический барьер просадки (%)
RefreshInterval = _input('RefreshInterval', 1)  # Интервал обновления (в секундах)
totalAmount = Arr(0, 0.0)
indicatorBuffer = Arr(0, 0.0)
objPrefix = 'TradingCalc_'
windowWidth = 400
windowHeight = 480
chartWidth = 0
chartHeight = 0

class TradingMetrics(MqlObject):
    _q_fields = ('maxRiskPerTrade', 'expectedMonthlyReturn', 'expectedAnnualReturn', 'monthlyTrades', 'probabilityOfRuin', 'expectedMonthlyCapital', 'expectedAnnualCapital', 'expectedFinalCapital')
    def __init__(self, *args):
        self.maxRiskPerTrade = 0.0
        self.expectedMonthlyReturn = 0.0
        self.expectedAnnualReturn = 0.0
        self.monthlyTrades = 0
        self.probabilityOfRuin = 0.0
        self.expectedMonthlyCapital = 0.0
        self.expectedAnnualCapital = 0.0
        self.expectedFinalCapital = 0.0

def OnInit():
    SetIndexBuffer(0, indicatorBuffer, INDICATOR_DATA)
    ArrayResize(totalAmount, Years * 12)
    if not ValidateInputs():
        return INIT_PARAMETERS_INCORRECT
    CreatePanel()
    EventSetTimer(RefreshInterval)
    return INIT_SUCCEEDED

def ValidateInputs():
    if (InitialCapital <= 0 or MonthlyDeposit < 0) or Years <= 0:
        return False
    if (TradesPerDay <= 0 or WinRate <= 0) or WinRate >= 100:
        return False
    if (RiskRewardRatio <= 0 or MaxDrawdownLimit <= 0) or MaxDrawdownLimit >= 100:
        return False
    return True

def CalculateTradingMetrics():
    metrics.monthlyTrades = TradesPerDay * 22
    maxRiskAmount = _fdiv((InitialCapital * MaxDrawdownLimit) / 100, sqrt(metrics.monthlyTrades))
    metrics.maxRiskPerTrade = NormalizeDouble((maxRiskAmount / InitialCapital) * 100, 2)
    winProb = WinRate / 100
    loseProb = 1 - winProb
    expectedValuePerTrade = (winProb * RiskRewardRatio) - loseProb
    metrics.expectedMonthlyReturn = expectedValuePerTrade * metrics.monthlyTrades * metrics.maxRiskPerTrade
    metrics.expectedAnnualReturn = metrics.expectedMonthlyReturn * 12
    kellyPercentage = ((winProb * RiskRewardRatio) - loseProb) / RiskRewardRatio
    metrics.probabilityOfRuin = exp(-2 * pow(_fdiv(InitialCapital, maxRiskAmount), 2) * pow(kellyPercentage, 2))
    CalculateExpectedCapital()

def CalculateExpectedCapital():
    metrics.expectedMonthlyCapital = (InitialCapital * (1 + (metrics.expectedMonthlyReturn / 100))) + MonthlyDeposit
    metrics.expectedAnnualCapital = InitialCapital
    for i in range(0, 12):
        metrics.expectedAnnualCapital = (metrics.expectedAnnualCapital * (1 + (metrics.expectedMonthlyReturn / 100))) + MonthlyDeposit
    metrics.expectedFinalCapital = InitialCapital
    for i in range(0, Years * 12):
        metrics.expectedFinalCapital = (metrics.expectedFinalCapital * (1 + (metrics.expectedMonthlyReturn / 100))) + MonthlyDeposit
        totalAmount[i] = metrics.expectedFinalCapital

def CreatePanel():
    global chartHeight, chartWidth
    chartWidth = _int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS))
    chartHeight = _int(ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS))
    ObjectCreate(0, objPrefix + 'Background', OBJ_RECTANGLE_LABEL, 0, 0, 0)
    ObjectSetInteger(0, objPrefix + 'Background', OBJPROP_XDISTANCE, chartWidth - windowWidth - 10)
    ObjectSetInteger(0, objPrefix + 'Background', OBJPROP_YDISTANCE, 10)
    ObjectSetInteger(0, objPrefix + 'Background', OBJPROP_XSIZE, windowWidth)
    ObjectSetInteger(0, objPrefix + 'Background', OBJPROP_YSIZE, windowHeight)
    ObjectSetInteger(0, objPrefix + 'Background', OBJPROP_BGCOLOR, clrWhiteSmoke)
    ObjectSetInteger(0, objPrefix + 'Background', OBJPROP_BORDER_TYPE, BORDER_FLAT)
    ObjectSetInteger(0, objPrefix + 'Background', OBJPROP_COLOR, clrBlack)
    CreateLabel('Title', 'Расширенный калькулятор сложного процента для трейдера', 10, 15, clrBlack, True)

def FormatMoney(value):
    result = DoubleToString(value, 2)
    pos = StringFind(result, '.')
    if pos == -1:
        pos = StringLen(result)
    while pos > 3:
        pos -= 3
        result = StringSubstr(result, 0, pos) + ' ' + StringSubstr(result, pos)
    return result

def YearDeclension(years):
    result = ""
    remainder100 = _imod(years, 100)
    remainder10 = _imod(years, 10)
    if remainder100 >= 11 and remainder100 <= 19:
        result = 'лет'
    elif remainder10 == 1:
        result = 'год'
    elif remainder10 >= 2 and remainder10 <= 4:
        result = 'года'
    else:
        result = 'лет'
    return result

def UpdatePanel():
    CalculateTradingMetrics()
    y = 40
    CreateLabel('Section1', '== Параметры капитала ==', 10, y, clrNavy, True)
    y += 25
    CreateLabel('InitialCapital', 'Начальный капитал: $' + FormatMoney(InitialCapital), 10, y, clrBlack)
    y += 20
    CreateLabel('MonthlyDeposit', 'Ежемесячное пополнение: $' + FormatMoney(MonthlyDeposit), 10, y, clrBlack)
    y += 20
    y += 10
    CreateLabel('Section2', '== Торговые параметры ==', 10, y, clrNavy, True)
    y += 25
    CreateLabel('TradesInfo', 'Сделок в день: ' + IntegerToString(TradesPerDay) + ' (' + IntegerToString(metrics.monthlyTrades) + ' в месяц)', 10, y, clrBlack)
    y += 20
    CreateLabel('WinRate', 'Вероятность успеха: ' + DoubleToString(WinRate, 1) + '%', 10, y, clrBlack)
    y += 20
    CreateLabel('RRR', 'Риск/Прибыль: 1:' + DoubleToString(RiskRewardRatio, 1), 10, y, clrBlack)
    y += 20
    y += 10
    CreateLabel('Section3', '== Риск-менеджмент ==', 10, y, clrNavy, True)
    y += 25
    CreateLabel('MaxRiskTrade', 'Максимальный риск на сделку: ' + DoubleToString(metrics.maxRiskPerTrade, 2) + '%', 10, y, clrBlack)
    y += 20
    CreateLabel('MaxDrawdown', 'Лимит просадки: ' + DoubleToString(MaxDrawdownLimit, 1) + '%', 10, y, clrBlack)
    y += 20
    CreateLabel('ProbRuin', 'Вероятность разорения: ' + DoubleToString(metrics.probabilityOfRuin * 100, 4) + '%', 10, y, clrBlack)
    y += 20
    y += 10
    CreateLabel('Section4', '== Ожидаемая доходность ==', 10, y, clrNavy, True)
    y += 25
    CreateLabel('MonthlyReturn', 'Месячная доходность: ' + DoubleToString(metrics.expectedMonthlyReturn, 2) + '%', 10, y, clrGreen)
    y += 20
    CreateLabel('AnnualReturn', 'Годовая доходность: ' + DoubleToString(metrics.expectedAnnualReturn, 2) + '%', 10, y, clrGreen)
    y += 20
    y += 10
    CreateLabel('Section5', '== Прогноз капитала ==', 10, y, clrNavy, True)
    y += 25
    CreateLabel('MonthCapital', 'Через месяц: $' + FormatMoney(metrics.expectedMonthlyCapital), 10, y, clrGreen)
    y += 20
    CreateLabel('YearCapital', 'Через год: $' + FormatMoney(metrics.expectedAnnualCapital), 10, y, clrGreen)
    y += 20
    CreateLabel('FinalCapital', 'Через ' + IntegerToString(Years) + ' ' + YearDeclension(Years) + ': $' + FormatMoney(metrics.expectedFinalCapital), 10, y, clrGreen)
    y += 40
    UpdateChart()

def OnDeinit(reason):
    ObjectsDeleteAll(0, objPrefix)
    EventKillTimer()

def OnTimer():
    UpdatePanel()

def CreateLabel(name, text, x, y, clr, isBold=False):
    ObjectCreate(0, objPrefix + name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, objPrefix + name, OBJPROP_XDISTANCE, chartWidth - windowWidth - 10 + x)
    ObjectSetInteger(0, objPrefix + name, OBJPROP_YDISTANCE, y)
    ObjectSetString(0, objPrefix + name, OBJPROP_TEXT, text)
    ObjectSetInteger(0, objPrefix + name, OBJPROP_COLOR, clr)
    ObjectSetString(0, objPrefix + name, OBJPROP_FONT, ('Arial Bold' if isBold else 'Arial'))
    ObjectSetInteger(0, objPrefix + name, OBJPROP_FONTSIZE, (10 if isBold else 9))

def UpdateChart():
    ObjectDelete(0, objPrefix + 'Graph')
    ObjectCreate(0, objPrefix + 'Graph', OBJ_TREND, 0, 0, totalAmount[0], Years * 12, totalAmount[(Years * 12) - 1])
    ObjectSetInteger(0, objPrefix + 'Graph', OBJPROP_COLOR, clrBlue)
    ObjectSetInteger(0, objPrefix + 'Graph', OBJPROP_WIDTH, 2)
    ObjectSetInteger(0, objPrefix + 'Graph', OBJPROP_RAY_RIGHT, False)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    while i < rates_total and i < ArraySize(totalAmount):
        indicatorBuffer[i] = totalAmount[i]
        i += 1
    return rates_total

# ---- global variables initialised from expressions
metrics = _alloc(TradingMetrics)
metrics.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CompoundPercentForTrader(_MQL5Indicator):
    name = 'CompoundPercent For Trader'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InitialCapital': 1000.0,  # Начальный капитал
        'Years': 10,  # Количество лет
        'MonthlyDeposit': 100.0,  # Ежемесячное пополнение
        'TradesPerDay': 3,  # Количество сделок в день
        'WinRate': 55.0,  # Вероятность прибыльной сделки (%)
        'RiskRewardRatio': 1.5,  # Отношение риска к прибыли (1:X)
        'MaxDrawdownLimit': 20.0,  # Психологический барьер просадки (%)
        'RefreshInterval': 1,  # Интервал обновления (в секундах)
    }

