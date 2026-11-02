import pandas as pd, numpy as np, json
from chart_style import *
import matplotlib.pyplot as plt
apply_style()
px=pd.read_csv('px.csv',parse_dates=['timestamp']).sort_values('timestamp').reset_index(drop=True)
c=px.close; r=np.log(c).diff().dropna()
out={}
out['last']=c.iloc[-1]
def ret(n): return c.iloc[-1]/c.iloc[-1-n]-1
for k,n in [('1d',1),('1w',5),('1m',21),('3m',63),('99d',99)]: out['ret'+k]=ret(n)
out['vol_ann']=r.std()*np.sqrt(252)
out['down_vol']=np.sqrt((np.minimum(r,0)**2).mean())*np.sqrt(252)
dd=c/c.cummax()-1; out['mdd']=dd.min(); out['mdd_date']=str(px.timestamp[dd.idxmin()].date()); out['curr_dd']=dd.iloc[-1]
out['hi']=c.max();out['lo']=c.min()
# RSI14
d=c.diff(); g=d.clip(lower=0).ewm(alpha=1/14,adjust=False).mean(); l=(-d.clip(upper=0)).ewm(alpha=1/14,adjust=False).mean()
rsi=100-100/(1+g/l); out['rsi']=rsi.iloc[-1]
ma20=c.rolling(20).mean(); ma50=c.rolling(50).mean(); out['ma20']=ma20.iloc[-1]; out['ma50']=ma50.iloc[-1]
e12=c.ewm(span=12,adjust=False).mean(); e26=c.ewm(span=26,adjust=False).mean(); macd=e12-e26; sig=macd.ewm(span=9,adjust=False).mean()
out['macd']=macd.iloc[-1]; out['macd_sig']=sig.iloc[-1]
tr=pd.concat([px.high-px.low,(px.high-c.shift()).abs(),(px.low-c.shift()).abs()],axis=1).max(axis=1); atr=tr.ewm(alpha=1/14,adjust=False).mean(); out['atr']=atr.iloc[-1]
out['vol20']=px.volume.tail(20).mean(); out['vol100']=px.volume.mean()
rb=np.log(px.bsac).diff().dropna(); out['corr_bsac']=r.corr(rb); out['beta_bsac']=np.cov(r,rb)[0,1]/rb.var()
out['bsac_ret99']=px.bsac.iloc[-1]/px.bsac.iloc[0]-1; out['bch_ret99']=c.iloc[-1]/c.iloc[0]-1
out['bsac_vol']=rb.std()*np.sqrt(252)
out['bsac_ret3m']=px.bsac.iloc[-1]/px.bsac.iloc[-64]-1
out['rets_since_sep']=c.iloc[-1]/c[px.timestamp=='2026-09-03'].iloc[0]-1
out['up_days']=(r>0).mean()
for k,v in out.items(): print(k, round(v,4) if isinstance(v,float) else v)
# derived year-end prices from mcap
mc={2012:14.25,2013:13.73,2014:10.71,2015:9.58,2016:11.54,2017:16.12,2018:14.54,2019:10.60,2020:10.29,2021:7.93,2022:10.52,2023:11.66,2024:11.46,2025:19.19}
ads=0.505085
print({y:round(v/ads,2) for y,v in mc.items()})
cur=18.46; print('now px implied',cur/ads)
# cover chart: last 63
p=px.tail(63)
f,a=plt.subplots(figsize=(6.4,2.5)); a.plot(p.timestamp,p.close,color=NAVY,lw=1.5)
a.fill_between(p.timestamp,p.close,p.close.min()*0.97,color=CAMEL,alpha=.3); a.set_ylim(p.close.min()*0.97,p.close.max()*1.03)
a.set_ylabel('USD per ADS'); import matplotlib.dates as md; a.xaxis.set_major_formatter(md.DateFormatter('%d %b')); save(f,'cover_price')
# price + MA50 + volume
f,(a,b)=plt.subplots(2,1,figsize=(6.4,3.2),sharex=True,gridspec_kw={'height_ratios':[3,1]})
a.plot(px.timestamp,c,color=NAVY,lw=1.3,label='Close'); a.plot(px.timestamp,ma20,color=BROWN,lw=1,label='20-day average'); a.plot(px.timestamp,ma50,color=OLIVE,lw=1,label='50-day average')
a.set_ylabel('USD per ADS'); a.legend(loc='lower left',ncol=3,fontsize=7); b.bar(px.timestamp,px.volume/1e3,color=CAMEL,width=1.0); b.set_ylabel('Volume, 000s'); b.xaxis.set_major_formatter(md.DateFormatter('%d %b')); save(f,'tech')
# relative
f,a=plt.subplots(figsize=(6.4,2.4)); a.plot(px.timestamp,100*c/c.iloc[0],color=NAVY,lw=1.4,label='Banco de Chile (BCH)'); a.plot(px.timestamp,100*px.bsac/px.bsac.iloc[0],color=BROWN,lw=1.4,label='Banco Santander-Chile (BSAC)')
a.set_ylabel('Rebased to 100 at 10 Jun 2026'); a.legend(loc='lower left'); a.xaxis.set_major_formatter(md.DateFormatter('%d %b')); save(f,'relative')
# market cap history
yrs=list(mc)+['Oct 2026']; vals=list(mc.values())+[cur]
f,a=plt.subplots(figsize=(6.4,2.4)); a.bar([str(y) for y in yrs],vals,color=[NAVY]*14+[BROWN],width=.6); a.set_ylabel('USD bn')
for i,t in enumerate(vals): a.text(i,t+.3,f'{t:.1f}',ha='center',fontsize=6.5)
a.set_ylim(0,22); plt.setp(a.get_xticklabels(),fontsize=6.5); save(f,'mcap')
# financial charts (CLP bn)
Y=['2021','2022','2023','2024','2025']
rev=[2224.871,3142.623,2994.872,3050.285,3026.043]; ni=[1056.316,1445.799,1243.634,1207.392,1192.262]
nii=[1574.022,2266.129,1546.916,1781.655,1746.115]; nonint=[650.849,876.494,1447.956,1268.630,1279.928]
f,a=plt.subplots(figsize=(6.4,2.4)); x=np.arange(5); w=.38
a.bar(x-w/2,rev,w,color=NAVY,label='Operating revenue before loan losses'); a.bar(x+w/2,ni,w,color=CAMEL,label='Net income')
for i in range(5):
    a.text(i-w/2,rev[i]+40,f'{rev[i]:,.0f}',ha='center',fontsize=6.5); a.text(i+w/2,ni[i]+40,f'{ni[i]:,.0f}',ha='center',fontsize=6.5)
