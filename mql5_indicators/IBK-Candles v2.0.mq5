//+------------------------------------------------------------------+
//|                                              IBK-Candles v2.0    |
//|                                             Copyright 2025, IBK. |
//+------------------------------------------------------------------+
//| v2.0 - Added neutral candle close alerts                         |
//+------------------------------------------------------------------+
#property  indicator_chart_window
#property  indicator_buffers 23
#property  indicator_plots 19
#property  strict
#property  indicator_type19   DRAW_COLOR_CANDLES
#property  indicator_color19  clrNONE,clrNONE,clrNONE

string ID = "CMAC";
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
string Name=MQLInfoString(MQL_PROGRAM_NAME),MyName="Custom Moving Average Candle v2.1";
//+------------------------------------------------------------------------------------------------------------------+
input string STR00                      = "<<<==== [00] Candle Settings ====>>>";
input bool showCandles                = true;              // Show Candles?
input color CandleUp                   = clrDeepSkyBlue;    // Candle Up Color //0,83,166
input color CandleWt                   = C'212,212,212';    // Candle Down Color
input color CandleDn                   = clrViolet;         // Candle Wait Color//C'145,15,96'
double candleO[],candleH[],candleL[],candleC[],candleCl[];
//+------------------------------------------------------------------------------------------------------------------+
input string STR01                      = "<<<==== [01] T2MA Trend Settings ====>>>";
input bool showT2MA                   = true;              // Show T2MA?
input int T2MAper                    = 960;               // T2MA high low period
input ENUM_MA_METHOD  T2MAmode   = MODE_EMA;          // T2MA moving average method
input int T2MAtf                     = 0;                 // T2MA tf
input int T2MAshft                   = 2;                 // T2MA shift
input int T2MAtype                   = 4;                 // T2MA type
input int T2MAwidth                  = 4;                 // T2MA line width
input color T2MAbgdclr                 = C'180,180,180';    // T2MA Bgd Color
input color T2MAupclr                  = clrBlue;           // T2MA Up Color
input color T2MAdnclr                  = clrCrimson;        // T2MA Down Color
bool calculateT2TREND;
double T2MAbgd[],T2MA[],T2MAdna[],T2MAdnb[],T2trend[];
//+------------------------------------------------------------------------------------------------------------------+
input string STR02                      = "<<<==== [02] T1MA Trend Settings ====>>>";
input bool showT1MA                   = false;             // Show T1MA?
input int T1MAper                    = 80;                // T1MA high low period
input ENUM_MA_METHOD  T1MAmode   = MODE_EMA;          // T1MA moving average method
input int T1MAtf                     = 0;                 // T1MA tf
input int T1MAshft                   = 2;                 // T1MA shift
input int T1MAtype                   = 3;                 // T1MA type
input int T1MAwidth                  = 4;                 // T1MA line width
input color T1MAbgdclr                 = clrBlack;          // T1MA Bgd Color
input color T1MAupclr                  = clrGreen;          // T1MA Up Color
input color T1MAdnclr                  = clrDarkKhaki;      // T1MA Down Color
bool calculateT1TREND;
double T1MAbgd[],T1MA[],T1MAdna[],T1MAdnb[],T1trend[];
//+------------------------------------------------------------------------------------------------------------------+
input string STR03                      = "<<<==== [03] S1MA Trend Settings ====>>>";
input bool showS1MA                   = false;             // Show S1MA?
input int S1MAper                    = 16;                // S1MA high low period
input ENUM_MA_METHOD  S1MAmode   = MODE_EMA;          // S1MA moving average method
input int S1MAtf                     = 0;                 // S1MA tf
input int S1MAshft                   = 2;                 // S1MA shift
input int S1MAtype                   = 0;                 // S1MA type
input int S1MAwidth                  = 3;                 // S1MA line width
input color S1MAbgdclr                 = C'180,180,180';    // S1MA Bgd Color
input color S1MAupclr                  = clrBlue;           // S1MA Up Color
input color S1MAdnclr                  = clrCrimson;        // S1MA Down Color
bool calculateS1TREND;
double S1MAbgd[],S1MA[],S1MAdna[],S1MAdnb[],S1trend[];
//+------------------------------------------------------------------------------------------------------------------+
input string STR04                      = "<<<==== [04] BOXtxt Settings ====>>>";
input bool showBOXtxt                 = true;
string FontType="Arial Black";
input int moveTxtLR                  = 0,moveTxtUD=0,FontSize=12;
string BOXtxt,BOXspc;;
color BOXclr;
//+------------------------------------------------------------------------------------------------------------------+
input string STR05                      = "<<<==== [05] Background ZONE Settings ====>>>";
input bool showbgd                    = true;
double Dummy=-1,ZONE[];
input color ColorUp                    = C'15,26,65';
input color ColorDown                  = C'65,15,26';
input color ColorWait                  = C'35,40,45';//C'20,30,30';//C'35,40,45';
//+------------------------------------------------------------------------------------------------------------------+
input string STR06                      = "<<<==== [06] Misc Settings ====>>>";
input int LR=240,UD=10,HDRsize=40,HDRsize2=14;
color Sbg=clrBlack,SymClr;
//+------------------------------------------------------------------------------------------------------------------+
input string STR07                      = "<<<==== [07] Alert Settings ====>>>";
input bool inpAlertsOn                = false;             // Turn alerts on?
input bool inpAlertsOnCurrent         = true;              // Alerts on current (still opened) bar?
input bool inpAlertsMessage           = true;              // Alerts should show pop-up message?
input bool inpAlertsSound             = false;             // Alerts should play alert sound?
input bool inpAlertsPushNotif         = false;             // Alerts should send push notification?
input bool inpAlertsEmail             = false;             // Alerts should send email?
double TRX[],data1;
string TimeFrame="Current time frame";
int timeFrame,Type;

