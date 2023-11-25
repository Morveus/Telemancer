import wifimgr
from machine import Timer
from time import sleep
import machine
import os
import ubluetooth
import ubinascii
import utime
import telemancer.tele_tokens as tokens
import telemancer.tele_actions as actions
from telemancer.tele_buttons import Button, ButtonConfig
import _thread, urequests, json

try:
  import usocket as socket
except:
  import socket
  
#dir_path = '/'

#if not os.path.isdir(dir_path):
#    os.mkdir(dir_path)

current_directory = os.getcwd()
print("current directory : " + current_directory)

print("HEEEEEEEEEEEY")
  
def get_ble_mac():
    ble = ubluetooth.BLE()
    ble.active(True)
    _, mac_bytes = ble.config('mac')  # Get the MAC address, which is the second element of the tuple
    mac_str = ubinascii.hexlify(mac_bytes, ':').decode()
    return mac_str

# Get MAC and extract the first four characters
ble_mac = get_ble_mac()
first_four = ble_mac.replace(":", "")[:4]
device_name = "Telemancer " + first_four

current_tokens = tokens.read_tokens()
print(current_tokens)


wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D

# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK -- Starting Telemancer")

def sendHTTPRequest(url, token = ""):
    headers = {}
    
    if token != "":
        headers = {
            "Authorization": "Bearer "+token,
            "Content-Type": "application/json"
        }
    response = urequests.get(url)
    response.close()


while True:
    actions.check_buttons()

def web_page():
  if led.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  
  html = """<html><head> <title>Telemancer</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
  <p>GPIO state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
  <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""
  return html

def get_action(button):
    print("Getting action : " + button)
    return false
  
try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('', 80))
  s.listen(5)
except OSError as e:
  machine.reset()

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    start = request.find('/?action=') + len('/?action=')
    if start != -1:
        end = request.find(' ', start)
        action = request[start:end]
    else:
        action = None

    if action == '1':
        print('LED ON')
        led.value(1)
    elif action == 'up':
        print('LED OFF')
        led.value(0)

    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')