a.set_xticks(x); a.set_xticklabels(Y); a.set_ylabel('CLP bn'); a.set_ylim(0,3700); a.legend(loc='upper left',ncol=2); save(f,'revni')
f,a=plt.subplots(figsize=(6.4,2.4)); a.bar(Y,nii,color=NAVY,label='Net interest income',width=.5); a.bar(Y,nonint,bottom=nii,color=CAMEL,label='Non-interest income',width=.5)
a.set_ylabel('CLP bn'); a.legend(loc='upper left',ncol=2); a.set_ylim(0,4000); save(f,'mix')
# ratios
eq=[4293.521,5431.435,5237.283,5622.999,5799.534]; ta=[51758.326,55108.854,55792.552,52095.441,54100.903]
roe=[None]+[ni[i]/((eq[i]+eq[i-1])/2)*100 for i in range(1,5)]
roa=[None]+[ni[i]/((ta[i]+ta[i-1])/2)*100 for i in range(1,5)]
nonex=[871.721,995.296,1114.937,1131.194,1129.764]; eff=[nonex[i]/rev[i]*100 for i in range(5)]
print('roe',roe,'roa',roa,'eff',eff)
f,a=plt.subplots(figsize=(6.4,2.4)); a.plot(x[1:],roe[1:],color=NAVY,marker='o',ms=3.5,label='Return on average equity (calculated)')
a.plot(x,eff,color=BROWN,marker='s',ms=3.5,label='Efficiency ratio (calculated)'); a2=a.twinx(); a2.plot(x[1:],roa[1:],color=OLIVE,marker='^',ms=3.5,label='Return on average assets, right axis'); a2.grid(False)
a2.spines['right'].set_visible(True); a.set_ylabel('Percent'); a2.set_ylabel('ROA, percent'); a2.set_ylim(0,4)
h=a.get_legend_handles_labels();h2=a2.get_legend_handles_labels(); a.legend(h[0]+h2[0],h[1]+h2[1],loc='upper right',fontsize=6.5); a.set_ylim(20,40); a.set_xticks(x); a.set_xticklabels(Y); save(f,'ratios')
# balance sheet
loans=[33951.181,36276.739,37249.983,38755.851,38754.122]; dep=[27053.594,27951.142,28687.222,28432.006,28470.164]; debt=[17580.363,19306.646,18720.316,15011.506,16211.812]
f,a=plt.subplots(figsize=(6.4,2.4)); w=.26
a.bar(x-w,[l/1000 for l in loans],w,color=NAVY,label='Net loans'); a.bar(x,[d/1000 for d in dep],w,color=CAMEL,label='Deposits'); a.bar(x+w,[d/1000 for d in debt],w,color=OLIVE,label='Borrowings and debt')
a.set_xticks(x); a.set_xticklabels(Y); a.set_ylabel('CLP trillion'); a.legend(loc='upper left',ncol=3); a.set_ylim(0,48); save(f,'bs')
# dividends
f,a=plt.subplots(figsize=(6.4,2.2)); dy=['2024','2025','2026']; dv=[1.23509,1.56956,1.65471]
a.bar(dy,dv,color=NAVY,width=.4); [a.text(i,v+.03,f'{v:.2f}',ha='center',fontsize=7) for i,v in enumerate(dv)]; a.set_ylabel('USD per ADS'); a.set_ylim(0,2); save(f,'div')
# scenario
f,a=plt.subplots(figsize=(6.4,2.4)); sc={'Bear':[1150,1100,1090],'Base':[1260,1300,1345],'Bull':[1320,1380,1450]}; x3=np.arange(3); w=.26
for k,(n,v) in enumerate(sc.items()):
    a.bar(x3+(k-1)*w,v,w,color=[BROWN,NAVY,OLIVE][k],label=n); [a.text(x3[i]+(k-1)*w,vv+10,f'{vv:,}',ha='center',fontsize=6.5) for i,vv in enumerate(v)]
