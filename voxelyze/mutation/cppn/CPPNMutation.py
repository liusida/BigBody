import numpy as np
from ...helper import largest_component
from ..Mutation import Mutation
from .CPPN import CPPN

class CPPNMutation(Mutation):
    def __init__(self, body_dimension, population_size):
        super(CPPNMutation, self).__init__(body_dimension, population_size)
        self.genotype_keys.append("CPPN")

    def init_geno(self, hidden_layers=[1]):
        super(CPPNMutation, self).init_geno()
        for g in self.population["genotype"]:
            g["CPPN"] = CPPN(hidden_layers=hidden_layers)

    def express(self):
        self.population["phenotype"] = []

        for robot_id in range(self.population_size):
            body_float, phaseoffset = self.population["genotype"][robot_id]["CPPN"].get_output(self.body_dimension)
            # get body integer value from float output, and zero out phaseoffset for non-voxel.
            body = np.zeros(self.body_dimension, dtype=int)
            threshold = np.amax(body_float) - (np.amax(body_float) - np.amin(body_float))*0.5
            body[body_float>threshold] = 1
            body = largest_component(body)
            phaseoffset[body==0] = 0.
            self.population["phenotype"].append( {
                "body": body,
                "phaseoffset": phaseoffset,
            })

    def mutate_single_value(self, key, value):
        if key=="CPPN":
            ret = value.clone()
            ret.mutate(num_random_activation_functions=1, num_random_weight_changes=5)
            return ret
        else:
            return value

    def load_dic(self, mutation_dic):
        super(CPPNMutation, self).load_dic(mutation_dic)
        for i in range(self.population_size):
            s = self.population["genotype"][i]["CPPN"]
            self.population["genotype"][i]["CPPN"] = CPPN()
            self.population["genotype"][i]["CPPN"].loads(s)