int hMA1High,hMA1Low,hMA1Gen;
int hMA2High,hMA2Low,hMA2Gen;
int hMASHigh,hMASLow,hMASGen;
double buf[1];
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int OnInit()
{
  hMA1High=iMA(Symbol(),(ENUM_TIMEFRAMES)T1MAtf,T1MAper,T1MAshft,T1MAmode,PRICE_HIGH);
  hMA1Low=iMA(Symbol(),(ENUM_TIMEFRAMES)T1MAtf,T1MAper,T1MAshft,T1MAmode,PRICE_LOW);
  hMA1Gen=iMA(Symbol(),(ENUM_TIMEFRAMES)T1MAtf,T1MAper,T1MAshft,T1MAmode,T1MAtype);

  hMA2High=iMA(Symbol(),(ENUM_TIMEFRAMES)T2MAtf,T2MAper,T2MAshft,T2MAmode,PRICE_HIGH);
  hMA2Low=iMA(Symbol(),(ENUM_TIMEFRAMES)T2MAtf,T2MAper,T2MAshft,T2MAmode,PRICE_LOW);
  hMA2Gen=iMA(Symbol(),(ENUM_TIMEFRAMES)T2MAtf,T2MAper,T2MAshft,T2MAmode,T2MAtype);

  hMASHigh=iMA(Symbol(),(ENUM_TIMEFRAMES)S1MAtf,S1MAper,S1MAshft,S1MAmode,PRICE_HIGH);
  hMASLow=iMA(Symbol(),(ENUM_TIMEFRAMES)S1MAtf,S1MAper,S1MAshft,S1MAmode,PRICE_LOW);
  hMASGen=iMA(Symbol(),(ENUM_TIMEFRAMES)S1MAtf,S1MAper,S1MAshft,S1MAmode,S1MAtype);
  //-
  Name=MQLInfoString(MQL_PROGRAM_NAME);
  timeFrame=stringToTimeFrame(TimeFrame);
  IndicatorSetInteger(INDICATOR_DIGITS,Digits());
  IndicatorSetString(INDICATOR_SHORTNAME,MyName);
//+----------------------------------------------
  int Buf=-1;
//+--------------------------------------
  if(showT2MA)
    Type=DRAW_LINE;
  else
    Type=DRAW_NONE;
  int T2W=T2MAwidth,T2B=T2W+2;
  Buf+=2;
  MySetIndexBuffer(Buf,T2MAbgd);
  MySetIndexStyle(Buf,Type,0,T2B,T2MAbgdclr);
  MySetIndexDrawBegin(Buf,T2MAper+1);
  Buf+=1;
  MySetIndexBuffer(Buf,T2MA);
  MySetIndexStyle(Buf,Type,0,T2W,T2MAupclr);
  MySetIndexDrawBegin(Buf,T2MAper+1);
  Buf+=1;
  MySetIndexBuffer(Buf,T2MAdna);
  MySetIndexStyle(Buf,Type,0,T2W,T2MAdnclr);
  MySetIndexDrawBegin(Buf,T2MAper+1);
  Buf+=1;
  MySetIndexBuffer(Buf,T2MAdnb);
  MySetIndexStyle(Buf,Type,0,T2W,T2MAdnclr);
  MySetIndexDrawBegin(Buf,T2MAper+1);
  Buf+=1;
  MySetIndexBuffer(Buf,T2trend);
  MySetIndexStyle(Buf,DRAW_NONE);//12
//+-------------------------------------------
  if(showT1MA)
    Type=DRAW_LINE;
  else
    Type=DRAW_NONE;
  int T1W=T1MAwidth,T1B=T1W+2;
  Buf+=1;
  MySetIndexBuffer(Buf,T1MAbgd);
  MySetIndexStyle(Buf,Type,0,T1B,T1MAbgdclr);
  MySetIndexDrawBegin(Buf,T1MAper+1);
  Buf+=1;
  MySetIndexBuffer(Buf,T1MA);
  MySetIndexStyle(Buf,Type,0,T1W,T1MAupclr);
  MySetIndexDrawBegin(Buf,T1MAper+1);
  Buf+=1;
  MySetIndexBuffer(Buf,T1MAdna);
  MySetIndexStyle(Buf,Type,0,T1W,T1MAdnclr);
  MySetIndexDrawBegin(Buf,T1MAper+1);
  Buf+=1;
  MySetIndexBuffer(Buf,T1MAdnb);
  MySetIndexStyle(Buf,Type,0,T1W,T1MAdnclr);
  MySetIndexDrawBegin(Buf,T1MAper+1);
  Buf+=1;
  MySetIndexBuffer(Buf,T1trend);
  MySetIndexStyle(Buf,DRAW_NONE);//17
//+-----------------------------------------
  if(showS1MA)
    Type=DRAW_LINE;
  else
    Type=DRAW_NONE;
  int S1W=S1MAwidth,S1B=S1W+2;
  Buf+=1;
  MySetIndexBuffer(Buf,S1MAbgd);
  MySetIndexStyle(Buf,Type,0,S1B,S1MAbgdclr);
  MySetIndexDrawBegin(Buf,S1MAper+1);
  Buf+=1;
  MySetIndexBuffer(Buf,S1MA);
  MySetIndexStyle(Buf,Type,0,S1W,S1MAupclr);
  MySetIndexDrawBegin(Buf,S1MAper+1);
  Buf+=1;
  MySetIndexBuffer(Buf,S1MAdna);
  MySetIndexStyle(Buf,Type,0,S1W,S1MAdnclr);
  MySetIndexDrawBegin(Buf,S1MAper+1);
  Buf+=1;
  MySetIndexBuffer(Buf,S1MAdnb);
  MySetIndexStyle(Buf,Type,0,S1W,S1MAdnclr);
  MySetIndexDrawBegin(Buf,S1MAper+1);
  Buf+=1;
  MySetIndexBuffer(Buf,S1trend);
  MySetIndexStyle(Buf,DRAW_NONE);
//+--------------------------------------
  Buf+=1;
  MySetIndexBuffer(Buf,ZONE);
  MySetIndexStyle(Buf,DRAW_NONE);
//+--------------------------------------
  Buf+=1;
  MySetIndexBuffer(Buf,TRX);
  MySetIndexStyle(Buf,DRAW_NONE);
//+---------------------------------------------
  if(showCandles)
    Type=DRAW_COLOR_CANDLES;
  else
    Type=DRAW_NONE;
  Buf+=1;
  MySetIndexBuffer(Buf,candleO,INDICATOR_DATA);
  PlotIndexSetInteger(Buf,PLOT_DRAW_TYPE,Type);
  PlotIndexSetInteger(Buf,PLOT_LINE_COLOR,0,CandleUp);
  PlotIndexSetInteger(Buf,PLOT_LINE_COLOR,1,CandleWt);
  PlotIndexSetInteger(Buf,PLOT_LINE_COLOR,2,CandleDn);
  PlotIndexSetDouble(Buf,PLOT_EMPTY_VALUE,0);
  Buf+=1;
  MySetIndexBuffer(Buf,candleH,INDICATOR_DATA);
  Buf+=1;
  MySetIndexBuffer(Buf,candleL,INDICATOR_DATA);
  Buf+=1;
  MySetIndexBuffer(Buf,candleC,INDICATOR_DATA);
  Buf+=1;
  MySetIndexBuffer(Buf,candleCl,INDICATOR_COLOR_INDEX);
  return(INIT_SUCCEEDED);
}
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void MySetIndexBuffer(int index, double &name[], ENUM_INDEXBUFFER_TYPE type=INDICATOR_DATA)
{
  SetIndexBuffer(index,name,type);
  ArraySetAsSeries(name,true);

}
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void MySetIndexStyle(int index,int type,int style=STYLE_SOLID,int width=-1,color clr=clrNONE)
{
  if(width>-1)
    PlotIndexSetInteger(index,PLOT_LINE_WIDTH,width);
  PlotIndexSetInteger(index,PLOT_LINE_COLOR,clr);
  switch(type) {
  case DRAW_COLOR_CANDLES:
    PlotIndexSetInteger(index,PLOT_DRAW_TYPE,DRAW_COLOR_CANDLES);
    break;
  case DRAW_LINE:
    PlotIndexSetInteger(index,PLOT_DRAW_TYPE,DRAW_LINE);
    break;
  case DRAW_NONE:
    PlotIndexSetInteger(index,PLOT_DRAW_TYPE,DRAW_NONE);
    break;
  default:
    PlotIndexSetInteger(index,PLOT_DRAW_TYPE,DRAW_LINE);
  }
}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void MySetIndexDrawBegin(int index,int begin)
{
  PlotIndexSetInteger(index,PLOT_DRAW_BEGIN,begin);
}
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
  CleanUpOnAisle5(); //End deinit
}

