#!/bin/bash

EXE_PATH="Fill this in"

nohup $EXE_PATH/weather_hat.py -f < config file > /tmp/weather_hat.log  2>&1 &
