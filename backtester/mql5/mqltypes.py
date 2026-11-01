"""Static types used by the translator, and the signatures of the MQL5
built-in functions it needs to know (return types for integer-division
typing, and which arguments are scalar references)."""

from __future__ import annotations

INTEGRAL = {"int", "uint", "long", "ulong", "short", "ushort", "char", "uchar", "bool",
            "datetime", "color"}
FLOATING = {"double", "float"}
NUMERIC = INTEGRAL | FLOATING

INT_WIDTH = {"int": (32, True), "uint": (32, False), "long": (64, True), "ulong": (64, False),
             "short": (16, True), "ushort": (16, False), "char": (8, True), "uchar": (8, False),
             "datetime": (64, True), "color": (32, False)}

CONVERTER = {"int": "_int", "uint": "_uint", "long": "_long", "ulong": "_ulong", "short": "_short",
             "ushort": "_ushort", "char": "_char", "uchar": "_uchar", "datetime": "_long",
             "color": "_uint"}

SIZEOF = {"bool": 1, "char": 1, "uchar": 1, "short": 2, "ushort": 2, "int": 4, "uint": 4,
          "color": 4, "float": 4, "long": 8, "ulong": 8, "double": 8, "datetime": 8, "string": 12}


def is_int(t: str) -> bool:
    return t in INTEGRAL or t.startswith("enum:")


def is_float(t: str) -> bool:
    return t in FLOATING


def is_num(t: str) -> bool:
    return is_int(t) or is_float(t)


def is_array(t: str) -> bool:
    return t.endswith("[]")


def elem(t: str) -> str:
    return t[:-2] if t.endswith("[]") else "?"


def is_obj(t: str) -> bool:
    return t.startswith("C:") or t.startswith("P:")


def obj_class(t: str) -> str:
    return t[2:] if is_obj(t) else ""


def is_ptr(t: str) -> bool:
    return t.startswith("P:")