//+------------------------------------------------------------------+
//|                                                                  |
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
  if(prev_calculated<1) {
    /* ArrayInitialize(rsi,EMPTY_VALUE);
     ArrayInitialize(maDa,EMPTY_VALUE);
     ArrayInitialize(maDb,EMPTY_VALUE);
     ArrayInitialize(maUa,EMPTY_VALUE);
     ArrayInitialize(maUb,EMPTY_VALUE);
     ArrayInitialize(avg,EMPTY_VALUE);
     ArrayInitialize(valup,EMPTY_VALUE);
     ArrayInitialize(valdn,EMPTY_VALUE);
     ArrayInitialize(trend,0);
     ArrayInitialize(count,0);*/
  }
  ArraySetAsSeries(time,true);
  ArraySetAsSeries(high,true);
  ArraySetAsSeries(low,true);
  ArraySetAsSeries(close,true);

  int i,limit=MathMin(rates_total-prev_calculated,rates_total-2);
  //--
  if(calculateT2TREND || timeFrame == Period()) {
    if(!calculateT2TREND && T2trend[limit]==-1)
      CleanPoint(limit,T2MAdna,T2MAdnb);
    for(i=limit; i>=0; i--) {
      T2MAdna[i]=EMPTY_VALUE;
      T2MAdnb[i]=EMPTY_VALUE;
      T2trend[i]=T2trend[i+1];
      CopyBuffer(hMA2High,0,i+1,1,buf);
      if(close[i]>buf[0]/*iMA(Symbol(),T2MAtf,T2MAper,T2MAshft,T2MAmode,PRICE_HIGH,i+1)*/)
        T2trend[i]= 1;
      CopyBuffer(hMA2Low,0,i+1,1,buf);
      if(close[i]<buf[0]/*iMA(Symbol(),T2MAtf,T2MAper,T2MAshft,T2MAmode,PRICE_LOW,i+1)*/)
        T2trend[i]=-1;
      CopyBuffer(hMA2Gen,0,i,1,buf);
      if(T2trend[i]==-1)
        T2MA[i]=buf[0];//iMA(Symbol(),T2MAtf,T2MAper,T2MAshft,T2MAmode,T2MAtype,i);
      else
        T2MA[i]=buf[0];//iMA(Symbol(),T2MAtf,T2MAper,T2MAshft,T2MAmode,T2MAtype,i);
      if(!calculateT2TREND && T2trend[i]==-1)
        PlotPoint(i,T2MAdna,T2MAdnb,T2MA);
      T2MAbgd[i]=T2MA[i];
    }
  }//EOF T2MA
