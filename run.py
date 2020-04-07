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
from voxelyze.evolution.cppn.CPPNEvolution import CPPNEvolution
import numpy as np
import shutil, random
random.seed(1)
np.random.seed(1)
generation = 0

try:
    from exp_settings import *
except:
    experiment_name = "v040704"
    population_size = 128
    body_dimension = (10, 10, 10)
    weight_mutation_std = 0.1
    hidden_layers = [10,10,10]

vx.clear_workspace()
evolution = CPPNEvolution(body_dimension, population_size)

# try to resume from last experiment
evolution_dic, generation = vx.load_last_generation(experiment_name)
# if failed, start from scratch
if evolution_dic is None:
    generation = 0
    evolution.init_geno(hidden_layers=hidden_layers, weight_mutation_std=weight_mutation_std)
    evolution.express()
else:
    evolution.load_dic(evolution_dic)

# infinity evolutionary loop
while(True):
    # write vxa vxd
    foldername = vx.prepare_directories(experiment_name, generation)
    vx.copy_vxa(experiment_name, generation)
    vx.write_all_vxd(experiment_name, generation, evolution.dump_dic())


    # start simulator
    print("simulating...")
    vx.start_simulator(experiment_name, generation)
    # record a brief history for the bestfit
    print("recording...")
    vx.record_bestfit_history(experiment_name, generation, stopsec=2)

    # read reporter
    sorted_result = vx.read_report(experiment_name, generation)


    # report the fitness
    msg = f"Experiment {experiment_name}, simulation for generation {generation} finished.\nThe top 3 bestfit fitness score of this generation are \n"
    for i in range(3):
        if i<len(sorted_result['id']):
            robot_id = sorted_result['id'][i]
            msg += f"{evolution.population['genotype'][robot_id]['firstname']} {evolution.population['genotype'][robot_id]['lastname']}'s fitness score: {sorted_result['fitness'][i]:.1e} \n"
    print(msg, flush=True)

    # if generation%3==0:
    #     import sida.slackbot.bot as bot
    #     bot.send(msg, 1, "GUB0XS56E")

    # next generation
    generation += 1
    next_generation = evolution.next_generation(sorted_result)
