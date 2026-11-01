//+------------------------------------------------------------------+
//|                                                   XU v50 Mt5.mq5 |
//|                                  Copyright 2023, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property version   "1.00"
#property indicator_chart_window
#property indicator_plots 0
#define Version "XU v50 MT5"

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
string Name=MQLInfoString(MQL_PROGRAM_NAME),MyName="XU v50-ADR D1";
//+------------------------------------------------------------------------------------------------------------------+
string Indicator                  = Version;
//+------------------------------------------------------------------------------------------------------------------+
//#include <WinUser32.mqh>
string ID,xTimeFrame                     = "Current time frame";
//+------------------------------------------------------------------------------------------------------------------+
input bool AutoRefresh                = true;//XARD: Req for lines to Auto Draw Next Day
input ENUM_TIMEFRAMES RefreshPeriod   = PERIOD_D1;
int hWindow=0,oldBars=0;
//+------------------------------------------------------------------------------------------------------------------+
input string STR01                      = "<<<==== [01] Open Postion level Settings ====>>>";
input bool showOpenPoslevels          = true;
double yClose,wClose;
int LABELmove=3;
double OpenPosPercent             = 10.00;
double OpenToday,CloseToday,ADR1,ADR5,ADR10,ADR20,ADRavg;
//+------------------------------------------------------------------------------------------------------------------+
input string STR02                      = "<<<==== [02] ADR% Target Settings ====>>>";
input ENUM_TIMEFRAMES TimeFrame_  = PERIOD_D1;
ENUM_TIMEFRAMES TimeFrame =TimeFrame_;
input bool showTARGETS                = true,showOpen=true,showADRlines=true,
           showOpenPoslines           = true,showOpenline=true,showCloseline=false;
input double lvl2                       = 21.4,lvl3=38.2,lvl4=61.8,lvl5=78.6,lvl6=100.,lvl7=121.4,lvl8=138.2,lvl9=161.8,
             lvl10                      = 178.6,lvl11=200.0,lvl12=221.4,lvl13=238.2,lvl14=261.8,lvl15=278.6,lvl16=300.0;
input color ADRColUP                   = clrDimGray,ADRColDN=clrDimGray,
            OpenBUY                    = clrAqua,OpenSELL=clrHotPink;
input ENUM_LINE_STYLE PrevOpenStyle  = STYLE_SOLID;
input int OrderLineWidth             = 1,ADRLineWidth=1,TextSize=12;
double RayLength                  = 0;
ENUM_LINE_STYLE ADRStyle   = STYLE_DASH;
bool TX=false;
double DecNos,CLOSE,myPoint,mPoint;
string FontType="Arial Black",SymPair="";
int pipsize;
double SetPoint() {if(_Digits<4) mPoint=0.01; else mPoint=0.0001; return(mPoint);}
datetime TimeBar=0, BarTime=0;