//+---T1MA Function--------------------------------------------------------------------------------------------------+
  if(calculateT1TREND || timeFrame == Period()) {
    if(!calculateT1TREND && T1trend[limit]==-1)
      CleanPoint(limit,T1MAdna,T1MAdnb);
    for(i=limit; i>=0; i--) {
      T1MAdna[i]=EMPTY_VALUE;
      T1MAdnb[i]=EMPTY_VALUE;
      T1trend[i]=T1trend[i+1];
      CopyBuffer(hMA1High,0,i+1,1,buf);
      if(close[i]>buf[0]/*iMA(Symbol(),T1MAtf,T1MAper,T1MAshft,T1MAmode,PRICE_HIGH,i+1)*/)
        T1trend[i]= 1;
      CopyBuffer(hMA1Low,0,i+1,1,buf);
      if(close[i]<buf[0]/*iMA(Symbol(),T1MAtf,T1MAper,T1MAshft,T1MAmode,PRICE_LOW,i+1)*/)
        T1trend[i]=-1;
      CopyBuffer(hMA1Gen,0,i,1,buf);
      if(T1trend[i]==-1)
        T1MA[i]=buf[0];//iMA(Symbol(),T1MAtf,T1MAper,T1MAshft,T1MAmode,T1MAtype,i);
      else
        T1MA[i]=buf[0];//iMA(Symbol(),T1MAtf,T1MAper,T1MAshft,T1MAmode,T1MAtype,i);
      if(!calculateT1TREND && T1trend[i]==-1)
        PlotPoint(i,T1MAdna,T1MAdnb,T1MA);
      T1MAbgd[i]=T1MA[i];
    }
  }//EOF T1MA
