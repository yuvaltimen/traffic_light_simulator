## Pedestrian Traffic Simulation

Runs a simulation of a walker walking in a grid city from the source to the target destinations.
Traffic light offset times are uniformly sampled, and run on a scheduled cycle (ie. 20s red, 30s green).
The walker has a policy of how they want to turn at traffic lights:

- `greedy` policy - will cross the traffic light in front of them if available
- `avenue first` policy - will cross the avenue first if available
- `street first` policy - will cross the street first if available

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