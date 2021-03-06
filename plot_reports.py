from exp_settings import *
import lxml.etree as etree
import re, os, json, glob, sys
import voxelyze as vx
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
# experiment_name = "v040711"

if len(sys.argv)>1:
    experiment_name = sys.argv[1]
generation_folders = glob.glob(f"data/experiment_{experiment_name}/generation_*")
print(f"data/{experiment_name}/generation_*")
generations = []
for f in generation_folders:
    ff = f.split('/')
    generations.append(int(re.search(r'\d+', ff[-1]).group()))
generations.sort()
x = []
x1 = []
x2 = []
body = []
mut = []
pop = []
for generation in generations:
    folder = vx.foldername_generation(experiment_name, generation)
    if folder is None:
        break
    generation_filename = f"{folder}/mutation.json"
    if not os.path.exists(generation_filename):
        break
    with open(generation_filename, "r", encoding="UTF-8") as f:
        generation_config = json.load(f)

    body_n = generation_config["body_dimension"][0]
    target_population_size = generation_config["target_population_size"]
    print(f"G {generation}, Body Dimension: {body_n}")
    report_filename = f"{folder}/report/output.xml"
    if not os.path.exists(report_filename):
        break
    report = etree.parse(report_filename)
    detail = report.xpath("/report/detail")[0]
    distances = []
    num_voxels = []
    end_zs = []
    # read all detail. robot_id and distance.
    for robot in detail:
        robot_id = int(re.search(r'\d+', robot.tag).group())
        init_x = float(robot.xpath("initialCenterOfMass/x")[0].text)
        init_y = float(robot.xpath("initialCenterOfMass/y")[0].text)
        init_z = float(robot.xpath("initialCenterOfMass/z")[0].text)
        end_x = float(robot.xpath("currentCenterOfMass/x")[0].text)
        end_y = float(robot.xpath("currentCenterOfMass/y")[0].text)
        end_z = float(robot.xpath("currentCenterOfMass/z")[0].text)
        distance = np.sqrt((end_x-init_x)**2 + (end_y-init_y)**2)
        num_voxel = int(robot.xpath("num_voxel")[0].text)
        distances.append(distance)
        end_zs.append(end_z)
        num_voxels.append(num_voxel)
    body.append(body_n)
    mut.append(mutation_rate(generation)[1])
    pop.append(target_population_size)
    x.append(distances)
    x1.append(num_voxels)
    x2.append(end_zs)

large_f = max(x[-1])
ticks = []
stepsize = int(len(x)/10)+1
for i in range(len(x)):
    if i%stepsize==0:
        ticks.append(i)
plt.boxplot(x)
plt.xticks(ticks, ticks)

large_b = body[-1]
body = np.array(body)
body = body * large_f / large_b

large_m = mut[0]
mut = np.array(mut)
mut = mut * large_f / large_m

large_p = pop[-1]
pop = np.array(pop)
pop = pop * large_f / large_p

xx = list(range(len(x)))
plt.plot(xx,body, label=f"body: {large_b}")
plt.plot(xx,mut, label=f"mutate: {large_m}")
plt.plot(xx,pop, label=f"pop: {large_p}")
plt.legend()
plt.ylabel("Travel Distance")
plt.xlabel("Generation")
plt.savefig(f"{experiment_name}_travel_distance.png")
plt.close()

plt.figure(figsize=(9,6))
pboxplot = plt.boxplot(x1, showfliers=False)
plt.xticks(ticks, ticks)
for patch in pboxplot['boxes']:
    patch.set_color("#DDDDDD")
plt.savefig(f"{experiment_name}_boxplot_num_voxels.png")
plt.close()

plt.figure(figsize=(9,6))
pboxplot = plt.boxplot(x2, showfliers=False)
plt.xticks(ticks, ticks)
plt.xlabel("Generation")
plt.ylabel("Height of the Center of Mass in the end.")
for patch in pboxplot['boxes']:
    patch.set_color("#DDDDDD")
plt.savefig(f"{experiment_name}_boxplot_end_z.png")
plt.close()