# ---------------------------------------------------------------- built-ins
# name: return type.  'same' = type of the first argument
_RET = """
double: MathAbs MathMax MathMin MathSqrt MathPow MathLog MathLog10 MathLog2 MathLog1p MathExp MathExpm1
 MathFloor MathCeil MathRound MathMod MathSin MathCos MathTan MathArcsin MathArccos MathArctan MathArctan2
 MathSinh MathCosh MathTanh MathArcsinh MathArccosh MathArctanh fabs sqrt pow log log10 exp floor ceil fmod sin cos
 tan asin acos atan atan2 round NormalizeDouble StringToDouble iOpen iHigh iLow iClose SymbolInfoDouble
 AccountInfoDouble ObjectGetDouble ChartGetDouble GlobalVariableGet ObjectGetValueByTime PositionGetDouble
 OrderGetDouble HistoryDealGetDouble HistoryOrderGetDouble FileReadDouble FileReadNumber MathRandomNonZero
 TerminalInfoDouble AccountBalance AccountEquity AccountFreeMargin TesterStatistics MathQuantile
int: ArrayResize ArraySize ArrayRange ArrayInitialize ArrayCopy ArrayMaximum ArrayMinimum ArrayBsearch
 ArrayCompare Bars iBars iBarShift iHighest iLowest CopyBuffer CopyTime CopyOpen CopyHigh CopyLow CopyClose
 CopyTickVolume CopyRealVolume CopySpread CopyRates CopyTicks BarsCalculated iMA iRSI iATR iStdDev iBands iMACD
 iOsMA iStochastic iCCI iMomentum iWPR iSAR iADX iADXWilder iDeMarker iMFI iRVI iTriX iBearsPower iBullsPower
 iForce iAO iAC iAlligator iEnvelopes iFractals iGator iIchimoku iBWMFI iAD iOBV iVolumes iChaikin iDEMA iTEMA
 iFrAMA iAMA iVIDyA iCustom IndicatorCreate StringLen StringFind StringGetCharacter StringGetChar StringReplace
 StringSplit StringToCharArray StringToShortArray StringCompare StringConcatenate StringTrimLeft StringTrimRight
 StringBufferLen PeriodSeconds Period ChartPeriod GetLastError Digits ObjectFind ObjectsTotal ObjectsDeleteAll
 ChartWindowFind WindowFind MathRand rand GetTickCount UninitializeReason MQLInfoInteger MQL5InfoInteger
 TerminalInfoInteger SymbolsTotal PositionsTotal OrdersTotal HistoryDealsTotal HistoryOrdersTotal
 FileOpen FileWrite FileWriteString FileReadInteger FileSize FileTell FileWriteDouble FileWriteInteger
 FileReadArray FileWriteArray FileFindFirst FileLoad TimeDayOfWeek TimeDayOfYear TimeYear TimeMonth TimeDay
 TimeHour TimeMinute TimeSeconds MessageBox IndicatorParameters GlobalVariablesTotal GlobalVariablesDeleteAll
 ChartIndicatorsTotal ChartIndicatorGet StringToInteger_i ColorToARGB ArrayDimension WebRequest
 MathClassify CharToString_len TimeDaylightSavings TimeGMTOffset ChartWindowOnDropped EventChartCustom_i
 SymbolInfoSessionsTotal ResourceCreate_i CheckPointer
long: StringToInteger SymbolInfoInteger AccountInfoInteger ObjectGetInteger ChartGetInteger SeriesInfoInteger
 ChartID ChartFirst ChartNext ChartOpen PositionGetInteger OrderGetInteger HistoryDealGetInteger
 HistoryOrderGetInteger GetTickCount64 GetMicrosecondCount PlotIndexGetInteger iVolume iTickVolume iRealVolume
 TerminalInfoLong PositionGetTicket OrderGetTicket HistoryDealGetTicket HistoryOrderGetTicket
int_spread: iSpread
datetime: TimeCurrent TimeLocal TimeGMT TimeTradeServer StringToTime StructToTime iTime GlobalVariableTime
 GlobalVariableSet FileReadDatetime
string: DoubleToString IntegerToString CharToString ShortToString StringSubstr StringFormat TimeToString
 Symbol ChartSymbol SymbolName EnumToString ColorToString TerminalInfoString MQLInfoString MQL5InfoString
 SymbolInfoString AccountInfoString ObjectGetString ObjectName ChartGetString GlobalVariableName
 CharArrayToString ShortArrayToString FileReadString PositionGetString OrderGetString HistoryDealGetString
 HistoryOrderGetString StringToUpper_s StringToLower_s ChartIndicatorName typename DoubleToStr
 ObjectDescription StringTrim
bool: ArraySetAsSeries ArrayGetAsSeries ArrayIsSeries ArrayIsDynamic ArrayFree_b ArraySort ArrayReverse
 ArrayInsert ArrayRemove ArraySwap IsStopped SetIndexBuffer IndicatorSetInteger IndicatorSetDouble
 IndicatorSetString PlotIndexSetInteger PlotIndexSetDouble PlotIndexSetString IndicatorRelease ObjectCreate
 ObjectDelete ObjectSetInteger ObjectSetDouble ObjectSetString ObjectMove ChartSetInteger ChartSetDouble
 ChartSetString ChartRedraw_b TimeToStruct SymbolSelect SymbolInfoTick MathIsValidNumber StringSetCharacter
 StringToUpper StringToLower StringAdd StringInit StringFill GlobalVariableCheck GlobalVariableDel
 GlobalVariableTemp EventSetTimer EventSetMillisecondTimer PlaySound SendMail SendNotification SendFTP
 FileIsExist FileDelete FileIsEnding FileIsLineEnding FileSeek FileReadBool FileFindNext FolderCreate
 SymbolIsSynchronized SymbolExist PositionSelect PositionSelectByTicket OrderSelect HistorySelect
 HistorySelectByPosition OrderSend OrderCheck ChartTimePriceToXY ChartXYToTimePrice TextSetFont TextOut
 TextGetSize ResourceCreate ResourceSave ResourceReadImage ChartApplyTemplate ChartSaveTemplate ChartScreenShot
 ChartNavigate ChartIndicatorAdd ChartIndicatorDelete MarketBookAdd MarketBookRelease MarketBookGet
 GlobalVariableSetOnCondition SymbolInfoSessionQuote SymbolInfoSessionTrade ChartClose ChartSetSymbolPeriod
 IndicatorShortName IndicatorDigits ObjectSetText ArrayPrint_b
uint: ColorToARGB_u
color: StringToColor RGB
void: Print Alert Comment PrintFormat printf ArrayFree ArrayFill ArrayPrint ResetLastError SetUserError
 ChartRedraw WindowRedraw EventKillTimer FileClose FileFlush FileFindClose MathSrand srand Sleep ZeroMemory
 MathSwap DebugBreak ExpertRemove TesterStop GlobalVariablesFlush
"""

