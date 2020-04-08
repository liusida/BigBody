from exp_settings import *
import lxml.etree as etree
import re, os
import voxelyze as vx
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

# experiment_name = "v040711"

x = []
x1 = []
body = []
mut = []
pop = []
for generation in range(10000):
    folder = vx.foldername_generation(experiment_name, generation)
    if folder is None:
        break
    report_filename = f"{folder}/report/output.xml"
    if not os.path.exists(report_filename):
        break
    report = etree.parse(report_filename)
    detail = report.xpath("/report/detail")[0]
    fitnesses = []
    num_voxels = []
    # read all detail. robot_id and fitness.
    for robot in detail:
        robot_id = int(re.search(r'\d+', robot.tag).group())
        fitness = float(robot.xpath("fitness_score")[0].text)
        num_voxel = int(robot.xpath("num_voxel")[0].text)
        fitnesses.append(fitness)
        num_voxels.append(num_voxel)
    body.append(body_dimension(generation)[0])
    mut.append(mutation_rate(generation)[1])
    pop.append(target_population_size(generation))
    x.append(fitnesses)
    x1.append(num_voxels)

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
print(len(xx), len(body))
plt.plot(xx,body, label=f"body: {large_b}")
plt.plot(xx,mut, label=f"mutate: {large_m}")
plt.plot(xx,pop, label=f"pop: {large_p}")
plt.legend()
plt.savefig("boxplot.png")
plt.close()
plt.figure(figsize=(9,6))
pboxplot = plt.boxplot(x1, showfliers=False)
plt.xticks(ticks, ticks)
for patch in pboxplot['boxes']:
    patch.set_color("#DDDDDD")
plt.savefig("boxplot_num_voxels.png")
plt.close()