//+---S1MA Function--------------------------------------------------------------------------------------------------+
  if(calculateS1TREND || timeFrame == Period()) {
    if(!calculateS1TREND && S1trend[limit]==-1)
      CleanPoint(limit,S1MAdna,S1MAdnb);
    for(i=limit; i>=0; i--) {
      S1MAdna[i]=EMPTY_VALUE;
      S1MAdnb[i]=EMPTY_VALUE;
      S1trend[i]=S1trend[i+1];
      CopyBuffer(hMASHigh,0,i+1,1,buf);
      if(close[i]>buf[0]/*iMA(Symbol(),S1MAtf,S1MAper,S1MAshft,S1MAmode,PRICE_HIGH,i+1)*/)
        S1trend[i]= 1;
      CopyBuffer(hMASLow,0,i+1,1,buf);
      if(close[i]<buf[0]/*iMA(Symbol(),S1MAtf,S1MAper,S1MAshft,S1MAmode,PRICE_LOW,i+1)*/)
        S1trend[i]=-1;
      CopyBuffer(hMASGen,0,i,1,buf);
      if(S1trend[i]==-1)
        S1MA[i]=buf[0];//iMA(Symbol(),S1MAtf,S1MAper,S1MAshft,S1MAmode,S1MAtype,i);
      else
        S1MA[i]=buf[0];//iMA(Symbol(),S1MAtf,S1MAper,S1MAshft,S1MAmode,S1MAtype,i);
      if(!calculateS1TREND && S1trend[i]==-1)
        PlotPoint(i,S1MAdna,S1MAdnb,S1MA);
      S1MAbgd[i]=S1MA[i];
    }
  }//EOF S1MA
//+---Background Function--------------------------------------------------------------------------------------------+
  if(showbgd) {
    datetime tDummy=(datetime)Dummy;
    if(Dummy<=time[0])
      tDummy=time[0];
    double MaxValue = high[0]*10.0;
    for(i=limit; i>=0; i--) {
      if(i>rates_total-2)
        continue;
      int index;
      ZONE[i] = ZONE[i+1];
      ZONE[i] = 0;
      if(T1trend[i+0] == 1 && S1trend[i+0] == 1) {
        ZONE[i] = 1;
      }
      if(T1trend[i+0] ==-1 && S1trend[i+0] ==-1) {
        ZONE[i] =-1;
      }
      for(index=i; index<rates_total; index++)
        if(ZONE[index]!=ZONE[index+1])
          break;
      string name=ID+"C"+(string)time[index+1];
      ObjectDelete(0,name);
      ObjectDelete(0,ID+"C"+(string)time[1]);
      datetime lastTime=time[i];
      if(i==0)
        lastTime=tDummy;
      ObjectCreate(0,name,OBJ_RECTANGLE,0,time[index+1],0,lastTime,MaxValue);
      ObjectSetInteger(0,name,OBJPROP_BACK,true);
      ObjectSetInteger(0,name,OBJPROP_FILL,true);
      switch((int)ZONE[i]) {
      case -1 :
        ObjectSetInteger(0,name,OBJPROP_COLOR,ColorDown);
        break;
      case  1 :
        ObjectSetInteger(0,name,OBJPROP_COLOR,ColorUp);
        break;
      default :
        ObjectSetInteger(0,name,OBJPROP_COLOR,ColorWait);
        break;
      }
    }
  }//End background
