# from voxelyze.mutation.CPPNMutation import CPPNMutation

# cppn = CPPNMutation(2,2)
# p = cppn.population
# print(p)

from voxelyze.mutation.cppn.CPPNMutation import CPPNMutation

m = CPPNMutation(body_dimension=[1,1,1],population_size=2)
m.init_geno(hidden_layers=[1])
m.express()
dic = m.dump_dic()
print(dic)