import os




def run_algorithm(algo, sup, maxedge, filename, outputfile, 
                  superverbose = False, verbose = True,
                  directed = True, edge_removal = False, 
                  projection = 'full', edge_color = False, node_color = False, 
                 ):
    
    
     '''
    Runs the command of the original ger algorithm

    algo = ger algorithm choose between GERM: ['germ','Germ','GERM'] or EvoMine: ['evomine','EvoMine','EVOMINE','Evomine']
    sup = max support, for reference, in the classical dblp dataset, the support is usually set to 5000
    maxedge = maxmimum number of edge of the postcondition (head), normally set to 3 or 4
    filename = input file of the algorithm 
    outputfile = name of the output file (renaming the original output)
    superverbose = default is False, otherwise it will return the full output of the original command line (it can be long, especially for evomine)
    verbose = default is True, prints feedback for file saving and moving
    directed = default is True, it's important to specify it for the Evomine algorithm because it supports both directed and undirected graphs
    edge_removal = default is False, it's important to specify it for the Evomine algorithm 
                   because it supports also edge removal as event, not only edge insertion/creation
    projection  = type of support, choose from ['full', 'neigh','event'], 'full', 'neigh' corresponds to the MIB support while 'event' for the event support
    edge_color = default is False, it's important to specify it for the Evomine algorithm because it supports also edge-labeled graphs 
    node_color = default is False, it's important to specify it for the Evomine algorithm because it supports also node-labeled graphs      

    OUTPUT
    write the output file in outputfile path

    '''
    
    if algo in ['germ','Germ','GERM']:
        
        command = f"./algorithms/germ {sup} {filename} {maxedge} > /dev/null"
        if superverbose: command = f"./algorithms/germ {sup} {filename} {maxedge}"
        
        if verbose:
            print("Running command:")
            print(command)
        
        os.system(command)
        #germ saves output in file folder
        os.system(f'cp {filename}.out.{sup}.{maxedge}.REL ./output-files/{outputfile}')
        os.system(f'rm {filename}.out.{sup}.{maxedge}.REL ')
        
        if verbose:print(f'Output moved from {filename}.out.{sup}.{maxedge}.REL to ./output-files/{outputfile}')

        
    elif algo in ['evomine','EvoMine','EVOMINE','Evomine']:
        params = '-t'
        
        if directed: params += ' -d'
        else: params += ' -u'
        
        if edge_removal: params += ' -r'
        
        if edge_color: params += ' -c'
        if node_color: params += ' -C'
        
        command = f"./algorithms/evomine -s {sup} -e {maxedge} -T {projection} {params} -f {filename} > /dev/null"
        if superverbose: command = f"./algorithms/evomine -s {sup} -e {maxedge} -T {projection} {params} -f {filename}"
        if verbose:
            print("Running command:")
            print(command)
        os.system(command)
        #evomine saves output in notebook folder
        filename_w = filename.split('/')[-1]
        os.system(f'cp {filename_w}.out.evomine.{projection.upper()}.{sup}.{maxedge} {outputfile}')
        os.system(f'rm {filename_w}.out.evomine.{projection.upper()}.{sup}.{maxedge}')
        
        if verbose:print(f'Output moved from {filename}.out.evomine.{projection.upper()}.{sup}.{maxedge} to {outputfile}')



    