//+----Directional Trading-------------------------------------------------------------------------------------------+
  for(i=limit; i>=0; i--) {
    TRX[i]= 0;
    candle(2,i);
    BOXtxt="  NO TRADES - WAITING . . .";
    BOXclr=clrGray;
    BOXspc="gggggggggggggggggg";
    SymClr=clrDimGray;
    if(T1trend[i]== 1 && S1trend[i] == 1) {
      TRX[i]= 1;
      candle(1,i);
      BOXtxt=" UP TREND - BUYS ONLY";
      BOXclr=clrBlue;
      BOXspc="gggggggggggggggg";
      SymClr=clrDeepSkyBlue;
    }
    if(T1trend[i]==-1 && S1trend[i] ==-1) {
      TRX[i]=-1;
      candle(3,i);
      BOXtxt="  DOWN TREND - SELLS ONLY";
      BOXclr=clrMagenta;
      BOXspc="ggggggggggggggggggg";
      SymClr=clrViolet;
    }
  }//End Directional Trading
  //--
  if(showBOXtxt) {
    Panels(ID+"X070",2,-1+28,BOXspc,FontSize+2,"Webdings",BOXclr);
    Labels(ID+"X071",7,-3+28);
    myObjectSetText(ID+"X071",timeFrameToString(timeFrame)+BOXtxt,FontSize+2,FontType,clrSnow);
  }
  //--
  manageAlerts();
  return(rates_total);
}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void Panels(string aa3,int x,int y,string Text,int fontSize,string Font,color Color)
{
  ObjectDelete(0,aa3);
  ObjectCreate(0,aa3,OBJ_LABEL,0,0,0);
  ObjectSetInteger(0,aa3,OBJPROP_CORNER,CORNER_LEFT_LOWER);
  ObjectSetInteger(0,aa3,OBJPROP_XDISTANCE,x+moveTxtLR+4);
  ObjectSetInteger(0,aa3,OBJPROP_YDISTANCE,y+moveTxtUD+4);
  ObjectSetInteger(0,aa3,OBJPROP_BACK,false);
  myObjectSetText(aa3,Text,fontSize,Font,Color);
}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void Labels(string aa4,int x,int y)
{
  ObjectDelete(0,aa4);
  ObjectCreate(0,aa4,OBJ_LABEL,0,0,0);
  ObjectSetInteger(0,aa4,OBJPROP_CORNER,CORNER_LEFT_LOWER);
  ObjectSetInteger(0,aa4,OBJPROP_XDISTANCE,x+moveTxtLR+4);
  ObjectSetInteger(0,aa4,OBJPROP_YDISTANCE,y+moveTxtUD+7);
  ObjectSetInteger(0,aa4,OBJPROP_BACK,false);
}

string sTfTable[] = {"M1","M5","M15","M30","H1","H4","D1","W1","MN"};
int    iTfTable[] = {1,5,15,30,60,240,1440,10080,43200};
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int stringToTimeFrame(string tfs)
{
  for(int i=ArraySize(iTfTable)-1; i>=0; i--)
    if(tfs==sTfTable[i] || tfs==(string)iTfTable[i])
      return(MathMax(iTfTable[i],Period()));
  return(Period());
}
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
string timeFrameToString(int tf)
{
  return(StringSubstr(EnumToString((ENUM_TIMEFRAMES)tf),7));
}

