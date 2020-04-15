import random
import numpy as np
from voxelyze.helper import cprint

random.seed(1001)
np.random.seed(1001)

# ============== should be able to change during evolution: ================
#  Plan: evolve a 100x100x100 body
#  target generation = 500
# 1. effect at this generation:
# only if fitness score pass new height multiple times, increase body dimension
# otherwise, keep adapting.

best_last_round = 0
body_dimension_n = 3
fitness_score_surpass_time = 0

def init_body_dimension_n(n):
    global body_dimension_n
    body_dimension_n = n

def body_dimension(generation=0, fitness_scores=[0]):
    global best_last_round, body_dimension_n, fitness_score_surpass_time
    fitness_score = np.median(fitness_scores)
    cprint(f"Median fitness score this round: {fitness_score}.")
    # if fitness_score > (body_dimension_n+1)/body_dimension_n * 1.05 * best_last_round: # this is too harsh, since the body doesn't get bigger.
    if fitness_score > best_last_round:
        fitness_score_surpass_time += 1
        cprint(title=f"Good News", msg=f"fitness score hit threshold {fitness_score_surpass_time} time(s).", code="OKGREEN")
        if fitness_score_surpass_time>max(1,30-body_dimension_n):
            fitness_score_surpass_time = 0
            body_dimension_n = body_dimension_n + 1
            best_last_round = fitness_score
            cprint(title=f"Congradulations", msg=f"body dimension increase to {body_dimension_n}. Setting best median fitness score last round to {best_last_round}.", code="OKGREEN")
    # n = int(3 + generation/5)
    # # n = 30
    ret = (body_dimension_n, body_dimension_n, body_dimension_n)
    print(f"Using body dimension {ret}")
    return ret

# 2. effect between this generation and the next:
def mutation_rate(generation=0):
    # if generation==0:
    #     ret = [2, 0.5]    # this is aggressive
    # elif generation<20:
    #     ret = [20, 0.05]    # this is less aggressive
    # else:
    #     ret = [20, 0.001]    # this is stable
    ret = [9, 0.1] # search more aggressively
    # ret[0]: 9:1
    # every 10 times of mutation, there's once mutate on activation function, so in a generation of 40, there will be 
    # 4 times of mutation on activation function, which hopefully bring us some new archietecture.
    # ret[1]: 0.1
    # if mutate on weights, set standard deviation to be 0.1, so weight change will happen mostly in (-0.3,0.3).
    print(f"Using mutation rate {ret}")
    return ret

# 3. effect at next generation:
def target_population_size(generation=0):
    # ret = int(30 + generation/20)
    ret = 40
    print(f"Using population size {ret}")
    return ret

# =================== cannot change during evolution: =======================
experiment_name = "v04142009"
hidden_layers = [10,10,10]
