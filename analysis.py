import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from mycolorpy import colorlist as mcp
flatten = lambda l: [item for sublist in l for item in sublist]
from collections import Counter, defaultdict
import numpy as np


def get_profiles(support_file, all_patterns_id, profiles_path=False):
    
    support_file = {p:int(s) for p,s in support_file.items()}

    profile = [(p,support_file.get(p,0)) for p in all_patterns_id]
    profile.sort(key = lambda x: x[0])
    
    tot = sum(support_file.values())

    profile_rel = [p[1]/tot for p in profile]
    profile_rel_dict = {p: sup/tot for p,sup in profile}
    profile_absolute = [p[1] for p in profile]
    
    if profiles_path != False:
        pickle.dump(profile_rel, open(profiles_path+'_profiles_rel.p','wb'))
        pickle.dump(profile_rel_dict, open(profiles_path+'_profile_rel_dict.p','wb'))
        pickle.dump(profile_absolute, open(profiles_path+'_profile_absolute.p','wb'))

    return profile_rel


def plot_profile(profiles, 
                 ger_ids,
                 single_profile = True, 
                 cmap = 'Spectral',
                 color = 'navy',
                 fs = (10,5),
                 legend = False,
                 labels = [],
                 plot_params = {'ms' : 9, 'lw' : 2, 'style':'.-'},
                 ticks_params = {'fontsize_x':8, 'rotation':0,'fontweight':'bold'},
                 label_params = {'xlabel': "\nRules' indexes", 'fontsize_x' :10, 'fontweight_x':'bold',
                                'ylabel': "Relative frequency of rules\n", 'fontsize_y' :10, 'fontweight_y':'bold'}):
    
    plt.figure(figsize = fs)
    if not single_profile:
        if type(cmap) !=list:
            cmap =mcp.gen_color(cmap=cmap,n=len(profiles))
        for i,profile in enumerate(profiles):
            plt.plot(profile, plot_params['style'], ms = plot_params['ms'], lw = plot_params['lw'], color = cmap[i], label = labels[i])

    else: 
        plt.plot(profiles, plot_params['style'], ms = plot_params['ms'], lw = plot_params['lw'], color = color )
    plt.xticks(range(len(ger_ids)),list(ger_ids), 
               fontsize = ticks_params['fontsize_x'], 
               rotation = ticks_params['rotation'], 
               fontweight = ticks_params['fontweight'])
    
    plt.xlabel(label_params['xlabel'], fontsize = label_params['fontsize_x'], fontweight = label_params['fontweight_x'])
    plt.ylabel(label_params['ylabel'], fontsize = label_params['fontsize_y'], fontweight = label_params['fontweight_y'])
    
    plt.grid()
    if legend: plt.legend(fontsize = 'x-large')
    plt.show()
    
    
