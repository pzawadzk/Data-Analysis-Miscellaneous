import matplotlib.pyplot as plt
import numpy as np

def plot_phase_diagram(data_to_plot, species, range=[-1,-1], axis=[1,0], legend = False, showx=True, showy=True, name = False):
    fig = plt.figure(figsize=(4,6))
    ax = fig.gca()


    loc=list(np.linspace(-2,0,5))
    ax.xaxis.set_major_locator(plt.FixedLocator(loc))
    ax.yaxis.set_major_locator(plt.FixedLocator(loc))
    
    loc=list(np.linspace(-2,0,5))
    ax.xaxis.set_major_locator(plt.FixedLocator(loc))
    col = {'Cu2S3Sn1': 'BlanchedAlmond',  'Cu3S4Sn1':'Cyan', 'Cu4S16Sn7':'r', "Cu4S4Sn1": 'g', "Cu4S32Sn15":'m',  
           'Cu1S2Sb1': 'BlanchedAlmond',  'Cu3S4Sb1':'Cyan', 'Cu12S13Sb4':'r', "Cu3S3Sb1": 'g',  
            "Cu2S1":'DeepSkyBlue','Cu1S1':'y',
           "S1Sn1":'LightSeaGreen',  "S2Sn1":'DarkSalmon',
            "S3Sb2":'LightSeaGreen', 
            'S': 'w', 'Cu': 'w', 'Sn': 'w', 'Sb': 'w',
           "Cu1S1Sn1": 'k', "Cu1S2Sn1": 'm'
            }
    col = ['k', 'r', 'b', 'g', 'y', 'c', 'm', 'DarkSalmon', 'LightSeaGreen', 'BlanchedAlmond', 'DeepSkyBlue']*40
    for i, key in enumerate(data_to_plot.keys()):
        
        if len(data_to_plot[key][1])>1:
            ax.fill(data_to_plot[key][axis[0]], data_to_plot[key][axis[1]], col[i], alpha=0.75, label = key)
            
            #print i, key, col[i]
    if legend:
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
    if showy:
      ax.set_ylabel(r'$\Delta\mu_{\mathrm{%s}}$ [eV]'%species[axis[1]], fontsize=25)
    else:    
        plt.setp(ax.get_yticklabels(), visible=False)
        
    if showx:
        ax.set_xlabel(r'$\Delta\mu_{\mathrm{%s}}$ [eV]'%species[axis[0]], fontsize=25)
    else:    
        plt.setp(ax.get_xticklabels(), visible=False)
        
    ax.axis(xmin=range[0], xmax=0, ymin =range[1], ymax=0)
    
    if name:
        savefig(name)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
          fancybox=True, shadow=True, ncol=5)
