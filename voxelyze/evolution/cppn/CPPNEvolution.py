import numpy as np
from ...helper import largest_component
from ..Evolution import Evolution
from .CPPN import CPPN

class CPPNEvolution(Evolution):
    def __init__(self, body_dimension=[1,1,1], target_population_size=1, mutation_rate=[1,0]):
        """
        mutation_rate is a list: 0->weight to fn ratio, 1->weight change rate
        """
        super(CPPNEvolution, self).__init__(body_dimension, target_population_size, mutation_rate)
        self.genotype_keys.append("CPPN")

    def init_geno(self, hidden_layers=[1]):
        super(CPPNEvolution, self).init_geno()
        for g in self.population["genotype"]:
            g["CPPN"] = CPPN()
            g["CPPN"].init(hidden_layers=hidden_layers, weight_mutation_std=self.mutation_rate[1])

    def express(self):
        self.population["phenotype"] = []

        for robot_id in range(len(self.population["genotype"])):
            body_float, phaseoffset = self.population["genotype"][robot_id]["CPPN"].get_output(self.body_dimension)
            # get body integer value from float output, and zero out phaseoffset for non-voxel.
            body = np.zeros(self.body_dimension, dtype=int)
            threshold = np.quantile(body_float, 0.7) # force the body to be 70% full to avoid cube.
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
            ret.mutate(num_random_activation_functions=1, num_random_weight_changes=self.mutation_rate[0])
            return ret
        else:
            return value

    def load_dic(self, Evolution_dic):
        super(CPPNEvolution, self).load_dic(Evolution_dic)
        self.mutation_rate = Evolution_dic["mutation_rate"]
        for i in range(len(self.population["genotype"])):
            s = self.population["genotype"][i]["CPPN"]
            self.population["genotype"][i]["CPPN"] = CPPN()
            self.population["genotype"][i]["CPPN"].loads(s)
            self.population["genotype"][i]["CPPN"].weight_mutation_std = self.mutation_rate[1]
        self.express()