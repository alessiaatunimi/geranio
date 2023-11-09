import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from datetime import *
import random
import os
flatten = lambda l: [item for sublist in l for item in sublist]

############################################################ INPUT ##########################################################


def mapping_nodes(edges_list,vertices_list):
    
    '''
    it changes the id of vertixes in order to not have any missing value

    INPUT:
    edges_list = edge list where each edge is expressed in the following format: (source, destination, timestamp)
    vertices_list = node list 

    OUTPUT:

    edges_list = edge list mapped with incremental node indexes
    vertices_list = node list mapped with incremental node indexes

    '''
    vertices = {node:i for i,node in enumerate(vertices_list)} 
    vertices_list = [vertices[node] for node in vertices_list]
    edges_list = [(vertices[s],vertices[d],t) for s,d,t in edges_list]
    
    return edges_list,vertices_list 

def from_stringlist_to_edgelist(edges, separator = ','): 
    '''
    It is the first step to obtain a file readable for ger algorithm

    INPUT:
    edges = must be a list of strings of this format: source{separator}destination{separator}timestamp
            where the timestamp is an incremental integer, not datetime or any other python format for date
            if separator = '0', then each elemet of the list would be like "source, destination, timestamp\n"
    separator = the character between elements 

    OUTPUT:
    e = edge list mapped through mapping_nodes function
    v = node list mapped through mapping_nodes function

    '''
    
    edges_list=[edge.strip('\n').split(separator,3) for edge in edges]
    edges_list.sort(key = lambda x:x[2])
    vertices_list = [el[:2] for el in edges_list]
    vertices_list = list(set(flatten(vertices_list)))
    vertices_list.sort(key = lambda s: int(s))
    e,v = mapping_nodes(edges_list,vertices_list)
    return e,v
    '''
    return the lists of edges and vertices
    '''
    

def from_edgelists_to_gerinput(dataset_path,edges_list,vertices_list):
    '''
    it is the second step to obtain a file readable for germ, subsequent to from_stringlist_to_edgelist

    INPUT:
    dataset_path = path where to write the output file, that will be the input for the ger algorithm. Preferably use the input-file/ forlder
    edges_list = mapped edge list obtained through from_stringlist_to_edgelist
    vertices_list = mapped node list obtained through from_stringlist_to_edgelist

    NO OUTPUT, the function write the file
    '''
    
    nodes_to_write = [f"v {n} 0\n" for n in vertices_list]
    edges_to_write = [f"e {a} {b} {t}\n" for a,b,t in edges_list]
    if os.path.isfile(dataset_path):
        os.system(f'rm {dataset_path}') #otherwise it keeps adding lines everytime the function is run! 
        print(f'removed {dataset_path}')
    with open(dataset_path, 'a+') as f:
        f.write('t # 0\n')
        for line in nodes_to_write:
            f.write(line)
        for line in edges_to_write:
            f.write(line)
    f.close()
    print("Edge list converted, ger format file saved in ", dataset_path)
    
    

def from_txtfile_to_gerinput(input_path, output_path, separator = ','):
    '''
    Overall function to obtain a file readable for ger algorithm

    INPUT:
    input_path = path where the raw edge list is contained. 
            The input list must be a list of strings of this format: source{separator}destination{separator}timestamp
            where the timestamp is an incremental integer, not datetime or any other python format for date
            if separator = '0', then each elemet of the list would be like "source, destination, timestamp\n"

    output_path = path where to write the file readable from the ger algorithm
    separator = the character between elements 

    NO OUTPUT
    
    '''
    edges = list(open(input_path, 'r'))
    e,v = from_stringlist_to_edgelist(edges, separator)
    from_edgelists_to_gerinput(output_path,e,v)
    
    

############################################################ OUTPUT ##########################################################
    

def from_ger_output(filename): 
'''
    Overall function to obtain a dictionary of rules from ger algorithm output

    INPUT:
    filename = path where output of the ger algorithm is saved

    OUTPUT:
    info_list = list of string per pattern (clean version of the file)
    patterns= dictionary of patterns, each pattern has this format --> patternid : {support: s, nodes : [a,b,c], edges: [(a,b,ts)]} 
    support_patterns = [filtered version of patterns] dictionary that map each pattern index to its support --> {patternid: support}
    mapping = dictionary that map the id of a pattern in patterns to the id in file or in info_list
    '''
    
    super_string = ''
    file = list(open(filename,'r'))
    for i in range(len(file)):
        super_string += file[i]
    info_list = super_string.split('t')[1:]
    info_list = [s[3:].replace('\n', '') for s in info_list]
    info_list = [s.replace('v', ' nodes ',1) for s in info_list]#
    info_list = [s.replace('e ', ' edges ',1) for s in info_list]
    info_list = [s.replace('v ', ' ') for s in info_list]
    info_list = [s.replace('e ', ' ') for s in info_list]
    info_list.sort(key = lambda s: int(s.split(" ")[1]), reverse = True)
    support_patterns = {}
    patterns = {}
    mapping = {}
    for i,line in enumerate(info_list):
        splitted = line.split(' ')
        pattern_id, support = splitted[0], splitted[1]
        support_patterns[i] = support
        mapping[i] = pattern_id
        nodes_id, edges_id = splitted.index('nodes'), splitted.index('edges')
        nodes_list = [int(x) for x in splitted[nodes_id+2 : edges_id]][::2]
        edges_list = [int(x) for x in splitted[edges_id+1:]]
        patterns[i] = {'support':support,
                       'nodes':nodes_list, 
                       'edges':[edges_list[k:k+3] for k in range(0, len(edges_list), 3)]}
        patterns[i]['edges'] = [tuple(sub) for sub in patterns[i]['edges'] ]
    return info_list, patterns, support_patterns, mapping
   
    
def obtain_pattern_list(patterns,support, algorithm):
    '''
   Fuction to obtain shorter versions of the patterns dictionary obtained thorugh the from_ger_output function

    INPUT:
    patterns = patterns dictionary from the from_ger_output function
    support = support dfictionary from the from_ger_output function
    algorithm = ger algorithm choose between GERM: ['germ','Germ','GERM'] or EvoMine: ['evomine','EvoMine','EVOMINE','Evomine']

    OUTPUT:
    pattern_list = dictionary of the form {ruleid: (edges 3-tuples)}
    support'''
    pattern_list = [patterns[i]['edges'] for i in patterns.keys()]
    if algorithm in ['evomine', 'EvoMine','Evomine']: 
        mapping_ts = {3:0, 1:1}
        pattern_list = {i:tuple([(e[0],e[1],mapping_ts[e[2]]) for e in e_l]) for i,e_l in enumerate(pattern_list)}
    else: 
        pattern_list = {i:tuple(e_l) for i,e_l in enumerate(pattern_list)}
    support = {i:int(s) for i,s in support.items()}
    return pattern_list, support