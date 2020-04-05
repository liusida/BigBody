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
import numpy as np
import shutil
import random
random.seed(1)
np.random.seed(1)
experiment_name = "v040501"
population_size = 60
generation = 0
body_dimension = (10, 10, 10)

vx.clear_workspace()
mutation = vx.mutation.RandomNetMutation(body_dimension)

# try to resume from last experiment
population, generation = vx.load_last_generation(experiment_name)
# if failed, start from scratch
if population is None:
    generation = 0
    population = mutation.get_population()
    mutation.init_geno(population, population_size)
    mutation.expression(population)
# infinity evolutionary loop
while(True):
    # write vxa vxd
    foldername = vx.prepare_directories(experiment_name, generation)
    vx.copy_vxa(experiment_name, generation)
    vx.write_all_vxd(experiment_name, generation, population)


    # start simulator
    print("simulating...")
    vx.start_simulator(experiment_name, generation)
    # record a brief history for the bestfit
    print("recording...")
    vx.record_bestfit_history(experiment_name, generation, stopsec=2)

    # read reporter
    sorted_result = vx.read_report(experiment_name, generation)

    next_generation = mutation.next_generation(sorted_result, population)

    # report the fitness
    msg = f"Simulation for generation {generation} finished.\nThe top 3 bestfit fitness score of this generation are \n"
    for i in range(3):
        msg += f"{population['firstname'][sorted_result['id'][i]]} {population['lastname'][sorted_result['id'][i]]}'s fitness score: {sorted_result['fitness'][i]:.1e} \n"
    print(msg, flush=True)

    if generation%100==0:
        import sida.slackbot.bot as bot
        bot.send(msg, 1, "GUB0XS56E")

    # next generation
    generation += 1
    population = next_generation
