import os




def run_algorithm(algo, sup, maxedge, filename, outputfile, 
                  verbose = False, 
                  directed = True, edge_removal = False, 
                  projection = 'full', edge_color = False, node_color = False,
                 ):
    
    
    
    
    if algo in ['germ','Germ','GERM']:
        
        command = f"./algorithms/germ {sup} {filename} {maxedge} > /dev/null"
        if verbose: command = f"./algorithms/germ {sup} {filename} {maxedge}"
        
        print("Running command:")
        print(command)
        
        os.system(command)
        #germ saves output in file folder
        os.system(f'cp {filename}.out.{sup}.{maxedge}.REL ./output-files/{outputfile}')
        os.system(f'rm {filename}.out.{sup}.{maxedge}.REL ')
        
        print(f'Output moved from {filename}.out.{sup}.{maxedge}.REL to ./output-files/{outputfile}')

        
    elif algo in ['evomine','EvoMine','EVOMINE','Evomine']:
        params = '-t'
        
        if directed: params += ' -d'
        else: params += ' -u'
        
        if edge_removal: params += ' -r'
        
        if edge_color: params += ' -c'
        if node_color: params += ' -C'
        
        command = f"./algorithms/evomine -s {sup} -e {maxedge} -T {projection} {params} -f {filename} > /dev/null"
        if verbose: command = f"./algorithms/evomine -s {sup} -e {maxedge} -T {projection} {params} -f {filename}"
        print("Running command:")
        print(command)
        os.system(command)
        #evomine saves output in notebook folder
        filename_w = filename.split('/')[-1]
        os.system(f'cp {filename_w}.out.evomine.{projection.upper()}.{sup}.{maxedge} ./output-files/{outputfile}')
        os.system(f'rm {filename_w}.out.evomine.{projection.upper()}.{sup}.{maxedge}')
        
        print(f'Output moved from {filename}.out.evomine.{projection.upper()}.{sup}.{maxedge} to ./output-files/{outputfile}')

    