"""Generates mock charts and a mock logo for the OCAD LaTeX template (palette-matched).
Run: python3 make_mock_images.py   (needs matplotlib, numpy)"""
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
NAVY='#172A3A';BROWN='#6B5744';OLIVE='#3F4A32';CAMEL='#C8AE82'
plt.rcParams.update({'font.family':'Liberation Sans','font.size':8,'axes.edgecolor':NAVY,'axes.labelcolor':NAVY,
 'xtick.color':BROWN,'ytick.color':BROWN,'axes.facecolor':'#FBF9F3','figure.facecolor':'#FBF9F3',
 'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':'#E3DAC3','grid.linewidth':0.5,'text.color':NAVY})
rng=np.random.default_rng(7)
def save(f,n): f.savefig(f'charts/{n}.png',dpi=220,bbox_inches='tight',facecolor=f.get_facecolor()); plt.close(f)
yrs=['2021','2022','2023','2024','2025']
# cover price chart (mock random walk)
p=100+np.cumsum(rng.normal(0.2,1.6,63)); f,a=plt.subplots(figsize=(6.4,2.6)); a.plot(p,color=NAVY,lw=1.5)
a.fill_between(range(63),p,p.min()*0.97,color=CAMEL,alpha=.3); a.set_ylim(p.min()*0.97,p.max()*1.03); a.set_ylabel('US$ per share'); a.set_xlabel('Trading days (mock data)'); save(f,'cover_price')
rev=[8200,9100,10050,11200,12400]
f,a=plt.subplots(figsize=(6.4,2.6)); a.bar(yrs,rev,color=NAVY,width=.5); a.set_ylabel('US$ million')
for i,v in enumerate(rev): a.text(i,v+200,f'{v:,}',ha='center',fontsize=7.5)
a2=a.twinx(); g=[(rev[i]/rev[i-1]-1)*100 for i in range(1,5)]; a2.plot(yrs[1:],g,color=BROWN,marker='o',ms=3.5,lw=1.3); a2.grid(False); a2.spines['right'].set_visible(True); a2.set_ylim(0,25); a2.set_ylabel('Growth, %',color=BROWN)
a.set_ylim(0,15000); save(f,'revenue')
f,a=plt.subplots(figsize=(6.4,2.4)); x=np.arange(5); w=.35
a.bar(x-w/2,[14,15,16,17,18],w,color=NAVY,label='Operating margin'); a.bar(x+w/2,[9,10,11,12,12.5],w,color=CAMEL,label='Net margin')
a.set_xticks(x); a.set_xticklabels(yrs); a.set_ylabel('% of revenue'); a.legend(frameon=False,loc='upper left'); a.set_ylim(0,24); save(f,'margins')
f,a=plt.subplots(figsize=(6.4,2.4)); w=.27; ocf=[1500,1700,1900,2100,2350]; cap=[600,650,720,800,900]
a.bar(x-w,ocf,w,color=NAVY,label='Operating cash flow'); a.bar(x,cap,w,color=CAMEL,label='Capital expenditure'); a.bar(x+w,[o-c for o,c in zip(ocf,cap)],w,color=OLIVE,label='Free cash flow')
a.set_xticks(x); a.set_xticklabels(yrs); a.set_ylabel('US$ million'); a.legend(frameon=False,loc='upper left'); a.set_ylim(0,3000); save(f,'cashflow')
f,a=plt.subplots(figsize=(6.4,2.4)); lab=['2023','2024','2025']; x=np.arange(3)
a.bar(x-w,[3000,2900,2700],w,color=NAVY,label='Gross debt'); a.bar(x,[900,1100,1400],w,color=CAMEL,label='Cash'); a.bar(x+w,[2100,1800,1300],w,color=BROWN,label='Net debt')
a.set_xticks(x); a.set_xticklabels(lab); a.set_ylabel('US$ million'); a.legend(frameon=False,loc='upper right'); a.set_ylim(0,4000); save(f,'debt')
f,(a,b)=plt.subplots(1,2,figsize=(6.4,2.2)); n=['Mock Co','Peer A','Peer B','Peer C']
a.bar(n,[11.2,13.5,9.8,15.1],color=[NAVY,CAMEL,CAMEL,CAMEL]); a.set_title('EV/EBITDA, times',fontsize=8,loc='left')
b.bar(n,[17.5,14.2,12.9,9.6],color=[NAVY,CAMEL,CAMEL,CAMEL]); b.set_title('Operating margin, %',fontsize=8,loc='left'); save(f,'peers')
m=np.arange(36); l=100*np.cumprod(1+rng.normal(.012,.06,36)); s=100*np.cumprod(1+rng.normal(.008,.035,36))
f,a=plt.subplots(figsize=(6.4,2.6)); a.plot(m,l,color=NAVY,lw=1.6,label='Mock Co'); a.plot(m,s,color=CAMEL,lw=1.6,label='Benchmark'); a.set_ylabel('Index, start = 100'); a.set_xlabel('Months (mock data)'); a.legend(frameon=False,loc='upper left'); save(f,'relative')
f,(a,b)=plt.subplots(1,2,figsize=(6.4,2.3),gridspec_kw={'width_ratios':[1,1.5]})
a.barh(['Other','Segment B','Segment A'],[300,1400,4300],color=[CAMEL,BROWN,NAVY]); a.set_title('Revenue by segment, US$ million',fontsize=8,loc='left')
b.barh(['Other','Marketing','R and D','Labor','Materials'],[420,380,520,1300,1900],color=NAVY); b.set_title('Principal costs, US$ million',fontsize=8,loc='left'); save(f,'mix')
# mock logo
f=plt.figure(figsize=(3,1)); f.patch.set_alpha(0); ax=f.add_axes([0,0,1,1]); ax.axis('off'); ax.set_facecolor('none')
ax.add_patch(plt.Rectangle((0.02,0.1),0.96,0.8,fill=False,ec=NAVY,lw=2)); ax.text(0.5,0.5,'MOCK LOGO',ha='center',va='center',fontsize=22,color=NAVY,family='Liberation Serif',weight='bold')
f.savefig('charts/mock_logo.png',dpi=220,transparent=True); plt.close(f)
