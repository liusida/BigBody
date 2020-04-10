# Lab Notes

## Apr 7.

The two exps runs, in folder BigBody and BigBody1, both with 8 GPUs. So far so good. the body dimension grew to 20x20x20.

## Apr 8. (1)

Checking two experiments running on DG, I found both exp resulted almost a full cube. Which may because it wants to use as many free voxels as possible. So I adjust the fitness function to `(x^2+y^2)/n`. Now every direction should be consider valid, and it punishs robots with many voxels.

Also I fixed the population to be 80 for every generation, instead of growing from 10. (10 is too few for evolution.)

I started another exp on DG in folder BigBody2 with 3 GPUs (no more GPUs available).

## Apr 8. (2)

It turns out the punishment is too harsh, the robots have never grow a normal body. Because `n=d^3`, I thought `n` is at the same magnitude of `x^2`, and I was wrong. Let's try `(x^2+y^2)/sqrt(n)`, and rerun BigBody2.

## Apr 8. (3)

It seems better to regulate num of voxel in CPPN expression. Use np.quantile to make the body contains exactly 70% voxels and 30% empties before throw away unconnected voxels. So the fitness function becomes `(x^2+y^2)`.

## Apr 8. (4)

I stopped the first exp BigBody, the elephant, giving the GPUs to BigBody2.

It seems that given a small initial shape, the final big body will be quite similar to the initial one. This is a new discovery. So that we can draw an initial shape, and let evolution algorithm figure out what the similar big body will looks like. It's just somehow expensive.


## Apr 8. (5)

Reading http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.28.5457&rep=rep1&type=pdf

Geno --\[NEAT\]--> Network --\[CPPN\]--> Body/Phaseoffset

## Apr 10. (1)

With 70% voxels, the body start to fall, slowly, no matter how I change the reinit position time, it only select for someone fall more slowly.

Add a term 10*z*abs(z) to the fitness function, and no reinit. so it will punish fall.

Start the 4th experiment in BigBody3 folder.

## Apr 10. (2)

Fitness score should be calculated in Python. So simulation only report facts, and calculation is done in `workflow.py`.

Now we are using 

```
fitness = end_z * 10 + np.sqrt((end_x-init_x)**2 + (end_y-init_y)**2)
```

Restart the 4th experiment in BidBody3 folder.

## Apr 10. (3)

Seems new exp is good. Start another identical one in BigBody4 folder.

## Apr 10. (4)

FALLING AGAIN! WTF!!!

Set evaluation time to 10 sec. See who is going to fall again!

Restart experiments in BigBody3 and 4.

## Apr 10. (5)

SO FAR SO GOOD! 10 sec is great! except require more running time. It's worthy.

Now we at least have two 10x10x10 interesting ones.
