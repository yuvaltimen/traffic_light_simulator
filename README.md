## Pedestrian Traffic Simulation

Runs a simulation of a walker walking in a grid city from the source to the target destinations.
Traffic light offset times are uniformly sampled, and run on a scheduled cycle (ie. 20s red, 30s green).
The walker has a policy of how they want to turn at traffic lights:

- `avenue` policy - will prefer to stay along the avenue unless it reaches the correct north value or encounters a red light
- `street` policy - will prefer to cross the avenue first if the avenue light is green 

## Configuring

All the simulation configs are located at `src/config.py`. 
Most configs are self-explanatory, but the most important one is the `output_mode`, 
which may warrant some explanation. 

The `output_mode` config controls what type of 
simulation is run. If you want to visually see everything, select `PYGAME`, if you 
want to output the state of the simulation at each timestep, select `JSON`, and if 
you want to see the costs for each of our walkers after the whole simulation has 
run, select `STATISTICS`.

## Running Locally

To run the simulation yourself, follow the instructions below.

1. Create and activate a virtual environment:

```bash
>> python -m venv .venv && source .venv/bin/activate
```
2. Install the dependencies from `requirements.txt`:

```bash
>> pip install -r requirements.txt
``` 
3. Invoke the program from the root level by running `python run.py`
4. To update configurations, pass in flags to override the default config values. For example: `python run.py --mode statistics --walker_speed 30.5`


### Helpful findings...
Using the default configs, the random seeds to use to find differences are:
- 61
- 76
- 88

Here are the top runs from experiment that had >5% difference:

street_policy                     82.266667
avenue_policy                     69.966667
num_streets                               5
num_avenues                               6
street_block_length                     200
street_crosswalk_length                  10
avenue_block_length                     200
avenue_crosswalk_length                  20
green_time                               25
red_time                                 20
traffic_light_grid_random_seed          NaN
walker_speed                             60
walker_starting_corner                   sw
Name: 6, dtype: object

street_policy                      69.966667
avenue_policy                     105.033333
num_streets                                5
num_avenues                                6
street_block_length                      200
street_crosswalk_length                   10
avenue_block_length                      200
avenue_crosswalk_length                   20
green_time                                40
red_time                                  35
traffic_light_grid_random_seed           NaN
walker_speed                              60
walker_starting_corner                    sw
Name: 18, dtype: object

street_policy                     85.066667
avenue_policy                          82.2
num_streets                               5
num_avenues                               6
street_block_length                     200
street_crosswalk_length                  10
avenue_block_length                     200
avenue_crosswalk_length                  40
green_time                               25
red_time                                 30
traffic_light_grid_random_seed          NaN
walker_speed                             60
walker_starting_corner                   sw
Name: 23, dtype: object

street_policy                          76.3
avenue_policy                     94.716667
num_streets                               5
num_avenues                               6
street_block_length                     200
street_crosswalk_length                  10
avenue_block_length                     200
avenue_crosswalk_length                  40
green_time                               25
red_time                                 20
traffic_light_grid_random_seed          NaN
walker_speed                             60
walker_starting_corner                   sw
Name: 25, dtype: object

street_policy                     92.266667
avenue_policy                     81.383333
num_streets                               5
num_avenues                               6
street_block_length                     200
street_crosswalk_length                  10
avenue_block_length                     200
avenue_crosswalk_length                  40
green_time                               40
red_time                                 35
traffic_light_grid_random_seed          NaN
walker_speed                             60
walker_starting_corner                   sw
Name: 38, dtype: object

street_policy                     93.8
avenue_policy                     98.9
num_streets                          5
num_avenues                          6
street_block_length                200
street_crosswalk_length             10
avenue_block_length                200
avenue_crosswalk_length             60
green_time                          25
red_time                            20
traffic_light_grid_random_seed     NaN
walker_speed                        60
walker_starting_corner              sw
Name: 47, dtype: object

street_policy                      82.633333
avenue_policy                     102.616667
num_streets                                5
num_avenues                                6
street_block_length                      200
street_crosswalk_length                   10
avenue_block_length                      200
avenue_crosswalk_length                   60
green_time                                40
red_time                                  35
traffic_light_grid_random_seed           NaN
walker_speed                              60
walker_starting_corner                    sw
Name: 58, dtype: object

street_policy                         174.75
avenue_policy                     179.216667
num_streets                                5
num_avenues                                6
street_block_length                      200
street_crosswalk_length                   10
avenue_block_length                      500
avenue_crosswalk_length                   20
green_time                                25
red_time                                  30
traffic_light_grid_random_seed           NaN
walker_speed                              60
walker_starting_corner                    sw
Name: 61, dtype: object

street_policy                     164.966667
avenue_policy                          206.2
num_streets                                5
num_avenues                                6
street_block_length                      200
street_crosswalk_length                   10
avenue_block_length                      500
avenue_crosswalk_length                   20
green_time                                25
red_time                                  30
traffic_light_grid_random_seed           NaN
walker_speed                              60
walker_starting_corner                    sw
Name: 62, dtype: object

street_policy                     170.633333
avenue_policy                     164.966667
num_streets                                5
num_avenues                                6
street_block_length                      200
street_crosswalk_length                   10
avenue_block_length                      500
avenue_crosswalk_length                   20
green_time                                25
red_time                                  30
traffic_light_grid_random_seed           NaN
walker_speed                              60
walker_starting_corner                    sw
Name: 63, dtype: object

