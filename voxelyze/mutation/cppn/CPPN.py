import copy, math, random
import numpy as np
import networkx as nx
from .CPPNActivationFunctions import *

class CPPN:
    input_node_names = ['x', 'y', 'z', 'd', 'b']
    output_node_names = ['body', 'phaseoffset']
    hidden_node_names = []
    activation_functions = [np.sin, np.abs, neg_abs, np.square, neg_square, sqrt_abs, neg_sqrt_abs]
    def __init__(self, hidden_layers=[10,10,10]):
        # There are many differences between networkx 1.x and 2.x, we'll use 2.x
        assert float(nx.__version__)>2.0
        self.hidden_layers = hidden_layers
        self.init_graph()
        self.last_node_index = 0
        self.random = random.random()

    def clone(self):
        ret = copy.copy(self)
        ret.graph = self.graph.copy()
        return ret

    def __str__(self):
        return "Not implemented."

    def init_graph(self):
        """Create a simple graph with each input attached to each output"""
        self.graph = nx.DiGraph()

        nodes_this_layer = []
        for name in self.input_node_names:
            self.graph.add_node(name, type="input", function=None)
            nodes_this_layer.append(name)

        for layer_id, layer in enumerate(self.hidden_layers):
            nodes_last_layer = nodes_this_layer
            nodes_this_layer = []
            for node in range(layer):
                name = f"hidden_{layer_id}_{node}"
                self.graph.add_node(name, type="hidden", function=random.choice(self.activation_functions))
                for last in nodes_last_layer:
                    self.graph.add_edge(last, name, weight=random.random())
                nodes_this_layer.append(name)
                self.hidden_node_names.append(name)

        nodes_last_layer = nodes_this_layer
        nodes_this_layer = []
        for name in self.output_node_names:
            self.graph.add_node(name, type="output", function=sigmoid)
            for last in nodes_last_layer:
                self.graph.add_edge(last, name, weight=random.random())
            nodes_this_layer.append(name)

    def _compute_value(self, node, input_data):
        if self.graph.nodes[node]["evaluated"]:
            return self.graph.nodes[node]["value"]
        if node in input_data:
            return input_data[node]
        predecessors = self.graph.predecessors(node)
        value = 0.0
        for predecessor in predecessors:
            edge = self.graph.get_edge_data(predecessor, node)
            value += self._compute_value(predecessor,input_data) * edge["weight"]
        if self.graph.nodes[node]["function"] is not None:
            value = self.graph.nodes[node]["function"](value)
        self.graph.nodes[node]["value"] = value
        self.graph.nodes[node]["evaluated"] = True
        return value

    def compute(self, input_data):
        """ return a dictionary, key is the output nodes, value is the output value """
        # for node in self.output_node_names:
        for node in self.graph.nodes:
            self.graph.nodes[node]["evaluated"] = False
        ret = {}
        for node in self.output_node_names:
            ret[node] = self._compute_value(node, input_data)
        return ret

    def draw(self):
        import matplotlib.pyplot as plt
        nx.draw_networkx(self.graph, pos=nx.drawing.nx_pydot.graphviz_layout(self.graph, prog='dot'))
        edge_labels_1 = nx.get_edge_attributes(self.graph,'weight')
        for key in edge_labels_1:
            edge_labels_1[key] = round(edge_labels_1[key],2)
        nx.draw_networkx_edge_labels(self.graph, pos=nx.drawing.nx_pydot.graphviz_layout(self.graph, prog='dot'), edge_labels=edge_labels_1, rotate=False)
        plt.show()

    def mutate(self, num_random_activation_functions=100, num_random_weight_changes=100):
        total = num_random_activation_functions + num_random_weight_changes
        # choose a mutation according to probability
        while True:
            fn = np.random.choice( [
                self.change_activation,
                self.change_weight,
                ], size=1, p=[
                    num_random_activation_functions / total,
                    num_random_weight_changes   / total,
                    ] )
            # print(fn[0])
            success = fn[0]()
            if success:
                break
            print("Retry.")

    def change_activation(self):
        if len(self.hidden_node_names)==0:
            return False
        node = random.choice(self.hidden_node_names)
        # print(node)
        # print(self.graph.nodes)
        success = False
        for i in range(10):
            activation = random.choice(self.activation_functions)
            if self.graph.nodes[node]["function"] != activation:
                self.graph.nodes[node]["function"]=activation
                success = True
                break
        return success

    def change_weight(self, mutation_std=0.5):
        edge = random.choice(list(self.graph.edges))
        np.random.normal(loc=self.graph.edges[edge[0], edge[1]]["weight"], scale=mutation_std)
        return True

    def get_output(self,body_dimension):
        body = np.zeros(body_dimension)
        phaseoffset = np.zeros(body_dimension)
        input_x = np.zeros(body_dimension)
        input_y = np.zeros(body_dimension)
        input_z = np.zeros(body_dimension)

        for i in range(body_dimension[0]):
            x = i*2/body_dimension[0] - 1
            for j in range(body_dimension[1]):
                y = j*2/body_dimension[1] - 1
                for k in range(body_dimension[2]):
                    z = k*2/body_dimension[2] - 1
                    input_x[i,j,k] = x
                    input_y[i,j,k] = y
                    input_z[i,j,k] = z

        input_d = np.sqrt(np.power(input_x,2) + np.power(input_y,2)  + np.power(input_z,2) )
        ret = self.compute({'x':input_x,'y':input_y,'z':input_z,'d':input_d,'b':1})
        body = ret["body"]
        phaseoffset = ret["phaseoffset"]
        return body, phaseoffset
