# The Env Differentiator

## Reason:
To compare the environment variables from one deployment to another in a K8s cluster.

## Language used:
Python 3.11

## How to make it:
1. Brute Force:
All the deployments will be searched one by one with everyother deployment with an 0(N^2) of time complexity

2. HashMap/HashSet:
We save all the environment variables with their respective names of a particular deployment in a hashmap and go on subtracting the environment variables of the other deployment.

Let suppose the value of a particular name is -1 that means that environment variable is not present in deployment 1.

If a frequency of a name of an EV is 1, then that it is not present in deployment 2.

## Output:
It will give 2 arrays 
1. extra ev in deployment 1 (freq = 1)
2. extra ev in deployment 2 (freq = -1›)