BUILTIN_RET: dict[str, str] = {}
for _block in _RET.strip().split("\n"):
    pass
_cur = None
for _tok in _RET.split():
    if _tok.endswith(":"):
        _cur = _tok[:-1]
        continue
    BUILTIN_RET[_tok] = {"int_spread": "int"}.get(_cur, _cur)

# argument positions passed by reference (scalars/strings), keyed by name -> {argcount: positions}
# argcount None = any
BUILTIN_REFS: dict[str, dict] = {
    "StringConcatenate": {None: (0,)},
    "StringReplace": {None: (0,)},
    "StringTrimLeft": {None: (0,)},
    "StringTrimRight": {None: (0,)},
    "StringToUpper": {None: (0,)},
    "StringToLower": {None: (0,)},
    "StringSetCharacter": {None: (0,)},
    "StringInit": {None: (0,)},
    "StringFill": {None: (0,)},
    "StringAdd": {None: (0,)},
    "SymbolInfoDouble": {3: (2,)},
    "SymbolInfoInteger": {3: (2,)},
    "SymbolInfoString": {3: (2,)},
    "SeriesInfoInteger": {4: (3,)},
    "ChartGetInteger": {4: (3,)},
    "ChartGetDouble": {4: (3,)},
    "ChartGetString": {3: (2,)},
    "ObjectGetInteger": {5: (4,)},
    "ObjectGetDouble": {5: (4,)},
    "ObjectGetString": {5: (4,)},
    "GlobalVariableGet": {2: (1,)},
    "TextGetSize": {None: (1, 2)},
    "ChartTimePriceToXY": {None: (4, 5)},
    "ChartXYToTimePrice": {None: (3, 4, 5)},
    "PositionGetDouble": {2: (1,)},
    "PositionGetInteger": {2: (1,)},
    "PositionGetString": {2: (1,)},
    "OrderGetDouble": {2: (1,)},
    "OrderGetInteger": {2: (1,)},
    "OrderGetString": {2: (1,)},
    "HistoryDealGetDouble": {3: (2,)},
    "HistoryDealGetInteger": {3: (2,)},
    "HistoryDealGetString": {3: (2,)},
    "HistoryOrderGetDouble": {3: (2,)},
    "HistoryOrderGetInteger": {3: (2,)},
    "HistoryOrderGetString": {3: (2,)},
    "MathSwap": {None: (0, 1)},
    "ZeroMemory": {None: (0,)},
    "SymbolExist": {2: (1,)},
    "IndicatorParameters": {None: (1,)},
}

# Names the translator rewrites
SPECIAL_NAMES = {
    "_Point": "Point()", "_Digits": "Digits()", "_Symbol": "Symbol()", "_Period": "Period()",
    "_LastError": "GetLastError()", "_StopFlag": "False", "_UninitReason": "0", "_RandomSeed": "0",
    "_IsX64": "True", "Point": None, "Digits": None,
}
SPECIAL_TYPES = {"_Point": "double", "_Digits": "int", "_Symbol": "string", "_Period": "enum:ENUM_TIMEFRAMES",
                 "_LastError": "int", "_StopFlag": "bool", "_UninitReason": "int", "_RandomSeed": "uint",
                 "_IsX64": "bool"}

# fields of built-in structs
BUILTIN_STRUCT_FIELDS = {
    "MqlRates": {"time": "datetime", "open": "double", "high": "double", "low": "double", "close": "double",
                 "tick_volume": "long", "spread": "int", "real_volume": "long"},
    "MqlDateTime": {"year": "int", "mon": "int", "day": "int", "hour": "int", "min": "int", "sec": "int",
                    "day_of_week": "int", "day_of_year": "int"},
    "MqlTick": {"time": "datetime", "bid": "double", "ask": "double", "last": "double", "volume": "ulong",
                "time_msc": "long", "flags": "uint", "volume_real": "double"},
    "MqlParam": {"type": "int", "integer_value": "long", "double_value": "double", "string_value": "string"},
    "MqlBookInfo": {"type": "int", "price": "double", "volume": "long", "volume_real": "double"},
    "MqlTradeRequest": {}, "MqlTradeResult": {}, "MqlTradeCheckResult": {}, "MqlTradeTransaction": {},
}
