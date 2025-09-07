#!/usr/bin/env bash

# Experiment to grid search across parameters
#street_block_length: 200.0 -> 1000.0
#street_crosswalk_length: float = 10.0 -> 50.0
#avenue_block_length: float = 200.0 -> 1000.0
#avenue_crosswalk_length: float = 20.0 -> 60.0
#avenue_traffic_light_cycle_times: tuple[float, float] = (25.0, 20.0) -> (50.0, 70.0)


for (( street_block_length=200; street_block_length<=800; street_block_length+=200 ))
    do
      for (( street_crosswalk_length=10; street_crosswalk_length<=50; street_crosswalk_length+=10 ))
      do
        for (( avenue_block_length=200; avenue_block_length<=800; avenue_block_length+=200 ))
        do
          for (( avenue_crosswalk_length=20; avenue_crosswalk_length<=60; avenue_crosswalk_length+=10 ))
          do
            for (( avenue_traffic_light_green_cycle=25; avenue_traffic_light_green_cycle<=50; avenue_traffic_light_green_cycle+=5 ))
              for light_bias in {1..2}
              do
                do
                  for _ in {1..5}  # run 5 trials to give randomness a chance
                  do
                    # get both the slight red and slightly green bias (+/- 5 seconds)
                    if [[ $light_bias -eq 1 ]]; then
                      val=5
                    else
                      val=-5
                    fi
                    python run.py --mode statistics --street_block_length $street_block_length --street_crosswalk_length $street_crosswalk_length --avenue_block_length $avenue_block_length --avenue_crosswalk_length $avenue_crosswalk_length --traffic_cycle $avenue_traffic_light_green_cycle,$(($avenue_traffic_light_green_cycle + $val)) >> experiment/experiment_data.jsonl
                  done
                done
              done
          done
        done
      done
    done















