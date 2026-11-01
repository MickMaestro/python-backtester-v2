"""digvariation — converted from MQL5: MQL5 Indicators/DigVariation/digvariation.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11823615]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Variation'}, 'levels': [0.0], 'description': [], 'name': 'digvariation', 'source': 'MQL5 Indicators/DigVariation/digvariation.mq5', 'folder': 'DigVariation', 'inputs': [{'mql': 'Period_', 'py': 'Period_', 'param': 'Period_', 'type': 'int', 'default': 12, 'label': 'period of averaging', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 0, 'label': 'method of averaging', 'sinput': False}, {'mql': 'SmoothPower', 'py': 'SmoothPower', 'param': 'SmoothPower', 'type': 'int', 'default': 1, 'label': 'power of the signal smoothing', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Smooth
dig_0 = 0
dig_1 = 1
dig_2 = 2
dig_3 = 3
dig_4 = 4
dig_5 = 5
dig_6 = 6
dig_7 = 7
dig_8 = 8
dig_9 = 9
dig_10 = 10
_enum('Smooth', {0: 'dig_0', 1: 'dig_1', 2: 'dig_2', 3: 'dig_3', 4: 'dig_4', 5: 'dig_5', 6: 'dig_6', 7: 'dig_7', 8: 'dig_8', 9: 'dig_9', 10: 'dig_10'})

# ---- inputs and global variables
Period_ = _input('Period_', 12)  # period of averaging
MA_Method_ = _input('MA_Method_', MODE_SMA)  # method of averaging
SmoothPower = _input('SmoothPower', dig_1)  # power of the signal smoothing
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ExtMapBuffer = Arr(0, 0.0)
ExtCalcBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    XMA = CXMA()
    min_rates_total = (XMA.GetStartBars(MA_Method_, Period_, 0) * 2) + 52
    SetIndexBuffer(0, ExtMapBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetString(0, PLOT_LABEL, 'Variation')
    SetIndexBuffer(1, ExtCalcBuffer, INDICATOR_CALCULATIONS)
    shortname = Box("")
    StringConcatenate(shortname, 'Variation( Period_ = ', Period_, ', MA_Method_ = ', MA_Method_, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_start1, _s_OnCalculate_start2, min_rates_total
    min_rates_total += begin
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    ma = 0.0
    vr = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = begin
        _s_OnCalculate_start1 = begin
        if MA_Method_ != MODE_EMA:
            _s_OnCalculate_start2 = Period_ + begin
        else:
            _s_OnCalculate_start2 = begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ma = _s_OnCalculate_MA.MASeries(_s_OnCalculate_start1, prev_calculated, rates_total, Period_, MA_Method_, price[bar], bar, False)
        vr = _s_OnCalculate_VR.MASeries(_s_OnCalculate_start2, prev_calculated, rates_total, Period_, MA_Method_, price[bar] - ma, bar, False)
        if bar >= first:
            ExtCalcBuffer[bar] = 1000 * (price[bar] - (ma + vr))
        else:
            ExtCalcBuffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        ExtMapBuffer[bar] = SP(SmoothPower, ExtCalcBuffer, bar)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def SP(Smooth_Power, Array, index):
    res = 0.0
    _sw1 = Smooth_Power
    if _sw1 == 0:
        res = Array[index]
    elif _sw1 == 1:
        res = (0.29268754843 * Array[index]) + (0.2698679548204 * Array[index - 1]) + (0.2277786802786 * Array[index - 2]) + (0.172658858602 * Array[index - 3]) + (0.1124127695806 * Array[index - 4]) + (0.0550645669333 * Array[index - 5]) + (0.00733791069745 * Array[index - 6]) - (0.02637426808863 * Array[index - 7]) - (0.0445334647733 * Array[index - 8]) - (0.0483673837716 * Array[index - 9]) - (0.0412219004631 * Array[index - 10]) - (0.02759007317598 * Array[index - 11]) - (0.01206738017651 * Array[index - 12]) + (0.001567315986223 * Array[index - 13]) + (0.01094916192054 * Array[index - 14]) + (0.01530469318242 * Array[index - 15]) + (0.01532526278128 * Array[index - 16]) + (0.01296015381098 * Array[index - 17]) + (0.01157140552294 * Array[index - 18]) - (0.00533181209765 * Array[index - 19])
    elif _sw1 == 2:
        res = (0.2447098565978 * Array[index]) + (0.2313977400697 * Array[index - 1]) + (0.2061379694732 * Array[index - 2]) + (0.1716623034064 * Array[index - 3]) + (0.131469079036 * Array[index - 4]) + (0.0895038754956 * Array[index - 5]) + (0.0496009165125 * Array[index - 6]) + (0.01502270569607 * Array[index - 7]) - (0.0118803373443 * Array[index - 8]) - (0.02989873856137 * Array[index - 9]) - (0.038989671049 * Array[index - 10]) - (0.0401411362639 * Array[index - 11]) - (0.035119680858 * Array[index - 12]) - (0.02611613850342 * Array[index - 13]) - (0.01539056955666 * Array[index - 14]) - (0.00495353651394 * Array[index - 15]) + (0.00368588764825 * Array[index - 16]) + (0.00963614049782 * Array[index - 17]) + (0.01265138888314 * Array[index - 18]) + (0.01307496106868 * Array[index - 19]) + (0.01169702291063 * Array[index - 20]) + (0.00974841844086 * Array[index - 21]) + (0.00898900012545 * Array[index - 22]) - (0.00649745721156 * Array[index - 23])
    elif _sw1 == 3:
        res = (0.2101888714743 * Array[index]) + (0.2017361306871 * Array[index - 1]) + (0.1854987469779 * Array[index - 2]) + (0.1627557943437 * Array[index - 3]) + (0.1352455218956 * Array[index - 4]) + (0.1049955517302 * Array[index - 5]) + (0.0741580960823 * Array[index - 6]) + (0.044826258609 * Array[index - 7]) + (0.01870440453637 * Array[index - 8]) - (0.002814841280245 * Array[index - 9]) - (0.01891352345654 * Array[index - 10]) - (0.02929206622741 * Array[index - 11]) - (0.0341888300133 * Array[index - 12]) - (0.0342703255777 * Array[index - 13]) - (0.03055656616909 * Array[index - 14]) - (0.02422648959598 * Array[index - 15]) - (0.01651476470542 * Array[index - 16]) - (0.00857503584404 * Array[index - 17]) - (0.001351831295525 * Array[index - 18]) + (0.00448511071596 * Array[index - 19]) + (0.00855374511399 * Array[index - 20]) + (0.01076725654789 * Array[index - 21]) + (0.01131091969998 * Array[index - 22]) + (0.01057394212462 * Array[index - 23]) + (0.00912947281517 * Array[index - 24]) + (0.00771484446233 * Array[index - 25]) + (0.00732318993223 * Array[index - 26]) - (0.00726358358348 * Array[index - 27])
    elif _sw1 == 4:
        res = (0.1841600001487 * Array[index]) + (0.1784754786728 * Array[index - 1]) + (0.1674508960246 * Array[index - 2]) + (0.151750469997 * Array[index - 3]) + (0.1323034848757 * Array[index - 4]) + (0.110240182466 * Array[index - 5]) + (0.0867964146007 * Array[index - 6]) + (0.0632389269284 * Array[index - 7]) + (0.040738964719 * Array[index - 8]) + (0.0203507547445 * Array[index - 9]) + (0.002915227087755 * Array[index - 10]) - (0.01100443994875 * Array[index - 11]) - (0.02116075293157 * Array[index - 12]) - (0.02747786871251 * Array[index - 13]) - (0.03024034479978 * Array[index - 14]) - (0.02988490637108 * Array[index - 15]) - (0.02702558542347 * Array[index - 16]) - (0.02236077351054 * Array[index - 17]) - (0.01662176948519 * Array[index - 18]) - (0.01050105629699 * Array[index - 19]) - (0.00460605501191 * Array[index - 20]) + (0.000582766458037 * Array[index - 21]) + (0.00473324688655 * Array[index - 22]) + (0.00766855376673 * Array[index - 23]) + (0.00936273985238 * Array[index - 24]) + (0.00991966879705 * Array[index - 25]) + (0.00955690928799 * Array[index - 26]) + (0.00857195408578 * Array[index - 27]) + (0.00734849040305 * Array[index - 28]) + (0.00634910972836 * Array[index - 29]) + (0.00617002099346 * Array[index - 30]) - (0.00780070803276 * Array[index - 31])
    elif _sw1 == 5:
        res = (0.163850442955 * Array[index]) + (0.159848509062 * Array[index - 1]) + (0.1520285056667 * Array[index - 2]) + (0.1407759621461 * Array[index - 3]) + (0.1266145946036 * Array[index - 4]) + (0.1101999467868 * Array[index - 5]) + (0.0922810246421 * Array[index - 6]) + (0.0736414430377 * Array[index - 7]) + (0.0550613836268 * Array[index - 8]) + (0.0372780690048 * Array[index - 9]) + (0.02094281812508 * Array[index - 10]) + (0.00658930585105 * Array[index - 11]) - (0.00538855535197 * Array[index - 12]) - (0.01474498292814 * Array[index - 13]) - (0.02139199173398 * Array[index - 14]) - (0.02541417253316 * Array[index - 15]) - (0.02702341057229 * Array[index - 16]) - (0.02647614727071 * Array[index - 17]) - (0.02421775125345 * Array[index - 18]) - (0.02065411010395 * Array[index - 19]) - (0.01625074823286 * Array[index - 20]) - (0.01145130552469 * Array[index - 21]) - (0.00665356586398 * Array[index - 22]) - (0.002196710270528 * Array[index - 23]) + (0.001656596678561 * Array[index - 24]) + (0.00473296009497 * Array[index - 25]) + (0.00694308970535 * Array[index - 26]) + (0.00827947138512 * Array[index - 27]) + (0.00880879507493 * Array[index - 28]) + (0.00865791955067 * Array[index - 29]) + (0.00800414344065 * Array[index - 30]) + (0.00706330074106 * Array[index - 31]) + (0.00608814048308 * Array[index - 32]) + (0.00538380036114 * Array[index - 33]) + (0.00532891349043 * Array[index - 34]) - (0.00819568487412 * Array[index - 35])
    elif _sw1 == 6:
        res = (0.1475657670368 * Array[index]) + (0.1446405411673 * Array[index - 1]) + (0.1389042575727 * Array[index - 2]) + (0.1305751002746 * Array[index - 3]) + (0.1199864911731 * Array[index - 4]) + (0.1075255410806 * Array[index - 5]) + (0.0936615730647 * Array[index - 6]) + (0.078894909305 * Array[index - 7]) + (0.0637465101034 * Array[index - 8]) + (0.0487276238639 * Array[index - 9]) + (0.0343174315294 * Array[index - 10]) + (0.02094370638877 * Array[index - 11]) + (0.00896531966221 * Array[index - 12]) - (0.001341999129024 * Array[index - 13]) - (0.00978712653663 * Array[index - 14]) - (0.01627791183058 * Array[index - 15]) - (0.02080151436502 * Array[index - 16]) - (0.02343895781894 * Array[index - 17]) - (0.02435214700067 * Array[index - 18]) - (0.02376786389147 * Array[index - 19]) - (0.02193912806308 * Array[index - 20]) - (0.01912053352973 * Array[index - 21]) - (0.01567028095913 * Array[index - 22]) - (0.01183273845729 * Array[index - 23]) - (0.00790611190014 * Array[index - 24]) - (0.00412385952442 * Array[index - 25]) - (0.000685399211775 * Array[index - 26]) + (0.002260911767506 * Array[index - 27]) + (0.00461801537249 * Array[index - 28]) + (0.00633741616229 * Array[index - 29]) + (0.00741961543986 * Array[index - 30]) + (0.00790789206069 * Array[index - 31]) + (0.00788111695823 * Array[index - 32]) + (0.00745129870298 * Array[index - 33]) + (0.00674985662064 * Array[index - 34]) + (0.00593128562366 * Array[index - 35]) + (0.00517071741994 * Array[index - 36]) + (0.00467211882117 * Array[index - 37]) + (0.00468906740665 * Array[index - 38]) - (0.0084985123607 * Array[index - 39])
    elif _sw1 == 7:
        res = (0.1342157583828 * Array[index]) + (0.1320168704847 * Array[index - 1]) + (0.1276873471586 * Array[index - 2]) + (0.1213643729739 * Array[index - 3]) + (0.113252071346 * Array[index - 4]) + (0.1036083698498 * Array[index - 5]) + (0.0927280425508 * Array[index - 6]) + (0.0809406915977 * Array[index - 7]) + (0.0686105258715 * Array[index - 8]) + (0.0560701395588 * Array[index - 9]) + (0.0436869941553 * Array[index - 10]) + (0.0317716835118 * Array[index - 11]) + (0.02062340027452 * Array[index - 12]) + (0.01049287508919 * Array[index - 13]) + (0.001578073235404 * Array[index - 14]) - (0.0059750742244 * Array[index - 15]) - (0.01207707288043 * Array[index - 16]) - (0.01669798399142 * Array[index - 17]) - (0.01986198555101 * Array[index - 18]) - (0.02164119825031 * Array[index - 19]) - (0.02215230961811 * Array[index - 20]) - (0.02155191142867 * Array[index - 21]) - (0.02002808597329 * Array[index - 22]) - (0.0177822020377 * Array[index - 23]) - (0.0150032597344 * Array[index - 24]) - (0.01187583268349 * Array[index - 25]) - (0.00865026821576 * Array[index - 26]) - (0.00543510816909 * Array[index - 27]) - (0.002420531056597 * Array[index - 28]) + (0.0002889057085442 * Array[index - 29]) + (0.002599652575601 * Array[index - 30]) + (0.0044534438683 * Array[index - 31]) + (0.00582556501823 * Array[index - 32]) + (0.00671941035514 * Array[index - 33]) + (0.00716358274204 * Array[index - 34]) + (0.00721108593431 * Array[index - 35]) + (0.00693382886173 * Array[index - 36]) + (0.00641737976071 * Array[index - 37]) + (0.00576046002138 * Array[index - 38]) + (0.00507417448638 * Array[index - 39]) + (0.00448195239124 * Array[index - 40]) + (0.00412727462648 * Array[index - 41]) + (0.00418669196944 * Array[index - 42]) - (0.00873780054566 * Array[index - 43])
    elif _sw1 == 8:
        res = (0.1230811432921 * Array[index]) + (0.121383026598 * Array[index - 1]) + (0.1180348688628 * Array[index - 2]) + (0.113124847739 * Array[index - 3]) + (0.1067888736447 * Array[index - 4]) + (0.0991886630563 * Array[index - 5]) + (0.0905283970643 * Array[index - 6]) + (0.0810323992972 * Array[index - 7]) + (0.0709406523601 * Array[index - 8]) + (0.0605028783409 * Array[index - 9]) + (0.0499660517196 * Array[index - 10]) + (0.0395768971912 * Array[index - 11]) + (0.02956612933181 * Array[index - 12]) + (0.0201298282845 * Array[index - 13]) + (0.01146221166452 * Array[index - 14]) + (0.00369983285522 * Array[index - 15]) - (0.003038977187834 * Array[index - 16]) - (0.00868021984873 * Array[index - 17]) - (0.01318508621117 * Array[index - 18]) - (0.01655096644715 * Array[index - 19]) - (0.01881253249101 * Array[index - 20]) - (0.02003063357865 * Array[index - 21]) - (0.02029727780544 * Array[index - 22]) - (0.01972188576919 * Array[index - 23]) - (0.0184347735491 * Array[index - 24]) - (0.01658081992154 * Array[index - 25]) - (0.01430671529886 * Array[index - 26]) - (0.01175302972849 * Array[index - 27]) - (0.00904320119485 * Array[index - 28]) - (0.00630514721661 * Array[index - 29]) - (0.00369357675439 * Array[index - 30]) - (0.001242693518572 * Array[index - 31]) + (0.000926258391563 * Array[index - 32]) + (0.002776968147451 * Array[index - 33]) + (0.00426926013496 * Array[index - 34]) + (0.00538851571708 * Array[index - 35]) + (0.00613947934547 * Array[index - 36]) + (0.00654179765073 * Array[index - 37]) + (0.00663281051554 * Array[index - 38]) + (0.00645954126814 * Array[index - 39]) + (0.00608069576729 * Array[index - 40]) + (0.00556313321406 * Array[index - 41]) + (0.00497954512068 * Array[index - 42]) + (0.00441241979276 * Array[index - 43]) + (0.00395101867555 * Array[index - 44]) + (0.00369891645504 * Array[index - 45]) + (0.00378072162625 * Array[index - 46]) - (0.00893024660315 * Array[index - 47])
    elif _sw1 == 9:
        res = (0.1136491141667 * Array[index]) + (0.112313087008 * Array[index - 1]) + (0.1096691394261 * Array[index - 2]) + (0.105783720779 * Array[index - 3]) + (0.1007420961698 * Array[index - 4]) + (0.0946599675379 * Array[index - 5]) + (0.0876755484183 * Array[index - 6]) + (0.0799429655454 * Array[index - 7]) + (0.0716292336416 * Array[index - 8]) + (0.0629123835413 * Array[index - 9]) + (0.0539767262326 * Array[index - 10]) + (0.0450048491714 * Array[index - 11]) + (0.0361703734359 * Array[index - 12]) + (0.02763520549089 * Array[index - 13]) + (0.019550114518 * Array[index - 14]) + (0.01205357915205 * Array[index - 15]) + (0.00525211553366 * Array[index - 16]) - (0.000770477101024 * Array[index - 17]) - (0.00593916191975 * Array[index - 18]) - (0.01022805895137 * Array[index - 19]) - (0.01361544672818 * Array[index - 20]) - (0.01611640231317 * Array[index - 21]) - (0.01776260795296 * Array[index - 22]) - (0.01860554342447 * Array[index - 23]) - (0.01871505916941 * Array[index - 24]) - (0.01817487448682 * Array[index - 25]) - (0.01707856129273 * Array[index - 26]) - (0.01552770218471 * Array[index - 27]) - (0.01362988259084 * Array[index - 28]) - (0.0114933268048 * Array[index - 29]) - (0.00921892385382 * Array[index - 30]) - (0.00689459719023 * Array[index - 31]) - (0.00459651305691 * Array[index - 32]) - (0.002411870743968 * Array[index - 33]) - (0.000431732873329 * Array[index - 34]) + (0.001353807064687 * Array[index - 35]) + (0.002857282707287 * Array[index - 36]) + (0.00408190921586 * Array[index - 37]) + (0.00501143566228 * Array[index - 38]) + (0.00565074521587 * Array[index - 39]) + (0.0060156430603 * Array[index - 40]) + (0.00613066979989 * Array[index - 41]) + (0.0060292357405 * Array[index - 42]) + (0.00575258932729 * Array[index - 43]) + (0.00534744169195 * Array[index - 44]) + (0.00486457915178 * Array[index - 45]) + (0.00435951288835 * Array[index - 46]) + (0.00389329662905 * Array[index - 47]) + (0.00353234960893 * Array[index - 48]) + (0.00335331131328 * Array[index - 49]) + (0.00344636014208 * Array[index - 50]) - (0.00908964634931 * Array[index - 51])
    elif _sw1 == 10:
        res = (0.363644232288 * Array[index]) + (0.319961361319 * Array[index - 1]) + (0.2429021537279 * Array[index - 2]) + (0.1499479402208 * Array[index - 3]) + (0.0606476023757 * Array[index - 4]) - (0.00876136797274 * Array[index - 5]) - (0.0492967601969 * Array[index - 6]) - (0.0606402244647 * Array[index - 7]) - (0.0496978153976 * Array[index - 8]) - (0.02724932305397 * Array[index - 9]) - (0.00400372352396 * Array[index - 10]) + (0.01244416185618 * Array[index - 11]) + (0.0192794164712 * Array[index - 12]) + (0.0182176723798 * Array[index - 13]) + (0.01598780862402 * Array[index - 14]) - (0.00338313465225 * Array[index - 15])
    return res

# ---- static local variables
_s_OnCalculate_start1 = 0
_s_OnCalculate_start2 = 0
_s_OnCalculate_MA = CMoving_Average()
_s_OnCalculate_VR = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Digvariation(_MQL5Indicator):
    name = 'digvariation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_': 12,  # period of averaging
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # method of averaging
        'SmoothPower': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10'}, default=1),  # power of the signal smoothing
        'Shift': 0,  # horizontal shift of the indicator in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

