#!/lusr/bin/python
'''
Created on Jun 3, 2011

@author: smirarab
'''
import dendropy
import sys
import os
import copy
import os.path

if __name__ == '__main__':

    treeName = sys.argv[1]
    sample = open(sys.argv[2])
    included = [s[:-1] for s in sample.readlines()]
    resultsFile="%s.%s" % (treeName, os.path.basename(sample.name))
    trees = dendropy.TreeList.get_from_path(treeName, 'newick',rooted=True)
    filt = lambda node: True if (node.taxon is not None and node.taxon.label not in included) else False
    for tree in trees:
        nodes = tree.get_node_set(filt)
        tree.prune_taxa([n.taxon for n in nodes])
        tree.deroot()
        #tree.reroot_at_midpoint(update_splits=False)
    print "writing results to " + resultsFile        
    trees.write(open(resultsFile,'w'),'newick',write_rooting=False)