//+------------------------------------------------------------------+
//| Alert management - v2.0 with neutral candle alerts              |
//+------------------------------------------------------------------+
void manageAlerts()
{
  if(inpAlertsOn) {
    int whichBar = (inpAlertsOnCurrent) ? 0 : 1;
    if(TRX[whichBar] != TRX[whichBar+1]) {
      if(TRX[whichBar] ==  1)
        doAlert(whichBar,"BUY BUY BUY");
      else if(TRX[whichBar] == -1)
        doAlert(whichBar,"SELL SELL SELL");
      else if(TRX[whichBar] ==  0)
        doAlert(whichBar,"NEUTRAL - WAIT");
    }
  }
}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void doAlert(int forBar, string doWhat)
{
  static string   previousAlert="nothing";
  static datetime previousTime;
  string msg;
  if(previousAlert != doWhat || previousTime != iTime(_Symbol,_Period,forBar)) {
    previousAlert  = doWhat;
    previousTime   = iTime(_Symbol,_Period,forBar);
    msg=_Symbol+" "+timeFrameToString(_Period)+" at "+TimeToString(TimeLocal(),TIME_SECONDS)+" Direction changed to "+doWhat;
    if(inpAlertsMessage)
      Alert(msg);
    if(inpAlertsEmail)
      SendMail(_Symbol+" Trading ",msg);
    if(inpAlertsPushNotif)
      SendNotification(msg);
    if(inpAlertsSound)
      PlaySound("alert2.wav");
  }
}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void CleanPoint(int i,double& first[],double& second[])
{
  if(i>=Bars(NULL,0)-3)
    return;
  if((second[i]  != EMPTY_VALUE) && (second[i+1] != EMPTY_VALUE))
    second[i+1] = EMPTY_VALUE;
  else if((first[i] != EMPTY_VALUE) && (first[i+1] != EMPTY_VALUE) && (first[i+2] == EMPTY_VALUE))
    first[i+1] = EMPTY_VALUE;
}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void PlotPoint(int i,double& first[],double& second[],double& from[])
{
  if(i>=Bars(NULL,0)-2)
    return;
  if(first[i+1] == EMPTY_VALUE)
    if(first[i+2] == EMPTY_VALUE) {
      first[i]  = from[i];
      first[i+1]  = from[i+1];
      second[i] = EMPTY_VALUE;
    } else {
      second[i] = from[i];
      second[i+1] = from[i+1];
      first[i]  = EMPTY_VALUE;
    } else {
    first[i]  = from[i];
    second[i] = EMPTY_VALUE;
  }
}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void CleanUpOnAisle5()
{
  int i;
  for(i=ObjectsTotal(0,0)-1; i>=0; i--)
    if(StringFind(ObjectName(0,i),ID,0)>-1)
      ObjectDelete(0,ObjectName(0,i));
}
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void candle(int direction,int i)
{
  candleO[i] = iOpen(NULL,0,i);
  candleH[i] = iHigh(NULL,0,i);
  candleL[i] = iLow(NULL,0,i);
  candleC[i] = iClose(NULL,0,i);
  switch(direction) {
  case 1:
    candleCl[i] = 0;
    break;
  case 2:
    candleCl[i] = 1;
    break;
  case 3:
    candleCl[i] = 2;
    break;
  }
}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void SetTextRight(string name,string text,int x,int y,color colour,int fontsize=10, string font="Arial Black")
{
  ObjectDelete(0,name);
  if(ObjectCreate(0,name,OBJ_LABEL,0,0,0)) {
    ObjectSetInteger(0,name,OBJPROP_CORNER,CORNER_LEFT_UPPER);
    ObjectSetInteger(0,name,OBJPROP_ANCHOR,ANCHOR_RIGHT_UPPER);
  }
  ObjectSetInteger(0,name,OBJPROP_XDISTANCE,x);
  ObjectSetInteger(0,name,OBJPROP_YDISTANCE,y);
  myObjectSetText(name,text,fontsize,font,colour);
}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void myObjectSetText(string name,
                     string text,
                     int font_size,
                     string font,
                     color text_color)
{
  ObjectSetString(0,name,OBJPROP_TEXT,text);
  ObjectSetInteger(0,name,OBJPROP_FONTSIZE,font_size);
  ObjectSetString(0,name,OBJPROP_FONT,font);
  ObjectSetInteger(0,name,OBJPROP_COLOR,text_color);
}
//+------------------------------------------------------------------+