//+----OnInit Function-----------------------------------------------------------------------------------------------+
int OnInit()
  {
   TimeFrame = TFMigrate(fmax(PeriodSeconds(TimeFrame)/60,PeriodSeconds(_Period)/60));
   Comment("");
   Print(TimeFrame);
   if(RayLength==0)
      RayLength=1;
   xTimeFrame = stringToTimeFrame(xTimeFrame);
   ID = timeFrameToString(TimeFrame)+": X ["+(string)OpenPosPercent+"] ";
   if(TextSize>4)
      TX=true;
   IndicatorSetInteger(INDICATOR_DIGITS,_Digits); //IndicatorShortName(ID);
//+------------------------------------------------------------------------------------------------------------------+
   if(AutoRefresh)
      hWindow=WindowHandle(Symbol(),Period());
   oldBars=iBars(_Symbol,RefreshPeriod);
//+------------------------------------------------------------------------------------------------------------------+
   if(SymPair=="")
      SymPair=Symbol();
   myPoint=SetPoint();
   if(StringFind(Symbol(),"JPY",0) != -1)
      DecNos=2;
   else
      if(StringSubstr(Symbol(),0,6)=="BTCUSD")
         DecNos=0;
      else
         if(StringSubstr(Symbol(),0,5)=="US500")
            DecNos=1;
         else
            if(StringSubstr(Symbol(),0,6)=="USOUSD")
               DecNos=3;
            else
               if(StringSubstr(Symbol(),0,4)=="HK50")
                  DecNos=0;
               else
                  if(StringSubstr(Symbol(),0,5)=="JP225")
                     DecNos=0;
                  else
                     if(StringSubstr(Symbol(),0,7)=="FTSE100")
                        DecNos=1;
                     else
                        if(StringSubstr(Symbol(),0,6)=="XAUUSD")
                           DecNos=1;
                        else
                           if(StringSubstr(Symbol(),0,6)=="USDMXN")
                              DecNos=3;
                           else
                              if(StringSubstr(Symbol(),0,6)=="ASX200")
                                 DecNos=1;
                              else
                                 if(StringSubstr(Symbol(),0,5)=="DAX30")
                                    DecNos=0;
                                 else
                                    if(StringSubstr(Symbol(),0,4)=="WS30")
                                       DecNos=0;
                                    else
                                       DecNos=4;
   if(SymPair=="")
      SymPair=Symbol();
   if(StringFind(Symbol(),"JPY",0) != -1)
      pipsize=10;
   else
      if(StringSubstr(Symbol(),0,6)=="BTCUSD")
         pipsize=100;
      else
         if(StringSubstr(Symbol(),0,6)=="ASX200")
            pipsize=10;
         else
            if(StringSubstr(Symbol(),0,4)=="HK50")
               pipsize=100;
            else
               if(StringSubstr(Symbol(),0,5)=="JP225")
                  pipsize=100;
               else
                  if(StringSubstr(Symbol(),0,7)=="FTSE100")
                     pipsize=100;
                  else
                     if(StringSubstr(Symbol(),0,6)=="USDMXN")
                        pipsize=100;
                     else
                        if(StringSubstr(Symbol(),0,6)=="XAUUSD")
                           pipsize=10;
                        else
                           if(StringSubstr(Symbol(),0,4)=="WS30")
                              pipsize=100;
                           else
                              if(StringSubstr(Symbol(),0,5)=="DAX30")
                                 pipsize=100;
                              else
                                 if(StringSubstr(Symbol(),0,6)=="ASX200")
                                    pipsize=100;
                                 else
                                    pipsize=10;
   return(INIT_SUCCEEDED);
  }//End OnInit
//+----deinit Function-----------------------------------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   CleanUpIsle1();
  }
//+----OnCalculate Function------------------------------------------------------------------------------------------+
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

   ENUM_TIMEFRAMES mytf=_Period;
//+---MARKET CLOSE---------------------------------------------------------------------------------------------------+
   string CLOSEy="";
   yClose=iClose(SymPair,TFMigrate(1440),1);
   CLOSEy=(DoubleToString(yClose,DecNos));
   string CLOSEw="";
   wClose=iClose(SymPair,TFMigrate(10080),1);
   CLOSEw=(DoubleToString(wClose,DecNos));
//+---ADR------------------------------------------------------------------------------------------------------------+
   string OPEN="";
   OpenToday=iOpen(SymPair,TFMigrate(1440),0);
   OPEN=(DoubleToString(OpenToday,DecNos));
   string PIPS="";
   CLOSE=iClose(SymPair,TFMigrate(1440),0);
   PIPS=DoubleToString((CLOSE-OpenToday)/_Point/pipsize,0);
   ADR1=0;
   ADR5=0;
   ADR10=0;
   ADR20=0;
   ADRavg=0;
   int a,b,c;
   int ypos=0;
   ADR1=(iHigh(_Symbol,TimeFrame,1)-iLow(_Symbol,TimeFrame,1));
   for(a=1;a<= 5;a++)
      ADR5= ADR5+(iHigh(_Symbol,TimeFrame,a)-iLow(_Symbol,TimeFrame,a));
   for(b=1;b<=10;b++)
      ADR10=ADR10+(iHigh(_Symbol,TimeFrame,b)-iLow(_Symbol,TimeFrame,b));
   for(c=1;c<=20;c++)
      ADR20=ADR20+(iHigh(_Symbol,TimeFrame,c)-iLow(_Symbol,TimeFrame,c));
   ADR5=ADR5/5;
   ADR10=ADR10/10;
   ADR20=ADR20/20;
   ADRavg=(((ADR1+ADR5+ADR10+ADR20)/4))/_Point/pipsize;
