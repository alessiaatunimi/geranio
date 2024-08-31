from collections import defaultdict
from igraph import Graph 
from io import StringIO
import itertools as it
import numpy as np
import subprocess
import networkx as nx
from multiprocessing import Pool
import time
from datetime import datetime,timedelta
from tqdm.auto import tqdm
from scipy.sparse import csr_matrix
import os
import pickle




flatten = lambda l: [item for sublist in l for item in sublist]
def pretty_now():
    from datetime import datetime
    ts = datetime.now()
    return f"{ts.hour}:{ts.minute}:{ts.second}.{ts.microsecond}"


def to_layered_edges(edges):
    max_layer = max(int(ts) for _,_,ts in edges)+1
    # layers from 0 to max_layer
    layered_edges = []
    nodes = set(flatten([x[:2] for x in edges]))
    n_nodes = len(nodes)
    node_to_int = { n:i for i, n in enumerate(sorted(nodes))}
    
    for n in nodes:
        for l in range(max_layer-1):
            layered_edges.append((node_to_int[n]+ (n_nodes*l), node_to_int[n]+ (n_nodes*(l+1))))
        
    # intra-layer edges (the actual triangle edges) 
    for u,v,t in edges:
        layered_edges.append((node_to_int[u]+ (n_nodes*t),node_to_int[v]+ (n_nodes*t)))
    return (layered_edges, n_nodes)
   
def get_adj_string_spaced(edges):
    order = len(set(flatten(edges)))
    r = np.zeros((order,order))
    for row,col in edges:
        r[row][col] = 1
    return '\n'.join([" ".join([str(int(i)) for i in row]) for row in r])


def get_canonical_code_fromedges(edges, n_nodes):
    matrix_string_spaced = get_adj_string_spaced(edges)
    matrix_string = matrix_string_spaced.replace('\n','').replace(' ','')
    original_graph = Graph.Read_Adjacency(StringIO(matrix_string_spaced))
    permutation = original_graph.canonical_permutation()
    canonical_graph = original_graph.permute_vertices(permutation)
    adj_string = ''.join([str(i) for i in list(it.chain.from_iterable(canonical_graph.get_adjacency()))])
    return (int('1'+adj_string, 2),int('1'+matrix_string, 2), n_nodes)



def mapping_pattern_ids(patterns, support, mapped_patterns_path, 
                        general_mapping_name = 'general_mapping_canonical.p',
                        general_mapping_updatename = 'general_mapping_canonical', 
                        check_meaningfull = False,
                       save_mapped = True):
    
    if not os.path.isfile(general_mapping_name):
        pickle.dump({},open(general_mapping_name,'wb') )
    
    general_mapping = pickle.load(open(general_mapping_name,'rb') )


    new_patterns = defaultdict(dict)
    new_support = {}
    
    for p,edges in patterns.items():
        if check_meaningfull: 
            ts = set([x[2] for x in edges])
            if len(ts) >1: 
                e_layered, n_nodes = to_layered_edges(edges)
                labels_evolution = get_canonical_code_fromedges(e_layered, n_nodes)
                new_patterns[labels_evolution[0]]['info'] = labels_evolution[1:]
                new_patterns[labels_evolution[0]]['edges'] = edges
                new_support[labels_evolution[0]] = support[p]

        else:
            ts = set([x[2] for x in edges])
            if len(ts) >1: 
                e_layered, n_nodes = to_layered_edges(edges)
                labels_evolution = get_canonical_code_fromedges(e_layered, n_nodes)
                new_patterns[labels_evolution[0]]['info'] = labels_evolution[1:]
                new_patterns[labels_evolution[0]]['edges'] = edges
                new_support[labels_evolution[0]] = support[p]
    #general mapping short id
    if len(general_mapping) == 0: 
        general_mapping = {canonical: (i,info)  for i,(canonical,info) in enumerate(new_patterns.items())} 
    else:
        for canonical,info in new_patterns.items():
            if canonical not in general_mapping.keys():
                next_i = len(general_mapping)
                general_mapping[canonical] = (next_i, info)
    pickle.dump(general_mapping,open(general_mapping_updatename,'wb') )
    
    new_patterns = {general_mapping[k][0]: {'canonical':k, 'info':v['info'],'edges':v['edges']} for k,v in new_patterns.items()}
    new_support = {general_mapping[k][0]: s for k,s in new_support.items()}
    if save_mapped:
        pickle.dump(new_patterns, open(mapped_patterns_path+"_short_canonical_patterns.p",'wb'))
        pickle.dump(new_support, open(mapped_patterns_path+"_short_canonical_supports.p",'wb'))
    
    return new_patterns,new_support




