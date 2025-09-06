## Pedestrian Traffic Simulation

Runs a simulation of a walker walking in a grid city from the source to the target destinations.
Traffic light offset times are uniformly sampled, and run on a scheduled cycle (ie. 20s red, 30s green).
The walker has a policy of how they want to turn at traffic lights:

- `greedy` policy - will cross the traffic light in front of them if available
- `avenue` policy - will stay along the avenue until it reaches the correct street
- `street` policy - will stay along the street until it reaches the correct avenue

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
3. Edit `src/config.py` for any simulation-level configurations you want to change. 
4. Go to `run.py` at the root level, and click run.
