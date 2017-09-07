# pi-foos
Raspberry Pi foosball table game automation

## Overview
Utilizes GPIO Pins on a Pi to record goals for teams up to 5, record best out of 3 wins and post the results to a RESTful API/Website.

A UUID is generated per _game_ which can be used by the API/Website to record all goals and round winners.

Users should log into the API/Website to claim their game - then all stats and records can be associated and reported.

## Running It
Run this in Python 2.7 on a Pi - should be configured to automatically start up on Pi boot... 

## TODO
Init script for automatic service start
