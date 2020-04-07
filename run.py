# This file contains high level logic.

# psuedocode of this file
#
# if last generation of population exist
#   read them in
# else
#   randomly generate a population
# send the population to simulation
# read the output report
# select high fitness population
# use report to train a model
# use the model to mutate high fitness population
# write the next generation of population with high fitnesses and mutants

import voxelyze as vx
from voxelyze.mutation.cppn.CPPNMutation import CPPNMutation
import numpy as np
import shutil
import random
random.seed(1)
np.random.seed(1)
experiment_name = "v040619"
population_size = 128
generation = 0
body_dimension = (5, 5, 5)

vx.clear_workspace()
mutation = CPPNMutation(body_dimension, population_size)

# try to resume from last experiment
mutation_dic = vx.load_last_generation(experiment_name)
# if failed, start from scratch
if mutation_dic is None:
    generation = 0
    mutation.init_geno(hidden_layers=[5,5])
    mutation.express()
else:
    mutation.load_dic(mutation_dic)

# infinity evolutionary loop
while(True):
    # write vxa vxd
    foldername = vx.prepare_directories(experiment_name, generation)
    vx.copy_vxa(experiment_name, generation)
    vx.write_all_vxd(experiment_name, generation, mutation.dump_dic())


    # start simulator
    print("simulating...")
    vx.start_simulator(experiment_name, generation)
    # record a brief history for the bestfit
    print("recording...")
    vx.record_bestfit_history(experiment_name, generation, stopsec=2)

    # read reporter
    sorted_result = vx.read_report(experiment_name, generation)


    # report the fitness
    msg = f"Simulation for generation {generation} finished.\nThe top 3 bestfit fitness score of this generation are \n"
    for i in range(3):
        if i<len(sorted_result['id']):
            robot_id = sorted_result['id'][i]
            msg += f"{mutation.population['genotype'][robot_id]['firstname']} {mutation.population['genotype'][robot_id]['lastname']}'s fitness score: {sorted_result['fitness'][i]:.1e} \n"
    print(msg, flush=True)

    if generation%3==0:
        import sida.slackbot.bot as bot
        bot.send(msg, 1, "GUB0XS56E")

    # next generation
    generation += 1
    next_generation = mutation.next_generation(sorted_result)