//+---Entry level Open Position--------------------------------------------------------------------------------------+
   string gap="                                           ",mgap="                              ";
   double OpenUP=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(OpenPosPercent/100));
   double OpenDN=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(OpenPosPercent/100));
   color clrOpen=clrNONE;
   if(showOpen)
     {

      string commtx="";
      if(CLOSE>OpenToday)
        {
         color clrOpen=clrLime;
         commtx=" UP";
        }
      else
        {
         clrOpen=clrCrimson;
         commtx=" DN";
        }
      string sc1=gap+"OPEN"+commtx ;
      if(TX)
         iLabel(ID+"X001",sc1,clrOpen,OpenToday,0);
     }
   if(showOpenline)
     {
      if(CLOSE>OpenToday)
        {
         clrOpen=clrLime;
        }
      else
         clrOpen=clrCrimson;
      if(TX)
         iLine1(ID+"X003",clrOpen,OpenToday);
     }
   if(_Period<=PERIOD_H1)
     {
      if(showOpenPoslevels)
        {
         color colUP=OpenBUY,colDN=OpenSELL;
         if(TX)
            iLabel(ID+"X068",gap+"BUY",colUP,OpenUP,0);
         if(TX)
            iLabel(ID+"X069",gap+"SELL",colDN,OpenDN,0);
         if(showOpenPoslines)
           {
            iLine1(ID+"X070",colUP,OpenUP);
            iLine1(ID+"X071",colDN,OpenDN);
           }
        }
      ChartRedraw(0);
     }
