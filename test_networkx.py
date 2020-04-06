import networkx as nx
from voxelyze.mutation.cppn.CPPNMutation import CPPN

g = CPPN()
g.graph.add_edge(1,2,weight=1)

b = g.clone()
b.graph.add_edge(2,3,weight=2)

print(g.graph.nodes)
print(b.graph.nodes)