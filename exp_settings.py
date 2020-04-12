import random
import numpy as np

random.seed(802)
np.random.seed(802)

# ============== should be able to change during evolution: ================
#  Plan: evolve a 100x100x100 body
#  target generation = 500
# 1. effect at this generation:
# only if fitness score pass new height by 5% 3 times, increase body dimension
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
    print(f"Median fitness score this round: {fitness_score}.")
    if fitness_score > (body_dimension_n+1)/body_dimension_n * 1.05 * best_last_round:
        fitness_score_surpass_time += 1
        print(f"Good News: fitness score hit threshold {fitness_score_surpass_time} time(s).")
        if fitness_score_surpass_time>3:
            fitness_score_surpass_time = 0
            body_dimension_n = body_dimension_n + 1
            best_last_round = fitness_score
            print(f"Congradulations, body dimension increase to {body_dimension_n}. Setting best median fitness score last round to {best_last_round}.")
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
    ret = [10, 0.01] # search more aggressively
    print(f"Using mutation rate {ret}")
    return ret

# 3. effect at next generation:
def target_population_size(generation=0):
    # ret = int(30 + generation/20)
    ret = 80
    print(f"Using population size {ret}")
    return ret

# =================== cannot change during evolution: =======================
experiment_name = "v04121712"
hidden_layers = [10,10,10]
