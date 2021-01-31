from qiskit import Aer
from qiskit_ionq_provider import IonQProvider 
import networkx as nx
import numpy as np

class Graph():
    # m: Number of rows, n: number of columns
    def __init__(self, m, n,periodic):
        #self.G=nx.grid_graph(dim=[m,n], periodic=False)
        self.G=nx.grid_2d_graph(m,n,periodic=True)
        self.adj_lst = nx.to_dict_of_dicts(self.G)
        self.xmax = m
        self.ymax = n
        self.periodic = periodic
        self.deg_of_freedom = 4
        self.vertex_coin = {}
        
    def draw_graph(self):    
        nx.draw(self.G)
        
    #returns neighbors of node v
    def get_neighbors(self,v):
        return [key for key in self.adj_lst[v]]

    # Finds the degree of freedom for outgoing edge from v to u
    def find_deg_of_freedom(self,v,u):
        neighbors = self.get_neighbors(v)
        if u in neighbors:
            return neighbors.index(u)
        else:
            return -1
    # Returns number of ndoes and edges in a graph
    def find_no_of_nodes_and_edges(self):
        return self.G.number_of_nodes(), self.G.number_of_edges()
    
    def get_adjacency_list(self):
        return self.adj_lst
    
    def get_bit_lims(self):
        return [int(x) for x in np.ceil(np.log2([self.xmax, self.ymax,self.deg_of_freedom]))]
    
    def find_bit_rep_vertex(self, v):
        x_id,y_id = v
        bin_max = self.get_bit_lims()
        # x_bin = [int(x) for x in list(format(x_id, '0'+str(bin_max[0])+'b'))]      
        # y_bin = [int(y) for y in list(format(y_id, '0'+str(bin_max[1])+'b'))] 

        x_bin = format(x_id, '0'+str(bin_max[0])+'b')
        y_bin = format(y_id, '0'+str(bin_max[1])+'b')


        return x_bin + y_bin
                                                      
        
    def find_bit_rep_edge(self, v, u):
        x_id,y_id = v
        c = self.find_deg_of_freedom(v,u)
        bin_max = self.get_bit_lims()
        bin_rep = []
        bin_vertex = self.find_bit_rep_vertex(v)
        deg_of_fdm_bin = [int(d) for d in list(format(c, '0'+str(bin_max[2])+'b'))] 
        
        return bin_vertex + deg_of_fdm_bin
    

    def add_coin(self, u, coin):
        self.vertex_coin[self.find_bit_rep_vertex] = coin
