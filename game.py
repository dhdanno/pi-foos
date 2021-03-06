#!/usr/bin/env python

import RPi.GPIO as GPIO
import time, sys, uuid, requests
import socket

# Global Vars
goal_wait_timeout = 2 # set this below 1 for testing, 3 for real play
game_uuid = ""
debug_mode = False

## Pin Config
reset_button_in   = 4
team_A_trigger_in = 27
team_A_light_out  = 22
team_B_trigger_in = 18
team_B_light_out  = 23

# Stats Server
remote_api_url = "http://foos.works:8080/log/"

# Get local IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
s.close()

# GPIO Pin Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(reset_button_in,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(team_A_trigger_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(team_B_trigger_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(team_A_light_out,  GPIO.OUT)
GPIO.setup(team_B_light_out,  GPIO.OUT)

# Light an LED for 1 second
def light(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(goal_wait_timeout)
    GPIO.output(pin, GPIO.LOW)
    return

def notify_api_goal(team):
    print("Goal scored team: {}".format(team))
    print("UUID: {}".format("xxx"))

    # POST to api
    data = { "local_ip": local_ip, "team": format(team), "event_type": "goal"  }
    
    try:
        response = requests.post(remote_api_url, json=data)
        print response.status_code
    except:
        pass

# Global Game Loop
while True:
    try:
        # Sleep delay prevents CPU pegging
        time.sleep(0.01)    
        
        # Game Reset Button
        game_reset = GPIO.input(reset_button_in)
        if (game_reset == False):
            reset_game()
            continue

        A_input_state = GPIO.input(team_A_trigger_in)
        B_input_state = GPIO.input(team_B_trigger_in)

        if (A_input_state == False):
           print("YELLOW Team Scored!")
           light(team_A_light_out)
           notify_api_goal("YELLOW")
           time.sleep(goal_wait_timeout)

        if (B_input_state == False):
            print("BLACK Team Scored!")
            light(team_B_light_out)
            notify_api_goal("BLACK")
            time.sleep(goal_wait_timeout)

    # Handle SIGINT
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Bye")
        sys.exit()