//+---Primary and Secondary Targets----------------------------------------------------------------------------------+
   double TU2=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl2/100)),
          TD2=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl2/100)),
          TU3=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl3/100)),
          TD3=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl3/100)),
          TU4=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl4/100)),
          TD4=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl4/100)),
          TU5=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl5/100)),
          TD5=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl5/100)),
          TU6=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl6/100)),
          TD6=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl6/100)),
          TU7=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl7/100)),
          TD7=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl7/100)),
          TU8=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl8/100)),
          TD8=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl8/100)),
          TU9=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl9/100)),
          TD9=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl9/100)),
          TU10=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl10/100)),
          TD10=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl10/100)),
          TU11=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl11/100)),
          TD11=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl11/100)),
          TU12=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl12/100)),
          TD12=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl12/100)),
          TU13=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl13/100)),
          TD13=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl13/100)),
          TU14=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl14/100)),
          TD14=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl14/100)),
          TU15=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl15/100)),
          TD15=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl15/100)),
          TU16=OpenToday+(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl16/100)),
          TD16=OpenToday-(((ADR1+ADR5+ADR10+ADR20)/4)*(lvl16/100));
   if(showTARGETS)
     {
      if(_Period<=PERIOD_H1)
        {
         if(TX)
            if(showADRlines)
              {
               iLine2(ID+"X011",ADRColUP,TU2);
               iLine2(ID+"X012",ADRColUP,TU3);
               iLine2(ID+"X013",ADRColUP,TU4);
               iLine2(ID+"X014",ADRColUP,TU5);
               iLine2(ID+"X015",ADRColUP,TU6);
               iLine2(ID+"X016",ADRColUP,TU7);
               iLine2(ID+"X017",ADRColUP,TU8);
               iLine2(ID+"X018",ADRColUP,TU9);

               iLine2(ID+"X019",ADRColDN,TD2);
               iLine2(ID+"X020",ADRColDN,TD3);
               iLine2(ID+"X021",ADRColDN,TD4);
               iLine2(ID+"X022",ADRColDN,TD5);
               iLine2(ID+"X023",ADRColDN,TD6);
               iLine2(ID+"X024",ADRColDN,TD7);
               iLine2(ID+"X025",ADRColDN,TD8);
               iLine2(ID+"X026",ADRColDN,TD9);
              }
         if(TX)
            iLabel(ID+"X031",gap+DoubleToString(lvl2,1)+"%",ADRColUP,TU2,0);
         if(TX)
            iLabel(ID+"X032",gap+DoubleToString(lvl3,1)+"%",ADRColUP,TU3,0);
         if(TX)
            iLabel(ID+"X033",gap+DoubleToString(lvl4,1)+"%",ADRColUP,TU4,0);
         if(TX)
            iLabel(ID+"X034",gap+DoubleToString(lvl5,1)+"%",ADRColUP,TU5,0);
         if(TX)
            iLabel(ID+"X035",gap+DoubleToString(lvl6,1)+"%",ADRColUP,TU6,0);
         if(TX)
            iLabel(ID+"X036",gap+DoubleToString(lvl7,1)+"%",ADRColUP,TU7,0);
         if(TX)
            iLabel(ID+"X037",gap+DoubleToString(lvl8,1)+"%",ADRColUP,TU8,0);
         if(TX)
            iLabel(ID+"X038",gap+DoubleToString(lvl9,1)+"%",ADRColUP,TU9,0);
         if(TX)
            iLabel(ID+"X039",gap+DoubleToString(lvl10,1)+"%",ADRColUP,TU10,0);
         if(TX)
            iLabel(ID+"X040",gap+DoubleToString(lvl11,1)+"%",ADRColUP,TU11,0);
         if(TX)
            iLabel(ID+"X041",gap+DoubleToString(lvl12,1)+"%",ADRColUP,TU12,0);
         if(TX)
            iLabel(ID+"X042",gap+DoubleToString(lvl13,1)+"%",ADRColUP,TU13,0);
         if(TX)
            iLabel(ID+"X043",gap+DoubleToString(lvl14,1)+"%",ADRColUP,TU14,0);
         if(TX)
            iLabel(ID+"X044",gap+DoubleToString(lvl15,1)+"%",ADRColUP,TU15,0);
         if(TX)
            iLabel(ID+"X045",gap+DoubleToString(lvl16,1)+"%",ADRColUP,TU16,0);


         if(TX)
            iLabel(ID+"X050",gap+DoubleToString(lvl2,1)+"%",ADRColDN,TD2,0);
         if(TX)
            iLabel(ID+"X051",gap+DoubleToString(lvl3,1)+"%",ADRColDN,TD3,0);
         if(TX)
            iLabel(ID+"X052",gap+DoubleToString(lvl4,1)+"%",ADRColDN,TD4,0);
         if(TX)
            iLabel(ID+"X053",gap+DoubleToString(lvl5,1)+"%",ADRColDN,TD5,0);
         if(TX)
            iLabel(ID+"X054",gap+DoubleToString(lvl6,1)+"%",ADRColDN,TD6,0);
         if(TX)
            iLabel(ID+"X055",gap+DoubleToString(lvl7,1)+"%",ADRColDN,TD7,0);
         if(TX)
            iLabel(ID+"X056",gap+DoubleToString(lvl8,1)+"%",ADRColDN,TD8,0);
         if(TX)
            iLabel(ID+"X057",gap+DoubleToString(lvl9,1)+"%",ADRColDN,TD9,0);
         if(TX)
            iLabel(ID+"X058",gap+DoubleToString(lvl10,1)+"%",ADRColDN,TD10,0);
         if(TX)
            iLabel(ID+"X059",gap+DoubleToString(lvl11,1)+"%",ADRColDN,TD11,0);
         if(TX)
            iLabel(ID+"X060",gap+DoubleToString(lvl12,1)+"%",ADRColDN,TD12,0);
         if(TX)
            iLabel(ID+"X061",gap+DoubleToString(lvl13,1)+"%",ADRColDN,TD13,0);
         if(TX)
            iLabel(ID+"X062",gap+DoubleToString(lvl14,1)+"%",ADRColDN,TD14,0);
         if(TX)
            iLabel(ID+"X063",gap+DoubleToString(lvl15,1)+"%",ADRColDN,TD15,0);
         if(TX)
            iLabel(ID+"X064",gap+DoubleToString(lvl16,1)+"%",ADRColDN,TD16,0);

        }
     }
