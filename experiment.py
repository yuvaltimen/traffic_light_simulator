from random import randint

from src.config import Config, OutputMode
from src.controller import run_simulation

# Ranges
# Experiment to grid search across parameters
street_block_lengths = (200, 500, 800)
avenue_block_lengths = (200, 500, 800)

street_crosswalk_lengths = (10, 30, 50)
avenue_crosswalk_lengths = (10, 30, 50)

avenue_traffic_light_cycle_times_tuples = [(10, 15), (25, 30), (50, 55)]
num_random_trials = 5

n = len(street_block_lengths) * len(avenue_block_lengths) * len(street_crosswalk_lengths) * len(
    avenue_crosswalk_lengths) * len(avenue_traffic_light_cycle_times_tuples) * 2 * num_random_trials


file_path = "experiment/both_biases_experiment.jsonl"
print(f"Running {n} simulations")

with open(file_path, "w+") as file:

    for street_block_length in street_block_lengths:
        for street_crosswalk_length in street_crosswalk_lengths:
            for avenue_block_length in avenue_block_lengths:
                for avenue_crosswalk_length in avenue_crosswalk_lengths:
                    for time_pair in avenue_traffic_light_cycle_times_tuples:
                        for _ in range(num_random_trials):
                            for i in range(2):
                                cfg = Config()
                                cfg.output_mode = OutputMode.STATISTICS
                                cfg.street_block_length = street_block_length
                                cfg.avenue_block_length = avenue_block_length
                                cfg.street_crosswalk_length = street_crosswalk_length
                                cfg.avenue_crosswalk_length = avenue_crosswalk_length
                                cfg.avenue_traffic_light_cycle_times = time_pair if i == 0 else time_pair[::-1]
                                # Pick seed randomly, but log it out for repeatability
                                cfg.traffic_light_grid_random_seed = randint(0, 100)

                                file.write(run_simulation(cfg))
                                file.write("\n")
