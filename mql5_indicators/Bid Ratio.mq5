#property copyright "Bid Ratio"
#property version   "1.00"
#property indicator_chart_window

input group    "Display Settings"
input bool     AutoColor = true;          // Enable Auto-Coloring
input color    BaseColor = clrGray;        // Default Text Color
input int      FontSize = 12;              // Font Size
input string   FontName = "Arial";         // Font Name
input ENUM_BASE_CORNER Corner = CORNER_LEFT_LOWER;  // Corner Position
input int      XOffset = 300;               // X Distance from Corner
input int      YOffset = 50;               // Y Distance from Corner

//+------------------------------------------------------------------+
//| Custom indicator initialization function                           |
//+------------------------------------------------------------------+
int OnInit()
{
    ObjectCreate(0,"BidRatioLabel",OBJ_LABEL,0,0,0);
    ObjectSetInteger(0,"BidRatioLabel",OBJPROP_CORNER,Corner);
    ObjectSetInteger(0,"BidRatioLabel",OBJPROP_XDISTANCE,XOffset);
    ObjectSetInteger(0,"BidRatioLabel",OBJPROP_YDISTANCE,YOffset);
    ObjectSetString(0,"BidRatioLabel",OBJPROP_FONT,FontName);
    ObjectSetInteger(0,"BidRatioLabel",OBJPROP_FONTSIZE,FontSize);
    ObjectSetInteger(0,"BidRatioLabel",OBJPROP_COLOR,BaseColor);
    return(INIT_SUCCEEDED);
}
//+------------------------------------------------------------------+
//| Custom indicator iteration function                                |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
    double dayHigh = iHigh(Symbol(), PERIOD_D1, 0);
    double dayLow = iLow(Symbol(), PERIOD_D1, 0);
    double dayOpen = iOpen(Symbol(), PERIOD_D1, 0);
    double dayClose = iClose(Symbol(), PERIOD_D1, 0);
    double dayRange = dayHigh - dayLow;
    double bidRatio = 0;
    
    if(dayRange > 0)
    {
        if(dayClose >= dayOpen)
            bidRatio = ((dayClose - dayLow) * 100) / dayRange;
        else
            bidRatio = ((dayRange + dayClose - dayHigh) * 100) / dayRange;
    }
    
    color textColor = BaseColor;
    if(AutoColor)
    {
        if(bidRatio >= 80) textColor = clrDodgerBlue;
        else if(bidRatio <= 20) textColor = clrDeepPink;
        else if(bidRatio < 50) textColor = clrLightPink;
        else if(bidRatio > 50) textColor = clrSkyBlue;
    }
    
    string labelText = "D1 Bid Ratio " + DoubleToString(bidRatio, 2) + "%";
    ObjectSetString(0,"BidRatioLabel",OBJPROP_TEXT,labelText);
    ObjectSetInteger(0,"BidRatioLabel",OBJPROP_COLOR,textColor);
    return(rates_total);
}
//+------------------------------------------------------------------+
//| Custom indicator deinitialization function                         |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    ObjectDelete(0,"BidRatioLabel");
}