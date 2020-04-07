from exp_settings import *
import lxml.etree as etree
import re, os
import voxelyze as vx
import matplotlib.pyplot as plt

experiment_name = "v040718"

x = []
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
    # read all detail. robot_id and fitness.
    for robot in detail:
        robot_id = int(re.search(r'\d+', robot.tag).group())
        fitness = float(robot.xpath("fitness_score")[0].text)
        fitnesses.append(fitness)
    x.append(fitnesses)

plt.boxplot(x)
plt.show()