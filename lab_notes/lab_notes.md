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

## Apr 11. (1)

Big ones tend to be too soft to move. To confirm this, I started another identical experiment BigBody5, to see if at the same scale, the body be unable to move.

Then I add another output node to CPPN, indicating the proportion of BONEs, so the final robot won't be merely a MEAT ball.

Started another experiment with bone in BigBody6. (Don't forget set t=10.)

## Apr 11. (2)

change the logic: it should be empty -> muscle -> bone, not empty -> bone -> muscle, so bone propbably is inside muscle, not outside. (for BigBody6)

Restart exp BigBody5 and BigBody6 with the same seed 802.

## Apr 11. (3)

BB3 and BB4 stopped. BB5 and BB6 has a bug, didn't sort by fitness score, so no evolution happen. :(

BB5 started on dg-gpunode09 with 7 gpus. v041124
22099     dggpu      BB5    sliu1  R       0:06      1 dg-gpunode09

BB6 started on dg-gpunode06 with 8 gpus. v041123
22092     dggpu      BB6    sliu1  R       6:08      1 dg-gpunode06

## Apr 11. (4)

Bone is too slow to simulate. If the elastic modulus increase 100 times, the simulation will be 10 times slower. :~(

So in this sense, simulation for soft robots is not suitable for rigid body.

Set Material 2 to a light, but non-actuate material (LightFat), with the same elastic modulus.

Deleted BB6, Bone, too slow.
BB7 started on dg-gpunode06 with 8 gpus. v04112155
22101     dggpu      BB7    sliu1  R       1:43      1 dg-gpunode06

## Apr 11. (5)

results of BB3(random=128) and BB4(random=4) seems clear, summarize as follow:

Both CTE=0.01;
Both exp peak at body 14x14x14. then when body grow bigger, travel distance decreases.
High density makes the body too heavy and no longer able to life the feet.

BB3 and BB4 terminated. Should be included in report.

BB2 is softly and slowly falling. no use.
BB1 before gen170, is CTE=0.03, cube, walking. But not realistic. But at generation 80 (18x18x18), it runs quite happily. 
BB before gen168, is CTE=0.03, cube with a tail, walking, but not realistic, same as BB1. gen 80, it was jumping, seems cheating.

## Apr 11. (6)

So scaffolding from smaller one is hard to transfer to larger body, there is pysical limitation. The conclusion is that, given the same material and envrionment, it is not just resolution difference between 10-voxel body and 1000-voxel body, there is real body size difference between them. The simulation can give us clear description of what will happen when the body gets bigger.

Now try to directly search for 30x30x30 body in BB8.

started BB8 with 8 gpus. v04112232

## Apr 11. (7)

Resolution... Actually we can design an experiment that the only difference is the resolution.

suppose at the beginning, vox_size=1m, vox_dim=1, if we increase vox_dim to be 3, vox_size should be 1/3 m, then everything will be the same? Let try.

Start experiment BB9 with 8 gpus, random=802. to test only change resolution.

Start experiment BBA with 2 gpus. random=1

Promising!

## Apr 12. (1)

BB9 and BBA are doing a great job. now they have 16x16x16 body.

BB5 failed as expect (it is a control exp). body is too soft and heavy and crash.
But the treatment BB7 failed to develop interesting shape. it doesn't move at all.

Since "high resolution" plan is working, stop BB5 and BB7, free resource to start another one identical (to BB9) BBB using difference random seeds 808.

Start experiment BBB with 8 gpus, random=808, 5 gen/dim

Start BBC using random seeds 808 but with quicker growth, not 5 generations per voxel in dimension, but only 2 generations per voxel in dimension. See if it can increase resolution faster than BB9 BBA and BBB and still works.

Start experiment BBC with 7 gpus, random=808, 2 gen/dim

## Apr 12. (2)

BB8 is a control. directly evolving 30x30x30, but it is super slow, takes 3 hours per generation.

I need another control, BB8 has two types of material, and not shrink voxel size. so let me start another BBD, with the same setting with BBB (random 808), but directly evolving 30x30x30.

Start experiment BBD with 8 gpus, random=808, direct 30.


## Apr 12. (3)

Unfortunately, BB9, BBA, BBB, BBC all peaked at certain scale and the fitness goes down. Maybe not enough time to adapt.

BB9 peak at Gen30, 8x8x8, 5 gen/dim, dist=0.42, random=802
BBA peak at Gen30, 8x8x8, 5 gen/dim, dist=0.42, random=1
BBB peak at Gen35, 9x9x9, 5 gen/dim, dist=0.18, random=808
BBC peak at Gen16, 10x10x10, 2 gen/dim, dist=0.18, random=808
BBD still running, 30x30x30, , dist=0.06, random=808

Need more generation per body_dim. If not surpass the previous max, don't increase.

Start new exp BBE with new schedualing: only increase body dimension after surpass the performance of last body dimension 5% 3times.

Terminate BBB.
Start BBE on dg-gpunode06 with 8 gpus, random=802.

Terminate BB9.
Try BBF with weight mutate rate: 0.1, more aggresive, and population size 40, faster.
Start BBF on dg-jup with 8 gpus, random=802.

## Apr 12. (4)

asking for (dim+1)/dim is too harshing, since body never get bigger.
instead, asking for passing multiple times. max(1,30-dim). will be better.
faster simulation with low dim can do more rounds.

Restart BBE. made a mistake, used parameter for BBF. so now BBE are using mutation rate:9, 0.1, and population of 40.
Restart BBF with mutation rate:9, 0.1, population of 80.

Restart BBE with population of 80. random seed 803.

Terminate BBC.
Start BBG. with new fitness function f= z_offset * 10 + sqrt(x_offset^2 + y_offset^2). with 7 gpus. random seed 804.

## Apr 13. (1)

Try shorter evaluation time. since we have z_offset*10 to provent falling already.
Change BBG's base.vxa. t=3. random=802. Start over. v04131008

## Apr 13. (2)

BB3 has a good start, seems have potential to make it.

Copy BB3 to BBH. delete generation after 60. using not newest strategy: update fitness function, use mutation 9,0.1, population 80, not increase dim until at least as good as previous best. no resource.
start with only 2 gpus on dg-gpunode05.

## Apr 14. (1)

BBF started suffer from the same problem, fitness score peak and then recess.
Till now we only have BBF 16x, 

OK, change plan, let's revisit this later. Do several 30x robots with expansion instead.


# ONLY do 30x30x30.

## Apr 14. (2)

Start BBI, random_seed=1001, 30x30x30, with expansion, population=40, evaluation_time=3sec, fitness_function=z*10+sqrt(x^2+y^2), TempPeriod=0.2, No Collision.
(this fitness function is proven to prevent falling strategy, so use 3sec.)
go

Start BBJ, start from BBG's checkpoint, unsample and continue evolve. random_seed=802 but not important. parameters are the same with BBI.

## Apr 14. (3)

Idea another paper: It will be worth to compare different choices of population size. evolving 6x6x6 is fast. so it is possible to see in the same wall clock time, compare the achievement across different population sizes. I guess there will be a sweet point, since too large is slow every generation, and too small there's not enough diversity.

(laptop with 1 GPU)
6x6x6, pop=1000, 5 minutes per generation, 1.9e-01 after 46 minutes.
6x6x6, pop=100, 1 minutes per generation, 

