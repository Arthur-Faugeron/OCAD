"""OCAD chart style. Import apply_style() in any chart script, then save with save().
Palette: Oxford Navy, Tweed Brown, Deep Olive, Camel Beige. Run this file to rebuild the sample charts."""
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
NAVY='#172A3A'; BROWN='#6B5744'; OLIVE='#3F4A32'; CAMEL='#C8AE82'

def apply_style():
    plt.rcParams.update({'font.family':'Liberation Sans','font.size':8,'axes.edgecolor':NAVY,'axes.labelcolor':NAVY,
     'xtick.color':BROWN,'ytick.color':BROWN,'axes.facecolor':'#FBF9F3','figure.facecolor':'#FBF9F3',
     'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':'#E3DAC3','grid.linewidth':0.5,
     'text.color':NAVY,'legend.frameon':False})

def save(fig,name,folder='charts'):
    fig.savefig(f'{folder}/{name}.png',dpi=220,bbox_inches='tight',facecolor=fig.get_facecolor()); plt.close(fig)

if __name__=='__main__':
    apply_style(); rng=np.random.default_rng(3)
    p=100+np.cumsum(rng.normal(0.2,1.5,63)); f,a=plt.subplots(figsize=(6.4,2.5))
    a.plot(p,color=NAVY,lw=1.5); a.fill_between(range(63),p,p.min()*0.97,color=CAMEL,alpha=.3)
    a.set_ylim(p.min()*0.97,p.max()*1.03); a.set_ylabel('Currency per share'); a.set_xlabel('Trading days'); save(f,'cover_price')
    yrs=['FY1','FY2','FY3','FY4','FY5']; v=[100,108,115,124,131]
    f,a=plt.subplots(figsize=(6.4,2.4)); a.bar(yrs,v,color=NAVY,width=.5); a.set_ylabel('Currency million'); a.set_ylim(0,160)
    for i,t in enumerate(v): a.text(i,t+3,str(t),ha='center',fontsize=7.5)
    a2=a.twinx(); a2.plot(yrs[1:],[8,6.5,7.8,5.6],color=BROWN,marker='o',ms=3.5,lw=1.3); a2.grid(False)
    a2.spines['right'].set_visible(True); a2.set_ylim(0,20); a2.set_ylabel('Growth, %',color=BROWN); save(f,'bar_line_example')
    f,a=plt.subplots(figsize=(6.4,2.4)); x=np.arange(5); w=.27
    for k,(lab,c,vals) in enumerate([('Series A',NAVY,[10,12,13,15,16]),('Series B',CAMEL,[4,4,5,5,6]),('Series C',OLIVE,[6,8,8,10,10])]):
        a.bar(x+(k-1)*w,vals,w,color=c,label=lab)
    a.set_xticks(x); a.set_xticklabels(yrs); a.legend(loc='upper left',ncol=3); a.set_ylim(0,20); save(f,'grouped_bars_example')
