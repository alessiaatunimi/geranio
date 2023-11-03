#imports
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
#from collections import Counter
import sys 
sys.path.append('/work/')

flatten = lambda l: [item for sublist in l for item in sublist]
to_G = lambda edges: nx.from_pandas_edgelist(pd.DataFrame(edges, columns = ['from','to','value']), 'from', 'to', edge_attr = 'value',create_using=nx.Graph())
to_diG = lambda edges: nx.from_pandas_edgelist(pd.DataFrame(edges, columns = ['from','to','value']), 'from', 'to', edge_attr = 'value',create_using=nx.DiGraph())
     
def select_head(t,all_ts):
        ts_head = max(all_ts)
        if t == 0: return 0
        elif t == ts_head: return 1
        else: return 0

def draw_pattern_ger(algorithm, edge_list,
                     w = 5, h = 5, pos_node = False, where_ax = False):
  
    col_map = {0:"navy", 1:"mediumseagreen", 3:'navy'}
    #### EVOMINE ####
    if algorithm in ['evomine','EvoMine','EVOMINE','Evomine']:

        if type(edge_list) in [list, tuple]: 
            g = to_diG(edge_list)
        else: 
            g = edge_list
            edge_list = [list(x[:2]) + [x[2]['value']] for x in g.edges(data = True)]
        if not pos_node: 
            pos_node = nx.circular_layout(g)
            if g.size()<2: 
                pos_node = nx.spring_layout(g)

        if where_ax == False: 
            plt.figure(figsize = (w,h))
            

            nx.draw(g, with_labels=False,
                            pos=pos_node,
                            node_color='lightgrey',
                            node_size= w * 300,
                            edge_color = [col_map[g[u][v]['value']] for u,v in g.edges()],
                            width=w,
                            arrowsize = w*10,
                            connectionstyle = 'arc3, rad = 0.1')

        else:
            nx.draw(g, with_labels=False,
                        pos=pos_node,
                        node_color='lightgrey',
                        node_size= w * 300,
                        edge_color = [col_map[g[u][v]['value']] for u,v in g.edges()],
                        width=w*1.5,
                        arrowsize = w*10,
                        connectionstyle = 'arc3, rad = 0.1',
                        #edge_cmap=ListedColormap(["navy", "mediumseagreen"]),
                        ax = where_ax)

    #### GERM ####
    elif algorithm in ['germ','Germ','GERM']:
        

        if type(edge_list) in [list, tuple] : g = to_G(edge_list)
        else: 
            g = edge_list
            edge_list = [list(x[:2]) + [x[2]['value']] for x in g.edges(data = True)]
        if not pos_node: 
            pos_node = nx.circular_layout(g)
            if g.size()<2: 
                pos_node = nx.spring_layout(g)
        

        ts = set([x[-1] for x in edge_list])

        edge_list_color = [tuple(list(edge)[:2]+[select_head(edge[-1], ts)]) for edge in edge_list]
        g_color = to_G(edge_list_color)

        if where_ax == False: 
            plt.figure(figsize = (w,h))
            nx.draw_networkx_nodes(g, pos_node,
                                    node_color = 'lightgrey',node_size = w * 300)
            nx.draw_networkx_edges(g, pos_node, 
                                    edge_color = [col_map[g_color[u][v]['value']] for u,v in g_color.edges()],
                        width=w)
            nx.draw_networkx_edge_labels(
                g, pos_node,
                edge_labels={(edge[0],edge[1]):edge[2]['value'] for edge in g.edges(data = True)},
                
                font_color='navy',font_size = 20,
                
            )

        else: 
            
            nx.draw_networkx_nodes(g, pos_node,
                                    node_color = 'lightgrey',node_size = w * 300,ax = where_ax)
            nx.draw_networkx_edges(g, pos_node, 
                                    edge_color = [col_map[g_color[u][v]['value']] for u,v in g_color.edges()],
                        width=w,ax = where_ax)
            nx.draw_networkx_edge_labels(
                g, pos_node,
                edge_labels={(edge[0],edge[1]):edge[2]['value'] for edge in g.edges(data = True)},
                
                font_color='navy',font_size = 20,ax = where_ax
                
            )

            
    
def draw_several_patterns(algorithm, edge_list, 
                          columns = 5, w_box = 4):
    howmany = len(edge_list)
    rows = howmany//columns + (howmany%columns +(columns-1))//columns
    
    fig,ax = plt.subplots(rows, columns, figsize = (columns*w_box, rows*w_box))
    
    for i in range(len(edge_list)):
        draw_pattern_ger(algorithm, [p['edges'] for p in edge_list.values()][i],
                                 w = w_box/2, where_ax = ax[i//columns, i%columns])
        ax[i//columns, i%columns].axis('off')
        
    for over in range(howmany%columns, columns):
        ax[rows-1,over].axis('off')

    
def draw_rule(algorithm , edgelist, w_box ):
    
    fig,ax = plt.subplots(1, 5, figsize = (5*w_box, w_box))
    for x in range(5):ax[x].axis('off')
    
    ts = set([x[-1] for x in edgelist])
    edge_list_color = [tuple(list(edge)[:2]+[select_head(edge[-1], ts)]) for edge in edgelist]
    
    precondition = [edge for edge in edge_list_color if edge[-1] == 0]
    
    
    if algorithm in ['evomine','EvoMine','EVOMINE','Evomine']:
        post_G = to_diG(edge_list_color)
        pre_G = to_diG(precondition)
        pre_G.add_nodes_from(post_G.nodes())
    elif algorithm in ['germ','Germ','GERM']:
        post_G = to_G(edge_list_color)
        pre_G = to_G(precondition)
        pre_G.add_nodes_from(post_G.nodes())
        
    pos = nx.circular_layout(post_G)
    draw_pattern_ger(algorithm, pre_G, w = w_box/2, pos_node=pos, where_ax = ax[1])
    
    arrow = plt.imread("./arrow-white.png")
    ax[2].imshow(arrow)
    
    draw_pattern_ger(algorithm, post_G, w = w_box/2, pos_node=pos, where_ax = ax[3])
    
    