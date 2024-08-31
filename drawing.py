#imports
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
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

            
    
def draw_several_patterns(algorithm, edge_lists,
                          columns = 5, w_box = 4):
    howmany = len(edge_lists)
    rows = howmany//columns + (howmany%columns +(columns-1))//columns
    
    fig,ax = plt.subplots(rows, columns, figsize = (columns*w_box, rows*w_box))
    
    for i in range(len(edge_lists)):
        draw_pattern_ger(algorithm, edge_lists[i],
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
    
    arrow = plt.imread("./imgs/arrow-white.png")
    ax[2].imshow(arrow)
    
    draw_pattern_ger(algorithm, post_G, w = w_box/2, pos_node=pos, where_ax = ax[3])
    
    
    
def draw_subgraph(G,  pos=False, figsize = False, temporal = False,where_ax = False, 
                  labels_nodes = True):
    if not figsize : figsize = (2,2)
    plt.figure(figsize = figsize)
    if not pos: pos = nx.circular_layout(G)
    if where_ax == False:
        nx.draw(G, 
                pos, 
                with_labels = labels_nodes,
               node_color= 'navy',
               edge_color = 'lightgray',
               font_color = 'white',
                width = 3,
                arrowsize = 25
                
                #connectionstyle = 'arc3, rad = 0.1'
               )
        if temporal:
            nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels={(edge[0],edge[1]):edge[2]['ts'] for edge in G.edges(data = True)},
            label_pos=0.27,# label of the edge close to the arrow (destination node)
            font_color='navy',font_size = 12

            )
    else:
        nx.draw(G, 
                pos, 
                with_labels = True,
               node_color= 'navy',
               edge_color = 'lightgray',
               font_color = 'white',
                width = 3,
                arrowsize = 25,
                ax = where_ax
                #connectionstyle = 'arc3, rad = 0.1'
               )
        if temporal:
            nx.draw_networkx_edge_labels(
                G, pos,
                edge_labels={(edge[0],edge[1]):edge[2]['ts'] for edge in G.edges(data = True)},
                label_pos=0.27,# label of the edge close to the arrow (destination node)
                font_color='navy',font_size = 12,ax = where_ax

            )

######### DRAWING FROM CANONICAL ######
def from_int_to_temporaledges(input_cod, nodes):
    if type(input_cod) == int: input_cod = bin(input_cod)[3:]
    n = int(np.sqrt(len(input_cod)))
    matrix = [[int(x) for x in input_cod[n*i:n*(i+1)]] for i in range(n)]
    edges = [(i,j) for i, row in enumerate(matrix) for j,column in enumerate(row) if column ==1]
    
    temporal_edges = set([(u%nodes,v%nodes, u//nodes) for (u,v) in edges if u%nodes!=v%nodes])
    #nx.DiGraph([(0,1),(1,0)])
    return temporal_edges
def draw_subgraph(G, ns, temporal = False, labels_nodes = True, size = (5,5), where_ax = False):
    plt.figure(figsize = size)
    pos = nx.circular_layout(G)
    if G.size()>6: pos = nx.spring_layout(G)
    

    if not where_ax: 
        nx.draw(G, 
            pos, 
            with_labels = labels_nodes,
           node_color= 'navy',
           edge_color = 'lightgray',
           font_color = 'white',
            width = 1,
            arrows = True,
            arrowsize = 25,
            node_size = ns
    
            #connectionstyle = 'arc3, rad = 0.1'
           )
        if temporal:
            nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels={(edge[0],edge[1]):edge[2]['ts'] for edge in G.edges(data = True)},
            label_pos=0.27,# label of the edge close to the arrow (destination node)
            font_color='navy',font_size = 12

            )
    else:
        nx.draw(G, 
            pos, 
            with_labels = labels_nodes,
           node_color= 'navy',
           edge_color = 'lightgray',
           font_color = 'white',
            width = 1,
            arrows = True,
            arrowsize = 25,
            node_size = ns,
            ax=where_ax
            #connectionstyle = 'arc3, rad = 0.1'
           )
        if temporal:
            nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels={(edge[0],edge[1]):edge[2]['ts'] for edge in G.edges(data = True)},
            label_pos=0.27,# label of the edge close to the arrow (destination node)
            font_color='navy',font_size = 12,ax=where_ax

            )


def draw_pattern_from_int(input_cod, mapping_starting, ns=400, w = 2, h=2, where_ax=False):
    code, nodes = mapping_starting[input_cod]
    edges = from_int_to_temporaledges(code, nodes)
    g = nx.DiGraph()
    for (u,v,t) in edges: g.add_edge(u,v, ts = t)
    draw_subgraph(g, temporal=True, labels_nodes=False,  ns = ns, size = (w,h), where_ax=where_ax)
    
