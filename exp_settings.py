# ============== should be able to change during evolution: ================
#  Plan: evolve a 100x100x100 body
#  target generation = 500
# 1. effect at this generation:
def body_dimension(generation=0):
    n = int(3 + generation/5)
    ret = (n, n, n)
    print(f"Using body dimension {ret}")
    return ret

# 2. effect between this generation and the next:
def mutation_rate(generation=0):
    if generation==0:
        ret = [2, 0.5]    # this is aggressive
    elif generation<10:
        ret = [20, 0.05]    # this is less aggressive
    else:
        ret = [200, 0.001]    # this is stable
    print(f"Using mutation rate {ret}")
    return ret

# 3. effect at next generation:
def target_population_size(generation=0):
    ret = int(10 + generation/10)
    print(f"Using population size {ret}")
    return ret

# =================== cannot change during evolution: =======================
experiment_name = "v040711"
hidden_layers = [10,10,10]
