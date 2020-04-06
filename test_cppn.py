# from voxelyze.mutation.CPPNMutation import CPPNMutation

# cppn = CPPNMutation(2,2)
# p = cppn.population
# print(p)

from voxelyze.mutation.cppn.CPPNMutation import CPPNMutation

m = CPPNMutation(body_dimension=[6,6,6],population_size=2)
m.init_geno()
m.express()
print(m.population)
# run simulation
# read report
sorted_result = {"id":[0], "fitness":[10]}
m.next_generation(sorted_result)
print(m.population)

m.next_generation(sorted_result)
m.next_generation(sorted_result)
m.next_generation(sorted_result)
m.next_generation(sorted_result)
m.next_generation(sorted_result)
m.next_generation(sorted_result)
m.next_generation(sorted_result)

# print("")
# m.population["genotype"][0]["CPPN"].draw()