def plot_heatmap(profiles, 
                 ger_ids,
                 single_profile = True, 
                 cmap = 'Blues',
                 fs = (20,15),
                 cbar_ticks_size = 25,
                 savefig = False,
                 yticks = 'default',
                 xticks = 'default',
                 vmax = 'default',
                 vertical_rules = True,
                 plot_params = {'ms' : 9, 'lw' : 2, 'style':'.-', 'title':'', 'title_size':30},
                 ticks_params = {'fontsize_x':25, 'rotation_x':0,'fontweight_x':'bold',
                                'fontsize_y':25, 'rotation_y':0,'fontweight_y':'bold'},
                 label_params = {'xlabel': "\nRules' indexes", 'fontsize_x' :30, 'fontweight_x':'bold',
                                'ylabel': "", 'fontsize_y' :30, 'fontweight_y':'bold'}):
    

    plt.figure(figsize = fs)
    import seaborn as sns
    if single_profile:
        matrix = np.array(profiles).reshape(len(profiles),-1)
        xticks = []
    else:
        matrix = np.array(profiles)
        if vertical_rules: matrix = matrix.T
        
        if xticks =='default':  xticks = range(len(profiles))

        
    if vmax=='default':
        ax = sns.heatmap(matrix, cmap = cmap)
    else:
        ax = sns.heatmap(matrix, cmap = cmap, vmax = vmax)
    
    
    if vertical_rules: 
        plt.yticks([x+0.5 for x in range(len(ger_ids))],ger_ids, 
               fontsize = ticks_params['fontsize_y'], 
               rotation = ticks_params['rotation_y'], 
               fontweight = ticks_params['fontweight_y'])
    
        plt.xticks([x+0.5 for x in range(len(xticks))],xticks, 
               fontsize = ticks_params['fontsize_x'], 
               rotation = ticks_params['rotation_x'], 
               fontweight = ticks_params['fontweight_x'])
    else: 
        plt.xticks([x+0.5 for x in range(len(ger_ids))],ger_ids, 
               fontsize = ticks_params['fontsize_y'], 
               rotation = ticks_params['rotation_y'], 
               fontweight = ticks_params['fontweight_y'])
    
        plt.yticks([x+0.5 for x in range(len(xticks))],xticks, 
               fontsize = ticks_params['fontsize_x'], 
               rotation = ticks_params['rotation_x'], 
               fontweight = ticks_params['fontweight_x'])
    
    plt.xlabel(label_params['xlabel'], fontsize = label_params['fontsize_x'], fontweight = label_params['fontweight_x'])
    plt.ylabel(label_params['ylabel'], fontsize = label_params['fontsize_y'], fontweight = label_params['fontweight_y'])
    
   
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=cbar_ticks_size)
    if plot_params['title'] != '': plt.title(plot_params['title']+"\n", fontsize = plot_params['title_size'], fontweight = 'bold')
    if savefig != False: plt.savefig(savefig,bbox_inches = 'tight')
    plt.show()

    
    
def t_span_plot(pattern_list,
               cmap = 'Blues',
                fs = (15,6),
                 cbar_ticks_size = 25,
                 plot_params = {'ms' : 9, 'lw' : 2, 'style':'.-'},
                 ticks_params = {'fontsize_x':25, 'rotation_x':0,'fontweight_x':'bold',
                                'fontsize_y':25, 'rotation_y':0,'fontweight_y':'bold'},
                 label_params = {'xlabel': "\nT-span", 'fontsize_x' :30, 'fontweight_x':'bold',
                                'ylabel': "Frequency of t-span\n", 'fontsize_y' :30, 'fontweight_y':'bold'}):
    
                   
    ##### ONLY FOR GERM ALGORITHM #####
    ## because evomine only has to and t1 as timestamps ##
    
    spans = {p_id : max([e[-1] for e in info['edges']]) for p_id, info in pattern_list.items()}
    count_span = Counter(spans.values())
    tot = len(spans)
    
    plt.figure(figsize = fs)
    
    count_span = Counter(spans.values())
    tot = sum(count_span.values())
    count_span = {span:c/tot for span,c in count_span.items()}
    count_span = [(span,perc) for span,perc in count_span.items()]
    count_span.sort(key = lambda x:x[0])
    
    colormap = mcp.gen_color(cmap=cmap,n=max(dict(count_span).keys())+1)
    color_tspan = {i:c for i,c in enumerate(colormap)}

    for xindex,(span,count) in enumerate(count_span):
        plt.bar(xindex,count, color = color_tspan[span], width = 1)
        xindex+=1   

    plt.xticks(range(len(count_span)), [x[0] for x in count_span], size = ticks_params['fontsize_x'])
    plt.yticks(size = ticks_params['fontsize_x'])
    plt.xlabel(label_params['xlabel'],size = label_params['fontsize_x'], weight = label_params['fontweight_x'] )
    plt.ylabel(label_params['ylabel'],size = label_params['fontsize_x'], weight = label_params['fontweight_y'] )
   
    plt.show()
    
    
    return spans