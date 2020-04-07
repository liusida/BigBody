# This is the base class for any mutation method

from .. import names as names
from ..helper import largest_component
import numpy as np
import string, random, json

"""
Usage:

```
from voxelyze.mutation.Mutation import Mutation
m = Mutation(body_dimension=3,population_size=10)
m.init_geno()
m.express()
# run simulation
# read report
sorted_result = {"id":[0,1], "fitness":[10,9]}
m.next_generation(sorted_result)
```

Public interface:
    __init__:           init
    init_geno:          create genotypes
    express:            create phenotypes based on existing genotypes
    next_generation:    step to next generation

"""

class Mutation:
    def __init__(self, body_dimension, population_size):
        """ init
        body_dimension = [6,6,5] for 6x6x5 robot
        population_size is an integer
        Define what is genotype and phenotype, etc."""
        self.body_dimension = body_dimension
        self.population_size = population_size
        self.population = {"genotype": [], "phenotype": []}
        self.init_geno()
        self.express()
        self.phenotype_keys = ["body", "phaseoffset"]
        self.genotype_keys = ["firstname", "lastname", "DNA"]
        # DNA is a 32 bytes string of digits;
        # firstname and lastname are strings;

    def init_geno(self):
        """ random init, start from scratch """
        self.population["genotype"] = []
        for robot_id in range(self.population_size):
            DNA = ''.join([random.choice(string.digits) for n in range(32)])
            self.population["genotype"].append( {
                "DNA": DNA,
                "firstname": names.get_first_name(),
                "lastname": names.get_first_name(),
            })

    def express(self):
        """ express genotype (a list of digits) to phenotype (body and phaseoffset) """
        self.population["phenotype"] = []
        for robot_id in range(self.population_size):
            # random, not depend on genotype.
            body_random = np.random.random(self.body_dimension)
            body = np.zeros_like(body_random, dtype=int)
            body[body_random < 0.5] = 1
            body = largest_component(body)
            phaseoffset = np.random.random(self.body_dimension)
            self.population["phenotype"].append( {
                "body": body,
                "phaseoffset": phaseoffset,
            })

    def next_generation(self, sorted_result):
        """ step to next generation based on the sorted result
        sorted_result is a dictionary with keys id and fitness sorted by fitness desc"""
        # select the first half
        selected_geno = []
        half = int(np.ceil(len(sorted_result["id"])/2))
        for i in sorted_result["id"][:half]:
            selected_geno.append(self.population["genotype"][i])

        # mutate first half to two mutant groups
        mutated_geno_1 = self.mutate(selected_geno)
        mutated_geno_2 = self.mutate(selected_geno)

        # combine two mutant groups into next generation
        next_generation = {}
        next_generation["genotype"] = mutated_geno_1 + mutated_geno_2
        self.population = next_generation
        self.population_size = len(next_generation["genotype"])
        self.express()

    def mutate(self, geno):
        """ Mutate a group of geno """
        mutants = []
        for i in range(len(geno)):
            mutant = {}
            for key in self.genotype_keys:
                mutant[key] = self.mutate_single_value(key, geno[i][key])
            mutant["firstname"] = names.get_first_name()
            mutant["lastname"] = geno[i]["firstname"]
            mutants.append(mutant)
        return mutants

    def mutate_single_value(self, key, value):
        if key=="DNA":
            pos = random.randint(0, len(value)-1)
            value = list(value)
            value[pos] = str((int(value[pos]) + 1) % 10)
            value = "".join(value)
            return value
        else:
            return value

    def dump_dic(self):
        """ dump a dictionary, each of which is a string for one robot """
        ret = {}
        population = {}
        for robot_id in range(self.population_size):
            robot = {"phenotype":{}, "genotype":{}}
            robot["phenotype"]["body"] = self.population["phenotype"][robot_id]["body"]
            robot["phenotype"]["phaseoffset"] = self.population["phenotype"][robot_id]["phaseoffset"]
            for key in self.genotype_keys:
                robot["genotype"][key] = str(self.population["genotype"][robot_id][key])
            population[robot_id] = robot
        ret["population"] = population
        ret["body_dimension"] = self.body_dimension
        ret["population_size"] = self.population_size
        ret["phenotype_keys"] = self.phenotype_keys
        ret["genotype_keys"] = self.genotype_keys
        return ret

    def load_dic(self, mutation_dic):
        """ load a dictionary """
        self.body_dimension = mutation_dic["body_dimension"]
        self.population_size = mutation_dic["population_size"]
        self.phenotype_keys = mutation_dic["phenotype_keys"]
        self.genotype_keys = mutation_dic["genotype_keys"]
        population = mutation_dic["population"]
        # ...
        self.population = {"genotype": [], "phenotype": []}
        for i in population:
            self.population["genotype"].append(population[i]["genotype"])
            self.population["phenotype"].append(population[i]["phenotype"])
 