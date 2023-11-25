from tele_buttons import Button, ButtonConfig
from machine import Timer, Pin
import utime

button_config = ButtonConfig()
buttons_list = button_config.load_buttons()
button_config.init_buttons_pins()
print(buttons_list)

last_executed_time = 0
current_program = 1

def check_buttons():
    global last_executed_time
    for btn in buttons_list:
        previouslyHeld = btn.held
        
        pinv = btn.pin.value()
        n = btn.button_name
        o = btn.gpio
        p = str(btn.gpio)
        i = btn.interval
        
        if pinv == 1 and btn.held == False:
            btn.held = True
            handle_system_button(n)
            print("Pressed " + n + ", setting 'held' (GPIO " + p + ")")
        
        if btn.held == True and pinv == 0:
            print(n + " is not held anymore (GPIO " + p + ")")
            btn.held = False
            pass
            
        if btn.held and not(btn.repeatable) and not(previouslyHeld):
            print("Running call once (" + btn.url + ")")
            #_thread.start_new_thread(sendHTTPRequest, (btn.url,))
            #sendHTTPRequest(btn.URL)
            pass
        
        if btn.held and btn.repeatable:
            current_time = utime.ticks_ms()
            elapsed_time_ms = (current_time - last_executed_time)
            
            if elapsed_time_ms >= i:
                # Update the last executed time
                last_executed_time = utime.ticks_ms()
                # Execute your instruction here
                print("Waited for " + str(elapsed_time_ms) + " milliseconds, calling " + btn.url)
                #_thread.start_new_thread(sendHTTPRequest, (btn.url,))
                #sendHTTPRequest(btn.url)

def handle_system_button(name):
    if name == "program":
        change_program()
        pass
    
    if name == "wifi":
        print("WIFI RESET // TODO")
        pass

def change_program():
    current_program += 1
    if current_program > 4:
        current_program = 1
        
    print("Program is now " + str(current_program))
