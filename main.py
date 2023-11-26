import gc
import telemancer.tele_buzzer as buzzer
buzzer.play_startup_sound()

import machine, os, utime, uasyncio as asyncio
import _thread, urequests, json
import ubluetooth,telemancer.tele_wifi as wifimgr, ubinascii
import telemancer.tele_actions as actions
import telemancer.tele_web as web

try:
  import usocket as socket
except:
  import socket

print("Starting Telemancer...")
  
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

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D

gc.collect()

# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
buzzer.play_ready_sound()
print("ESP OK -- Telemancer resources loaded. Running Web server...")
  
try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('', 80))
  s.listen(5)
except OSError as e:
  machine.reset()

gc.collect()
debug = False
while debug:
    if gc.mem_free() < 102000:
          gc.collect()
    actions.check_buttons()
  
async def check_buttons_loop():
    while True:
        actions.check_buttons()
        await asyncio.sleep(0.1)  # Sleep to yield control to other tasks

web_context = {
    'ip': wifimgr.get_ip(),
    'ap': wifimgr.get_ap(),
    'uptime': utime.time()
}

async def web_server_loop():
    while True:
      try:
        web_context['uptime'] = utime.time()
        
        actions.check_buttons()
        
        if gc.mem_free() < 102000:
          gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        req_bytes = request
        req_str = str(request)
        
        if 'GET /' in req_str:
            print("GET request")
            # Find the start and end of the file name
            start = req_str.find('GET /') + len('GET /')
            end = req_str.find(' ', start)

            # Extract the file name
            file_name = req_str[start:end]
            if file_name == "":
                file_name = "index"

            response = web.load_content(file_name, web_context)
        
        elif 'POST /' in req_str:
            print("POST request")
            start = req_str.find('POST /api/') + len('POST /api/')
            end = req_str.find(' ', start)
            endpoint = req_str[start:end]
            response = web.process_api_call(endpoint, req_bytes)

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
      except OSError as e:
        conn.close()
        print('Connection closed')

loop = asyncio.get_event_loop()
loop.create_task(check_buttons_loop())
loop.run_until_complete(web_server_loop())