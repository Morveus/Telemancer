import telemancer.tele_tokens as tokens
from telemancer.tele_buttons import Button, ButtonConfig
from machine import Timer, Pin
import utime, json, urequests, gc

button_config = ButtonConfig()
buttons_list = button_config.load_buttons()
button_config.init_buttons_pins()

last_executed_time = 0
current_program = 1

tokens.read_tokens()

def check_buttons():
    global last_executed_time
    for btn in buttons_list:
        if btn.program == current_program:
            previouslyHeld = btn.held
            
            pinv = btn.pin.value()
            n = btn.button_name
            o = btn.gpio
            p = str(btn.gpio)
            i = btn.interval
            
            sendRequest = False
                    
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
                sendRequest = True
            
            if btn.held and btn.repeatable:
                current_time = utime.ticks_ms()
                elapsed_time_ms = (current_time - last_executed_time)
                
                if elapsed_time_ms >= i:
                    last_executed_time = utime.ticks_ms()
                    print("Waited for " + str(elapsed_time_ms) + " milliseconds, calling " + btn.url)
                    sendRequest = True
                    
            if sendRequest:
                sendHTTPRequest("POST", btn.url, tokens.get_token(btn.token_id), btn.payload)

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

def sendHTTPRequest(method, url, token="", payload=""):
    print(gc.mem_free())
    headers = {}
    
    if token:
        headers["Authorization"] = "Bearer " + token['token_value']

    data = payload if payload else None

    if method.upper() == "GET":
        print(gc.mem_free())
        response = urequests.get(url, headers=headers)

    elif method.upper() == "POST":
        headers["Content-Type"] = "application/json"
        print(url)
        print(headers)
        print(data)
        response = urequests.post(url, headers=headers, data=data)
        
    response.close()