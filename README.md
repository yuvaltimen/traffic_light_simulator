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
street_policy                     66.8
avenue_policy                     73.3
num_streets                          5
num_avenues                          6
street_block_length                200
street_crosswalk_length             10
avenue_block_length                200
avenue_crosswalk_length             10
green_time                          10
red_time                            15
traffic_light_grid_random_seed      59
walker_speed                        60
walker_starting_corner              sw
Name: 4, dtype: object

street_policy                     69.766667
avenue_policy                         87.95
num_streets                               5
num_avenues                               6
street_block_length                     200
street_crosswalk_length                  10
avenue_block_length                     200
avenue_crosswalk_length                  10
green_time                               15
red_time                                 10
traffic_light_grid_random_seed           94
walker_speed                             60
walker_starting_corner                   sw
Name: 5, dtype: object

street_policy                         127.65
avenue_policy                     114.766667
num_streets                                5
num_avenues                                6
street_block_length                      200
street_crosswalk_length                   10
avenue_block_length                      200
avenue_crosswalk_length                   10
green_time                                55
red_time                                  50
traffic_light_grid_random_seed            21
walker_speed                              60
walker_starting_corner                    sw
Name: 27, dtype: object

street_policy                     84.233333
avenue_policy                     73.133333
num_streets                               5
num_avenues                               6
street_block_length                     200
street_crosswalk_length                  10
avenue_block_length                     200
avenue_crosswalk_length                  30
green_time                               10
red_time                                 15
traffic_light_grid_random_seed           88
walker_speed                             60
walker_starting_corner                   sw
Name: 34, dtype: object

street_policy                         269.15
avenue_policy                     310.216667
num_streets                                5
num_avenues                                6
street_block_length                      800
street_crosswalk_length                   50
avenue_block_length                      800
avenue_crosswalk_length                   50
green_time                                30
red_time                                  25
traffic_light_grid_random_seed            15
walker_speed                              60
walker_starting_corner                    sw
Name: 2415, dtype: object

street_policy                         269.15
avenue_policy                     298.683333
num_streets                                5
num_avenues                                6
street_block_length                      800
street_crosswalk_length                   50
avenue_block_length                      800
avenue_crosswalk_length                   50
green_time                                25
red_time                                  30
traffic_light_grid_random_seed            82
walker_speed                              60
walker_starting_corner                    sw
Name: 2416, dtype: object

street_policy                         269.15
avenue_policy                     308.883333
num_streets                                5
num_avenues                                6
street_block_length                      800
street_crosswalk_length                   50
avenue_block_length                      800
avenue_crosswalk_length                   50
green_time                                30
red_time                                  25
traffic_light_grid_random_seed            56
walker_speed                              60
walker_starting_corner                    sw
Name: 2419, dtype: object

street_policy                     301.733333
avenue_policy                          315.3
num_streets                                5
num_avenues                                6
street_block_length                      800
street_crosswalk_length                   50
avenue_block_length                      800
avenue_crosswalk_length                   50
green_time                                55
red_time                                  50
traffic_light_grid_random_seed            88
walker_speed                              60
walker_starting_corner                    sw
Name: 2421, dtype: object

street_policy                         269.15
avenue_policy                     349.216667
num_streets                                5
num_avenues                                6
street_block_length                      800
street_crosswalk_length                   50
avenue_block_length                      800
avenue_crosswalk_length                   50
green_time                                50
red_time                                  55
traffic_light_grid_random_seed            15
walker_speed                              60
walker_starting_corner                    sw
Name: 2426, dtype: object
