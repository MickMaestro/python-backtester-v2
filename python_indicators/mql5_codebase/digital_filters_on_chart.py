"""Digital filters - on chart — converted from MQL5: MQL5 Indicators/Digital Filters - on chart/Digital filters - on chart.mq5

Digital filters - on chart
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Digital filter'}, 'levels': [], 'description': ['Digital filters - on chart'], 'name': 'Digital filters - on chart', 'source': 'MQL5 Indicators/Digital Filters - on chart/Digital filters - on chart.mq5', 'folder': 'Digital Filters - on chart', 'inputs': [{'mql': 'inpType', 'py': 'inpType', 'param': 'inpType', 'type': 'int', 'default': 1, 'label': 'Filter type', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enType
fatl = 0
satl = 1
rftl = 2
rstl = 3
_enum('enType', {0: 'fatl', 1: 'satl', 2: 'rftl', 3: 'rstl'})

# ---- inputs and global variables
inpType = _input('inpType', satl)  # Filter type
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)
filter_ = Arr(0, 0.0)
filterSize = 0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    _sw1 = inpType
    if _sw1 == fatl:
        fillFatl(filter_, _GlobRef(globals(), 'filterSize'))
    elif _sw1 == satl:
        fillSatl(filter_, _GlobRef(globals(), 'filterSize'))
    elif _sw1 == rftl:
        fillRftl(filter_, _GlobRef(globals(), 'filterSize'))
    elif _sw1 == rstl:
        fillRstl(filter_, _GlobRef(globals(), 'filterSize'))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Digital ' + EnumToString(inpType, 'enType'))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = 0.0
        j = 0
        while j < filterSize and (i - j) >= 0:
            val[i] += filter_[j] * prices[i - j]
            j += 1
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

def fillFatl(array, size):
    size.v = 39
    ArrayResize(array, size.v)
    array[0] = 0.4360392246
    array[1] = 0.365867866
    array[2] = 0.2460451052
    array[3] = 0.1104516027
    array[4] = -0.0054023158
    array[5] = -0.0760358291
    array[6] = -0.0933055008
    array[7] = -0.0670117473
    array[8] = -0.0190807171
    array[9] = 0.0259599784
    array[10] = 0.050204072
    array[11] = 0.0477820398
    array[12] = 0.0249261523
    array[13] = -0.0047695503
    array[14] = -0.0272425079
    array[15] = -0.0338916063
    array[16] = -0.0244149695
    array[17] = -0.0055783815
    array[18] = 0.0128142457
    array[19] = 0.0226517983
    array[20] = 0.0208782158
    array[21] = 0.0100306129
    array[22] = -0.0036762908
    array[23] = -0.0136739537
    array[24] = -0.0160483888
    array[25] = -0.0108602627
    array[26] = -0.0016069184
    array[27] = 0.0069474613
    array[28] = 0.0110571907
    array[29] = 0.0095715934
    array[30] = 0.004045013
    array[31] = -0.0023819606
    array[32] = -0.0067092445
    array[33] = -0.007200056
    array[34] = -0.0047729647
    array[35] = 0.0005556585
    array[36] = 0.0007839957
    array[37] = 0.0130102968
    array[38] = 0.0040410425

def fillSatl(array, size):
    size.v = 65
    ArrayResize(array, size.v)
    array[0] = 0.0982914968
    array[1] = 0.0975734782
    array[2] = 0.0961453702
    array[3] = 0.0940284799
    array[4] = 0.0912491201
    array[5] = 0.0878446115
    array[6] = 0.0838599824
    array[7] = 0.0793462193
    array[8] = 0.0743626146
    array[9] = 0.0689724471
    array[10] = 0.0632438243
    array[11] = 0.0572485969
    array[12] = 0.0510590362
    array[13] = 0.0447524857
    array[14] = 0.0384014162
    array[15] = 0.0320788522
    array[16] = 0.0258588591
    array[17] = 0.0198052896
    array[18] = 0.0139852899
    array[19] = 0.0084553106
    array[20] = 0.0032675186
    array[21] = -0.0015319201
    array[22] = -0.005903443
    array[23] = -0.009817083
    array[24] = -0.0132494238
    array[25] = -0.0161868549
    array[26] = -0.0186163816
    array[27] = -0.0205453419
    array[28] = -0.0219751066
    array[29] = -0.0229225089
    array[30] = -0.0234106677
    array[31] = -0.0234597715
    array[32] = -0.0231055463
    array[33] = -0.0223841389
    array[34] = -0.0213348833
    array[35] = -0.0199977823
    array[36] = -0.0184183252
    array[37] = -0.016643857
    array[38] = -0.0147201173
    array[39] = -0.012686121
    array[40] = -0.0106002368
    array[41] = -0.0084800087
    array[42] = -0.0063906493
    array[43] = -0.0043529032
    array[44] = -0.0024016281
    array[45] = -0.0005592474
    array[46] = 0.0011366688
    array[47] = 0.0026794401
    array[48] = 0.0040424396
    array[49] = 0.0052338017
    array[50] = 0.0062156364
    array[51] = 0.0070307929
    array[52] = 0.007623496
    array[53] = 0.008035494
    array[54] = 0.0083018972
    array[55] = 0.0083678562
    array[56] = 0.0082888626
    array[57] = 0.0080733795
    array[58] = 0.0077539545
    array[59] = 0.0073259318
    array[60] = 0.006816384
    array[61] = 0.0062328194
    array[62] = 0.0056082863
    array[63] = 0.004952251
    array[64] = 0.0161442562

def fillRftl(array, size):
    size.v = 44
    ArrayResize(array, size.v)
    array[0] = -0.0025092021
    array[1] = 0.05130122
    array[2] = 0.1142800445
    array[3] = 0.1699338663
    array[4] = 0.2025262073
    array[5] = 0.2025262073
    array[6] = 0.1699338663
    array[7] = 0.1142800445
    array[8] = 0.05130122
    array[9] = -0.0025092021
    array[10] = -0.0353161991
    array[11] = -0.0433374067
    array[12] = -0.0311248031
    array[13] = -0.0088623799
    array[14] = 0.0120575757
    array[15] = 0.0233181781
    array[16] = 0.022193222
    array[17] = 0.0115773967
    array[18] = -0.0022153029
    array[19] = -0.0126532694
    array[20] = -0.015741562
    array[21] = -0.0113399687
    array[22] = -0.002590979
    array[23] = 0.0059518053
    array[24] = 0.0105210324
    array[25] = 0.0096972603
    array[26] = 0.0046588974
    array[27] = -0.0017075189
    array[28] = -0.0063511121
    array[29] = -0.0074539609
    array[30] = -0.005044243
    array[31] = -0.0007463619
    array[32] = 0.0032268725
    array[33] = 0.0051357097
    array[34] = 0.0044456975
    array[35] = 0.0018787786
    array[36] = -0.0011063441
    array[37] = -0.0031162284
    array[38] = -0.0033441946
    array[39] = -0.0022168887
    array[40] = 0.0002580855
    array[41] = 0.0003641408
    array[42] = 0.0060428648
    array[43] = 0.0018769344

def fillRstl(array, size):
    size.v = 91
    ArrayResize(array, size.v)
    array[0] = -0.0074144779
    array[1] = -0.0060689714
    array[2] = -0.0044967689
    array[3] = -0.0027041045
    array[4] = -0.0007017044
    array[5] = 0.0014967048
    array[6] = 0.0038730015
    array[7] = 0.0064060389
    array[8] = 0.0090719218
    array[9] = 0.0118447926
    array[10] = 0.0146938946
    array[11] = 0.0175899798
    array[12] = 0.0204991221
    array[13] = 0.0233878722
    array[14] = 0.0262230345
    array[15] = 0.0289691814
    array[16] = 0.0315932085
    array[17] = 0.0340622044
    array[18] = 0.036344972
    array[19] = 0.038412526
    array[20] = 0.0402377072
    array[21] = 0.0417971611
    array[22] = 0.0430702622
    array[23] = 0.0440399154
    array[24] = 0.0446940681
    array[25] = 0.0450229605
    array[26] = 0.0450229605
    array[27] = 0.0446940681
    array[28] = 0.0440399154
    array[29] = 0.0430702622
    array[30] = 0.0417971611
    array[31] = 0.0402377072
    array[32] = 0.038412526
    array[33] = 0.036344972
    array[34] = 0.0340622044
    array[35] = 0.0315932085
    array[36] = 0.0289691814
    array[37] = 0.0262230345
    array[38] = 0.0233878722
    array[39] = 0.0204991221
    array[40] = 0.0175899798
    array[41] = 0.0146938946
    array[42] = 0.0118447926
    array[43] = 0.0090719218
    array[44] = 0.0064060389
    array[45] = 0.0038730015
    array[46] = 0.0014967048
    array[47] = -0.0007017044
    array[48] = -0.0027041045
    array[49] = -0.0044967689
    array[50] = -0.0060689714
    array[51] = -0.0074144779
    array[52] = -0.008527336
    array[53] = -0.0094109068
    array[54] = -0.0100658184
    array[55] = -0.0104997812
    array[56] = -0.010723385
    array[57] = -0.0107458773
    array[58] = -0.0105836225
    array[59] = -0.0102531779
    array[60] = -0.0097725606
    array[61] = -0.0091600941
    array[62] = -0.0084366151
    array[63] = -0.0076238102
    array[64] = -0.0067426306
    array[65] = -0.0058109474
    array[66] = -0.0048554967
    array[67] = -0.0038843146
    array[68] = -0.0029272721
    array[69] = -0.0019938713
    array[70] = -0.001100079
    array[71] = -0.0002561664
    array[72] = 0.0005206574
    array[73] = 0.0012273323
    array[74] = 0.0018516617
    array[75] = 0.0023973716
    array[76] = 0.0028471064
    array[77] = 0.0032204933
    array[78] = 0.0034919843
    array[79] = 0.0036807022
    array[80] = 0.0038027296
    array[81] = 0.0038329425
    array[82] = 0.0037967591
    array[83] = 0.0036980559
    array[84] = 0.0035517415
    array[85] = 0.0033556833
    array[86] = 0.0031222822
    array[87] = 0.0028549772
    array[88] = 0.0025689064
    array[89] = 0.0022684058
    array[90] = 0.0073949653

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
        _sw2 = tprice
        if _sw2 == PRICE_CLOSE:
            return close[i]
        elif _sw2 == PRICE_OPEN:
            return open[i]
        elif _sw2 == PRICE_HIGH:
            return high[i]
        elif _sw2 == PRICE_LOW:
            return low[i]
        elif _sw2 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw2 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw2 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DigitalFiltersOnChart(_MQL5Indicator):
    name = 'Digital filters - on chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpType': _Choice({0: 'FATL(Fast Adaptive Trend Line)', 1: 'SATL(Slow Adaptive Trend Line)', 2: 'RFTL(Reference Fast Trend Line)', 3: 'RSTL(Reference Slow Trend Line)'}, default=1),  # Filter type
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

