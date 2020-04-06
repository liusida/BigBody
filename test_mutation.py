from voxelyze.mutation.Mutation import Mutation

m = Mutation(body_dimension=[3,2,2],population_size=2)
m.init_geno()
m.express()
print(m.population)

# run simulation
# read report
sorted_result = {"id":[0,1], "fitness":[10,9]}
m.next_generation(sorted_result)

print(m.population)