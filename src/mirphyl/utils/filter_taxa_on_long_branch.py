#!/usr/bin/env python
'''
Created on Jun 3, 2011

@author: smirarab
'''
import dendropy
import sys
LIMIT = 10

def meanstdv(x):
    from math import sqrt
    n, mean, std = len(x), 0, 0
    for a in x:
        mean = mean + a
    mean = mean / float(n)
    for a in x:
        std = std + (a - mean)**2
    std = sqrt(std / float(n-1))
    return mean, std

if __name__ == '__main__':

    treeName = sys.argv[1]
    
    #cmd = 'find %s -name "%s" -print' % (treeDir,treeName)
    #print cmd
    #for file in os.popen(cmd).readlines():     # run find command        
    #    name = file[:-1]                       # strip '\n'                
    #    fragmentsFile=name.replace(treeName,"sequence_data/short.alignment");
    resultsFile="%s.%dfold.longbranch.removed" % (treeName,LIMIT)
            
    trees = dendropy.TreeList.get_from_path(treeName, 'newick')    
    for tree in trees:
        N = len(tree.taxon_set)
        print "%s" %treeName,
        elen = {}
        for edge in tree.postorder_edge_iter():
            elen[edge] = edge.length
        
        elensort = sorted([float(x) for x in elen.values() if x is not None])
        n = len(elensort)
        mid = elensort[n/2]
        hm_avg  = n / sum([ 1/x for x in elensort])
        
        '''
        The Standard Errors of the Geometric and Harmonic Means and Their Application to Index Numbers
            Nilan Norris
            The Annals of Mathematical Statistics 
            Vol. 11, No. 4 (Dec., 1940), pp. 445-448
            Published by: Institute of Mathematical Statistics
            Stable URL: http://www.jstor.org/stable/2235723
        '''
        from math import sqrt
        sdhm =   sqrt(sum([ pow(1./x - 1./hm_avg,2) for x in elensort]))*pow(hm_avg,2) / sqrt(n-1)         
        
        #print hm_avg, sehm
        # Find long edges
        l = mid * LIMIT
        torem=[]
        for k,v in elen.items():
            if v > l:
                if len(k.head_node.leaf_nodes()) < N/2:
                    r = [n.taxon for n in k.head_node.leaf_nodes()]
                else:
                    r = [n.taxon for n in tree.leaf_nodes() if n not in k.head_node.leaf_nodes()]                    
                torem.append(r)

        torem2=[]
        for r in torem: 
            nl = set(r)
            skipthis = False
            for o in torem2:
                #print set(o.leaf_nodes()), nl, set(o.leaf_nodes()).issuperset(nl)
                if set(o).issuperset(nl):
                    skipthis = True
            if not skipthis:
                if len(r) == 1:
                    torem2.append(r)
                    print [n.label for n in r],
                
        for r in torem2:     
            #print [x.taxon.label for x in n.leaf_nodes()], tree.seed_node, n            
            tree.prune_taxa(r)
        #nodes = tree.get_node_set(filter)
        #tree.prune_taxa([n.taxon for n in nodes])
        #tree.deroot()
        #tree.reroot_at_midpoint(update_splits=False)
        
    trees.write(open(resultsFile,'w'),'newick',write_rooting=False)
