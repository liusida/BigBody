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


vx.clear_workspace()
hidden_layers = [10,10,10]
def body_dimension(generation=0, fitness_scores=[0]):
    return [6,6,6]
def target_population_size(generation=0):
    return 1000
def mutation_rate(generation=0):
    return [9,0.1]
outer_species = 100
inner_generation = 50

for current_run in range(2,outer_species):
    random.seed(current_run)
    np.random.seed(current_run)
    experiment_name = f"MULTI_{current_run}"
    generation = 0
    evolution = CPPNEvolution(body_dimension(), target_population_size(), mutation_rate())
    evolution.init_geno(hidden_layers=hidden_layers)
    evolution.express()

    # 40 generations
    for g_id in range(inner_generation):
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

        if g_id >= inner_generation-2:
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
