# coding: utf-8

from dgl import DGLGraph
import numpy as np
import re

class Graphtools(object):

    def __init__(self):
        pass
    
    def fromText(self, fileName):
        '''
        The text file should be of the following format:
        [several rows of description here]
        [The first valid line should give nodes number and edges number: e.g. 'N180 E1999']
        [Rows of data, with each row being '{fromID} {toID}']

        And this function will return a graph generated by the given information.
        '''

        with open(fileName, 'r') as f:
            notStarted=True
            while notStarted:
                retr=f.readline()
                if retr=='':
                    return None
                
                match=re.search(r'N(\d+)\s+E(\d+)', retr)
                if match:
                    # Number of nodes and edges
                    self.size=[int(i) for i in match.groups()]
                    break
            # retrieve edges
            tmpData=f.readlines()
            pat=re.compile(r'(\d+)\s+(\d+)')

            Fromlist, Tolist=np.empty(self.size[1], dtype=np.int64), np.empty(self.size[1], dtype=np.int64)
            for i in range(len(tmpData)):
                match=pat.search(tmpData[i])
                Fromlist[i], Tolist[i]=[int(j) for j in match.groups()]

            G=DGLGraph()
            G.add_nodes(self.size[0])
            G.add_edges(Fromlist, Tolist)

            return G

if __name__=='__main__':
    gtools=Graphtools()
    G=gtools.fromText('p2p-Gnutella08.txt')
    print(G)
    nodes=G.nodes().numpy()
    print(len(G.nodes))  