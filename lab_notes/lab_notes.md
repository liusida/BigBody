# Lab Notes

## Apr 8. 

Checking two experiments running on DG, I found both exp resulted almost a full cube. Which may because it wants to use as many free voxels as possible. So I adjust the fitness function to `(x^2+y^2)/n`. Now every direction should be consider valid, and it punishs robots with many voxels.

Also I fixed the population to be 80 for every generation, instead of growing from 10. (10 is too few for evolution.)

I started another exp on DG in folder BigBody2 with 3 GPUs (no more GPUs available).

## Apr 7.

The two exps runs, both with 8 GPUs. So far so good. the body dimension grew to 20x20x20.