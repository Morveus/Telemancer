from machine import Pin, PWM
import time

# Initialize GPIO13 as a PWM pin
buzzer = PWM(Pin(32))

def play_tone(frequency, duration):
    buzzer.freq(frequency)
    buzzer.duty(512)  # Set duty cycle (0-1023)
    time.sleep(duration)
    buzzer.duty(0)  # Stop the buzzer

def play_startup_sound():
    print("Playing Startup sound")
    play_tone(500, 0.1)
    play_tone(1500, 0.1)
    play_tone(2500, 0.1)
    play_tone(3500, 0.1)

def play_ready_sound():
    print("Playing Ready sound")
    play_tone(5000, 0.1)
    time.sleep(0.1)
    play_tone(5000, 0.1)