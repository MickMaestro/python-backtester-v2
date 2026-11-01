"""HarmonicPatternFinder — converted from MQL5: MQL5 Indicators/Harmonic Pattern Finder/HarmonicPatternFinder.mq5

Indicator to display existent and emerging harmonic chart patterns.
Copyright: Copyright 2016, Andre S. Enger.; Link: andre_enger@hotmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, Andre S. Enger.', 'link': 'andre_enger@hotmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [4294967295]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Zig Zag'}, 'levels': [], 'description': ['Indicator to display existent and emerging harmonic chart patterns.'], 'name': 'HarmonicPatternFinder', 'source': 'MQL5 Indicators/Harmonic Pattern Finder/HarmonicPatternFinder.mq5', 'folder': 'Harmonic Pattern Finder', 'inputs': [{'mql': 'SwingSize', 'py': 'SwingSize', 'param': 'SwingSize', 'type': 'int', 'default': 100, 'label': 'ZZ sensitivity in points', 'sinput': False}, {'mql': 'SlackRange', 'py': 'SlackRange', 'param': 'SlackRange', 'type': 'double', 'default': 0.01, 'label': 'Max slack for fib ratios (range)', 'sinput': False}, {'mql': 'SlackUnary', 'py': 'SlackUnary', 'param': 'SlackUnary', 'type': 'double', 'default': 0.1, 'label': 'Max slack for fib ratios (unary)', 'sinput': False}, {'mql': 'BarsAnalyzed', 'py': 'BarsAnalyzed', 'param': 'BarsAnalyzed', 'type': 'int', 'default': 200, 'label': 'Max bars per pattern', 'sinput': False}, {'mql': 'History', 'py': 'History', 'param': 'History', 'type': 'int', 'default': 1000, 'label': 'Max history bars to process', 'sinput': False}, {'mql': 'MaxSamePoints', 'py': 'MaxSamePoints', 'param': 'MaxSamePoints', 'type': 'int', 'default': 0, 'label': 'Max shared points per pattern', 'sinput': False}, {'mql': 'EmergingPatterns', 'py': 'EmergingPatterns', 'param': 'EmergingPatterns', 'type': 'bool', 'default': False, 'label': 'Enable emerging pattern projections', 'sinput': False}, {'mql': 'NumProjectionTries', 'py': 'NumProjectionTries', 'param': 'NumProjectionTries', 'type': 'int', 'default': 100, 'label': 'Number of projections', 'sinput': False}, {'mql': 'AtrIncrement', 'py': 'AtrIncrement', 'param': 'AtrIncrement', 'type': 'double', 'default': 0.1, 'label': 'Increment per projection in ATRs', 'sinput': False}, {'mql': 'AtrPeriod', 'py': 'AtrPeriod', 'param': 'AtrPeriod', 'type': 'int', 'default': 50, 'label': 'ATR-period used in projections', 'sinput': False}, {'mql': 'ClrBull', 'py': 'ClrBull', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Color for bullish patterns', 'sinput': False}, {'mql': 'ClrBear', 'py': 'ClrBear', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color for bearish patterns', 'sinput': False}, {'mql': 'ClrBullProjection', 'py': 'ClrBullProjection', 'param': None, 'type': 'color', 'default': 13959039, 'label': 'Color for projected bullish patterns', 'sinput': False}, {'mql': 'ClrBearProjection', 'py': 'ClrBearProjection', 'param': None, 'type': 'color', 'default': 11823615, 'label': 'Color for projected bearish patterns', 'sinput': False}, {'mql': 'Show_abcd', 'py': 'Show_abcd', 'param': 'Show_abcd', 'type': 'bool', 'default': True, 'label': 'Display AB=CD', 'sinput': False}, {'mql': 'Show_gartley', 'py': 'Show_gartley', 'param': 'Show_gartley', 'type': 'bool', 'default': True, 'label': 'Display Gartley', 'sinput': False}, {'mql': 'Show_bat', 'py': 'Show_bat', 'param': 'Show_bat', 'type': 'bool', 'default': True, 'label': 'Display Bat', 'sinput': False}, {'mql': 'Show_altbat', 'py': 'Show_altbat', 'param': 'Show_altbat', 'type': 'bool', 'default': True, 'label': 'Display Alt. Bat', 'sinput': False}, {'mql': 'Show_butterfly', 'py': 'Show_butterfly', 'param': 'Show_butterfly', 'type': 'bool', 'default': True, 'label': 'Display Butterfly', 'sinput': False}, {'mql': 'Show_crab', 'py': 'Show_crab', 'param': 'Show_crab', 'type': 'bool', 'default': True, 'label': 'Display Crab', 'sinput': False}, {'mql': 'Show_deepcrab', 'py': 'Show_deepcrab', 'param': 'Show_deepcrab', 'type': 'bool', 'default': True, 'label': 'Display Deepcrab', 'sinput': False}, {'mql': 'Show_threedrives', 'py': 'Show_threedrives', 'param': 'Show_threedrives', 'type': 'bool', 'default': True, 'label': 'Display Three Drives', 'sinput': False}, {'mql': 'Show_cypher', 'py': 'Show_cypher', 'param': 'Show_cypher', 'type': 'bool', 'default': True, 'label': 'Display Cypher', 'sinput': False}, {'mql': 'Show_shark', 'py': 'Show_shark', 'param': 'Show_shark', 'type': 'bool', 'default': True, 'label': 'Display Shark', 'sinput': False}, {'mql': 'Show_fiveo', 'py': 'Show_fiveo', 'param': 'Show_fiveo', 'type': 'bool', 'default': True, 'label': 'Display 5-0', 'sinput': False}, {'mql': 'Show_nenstar', 'py': 'Show_nenstar', 'param': 'Show_nenstar', 'type': 'bool', 'default': True, 'label': 'Display Nen Star', 'sinput': False}, {'mql': 'Show_blackswan', 'py': 'Show_blackswan', 'param': 'Show_blackswan', 'type': 'bool', 'default': True, 'label': 'Display Black Swan', 'sinput': False}, {'mql': 'Show_whiteswan', 'py': 'Show_whiteswan', 'param': 'Show_whiteswan', 'type': 'bool', 'default': True, 'label': 'Display White Swan', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SwingSize = _input('SwingSize', 100)  # ZZ sensitivity in points
SlackRange = _input('SlackRange', 0.01)  # Max slack for fib ratios (range)
SlackUnary = _input('SlackUnary', 0.1)  # Max slack for fib ratios (unary)
BarsAnalyzed = _input('BarsAnalyzed', 200)  # Max bars per pattern
History = _input('History', 1000)  # Max history bars to process
MaxSamePoints = _input('MaxSamePoints', 0)  # Max shared points per pattern
EmergingPatterns = _input('EmergingPatterns', False)  # Enable emerging pattern projections
NumProjectionTries = _input('NumProjectionTries', 100)  # Number of projections
AtrIncrement = _input('AtrIncrement', 0.1)  # Increment per projection in ATRs
AtrPeriod = _input('AtrPeriod', 50)  # ATR-period used in projections
ClrBull = _input('ClrBull', clrGreen)  # Color for bullish patterns
ClrBear = _input('ClrBear', clrRed)  # Color for bearish patterns
ClrBullProjection = _input('ClrBullProjection', clrAquamarine)  # Color for projected bullish patterns
ClrBearProjection = _input('ClrBearProjection', clrHotPink)  # Color for projected bearish patterns
Show_abcd = _input('Show_abcd', True)  # Display AB=CD
Show_gartley = _input('Show_gartley', True)  # Display Gartley
Show_bat = _input('Show_bat', True)  # Display Bat
Show_altbat = _input('Show_altbat', True)  # Display Alt. Bat
Show_butterfly = _input('Show_butterfly', True)  # Display Butterfly
Show_crab = _input('Show_crab', True)  # Display Crab
Show_deepcrab = _input('Show_deepcrab', True)  # Display Deepcrab
Show_threedrives = _input('Show_threedrives', True)  # Display Three Drives
Show_cypher = _input('Show_cypher', True)  # Display Cypher
Show_shark = _input('Show_shark', True)  # Display Shark
Show_fiveo = _input('Show_fiveo', True)  # Display 5-0
Show_nenstar = _input('Show_nenstar', True)  # Display Nen Star
Show_blackswan = _input('Show_blackswan', True)  # Display Black Swan
Show_whiteswan = _input('Show_whiteswan', True)  # Display White Swan
peaks = Arr(0, 0.0)
troughs = Arr(0, 0.0)
lastDirection = False
_atr = 0.0
_lastPeak = 0
_lastTrough = 0
maxPatternInstances = 0
zzHandle = 0
numPatterns = 0
patternInstanceCounter = 0
monotonicIndices = Arr(0, 0)
monotonicIndicesCounter = Arr(0, 0)
patternCounter = Arr(0, 0)
patternNames = Arr(0, "")
patternX = Arr(0, 0, dims=(10,))
patternA = Arr(0, 0, dims=(10,))
patternB = Arr(0, 0, dims=(10,))
patternC = Arr(0, 0, dims=(10,))
patternD = Arr(0, 0, dims=(10,))

class PATTERN_DESCRIPTOR(MqlObject):
    _q_fields = ('ab2xa_min', 'ab2xa_max', 'bc2ab_min', 'bc2ab_max', 'cd2bc_min', 'cd2bc_max', 'ad2xa_min', 'ad2xa_max', 'cd2xc_min', 'cd2xc_max', 'xc2xa_min', 'xc2xa_max')
    def __init__(self, *args):
        self.ab2xa_min = 0.0
        self.ab2xa_max = 0.0
        self.bc2ab_min = 0.0
        self.bc2ab_max = 0.0
        self.cd2bc_min = 0.0
        self.cd2bc_max = 0.0
        self.ad2xa_min = 0.0
        self.ad2xa_max = 0.0
        self.cd2xc_min = 0.0
        self.cd2xc_max = 0.0
        self.xc2xa_min = 0.0
        self.xc2xa_max = 0.0

class PATTERN_INSTANCE(MqlObject):
    _q_fields = ('patternIndex', 'patternBufferIndex', 'bullish', 'XDateTime', 'ADateTime', 'BDateTime', 'CDateTime', 'DDateTime')
    def __init__(self, *args):
        self.patternIndex = 0
        self.patternBufferIndex = 0
        self.bullish = False
        self.XDateTime = 0
        self.ADateTime = 0
        self.BDateTime = 0
        self.CDateTime = 0
        self.DDateTime = 0

def OnInit():
    global _atr, zzHandle
    SetIndexBuffer(0, peaks, INDICATOR_DATA)
    SetIndexBuffer(1, troughs, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    zzHandle = iCustom(None, 0, 'Downloads\\fastzz', SwingSize)
    if zzHandle == INVALID_HANDLE:
        printf('Error obtaining handle')
    if ArrayResize(monotonicIndices, BarsAnalyzed) < BarsAnalyzed:
        printf('Error allocating array')
    if ArrayResize(monotonicIndicesCounter, BarsAnalyzed) < BarsAnalyzed:
        printf('Error allocating array')
    PopulatePatterns()
    _atr = 0.0
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ArrayFree(monotonicIndices)
    ArrayFree(monotonicIndicesCounter)
    ArrayFree(patterns)
    ArrayFree(patternInstances)
    ArrayFree(patternNames)
    ArrayFree(patternCounter)
    ArrayFree(patternX)
    ArrayFree(patternA)
    ArrayFree(patternB)
    ArrayFree(patternC)
    ArrayFree(patternD)
    for i in range(ObjectsTotal(0, 0, -1) - 1, 0 - 1, -1):
        name = ObjectName(0, i, 0, -1)
        if StringFind(name, 'Bullish') != -1 or StringFind(name, 'Bearish') != -1:
            ObjectDelete(0, name)

def OnReinit():
    global _atr, _lastPeak, _lastTrough, patternInstanceCounter
    _atr = 0.0
    _lastPeak = 0
    _lastTrough = 0
    patternInstanceCounter = 0
    ArrayFill(patternCounter, 0, numPatterns, 0)
    for i in range(0, numPatterns):
        for j in range(0, 10):
            patternX[i][j] = 0
            patternA[i][j] = 0
            patternB[i][j] = 0
            patternC[i][j] = 0
            patternD[i][j] = 0
    for i in range(ObjectsTotal(0, 0, -1) - 1, 0 - 1, -1):
        name = ObjectName(0, i, 0, -1)
        if StringFind(name, 'Bullish') != -1 or StringFind(name, 'Bearish') != -1:
            ObjectDelete(0, name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _atr, _lastPeak, _lastTrough, lastDirection, patternInstanceCounter
    start = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        OnReinit()
        start = 0
    else:
        start = prev_calculated - 1
    start = MathMax(1, start)
    CopyBuffer(zzHandle, 0, 0, rates_total, peaks)
    CopyBuffer(zzHandle, 1, 0, rates_total, troughs)
    atr = _atr
    for bar in range(start, rates_total):
        if bar < (rates_total - History):
            continue
        tr = MathMax(high[bar], close[bar - 1]) - MathMin(low[bar], close[bar - 1])
        atr += (tr - atr) * _fdiv(2.0, 1.0 + AtrPeriod)
        if bar < (rates_total - 1):
            _atr = atr
        lastPeak = FirstNonZeroFrom(bar, peaks)
        lastTrough = FirstNonZeroFrom(bar, troughs)
        if lastPeak == -1 or lastTrough == -1:
            continue
        endsInTrough = lastTrough > lastPeak
        verticalZZ = lastTrough == lastPeak
        zzUp = not endsInTrough
        if lastPeak == _lastPeak and lastTrough == _lastTrough:
            continue
        _lastPeak = lastPeak
        _lastTrough = lastTrough
        if verticalZZ:
            lastPeakBefore = FirstNonZeroFrom(lastPeak - 1, peaks)
            lastTroughBefore = FirstNonZeroFrom(lastTrough - 1, troughs)
            while lastPeakBefore == lastTroughBefore:
                lastPeakBefore = FirstNonZeroFrom(lastPeakBefore - 1, peaks)
                lastTroughBefore = FirstNonZeroFrom(lastTroughBefore - 1, troughs)
                if lastPeakBefore == -1 or lastTroughBefore == -1:
                    break
            if lastPeakBefore == -1 or lastTroughBefore == -1:
                continue
            zzUp = lastPeakBefore > lastTroughBefore
            endsInTrough = not zzUp
        patternIndex = 0
        while patternIndex < numPatterns:
            if verticalZZ:
                UndisplayProjection(patternIndex, True)
                UndisplayProjection(patternIndex, False)
            else:
                UndisplayProjection(patternIndex, endsInTrough)
            patternIndex += 1
        if (not verticalZZ) and lastDirection == endsInTrough:
            UndisplayPatterns()
        patternInstanceCounter = 0
        lastDirection = endsInTrough
        runTwice = verticalZZ
        maxProjections = (NumProjectionTries if EmergingPatterns else 1)
        projection = 0
        while projection < maxProjections:
            increment = (((maxProjections - projection - 1) * (atr * AtrIncrement)) if EmergingPatterns else 0)
            DIndex = (lastTrough if endsInTrough else lastPeak)
            D = ((troughs[DIndex] - increment) if endsInTrough else (peaks[DIndex] + increment))
            ArrayFill(monotonicIndices, 0, BarsAnalyzed, -1)
            ArrayFill(monotonicIndicesCounter, 0, BarsAnalyzed, -1)
            firstExtreme = (lastPeak if endsInTrough else lastTrough)
            if verticalZZ:
                if endsInTrough and zzUp:
                    firstExtreme = FirstNonZeroFrom(lastPeak - 1, peaks)
                if (not endsInTrough) and (not zzUp):
                    firstExtreme = FirstNonZeroFrom(lastTrough - 1, troughs)
            numExtremums = 0
            monotonicIndices[numExtremums] = firstExtreme
            for i in range(firstExtreme - 1, MathMax(0, DIndex - BarsAnalyzed) - 1, -1):
                currentExtreme = (peaks[i] if endsInTrough else troughs[i])
                if not IsProperValue(currentExtreme):
                    continue
                previousExtreme = (peaks[monotonicIndices[numExtremums]] if endsInTrough else troughs[monotonicIndices[numExtremums]])
                if (endsInTrough and currentExtreme > previousExtreme) or ((not endsInTrough) and currentExtreme < previousExtreme):
                    numExtremums += 1
                    monotonicIndices[numExtremums] = i
            numExtremums += 1
            for i in range(0, numExtremums - 1):
                youngerExtreme = monotonicIndices[i]
                olderExtreme = monotonicIndices[i + 1]
                counterExtreme = (LowestFromTo(olderExtreme, youngerExtreme, troughs) if endsInTrough else HighestFromTo(olderExtreme, youngerExtreme, peaks))
                if counterExtreme == -1:
                    counterExtreme = (LowestFromTo(olderExtreme, youngerExtreme, low) if endsInTrough else HighestFromTo(olderExtreme, youngerExtreme, high))
                if counterExtreme == -1:
                    continue
                monotonicIndicesCounter[i] = counterExtreme
            patternIndex = 0
            while patternIndex < numPatterns:
                if patternIndex == 0 and (not Show_abcd):
                    patternIndex += 1
                    continue
                if patternIndex == 1 and (not Show_gartley):
                    patternIndex += 1
                    continue
                if patternIndex == 2 and (not Show_bat):
                    patternIndex += 1
                    continue
                if patternIndex == 3 and (not Show_altbat):
                    patternIndex += 1
                    continue
                if patternIndex == 4 and (not Show_butterfly):
                    patternIndex += 1
                    continue
                if patternIndex == 5 and (not Show_crab):
                    patternIndex += 1
                    continue
                if patternIndex == 6 and (not Show_deepcrab):
                    patternIndex += 1
                    continue
                if patternIndex == 7 and (not Show_threedrives):
                    patternIndex += 1
                    continue
                if patternIndex == 8 and (not Show_cypher):
                    patternIndex += 1
                    continue
                if patternIndex == 9 and (not Show_shark):
                    patternIndex += 1
                    continue
                if patternIndex == 10 and (not Show_fiveo):
                    patternIndex += 1
                    continue
                if patternIndex == 11 and (not Show_nenstar):
                    patternIndex += 1
                    continue
                if patternIndex == 12 and (not Show_blackswan):
                    patternIndex += 1
                    continue
                if patternIndex == 13 and (not Show_whiteswan):
                    patternIndex += 1
                    continue
                pattern = _copy(patterns[patternIndex])
                ab2xaConstraint = pattern.ab2xa_max != 0 and pattern.ab2xa_min != 0
                ad2xaConstraint = pattern.ad2xa_max != 0 and pattern.ad2xa_min != 0
                bc2abConstraint = pattern.bc2ab_max != 0 and pattern.bc2ab_min != 0
                cd2bcConstraint = pattern.cd2bc_max != 0 and pattern.cd2bc_min != 0
                cd2xcConstraint = pattern.cd2xc_max != 0 and pattern.cd2xc_min != 0
                xc2xaConstraint = pattern.xc2xa_max != 0 and pattern.xc2xa_min != 0
                ab2xaSlack = (SlackUnary if (pattern.ab2xa_max == pattern.ab2xa_min) else SlackRange)
                ad2xaSlack = (SlackUnary if (pattern.ad2xa_max == pattern.ad2xa_min) else SlackRange)
                bc2abSlack = (SlackUnary if (pattern.bc2ab_max == pattern.bc2ab_min) else SlackRange)
                cd2bcSlack = (SlackUnary if (pattern.cd2bc_max == pattern.cd2bc_min) else SlackRange)
                cd2xcSlack = (SlackUnary if (pattern.cd2xc_max == pattern.cd2xc_min) else SlackRange)
                xc2xaSlack = (SlackUnary if (pattern.xc2xa_max == pattern.xc2xa_min) else SlackRange)
                insideA = True
                if bc2abConstraint:
                    insideA = pattern.bc2ab_min > 1.0
                if xc2xaConstraint:
                    insideA = pattern.xc2xa_min > 1.0
                insideB = True
                if cd2bcConstraint:
                    insideB = pattern.cd2bc_min > 1.0
                patternPossible = True
                for k in range(0, numExtremums):
                    CIndex = monotonicIndices[k]
                    C = (peaks[CIndex] if endsInTrough else troughs[CIndex])
                    CD = MathAbs(C - D)
                    counterExtremeIndex = 0
                    if k == 0:
                        counterExtremeIndex = (LowestFromTo(CIndex, DIndex, troughs) if endsInTrough else HighestFromTo(CIndex, DIndex, peaks))
                    else:
                        counterExtremeIndex = monotonicIndicesCounter[k - 1]
                    counterExtremeValue = (troughs[counterExtremeIndex] if endsInTrough else peaks[counterExtremeIndex])
                    if (endsInTrough and counterExtremeValue < D) or ((not endsInTrough) and counterExtremeValue > D):
                        patternPossible = False
                        break
                    previousBIndex = 0
                    previousB = (DBL_MIN if endsInTrough else DBL_MAX)
                    previousA = (DBL_MIN if endsInTrough else DBL_MAX)
                    k2 = (CIndex if insideA else k)
                    while True:
                        AIndex = 0
                        if insideA:
                            k2 -= 1
                            if k2 < MathMax(0, DIndex - BarsAnalyzed):
                                break
                            AIndex = k2
                        else:
                            k2 += 1
                            if k2 >= numExtremums:
                                break
                            AIndex = monotonicIndices[k2]
                        A = (peaks[AIndex] if endsInTrough else troughs[AIndex])
                        if not IsProperValue(A):
                            continue
                        if insideA and ((endsInTrough and A > C) or ((not endsInTrough) and A < C)):
                            break
                        newBIndex = 0
                        if not insideA:
                            newBIndex = monotonicIndicesCounter[k2 - 1]
                        else:
                            newBIndex = (LowestFromTo(AIndex, CIndex, troughs) if endsInTrough else HighestFromTo(AIndex, CIndex, peaks))
                        if newBIndex == -1:
                            patternPossible = False
                            break
                        newB = (troughs[newBIndex] if endsInTrough else peaks[newBIndex])
                        newBLower = (endsInTrough and newB < previousB) or ((not endsInTrough) and newB > previousB)
                        if not insideA:
                            if newBLower:
                                break
                            if (endsInTrough and previousB == DBL_MIN) or ((not endsInTrough) and previousB == DBL_MAX):
                                previousBIndex = newBIndex
                                previousB = newB
                        else:
                            if newBLower or ((endsInTrough and previousB == DBL_MIN) or ((not endsInTrough) and previousB == DBL_MAX)):
                                previousBIndex = newBIndex
                                previousB = newB
                                previousA = A
                            if (endsInTrough and A < previousA) or ((not endsInTrough) and A > previousA):
                                continue
                            previousA = A
                        BIndex = previousBIndex
                        B = previousB
                        AB = MathAbs(A - B)
                        BC = MathAbs(C - B)
                        AD = MathAbs(A - D)
                        if AB == 0:
                            continue
                        if BC == 0:
                            continue
                        if AD == 0:
                            continue
                        bc2abRatio = _fdiv(BC, AB)
                        cd2bcRatio = _fdiv(CD, BC)
                        if insideB and ((endsInTrough and B < D) or ((not endsInTrough) and B > D)):
                            patternPossible = False
                            break
                        bc2abConstraintSatisfied = not bc2abConstraint
                        bc2abConstraintSatisfied |= (pattern.bc2ab_min - bc2abSlack) <= bc2abRatio and bc2abRatio <= (pattern.bc2ab_max + bc2abSlack)
                        cd2bcConstraintSatisfied = not cd2bcConstraint
                        cd2bcConstraintSatisfied |= (pattern.cd2bc_min - cd2bcSlack) <= cd2bcRatio and cd2bcRatio <= (pattern.cd2bc_max + cd2bcSlack)
                        if bc2abConstraintSatisfied and cd2bcConstraintSatisfied:
                            if (((not ab2xaConstraint) and (not ad2xaConstraint)) and (not cd2xcConstraint)) and (not xc2xaConstraint):
                                if projection == (maxProjections - 1):
                                    DisplayPattern_1(patternIndex, endsInTrough, time[AIndex], A, time[BIndex], B, time[CIndex], C, time[DIndex], D)
                                else:
                                    DisplayProjection_1(patternIndex, endsInTrough, time[AIndex], A, time[BIndex], B, time[CIndex], C, time[bar], D)
                                patternPossible = False
                                break
                            previousX = (DBL_MAX if endsInTrough else DBL_MIN)
                            for k3 in range(AIndex - 1, MathMax(0, DIndex - BarsAnalyzed) - 1, -1):
                                intermediateExtreme = (peaks[k3] if endsInTrough else troughs[k3])
                                if IsProperValue(intermediateExtreme) and ((endsInTrough and intermediateExtreme > A) or ((not endsInTrough) and intermediateExtreme < A)):
                                    break
                                X = (troughs[k3] if endsInTrough else peaks[k3])
                                if not IsProperValue(X):
                                    continue
                                if (endsInTrough and X > previousX) or ((not endsInTrough) and X < previousX):
                                    continue
                                previousX = X
                                XA = MathAbs(A - X)
                                XC = MathAbs(X - C)
                                if XA == 0:
                                    continue
                                if XC == 0:
                                    continue
                                xabRatio = _fdiv(AB, XA)
                                xadRatio = _fdiv(AD, XA)
                                cd2xcRatio = _fdiv(CD, XC)
                                xc2xaRatio = _fdiv(XC, XA)
                                ab2xaConstraintSatisfied = not ab2xaConstraint
                                ab2xaConstraintSatisfied |= (pattern.ab2xa_min - ab2xaSlack) <= xabRatio and xabRatio <= (pattern.ab2xa_max + ab2xaSlack)
                                ad2xaConstraintSatisfied = not ad2xaConstraint
                                ad2xaConstraintSatisfied |= (pattern.ad2xa_min - ad2xaSlack) <= xadRatio and xadRatio <= (pattern.ad2xa_max + ad2xaSlack)
                                cd2xcConstraintSatisfied = not cd2xcConstraint
                                cd2xcConstraintSatisfied |= (pattern.cd2xc_min - cd2xcSlack) <= cd2xcRatio and cd2xcRatio <= (pattern.cd2xc_max + cd2xcSlack)
                                xc2xaConstraintSatisfied = not xc2xaConstraint
                                xc2xaConstraintSatisfied |= (pattern.xc2xa_min - xc2xaSlack) <= xc2xaRatio and xc2xaRatio <= (pattern.xc2xa_max + xc2xaSlack)
                                if ((ab2xaConstraintSatisfied and ad2xaConstraintSatisfied) and cd2xcConstraintSatisfied) and xc2xaConstraintSatisfied:
                                    if projection == (maxProjections - 1):
                                        DisplayPattern_2(patternIndex, endsInTrough, time[k3], X, time[AIndex], A, time[BIndex], B, time[CIndex], C, time[DIndex], D)
                                    else:
                                        DisplayProjection_2(patternIndex, endsInTrough, time[k3], X, time[AIndex], A, time[BIndex], B, time[CIndex], C, time[bar], D)
                                    patternPossible = False
                                    break
                    if not patternPossible:
                        break
                patternIndex += 1
            if runTwice and projection == (maxProjections - 1):
                projection = -1
                runTwice = False
                endsInTrough = not endsInTrough
            projection += 1
    return rates_total

def FirstNonZeroFrom(start, array):
    for j in range(start, 0 - 1, -1):
        if IsProperValue(array[j]):
            return j
    return -1

def LowestFromTo(start, end, array):
    min_ = DBL_MAX
    index = -1
    for i in range(start, end + 1):
        if IsProperValue(array[i]) and array[i] <= min_:
            min_ = array[i]
            index = i
    return index

def HighestFromTo(start, end, array):
    max_ = DBL_MIN
    index = -1
    for i in range(start, end + 1):
        if IsProperValue(array[i]) and array[i] >= max_:
            max_ = array[i]
            index = i
    return index

def IsProperValue(value):
    return value != 0 and value != EMPTY_VALUE

def DisplayPattern_1(k, bullish, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D):
    global maxPatternInstances, patternInstanceCounter
    unique = ' ' + TimeToString(ADateTime) + TimeToString(BDateTime) + TimeToString(CDateTime) + TimeToString(DDateTime)
    prefix = ('Bullish ' if bullish else 'Bearish ')
    name0 = prefix + patternNames[k] + ' AB' + unique
    name1 = prefix + patternNames[k] + ' BC' + unique
    name2 = prefix + patternNames[k] + ' CD' + unique
    if ObjectFind(0, name0) >= 0:
        return
    overlaps = False
    for i in range(0, 10):
        numMatches = 0
        if ADateTime == patternA[k][i]:
            numMatches += 1
        if BDateTime == patternB[k][i]:
            numMatches += 1
        if CDateTime == patternC[k][i]:
            numMatches += 1
        if DDateTime == patternD[k][i]:
            numMatches += 1
        if numMatches > MaxSamePoints:
            overlaps = True
            break
    if overlaps:
        return
    index = patternCounter[k]
    patternCounter[k] = _imod(index + 1, 10)
    patternA[k][index] = ADateTime
    patternB[k][index] = BDateTime
    patternC[k][index] = CDateTime
    patternD[k][index] = DDateTime
    ObjectCreate(0, name0, OBJ_TREND, 0, ADateTime, A, BDateTime, B)
    ObjectCreate(0, name1, OBJ_TREND, 0, BDateTime, B, CDateTime, C)
    ObjectCreate(0, name2, OBJ_ARROWED_LINE, 0, CDateTime, C, DDateTime, D)
    ObjectSetInteger(0, name0, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name1, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name2, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name0, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name1, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name2, OBJPROP_SELECTABLE, True)
    ObjectSetString(0, name0, OBJPROP_TOOLTIP, StringSubstr(name0, 0, StringLen(name0) - StringLen(unique)))
    ObjectSetString(0, name1, OBJPROP_TOOLTIP, StringSubstr(name1, 0, StringLen(name1) - StringLen(unique)))
    ObjectSetString(0, name2, OBJPROP_TOOLTIP, StringSubstr(name2, 0, StringLen(name2) - StringLen(unique)))
    if EmergingPatterns:
        UndisplayProjection(k, bullish)
    patternInstances[patternInstanceCounter].patternIndex = k
    patternInstances[patternInstanceCounter].patternBufferIndex = index
    patternInstances[patternInstanceCounter].bullish = bullish
    patternInstances[patternInstanceCounter].ADateTime = ADateTime
    patternInstances[patternInstanceCounter].BDateTime = BDateTime
    patternInstances[patternInstanceCounter].CDateTime = CDateTime
    patternInstances[patternInstanceCounter].DDateTime = DDateTime
    patternInstanceCounter += 1
    if patternInstanceCounter >= maxPatternInstances:
        maxPatternInstances *= 2
        if ArrayResize(patternInstances, maxPatternInstances) < maxPatternInstances:
            printf('Error allocating array')

def DisplayPattern_2(k, bullish, XDateTime, X, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D):
    global maxPatternInstances, patternInstanceCounter
    unique = ' ' + TimeToString(XDateTime) + TimeToString(ADateTime) + TimeToString(BDateTime) + TimeToString(CDateTime) + TimeToString(DDateTime)
    prefix = ('Bullish ' if bullish else 'Bearish ')
    name0 = prefix + patternNames[k] + ' XA' + unique
    name1 = prefix + patternNames[k] + ' AB' + unique
    name2 = prefix + patternNames[k] + ' BC' + unique
    name3 = prefix + patternNames[k] + ' CD' + unique
    name4 = prefix + patternNames[k] + ' XAB=' + unique
    name5 = prefix + patternNames[k] + ' XAD=' + unique
    name6 = prefix + patternNames[k] + ' ABC=' + unique
    name7 = prefix + patternNames[k] + ' BCD=' + unique
    if ObjectFind(0, name0) >= 0:
        return
    overlaps = False
    for i in range(0, 10):
        numMatches = 0
        if XDateTime == patternX[k][i]:
            numMatches += 1
        if ADateTime == patternA[k][i]:
            numMatches += 1
        if BDateTime == patternB[k][i]:
            numMatches += 1
        if CDateTime == patternC[k][i]:
            numMatches += 1
        if DDateTime == patternD[k][i]:
            numMatches += 1
        if numMatches > MaxSamePoints:
            overlaps = True
            break
    if overlaps:
        return
    index = patternCounter[k]
    patternCounter[k] = _imod(index + 1, 10)
    patternX[k][index] = XDateTime
    patternA[k][index] = ADateTime
    patternB[k][index] = BDateTime
    patternC[k][index] = CDateTime
    patternD[k][index] = DDateTime
    xab = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(A - B), MathAbs(X - A)))))
    xad = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(D - A), MathAbs(X - A)))))
    abc = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(C - B), MathAbs(B - A)))))
    if k == 8 or k == 11:
        abc = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(X - C), MathAbs(X - A)))))
    bcd = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(C - D), MathAbs(B - C)))))
    ObjectCreate(0, name0, OBJ_TREND, 0, XDateTime, X, ADateTime, A)
    ObjectCreate(0, name1, OBJ_TREND, 0, ADateTime, A, BDateTime, B)
    ObjectCreate(0, name2, OBJ_TREND, 0, BDateTime, B, CDateTime, C)
    ObjectCreate(0, name3, OBJ_ARROWED_LINE, 0, CDateTime, C, DDateTime, D)
    ObjectCreate(0, name4, OBJ_TREND, 0, XDateTime, X, BDateTime, B)
    if k != 10:
        ObjectCreate(0, name5, OBJ_TREND, 0, XDateTime, X, DDateTime, D)
    ObjectCreate(0, name6, OBJ_TREND, 0, ADateTime, A, CDateTime, C)
    ObjectCreate(0, name7, OBJ_TREND, 0, BDateTime, B, DDateTime, D)
    ObjectSetInteger(0, name0, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name1, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name2, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name3, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name4, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    if k != 10:
        ObjectSetInteger(0, name5, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name6, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name7, OBJPROP_COLOR, (ClrBull if bullish else ClrBear))
    ObjectSetInteger(0, name4, OBJPROP_STYLE, STYLE_DOT)
    if k != 10:
        ObjectSetInteger(0, name5, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, name6, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, name7, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, name0, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name1, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name2, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name3, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name4, OBJPROP_SELECTABLE, True)
    if k != 10:
        ObjectSetInteger(0, name5, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name6, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name7, OBJPROP_SELECTABLE, True)
    ObjectSetString(0, name0, OBJPROP_TOOLTIP, StringSubstr(name0, 0, StringLen(name0) - StringLen(unique)))
    ObjectSetString(0, name1, OBJPROP_TOOLTIP, StringSubstr(name1, 0, StringLen(name1) - StringLen(unique)))
    ObjectSetString(0, name2, OBJPROP_TOOLTIP, StringSubstr(name2, 0, StringLen(name2) - StringLen(unique)))
    ObjectSetString(0, name3, OBJPROP_TOOLTIP, StringSubstr(name3, 0, StringLen(name3) - StringLen(unique)))
    ObjectSetString(0, name4, OBJPROP_TOOLTIP, StringSubstr(name4, 0, StringLen(name4) - StringLen(unique)) + xab)
    if k != 10:
        ObjectSetString(0, name5, OBJPROP_TOOLTIP, StringSubstr(name5, 0, StringLen(name5) - StringLen(unique)) + xad)
    ObjectSetString(0, name6, OBJPROP_TOOLTIP, StringSubstr(name6, 0, StringLen(name6) - StringLen(unique)) + abc)
    ObjectSetString(0, name7, OBJPROP_TOOLTIP, StringSubstr(name7, 0, StringLen(name7) - StringLen(unique)) + bcd)
    if EmergingPatterns:
        UndisplayProjection(k, bullish)
    patternInstances[patternInstanceCounter].patternIndex = k
    patternInstances[patternInstanceCounter].patternBufferIndex = index
    patternInstances[patternInstanceCounter].bullish = bullish
    patternInstances[patternInstanceCounter].XDateTime = XDateTime
    patternInstances[patternInstanceCounter].ADateTime = ADateTime
    patternInstances[patternInstanceCounter].BDateTime = BDateTime
    patternInstances[patternInstanceCounter].CDateTime = CDateTime
    patternInstances[patternInstanceCounter].DDateTime = DDateTime
    patternInstanceCounter += 1
    if patternInstanceCounter >= maxPatternInstances:
        maxPatternInstances *= 2
        if ArrayResize(patternInstances, maxPatternInstances) < maxPatternInstances:
            printf('Error allocating array')

def DisplayProjection_1(k, bullish, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D):
    prefix = ('Projected Bullish ' if bullish else 'Projected Bearish ')
    name0 = prefix + patternNames[k] + ' AB'
    name1 = prefix + patternNames[k] + ' BC'
    name2 = prefix + patternNames[k] + ' CD'
    overlaps = False
    for i in range(0, 10):
        numMatches = 0
        if ADateTime == patternA[k][i]:
            numMatches += 1
        if BDateTime == patternB[k][i]:
            numMatches += 1
        if CDateTime == patternC[k][i]:
            numMatches += 1
        if DDateTime == patternD[k][i]:
            numMatches += 1
        if numMatches > MaxSamePoints:
            overlaps = True
            break
    if overlaps:
        return
    ObjectCreate(0, name0, OBJ_TREND, 0, ADateTime, A, BDateTime, B)
    ObjectCreate(0, name1, OBJ_TREND, 0, BDateTime, B, CDateTime, C)
    ObjectCreate(0, name2, OBJ_ARROWED_LINE, 0, CDateTime, C, DDateTime, D)
    ObjectSetInteger(0, name0, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name1, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name2, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name0, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name1, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name2, OBJPROP_SELECTABLE, True)

def DisplayProjection_2(k, bullish, XDateTime, X, ADateTime, A, BDateTime, B, CDateTime, C, DDateTime, D):
    prefix = ('Projected Bullish ' if bullish else 'Projected Bearish ')
    name0 = prefix + patternNames[k] + ' XA'
    name1 = prefix + patternNames[k] + ' AB'
    name2 = prefix + patternNames[k] + ' BC'
    name3 = prefix + patternNames[k] + ' CD'
    name4 = prefix + patternNames[k] + ' XAB='
    name5 = prefix + patternNames[k] + ' XAD='
    name6 = prefix + patternNames[k] + ' ABC='
    name7 = prefix + patternNames[k] + ' BCD='
    overlaps = False
    for i in range(0, 10):
        numMatches = 0
        if XDateTime == patternX[k][i]:
            numMatches += 1
        if ADateTime == patternA[k][i]:
            numMatches += 1
        if BDateTime == patternB[k][i]:
            numMatches += 1
        if CDateTime == patternC[k][i]:
            numMatches += 1
        if DDateTime == patternD[k][i]:
            numMatches += 1
        if numMatches > MaxSamePoints:
            overlaps = True
            break
    if overlaps:
        return
    xab = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(A - B), MathAbs(X - A)))))
    xad = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(D - A), MathAbs(X - A)))))
    abc = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(C - B), MathAbs(B - A)))))
    if k == 8 or k == 11:
        abc = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(X - C), MathAbs(X - A)))))
    bcd = IntegerToString(_int(MathRound(_fdiv(100 * MathAbs(C - D), MathAbs(B - C)))))
    ObjectCreate(0, name0, OBJ_TREND, 0, XDateTime, X, ADateTime, A)
    ObjectCreate(0, name1, OBJ_TREND, 0, ADateTime, A, BDateTime, B)
    ObjectCreate(0, name2, OBJ_TREND, 0, BDateTime, B, CDateTime, C)
    ObjectCreate(0, name3, OBJ_ARROWED_LINE, 0, CDateTime, C, DDateTime, D)
    ObjectCreate(0, name4, OBJ_TREND, 0, XDateTime, X, BDateTime, B)
    if k != 10:
        ObjectCreate(0, name5, OBJ_TREND, 0, XDateTime, X, DDateTime, D)
    ObjectCreate(0, name6, OBJ_TREND, 0, ADateTime, A, CDateTime, C)
    ObjectCreate(0, name7, OBJ_TREND, 0, BDateTime, B, DDateTime, D)
    ObjectSetInteger(0, name0, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name1, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name2, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name3, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name4, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    if k != 10:
        ObjectSetInteger(0, name5, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name6, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name7, OBJPROP_COLOR, (ClrBullProjection if bullish else ClrBearProjection))
    ObjectSetInteger(0, name4, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, name5, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, name6, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, name7, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, name0, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name1, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name2, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name3, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name4, OBJPROP_SELECTABLE, True)
    if k != 10:
        ObjectSetInteger(0, name5, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name6, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(0, name7, OBJPROP_SELECTABLE, True)
    ObjectSetString(0, name4, OBJPROP_TOOLTIP, name4 + xab)
    if k != 10:
        ObjectSetString(0, name5, OBJPROP_TOOLTIP, name5 + xad)
    ObjectSetString(0, name6, OBJPROP_TOOLTIP, name6 + abc)
    ObjectSetString(0, name7, OBJPROP_TOOLTIP, name7 + bcd)

def UndisplayProjection(k, bullish):
    prefix = ('Projected Bullish ' if bullish else 'Projected Bearish ')
    name0 = prefix + patternNames[k] + ' XA'
    name1 = prefix + patternNames[k] + ' AB'
    name2 = prefix + patternNames[k] + ' BC'
    name3 = prefix + patternNames[k] + ' CD'
    name4 = prefix + patternNames[k] + ' XAB='
    name5 = prefix + patternNames[k] + ' XAD='
    name6 = prefix + patternNames[k] + ' ABC='
    name7 = prefix + patternNames[k] + ' BCD='
    ObjectDelete(0, name0)
    ObjectDelete(0, name1)
    ObjectDelete(0, name2)
    ObjectDelete(0, name3)
    ObjectDelete(0, name4)
    ObjectDelete(0, name5)
    ObjectDelete(0, name6)
    ObjectDelete(0, name7)

def UndisplayPatterns():
    global patternInstanceCounter
    for i in range(0, patternInstanceCounter):
        instance = _copy(patternInstances[i])
        k = instance.patternIndex
        index = instance.patternBufferIndex
        bullish = instance.bullish
        XDateTime = instance.XDateTime
        ADateTime = instance.ADateTime
        BDateTime = instance.BDateTime
        CDateTime = instance.CDateTime
        DDateTime = instance.DDateTime
        unique = ' ' + ('' if (k == 0) else TimeToString(XDateTime)) + TimeToString(ADateTime) + TimeToString(BDateTime) + TimeToString(CDateTime) + TimeToString(DDateTime)
        prefix = ('Bullish ' if bullish else 'Bearish ')
        name0 = prefix + patternNames[k] + ' XA' + unique
        name1 = prefix + patternNames[k] + ' AB' + unique
        name2 = prefix + patternNames[k] + ' BC' + unique
        name3 = prefix + patternNames[k] + ' CD' + unique
        name4 = prefix + patternNames[k] + ' XAB=' + unique
        name5 = prefix + patternNames[k] + ' XAD=' + unique
        name6 = prefix + patternNames[k] + ' ABC=' + unique
        name7 = prefix + patternNames[k] + ' BCD=' + unique
        ObjectDelete(0, name0)
        ObjectDelete(0, name1)
        ObjectDelete(0, name2)
        ObjectDelete(0, name3)
        ObjectDelete(0, name4)
        ObjectDelete(0, name5)
        ObjectDelete(0, name6)
        ObjectDelete(0, name7)
        patternX[k][index] = 0
        patternA[k][index] = 0
        patternB[k][index] = 0
        patternC[k][index] = 0
        patternD[k][index] = 0
        count = patternCounter[k]
        patternCounter[k] = ((10 - 1) if (count == 0) else (count - 1))
    patternInstanceCounter = 0

def PopulatePatterns():
    global maxPatternInstances, numPatterns
    abcd = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 0.618, 0.786, 1.272, 1.618, 0, 0, 0, 0, 0, 0])
    gartley = _struct_init(PATTERN_DESCRIPTOR(), [0.618, 0.618, 0.382, 0.886, 1.272, 1.618, 0.786, 0.786, 0, 0, 0, 0])
    bat = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.5, 0.382, 0.886, 1.618, 2.618, 0.886, 0.886, 0, 0, 0, 0])
    altbat = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.382, 0.382, 0.886, 2, 3.618, 1.13, 1.13, 0, 0, 0, 0])
    butterfly = _struct_init(PATTERN_DESCRIPTOR(), [0.786, 0.786, 0.382, 0.886, 1.618, 2.618, 1.272, 1.618, 0, 0, 0, 0])
    crab = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 0.382, 0.886, 2.24, 3.618, 1.618, 1.618, 0, 0, 0, 0])
    deepcrab = _struct_init(PATTERN_DESCRIPTOR(), [0.886, 0.886, 0.382, 0.886, 2.618, 3.618, 1.618, 1.618, 0, 0, 0, 0])
    threedrives = _struct_init(PATTERN_DESCRIPTOR(), [1.272, 1.618, 0.618, 0.786, 1.272, 1.618, 0, 0, 0, 0, 0, 0])
    cypher = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 0, 0, 0, 0, 0, 0, 0.786, 0.786, 1.13, 1.414])
    shark = _struct_init(PATTERN_DESCRIPTOR(), [0, 0, 1.13, 1.618, 1.618, 2.24, 0, 0, 0.886, 1.13, 0, 0])
    fiveo = _struct_init(PATTERN_DESCRIPTOR(), [1.13, 1.618, 1.618, 2.24, 0.5, 0.5, 0, 0, 0, 0, 0, 0])
    nenstar = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.618, 0, 0, 0, 0, 0, 0, 1.272, 1.272, 1.13, 1.414])
    blackswan = _struct_init(PATTERN_DESCRIPTOR(), [1.382, 2.618, 0.236, 0.5, 1.128, 2, 1.128, 2.618, 0, 0, 0, 0])
    whiteswan = _struct_init(PATTERN_DESCRIPTOR(), [0.382, 0.724, 2, 4.237, 0.5, 0.886, 0.382, 0.886, 0, 0, 0, 0])
    numPatterns = 14
    maxPatternInstances = numPatterns * 10
    if ArrayResize(patterns, numPatterns) < numPatterns:
        printf('Error allocating array')
    if ArrayResize(patternNames, numPatterns) < numPatterns:
        printf('Error allocating array')
    if ArrayResize(patternX, numPatterns) < numPatterns:
        printf('Error allocating array')
    if ArrayResize(patternA, numPatterns) < numPatterns:
        printf('Error allocating array')
    if ArrayResize(patternB, numPatterns) < numPatterns:
        printf('Error allocating array')
    if ArrayResize(patternC, numPatterns) < numPatterns:
        printf('Error allocating array')
    if ArrayResize(patternD, numPatterns) < numPatterns:
        printf('Error allocating array')
    if ArrayResize(patternCounter, numPatterns) < numPatterns:
        printf('Error allocating array')
    if ArrayResize(patternInstances, maxPatternInstances) < maxPatternInstances:
        printf('Error allocating array')
    ArrayFill(patternCounter, 0, numPatterns, 0)
    _assign(patterns[0], abcd)
    patternNames[0] = 'AB=CD'
    _assign(patterns[1], gartley)
    patternNames[1] = 'Gartley'
    _assign(patterns[2], bat)
    patternNames[2] = 'Bat'
    _assign(patterns[3], altbat)
    patternNames[3] = 'Alt. Bat'
    _assign(patterns[4], butterfly)
    patternNames[4] = 'Butterfly'
    _assign(patterns[5], crab)
    patternNames[5] = 'Crab'
    _assign(patterns[6], deepcrab)
    patternNames[6] = 'Deep Crab'
    _assign(patterns[7], threedrives)
    patternNames[7] = 'Three Drives'
    _assign(patterns[8], cypher)
    patternNames[8] = 'Cypher'
    _assign(patterns[9], shark)
    patternNames[9] = 'Shark'
    _assign(patterns[10], fiveo)
    patternNames[10] = '5-0'
    _assign(patterns[11], nenstar)
    patternNames[11] = 'Nen Star'
    _assign(patterns[12], blackswan)
    patternNames[12] = 'Black Swan'
    _assign(patterns[13], whiteswan)
    patternNames[13] = 'White Swan'

# ---- global variables initialised from expressions
patterns = Arr(0, 0, factory=PATTERN_DESCRIPTOR)
patternInstances = Arr(0, 0, factory=PATTERN_INSTANCE)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HarmonicPatternFinder(_MQL5Indicator):
    name = 'HarmonicPatternFinder'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'SwingSize': 100,  # ZZ sensitivity in points
        'SlackRange': 0.01,  # Max slack for fib ratios (range)
        'SlackUnary': 0.1,  # Max slack for fib ratios (unary)
        'BarsAnalyzed': 200,  # Max bars per pattern
        'History': 1000,  # Max history bars to process
        'MaxSamePoints': 0,  # Max shared points per pattern
        'EmergingPatterns': False,  # Enable emerging pattern projections
        'NumProjectionTries': 100,  # Number of projections
        'AtrIncrement': 0.1,  # Increment per projection in ATRs
        'AtrPeriod': 50,  # ATR-period used in projections
        'Show_abcd': True,  # Display AB=CD
        'Show_gartley': True,  # Display Gartley
        'Show_bat': True,  # Display Bat
        'Show_altbat': True,  # Display Alt. Bat
        'Show_butterfly': True,  # Display Butterfly
        'Show_crab': True,  # Display Crab
        'Show_deepcrab': True,  # Display Deepcrab
        'Show_threedrives': True,  # Display Three Drives
        'Show_cypher': True,  # Display Cypher
        'Show_shark': True,  # Display Shark
        'Show_fiveo': True,  # Display 5-0
        'Show_nenstar': True,  # Display Nen Star
        'Show_blackswan': True,  # Display Black Swan
        'Show_whiteswan': True,  # Display White Swan
    }

