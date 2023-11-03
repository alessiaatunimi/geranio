import pickle
import networkx as nx
import pandas as pd
from collections import defaultdict


def pretty_now():
    from datetime import datetime
    ts = datetime.now()
    return f"{ts.hour}:{ts.minute}:{ts.second}.{ts.microsecond}"

def get_commonpattern_id(p, mapping):
    import networkx.algorithms.isomorphism as iso
    em = iso.numerical_edge_match("ts", 0)
    isom = [code for code, nxG in mapping.items() if nx.is_isomorphic(p, nxG, edge_match = em)]
    if len(isom) == 0: return 'new'
    return isom[0]

def has_isomorphisms_in_list(p, graphlist):
    import networkx.algorithms.isomorphism as iso
    em = iso.numerical_edge_match("ts", 0)
    isom = [nx.is_isomorphic(p, nxG, edge_match = em) for nxG in graphlist]
    if any(isom): return True
    return False

def get_if_present(k, d):
    if k in d.keys(): return d[k]
    else: return 0

def mapping_pattern_ids(algo,patterns, support, general_mapping, mapped_patterns_path, directed = False):
    new_patterns = defaultdict(dict)
    new_support = defaultdict(dict)
 
    if len(general_mapping) == 0:
        
        new_support = support
        for p,edges in patterns.items():
            
            new_patterns[p]['old-ids'] = p
            new_patterns[p]['edges'] = edges
            
            if directed: 
                general_mapping[p] = nx.DiGraph([(e[0],e[1],{'ts':e[2]}) for e in list(edges)])
            else: 
                general_mapping[p] = nx.Graph([(e[0],e[1],{'ts':e[2]}) for e in [list(x) for x in edges]])
        
    else:
        i = max(general_mapping.keys())
        for p,edges in patterns.items():
            edges = list(edges)
            temp_nx =  nx.Graph([(e[0],e[1],{'ts':e[2]}) for e in edges])
            code = get_commonpattern_id(temp_nx, general_mapping)
            if code == 'new': 
                code = i
                general_mapping[i] = temp_nx
                i = i+1

            new_patterns[code]['edges'] = edges
            new_patterns[code]['old-ids'] = p

            new_support[code] = support[p]
        
    pickle.dump(new_patterns, open(mapped_patterns_path+"_patterns.p",'wb'))
    pickle.dump(new_support, open(mapped_patterns_path+"_supports.p",'wb'))
    pickle.dump(general_mapping, open(algo.lower()+'_general_mapping.p','wb'))
    return new_patterns,new_support