//+-------------------------------------------------------------------------------------------------------------------+
   return(rates_total);
  }//End OnCalculate
//+----iLine1 Function------------------------------------------------------------------------------------------------+
void iLine1(string tls1, color a_color_8, double ad_12)
  {
   if(ObjectFind(0,tls1)!=0)
      ObjectDelete(0,tls1);
   ObjectCreate(0,tls1,OBJ_TREND,0,
                iTime(_Symbol,TimeFrame,0),ad_12,iTime(_Symbol,TimeFrame,0) +60*TimeFrame*RayLength,ad_12);
   ObjectSetInteger(0,tls1,OBJPROP_WIDTH,OrderLineWidth);
   ObjectSetInteger(0,tls1,OBJPROP_STYLE,PrevOpenStyle);
   ObjectSetInteger(0,tls1,OBJPROP_COLOR,a_color_8);
   ObjectSetInteger(0,tls1,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,tls1,OBJPROP_RAY,false);
   ObjectSetInteger(0,tls1,OBJPROP_BACK,true);
   ObjectSetInteger(0,tls1,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,tls1,OBJPROP_SELECTED,false);
   ObjectSetString(0,tls1,OBJPROP_TOOLTIP,"\n");
  }
//+----iLine2 Function------------------------------------------------------------------------------------------------+
void iLine2(string tls2, color a_color_8, double ad_12)
  {
   if(ObjectFind(0,tls2)!=0)
      ObjectDelete(0,tls2);
   ObjectCreate(0,tls2,OBJ_TREND,0,
                iTime(_Symbol,TimeFrame,0),ad_12,iTime(_Symbol,TimeFrame,0) +60*TimeFrame*RayLength,ad_12);
   ObjectSetInteger(0,tls2,OBJPROP_WIDTH,ADRLineWidth);
   ObjectSetInteger(0,tls2,OBJPROP_STYLE,ADRStyle);
   ObjectSetInteger(0,tls2,OBJPROP_COLOR,a_color_8);
   ObjectSetInteger(0,tls2,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,tls2,OBJPROP_RAY,false);
   ObjectSetInteger(0,tls2,OBJPROP_BACK,true);
   ObjectSetInteger(0,tls2,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,tls2,OBJPROP_SELECTED,false);
   ObjectSetString(0,tls2,OBJPROP_TOOLTIP,"\n");
  }
//+----iLabel Function-----------------------------------------------------------------------------------------------+
void iLabel(string name="Labelx",string text=" ",color bcolor=0,double xdist=0,int ydist=0)
  {
   if(ObjectFind(0,name)!=0)
      ObjectDelete(0,name);
   ObjectCreate(0,name,OBJ_TEXT,0,0,0);
   ObjectMove(0,name,0,iTime(_Symbol,0,0+LABELmove),xdist+(_Point*1));
   ObjectSetText(name,text,TextSize+2,"Consolas Bold",bcolor);
   ObjectSetInteger(0,name,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,name,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,name,OBJPROP_SELECTED,false);
   ObjectSetString(0,name,OBJPROP_TOOLTIP,"\n");
   ObjectSetInteger(0,name,OBJPROP_BACK,true);
  }
//+---Timeframe Function---------------------------------------------------------------------------------------------+
string sTfTable[]= {"M1","M5","M15","M30","H1","H4","D1","W1","MN"};
int    iTfTable[]= {1,5,15,30,60,240,1440,10080,43200};
//+------------------------------------------------------------------------------------------------------------------+
int stringToTimeFrame(string tfs)
  {
   tfs=stringUpperCase(tfs);
   for(int i=ArraySize(iTfTable)-1; i>=0; i--)
      if(tfs==sTfTable[i] || tfs==""+iTfTable[i])
         return(MathMax(iTfTable[i],_Period));
   return(_Period);
  }
//+------------------------------------------------------------------------------------------------------------------+
string timeFrameToString(int tf)
  {
   for(int i=ArraySize(iTfTable)-1;i>=0;i--)
      if(tf==iTfTable[i])
         return(sTfTable[i]);
   return("");
  }