a.axhline(1192,color=CAMEL,lw=1.2,ls='--'); a.text(2.45,1200,'FY2025 reported 1,192',fontsize=6.5,ha='right',color=BROWN)
a.set_xticks(x3); a.set_xticklabels(['FY2026E','FY2027E','FY2028E']); a.set_ylim(900,1550); a.set_ylabel('CLP bn'); a.legend(loc='upper left',ncol=3); save(f,'scen')
# peers
nm=['BCH','BSAC','CIB','BAP']; pe=[15.17,11.76,16.16,13.78]; pb=[3.08,2.58,2.14,2.66]; ro=[21.08,23.59,19.22,20.41]
f,axs=plt.subplots(1,3,figsize=(6.4,2.2))
for ax,v,t in zip(axs,[pe,pb,ro],['Trailing P/E, x','Price to book, x','ROE, %']):
    ax.bar(nm,v,color=[NAVY,CAMEL,CAMEL,CAMEL],width=.55); ax.set_title(t,fontsize=8); [ax.text(i,x_+max(v)*.02,f'{x_:.1f}',ha='center',fontsize=6.5) for i,x_ in enumerate(v)]
    ax.set_ylim(0,max(v)*1.18); plt.setp(ax.get_xticklabels(),fontsize=7)
plt.tight_layout(); save(f,'peers')
# justified P/B grid
bv=11.85
print('grid')
for coe in [9,10,11,12,13]:
    print(coe,[round(bv*(19-g)/(coe-g),2) for g in [2,3,4]], [round((19-g)/(coe-g),2) for g in [2,3,4]])
print('ROE sens g=3 COE10',[ (r_, round(bv*(r_-3)/(10-3),2)) for r_ in [15,17,19,21,23]])
print('pb now',36.55/bv, 'implied roe', 3.5+ (36.55/bv)*(10-3.5))
