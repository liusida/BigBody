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
from voxelyze.evolution.cppn_alife.CPPNEvolution import CPPNEvolution
import numpy as np
import shutil, random, os
generation = 0

try:
    from exp_settings_6x_to_30x import *
except:
    experiment_name = "v040708"
    target_population_size = 128
    body_dimension = (10, 10, 10)
    mutation_rate = [10, 0.1]
    hidden_layers = [10,10,10]

vx.clear_workspace()

# try to resume from last experiment
evolution_dic, generation = vx.load_last_generation(experiment_name)
# if failed, start from scratch
if evolution_dic is None:
    generation = 0
    evolution = CPPNEvolution(body_dimension(), target_population_size(), mutation_rate())
    evolution.init_geno(hidden_layers=hidden_layers)
    evolution.express()
else:
    # resize using new body_dimension
    evolution = CPPNEvolution()
    init_body_dimension_n(evolution_dic["body_dimension"][0])
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
    # read report
    sorted_result = vx.read_report(experiment_name, generation)
    # report the fitness
    top_n = 3 #len(sorted_result['id'])
    msg = f"Experiment {experiment_name}, simulation for generation {generation} finished.\nThe top {top_n} bestfit fitness score of this generation are \n"
    for i in range(top_n):
        if i<len(sorted_result['id']):
            robot_id = sorted_result['id'][i]
            msg += f"{evolution.population['genotype'][robot_id]['firstname']} {evolution.population['genotype'][robot_id]['lastname']}'s fitness score: {sorted_result['fitness'][i]:.1e} \n"
    print(msg, flush=True)

    # record a brief history for the bestfit
    print("recording...")
    vx.record_bestfit_history(experiment_name, generation, robot_id=sorted_result["id"][0], stopsec=2)

    # vx.write_box_plot(experiment_name, generation, sorted_result)

    # reporting
    # import sida.slackbot.bot as bot
    # bot.send(msg, 1, "GUB0XS56E")

    # dynamical sceduling
    evolution.target_population_size = target_population_size(generation)
    evolution.body_dimension = body_dimension(generation, sorted_result["fitness"])
    evolution.mutation_rate = mutation_rate(generation)

    # write report png
    # os.system("python plot_reports.py > /dev/null")
    # next generation
    generation += 1
    next_generation = evolution.next_generation(sorted_result)