//+------------------------------------------------------------------------------------------------------------------+
string stringUpperCase(string str)
  {
   string s=str;
   for(int length=StringLen(str)-1; length>=0; length--)
     {
      int tchar=StringGetCharacter(s,length);
      if((tchar>96 && tchar<123) || (tchar>223 && tchar<256))
         s=StringSetCharacter(s,length,tchar-32);
      else
         if(tchar>-33 && tchar<0)
            s=StringSetCharacter(s,length,tchar+224);
     }
   return(s);
  }
//+----Clean Chart Function------------------------------------------------------------------------------------------+
void CleanUpIsle1()
  {
   string name;
   for(int s=ObjectsTotal(0)-1; s>=0; s--)
     {
      name=ObjectName(0,s);
      if(StringSubstr(name,0,StringLen(ID))==ID)
        {
         ObjectDelete(0,name);  //EOF
        }
     }
  }
//+------------------------------------------------------------------------------------------------------------------+
int BoolNewTF()
  {
   datetime BarOpenTime=iTime(_Symbol,PERIOD_M1,0);
   if(BarTime==0)
      BarTime=BarOpenTime;
   if(BarTime!=BarOpenTime)
     {
      BarTime=BarOpenTime;
      return(1);
     }
   else
      return(0);
  }
//+----------------------------------------------------

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int WindowHandle(string symbol,
                 int tf)
  {
   ENUM_TIMEFRAMES timeframe=TFMigrate(tf);
   long currChart,prevChart=ChartFirst();
   int i=0,limit=100;
   while(i<limit)
     {
      currChart=ChartNext(prevChart);
      if(currChart<0)
         break;
      if(ChartSymbol(currChart)==symbol
         && ChartPeriod(currChart)==timeframe)
         return((int)currChart);
      prevChart=currChart;
      i++;
     }
   return(0);
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
ENUM_TIMEFRAMES TFMigrate(int tf)
  {
   switch(tf)
     {
      case 0:
         return(PERIOD_CURRENT);
      case 1:
         return(PERIOD_M1);
      case 5:
         return(PERIOD_M5);
      case 15:
         return(PERIOD_M15);
      case 30:
         return(PERIOD_M30);
      case 60:
         return(PERIOD_H1);
      case 240:
         return(PERIOD_H4);
      case 1440:
         return(PERIOD_D1);
      case 10080:
         return(PERIOD_W1);
      case 43200:
         return(PERIOD_MN1);

      case 2:
         return(PERIOD_M2);
      case 3:
         return(PERIOD_M3);
      case 4:
         return(PERIOD_M4);
      case 6:
         return(PERIOD_M6);
      case 10:
         return(PERIOD_M10);
      case 12:
         return(PERIOD_M12);
      case 16385:
         return(PERIOD_H1);
      case 16386:
         return(PERIOD_H2);
      case 16387:
         return(PERIOD_H3);
      case 16388:
         return(PERIOD_H4);
      case 16390:
         return(PERIOD_H6);
      case 16392:
         return(PERIOD_H8);
      case 16396:
         return(PERIOD_H12);
      case 16408:
         return(PERIOD_D1);
      case 32769:
         return(PERIOD_W1);
      case 49153:
         return(PERIOD_MN1);
      default:
         return(PERIOD_CURRENT);
     }
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool ObjectSetText(string name,
                   string text,
                   int font_size,
                   string font="",
                   color text_color=clrBlack)
  {
   int tmpObjType=(int)ObjectGetInteger(0,name,OBJPROP_TYPE);
   ObjectSetInteger(0,name,OBJPROP_BGCOLOR,clrWhite);
   ObjectSetString(0,name,OBJPROP_TEXT,text);
   ObjectSetInteger(0,name,OBJPROP_FONTSIZE,font_size);
   ObjectSetString(0,name,OBJPROP_FONT,"Arial");
   ObjectSetInteger(0,name,OBJPROP_COLOR,text_color);
   return(false);
  }  
//+------------------------------------------------------------------+
