import socket
import struct
import time

import socket
import threading
import os


bool_ban_menu_xbox_left=True
bool_ban_menu_xbox_right=False


int_index_allowed_min=0
int_index_allowed_max=4

BOOL_USE_PRINT = True
def is_ssh():
    return "SSH_CONNECTION" in os.environ or "SSH_TTY" in os.environ

def ssh_print(text, *args):
    if BOOL_USE_PRINT:
        print(text, *args)
BOOL_USE_PRINT = is_ssh()

# IF YOU  WANT TO LISTEN TO THE WORLD
LISTEN_TEXT_IPV4 = "0.0.0.0"
# IF YOU WANT TO LISTEN TO LOCALHOST ONLY
LISTEN_TEXT_IPV4 = "127.0.0.1"

# RELAY THE INTEGER TO THE TARGET IID LISTENER
SERVER_UDP_IPV4 = "127.0.0.1"

LISTEN_TEXT_PORT = 3614
SERVER_UDP_PORT = 3615

bool_use_print= False

def ssh_print(text, *args):
    if bool_use_print:
        print(text, *args)

# sudo nano /lib/systemd/system/scratch_to_warcraft_interpretor.service
"""
[Unit]
Description=Interpretor for Xbox Controller and keyboard to play games from integer standard.
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /git/scratch_to_warcraft_interpretor/RunInterpretor.py
Restart=always
User=root
WorkingDirectory=/git/scratch_to_warcraft_interpretor

[Install]
WantedBy=multi-user.target
"""
#1h
# sudo nano /etc/systemd/system/scratch_to_warcraft_interpretor.timer
"""
[Unit]
Description=Check that the script is Text to integer scratch to wow timer.

[Timer]
OnBootSec=0min
OnUnitActiveSec=10s

[Install]
WantedBy=timers.target
"""
# Learn: https://youtu.be/nvx9jJhSELQ?t=368
# cd /lib/systemd/system/
# sudo systemctl daemon-reload
# sudo systemctl enable scratch_to_warcraft_interpretor.service
# chmod +x /git/scratch_to_warcraft_interpretor/RunInterpretor.py
# sudo systemctl enable scratch_to_warcraft_interpretor.service
# sudo systemctl start scratch_to_warcraft_interpretor.service
# sudo systemctl status scratch_to_warcraft_interpretor.service
# sudo systemctl stop scratch_to_warcraft_interpretor.service
# sudo systemctl restart scratch_to_warcraft_interpretor.service

# sudo systemctl enable scratch_to_warcraft_interpretor.timer
# sudo systemctl start scratch_to_warcraft_interpretor.timer
# sudo systemctl status scratch_to_warcraft_interpretor.timer

# sudo systemctl list-timers | grep scratch_to_warcraft_interpretor


# The code use a listen port and can't work with two instances at the same time.
#># sudo systemctl stop scratch_to_warcraft_interpretor.timer
#># sudo systemctl stop scratch_to_warcraft_interpretor.service

#># sudo systemctl start scratch_to_warcraft_interpretor.timer
#># sudo systemctl start scratch_to_warcraft_interpretor.service



def get_time_in_milliseconds():
    return time.time() * 1000

CURRENT_TIME = get_time_in_milliseconds()



class WaitingShortcut:
    def __init__(self, shortcut, time_in_milliseconds, delay_in_milliseconds ):
        self.shortcut_text = shortcut
        self.local_time_created = time_in_milliseconds
        self.local_time_to_execute = time_in_milliseconds + delay_in_milliseconds
    
    def is_ready(self, current_time):
        return current_time >= self.local_time_to_execute
   
    def get_shortcut(self): 
        return self.shortcut_text


class QueueOfShortcuts:
    def __init__(self):
        self.list = list()
        
    def append_at_0(self, shortcut):
        self.list.insert(0, shortcut)
    
    def has_waiting_shortcut(self):
        return len(self.list)>0
    
    def check_for_shortcut_to_extract(self, current_time):
        list_result = list()
        int_index= len(self.list)-1
        while int_index>=0:
            shortcut = self.list[int_index]
            if shortcut.is_ready(current_time):
                list_result.append(shortcut)
                self.list.pop(int_index)
            int_index-=1
            
        return list_result

    def clear (self):
        self.list.clear()


in_queue_shortcut = QueueOfShortcuts()

def push_shortcut_to_queue(shortcut_text, delay_in_milliseconds):
    in_queue_shortcut.append_at_0(WaitingShortcut(shortcut_text, get_time_in_milliseconds(), delay_in_milliseconds))


def push_shortcut_to_queue_at_localTime(shortcut_text, time_in_milliseconds, delay_in_milliseconds):
    in_queue_shortcut.append_at_0(WaitingShortcut(shortcut_text, time_in_milliseconds, delay_in_milliseconds))



def check_the_queue_for_shortcuts():
    if not in_queue_shortcut.has_waiting_shortcut():
        return
    
    global CURRENT_TIME
    CURRENT_TIME = get_time_in_milliseconds()
    for s in in_queue_shortcut.check_for_shortcut_to_extract(CURRENT_TIME):
        ssh_print("Shortcut delayed: ", s.get_shortcut())
        push_text_to_interpretor(s.get_shortcut())

def is_integer_ban(integer):
    if bool_ban_menu_xbox_left and integer==XboxIntegerAction.press_menu_left:
        return True
    if bool_ban_menu_xbox_left and integer==XboxIntegerAction.press_menu_left+1000:
        return True
    if bool_ban_menu_xbox_right and integer==XboxIntegerAction.press_menu_right:
        return True
    if bool_ban_menu_xbox_right and integer==XboxIntegerAction.press_menu_right+1000:
        return True
    return False

def is_index_ban(index):
    if index<int_index_allowed_min:
        return True
    if index>int_index_allowed_max:
        return True
    return False


def send_udp_integer(integer):
    
    if is_integer_ban(integer):
        return
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = struct.pack("<i", integer)
    sock.sendto(message, (SERVER_UDP_IPV4,SERVER_UDP_PORT))
    sock.close()
    ssh_print("Sent: ", integer)


def send_udp_index_integer( index, integer):
    if is_integer_ban(integer):
        return
    if is_index_ban(index):
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = struct.pack("<ii", index, integer)
    sock.sendto(message, (SERVER_UDP_IPV4,SERVER_UDP_PORT))
    sock.close()
    ssh_print("Sent: ", index, integer)
    
def i(int_value):
    send_udp_integer(int_value)

def ii(index, int_value):
    send_udp_index_integer(index, int_value)


def ii_pr(index, int_value):
    ii(index, int_value)
    ii(index, int_value+1000)
    
def i_pr(int_value):
    i(int_value)
    i(int_value+1000)

def i_p(value):
    i(value)
def i_r(value):
    i(value+1000)
    
def ii_p(index, value):
    ii(index, value)
def ii_r(index, value):
    ii(index, value+1000)
    
step_time = 0.5
def push_all_debug(text, press_integer):
    
    ssh_print("Release:", text)
    i(press_integer)
    time.sleep(step_time)
    ssh_print("Release:", text)
    i(press_integer+1000)
    time.sleep(step_time)

class StringLinkToInteger:
    def __init__(self, string_id, integer_id):
        self.string_id = string_id
        self.integer_id = integer_id
  
class XboxIntegerAction:
            random_input =  1399
            release_all =  1390
            release_all_but_menu =  1391
            press_a =  1300
            press_x =  1301
            press_b =  1302
            press_y =  1303
            press_left_side_button =  1304
            press_right_side_button =  1305
            press_left_stick =  1306
            press_right_stick =  1307
            press_menu_right =  1308
            press_menu_left =  1309
            release_dpad =  1310
            press_arrow_north =  1311
            press_arrow_northeast =  1312
            press_arrow_east =  1313
            press_arrow_southeast =  1314
            press_arrow_south =  1315
            press_arrow_southwest =  1316
            press_arrow_west =  1317
            press_arrow_northwest =  1318
            press_xbox_home_button =  1319
            random_axis =  1320
            start_recording =  1321
            set_left_stick_neutral =  1330
            set_left_stick_up =  1331
            set_left_stick_up_right =  1332
            set_left_stick_right =  1333
            set_left_stick_down_right =  1334
            set_left_stick_down =  1335
            set_left_stick_down_left =  1336
            set_left_stick_left =  1337
            set_left_stick_up_left =  1338
            set_right_stick_neutral =  1340
            set_right_stick_up =  1341
            set_right_stick_up_right =  1342
            set_right_stick_right =  1343
            set_right_stick_down_right =  1344
            set_right_stick_down =  1345
            set_right_stick_down_left =  1346
            set_right_stick_left =  1347
            set_right_stick_up_left =  1348
            set_left_stick_horizontal_100 =  1350
            set_left_stick_horizontal_neg_100 =  1351
            set_left_stick_vertical_100 =  1352
            set_left_stick_vertical_neg_100 =  1353
            set_right_stick_horizontal_100 =  1354
            set_right_stick_horizontal_neg_100 =  1355
            set_right_stick_vertical_100 =  1356
            set_right_stick_vertical_neg_100 =  1357
            set_left_trigger_100 =  1358
            set_right_trigger_100 =  1359
            set_left_stick_horizontal_075 =  1360
            set_left_stick_horizontal_neg_075 =  1361
            set_left_stick_vertical_075 =  1362
            set_left_stick_vertical_neg_075 =  1363
            set_right_stick_horizontal_075 =  1364
            set_right_stick_horizontal_neg_075 =  1365
            set_right_stick_vertical_075 =  1366
            set_right_stick_vertical_neg_075 =  1367
            set_left_trigger_075 =  1368
            set_right_trigger_075 =  1369
            set_left_stick_horizontal_050 =  1370
            set_left_stick_horizontal_neg_050 =  1371
            set_left_stick_vertical_050 =  1372
            set_left_stick_vertical_neg_050 =  1373
            set_right_stick_horizontal_050 =  1374
            set_right_stick_horizontal_neg_050 =  1375
            set_right_stick_vertical_050 =  1376
            set_right_stick_vertical_neg_050 =  1377
            set_left_trigger_050 =  1378
            set_right_trigger_050 =  1379
            set_left_stick_horizontal_025 =  1380
            set_left_stick_horizontal_neg_025 =  1381
            set_left_stick_vertical_025 =  1382
            set_left_stick_vertical_neg_025 =  1383
            set_right_stick_horizontal_025 =  1384
            set_right_stick_horizontal_neg_025 =  1385
            set_right_stick_vertical_025 =  1386
            set_right_stick_vertical_neg_025 =  1387
            set_left_trigger_025 =  1388
            set_right_trigger_025 =  1389
            
            
            # Callable by text (duplicate it and make your own version)
            dictionary = {}
            dictionary["random_input"] =  random_input
            dictionary["press_a"] =  press_a
            dictionary["press_x"] =  press_x
            dictionary["press_b"] =  press_b
            dictionary["press_y"] =  press_y
            dictionary["press_left_side_button"] =  press_left_side_button
            dictionary["press_right_side_button"] =  press_right_side_button
            dictionary["press_left_stick"] =  press_left_stick
            dictionary["press_right_stick"] =  press_right_stick
            dictionary["press_menu_right"] =  press_menu_right
            dictionary["press_menu_left"] =  press_menu_left
            dictionary["release_dpad"] =  release_dpad
            dictionary["press_arrow_north"] =  press_arrow_north
            dictionary["press_arrow_northeast"] =  press_arrow_northeast
            dictionary["press_arrow_east"] =  press_arrow_east
            dictionary["press_arrow_southeast"] =  press_arrow_southeast
            dictionary["press_arrow_south"] =  press_arrow_south
            dictionary["press_arrow_southwest"] =  press_arrow_southwest
            dictionary["press_arrow_west"] =  press_arrow_west
            dictionary["press_arrow_northwest"] =  press_arrow_northwest
            dictionary["press_xbox_home_button"] =  press_xbox_home_button
            dictionary["random_axis"] =  random_axis
            dictionary["start_recording"] =  start_recording
            dictionary["set_left_stick_neutral"] =  set_left_stick_neutral
            dictionary["set_left_stick_up"] =  set_left_stick_up
            dictionary["set_left_stick_up_right"] =  set_left_stick_up_right
            dictionary["set_left_stick_right"] =  set_left_stick_right
            dictionary["set_left_stick_down_right"] =  set_left_stick_down_right
            dictionary["set_left_stick_down"] =  set_left_stick_down
            dictionary["set_left_stick_down_left"] =  set_left_stick_down_left
            dictionary["set_left_stick_left"] =  set_left_stick_left
            dictionary["set_left_stick_up_left"] =  set_left_stick_up_left
            dictionary["set_right_stick_neutral"] =  set_right_stick_neutral
            dictionary["set_right_stick_up"] =  set_right_stick_up
            dictionary["set_right_stick_up_right"] =  set_right_stick_up_right
            dictionary["set_right_stick_right"] =  set_right_stick_right
            dictionary["set_right_stick_down_right"] =  set_right_stick_down_right
            dictionary["set_right_stick_down"] =  set_right_stick_down
            dictionary["set_right_stick_down_left"] =  set_right_stick_down_left
            dictionary["set_right_stick_left"] =  set_right_stick_left
            dictionary["set_right_stick_up_left"] =  set_right_stick_up_left
            dictionary["set_left_stick_horizontal_100"] =  set_left_stick_horizontal_100
            dictionary["set_left_stick_horizontal_neg_100"] =  set_left_stick_horizontal_neg_100
            dictionary["set_left_stick_vertical_100"] =  set_left_stick_vertical_100
            dictionary["set_left_stick_vertical_neg_100"] =  set_left_stick_vertical_neg_100
            dictionary["set_right_stick_horizontal_100"] =  set_right_stick_horizontal_100
            dictionary["set_right_stick_horizontal_neg_100"] =  set_right_stick_horizontal_neg_100
            dictionary["set_right_stick_vertical_100"] =  set_right_stick_vertical_100
            dictionary["set_right_stick_vertical_neg_100"] =  set_right_stick_vertical_neg_100
            dictionary["set_left_trigger_100"] =  set_left_trigger_100
            dictionary["set_right_trigger_100"] =  set_right_trigger_100
            dictionary["set_left_stick_horizontal_075"] =  set_left_stick_horizontal_075
            dictionary["set_left_stick_horizontal_neg_075"] =  set_left_stick_horizontal_neg_075
            dictionary["set_left_stick_vertical_075"] =  set_left_stick_vertical_075
            dictionary["set_left_stick_vertical_neg_075"] =  set_left_stick_vertical_neg_075
            dictionary["set_right_stick_horizontal_075"] =  set_right_stick_horizontal_075
            dictionary["set_right_stick_horizontal_neg_075"] =  set_right_stick_horizontal_neg_075
            dictionary["set_right_stick_vertical_075"] =  set_right_stick_vertical_075
            dictionary["set_right_stick_vertical_neg_075"] =  set_right_stick_vertical_neg_075
            dictionary["set_left_trigger_075"] =  set_left_trigger_075
            dictionary["set_right_trigger_075"] =  set_right_trigger_075
            dictionary["set_left_stick_horizontal_050"] =  set_left_stick_horizontal_050
            dictionary["set_left_stick_horizontal_neg_050"] =  set_left_stick_horizontal_neg_050
            dictionary["set_left_stick_vertical_050"] =  set_left_stick_vertical_050
            dictionary["set_left_stick_vertical_neg_050"] =  set_left_stick_vertical_neg_050
            dictionary["set_right_stick_horizontal_050"] =  set_right_stick_horizontal_050
            dictionary["set_right_stick_horizontal_neg_050"] =  set_right_stick_horizontal_neg_050
            dictionary["set_right_stick_vertical_050"] =  set_right_stick_vertical_050
            dictionary["set_right_stick_vertical_neg_050"] =  set_right_stick_vertical_neg_050
            dictionary["set_left_trigger_050"] =  set_left_trigger_050
            dictionary["set_right_trigger_050"] =  set_right_trigger_050
            dictionary["set_left_stick_horizontal_025"] =  set_left_stick_horizontal_025
            dictionary["set_left_stick_horizontal_neg_025"] =  set_left_stick_horizontal_neg_025
            dictionary["set_left_stick_vertical_025"] =  set_left_stick_vertical_025
            dictionary["set_left_stick_vertical_neg_025"] =  set_left_stick_vertical_neg_025
            dictionary["set_right_stick_horizontal_025"] =  set_right_stick_horizontal_025
            dictionary["set_right_stick_horizontal_neg_025"] =  set_right_stick_horizontal_neg_025
            dictionary["set_right_stick_vertical_025"] =  set_right_stick_vertical_025
            dictionary["set_right_stick_vertical_neg_025"] =  set_right_stick_vertical_neg_025
            
            dictionary["release"]= release_all_but_menu
            dictionary["off"] = release_all_but_menu
            dictionary["r"] =  random_input
            dictionary["a"] =  press_a
            dictionary["x"] =  press_x
            dictionary["b"] =  press_b
            dictionary["y"] =  press_y
            #!s sbr+ 80> sbr- 1000> sbr+ 80> sbr- 1000>  sbr+ 80> sbr- 1000> 
            dictionary["slb"] =  press_left_side_button
            dictionary["srb"] =  press_right_side_button
            dictionary["sbl"] =  press_left_side_button
            dictionary["sbr"] =  press_right_side_button
            dictionary["ls"] =  press_left_stick
            dictionary["sl"] =  press_left_stick
            dictionary["rs"] =  press_right_stick
            dictionary["sr"] =  press_right_stick
            dictionary["mr"] =  press_menu_right
            dictionary["ml"] =  press_menu_left
            dictionary["ac"] =  release_dpad
            dictionary["an"] =  press_arrow_north
            dictionary["ane"] =  press_arrow_northeast
            dictionary["ae"] =  press_arrow_east
            dictionary["ase"] =  press_arrow_southeast
            dictionary["as"] =  press_arrow_south
            dictionary["asw"] =  press_arrow_southwest
            dictionary["aw"] =  press_arrow_west
            dictionary["anw"] =  press_arrow_northwest
            dictionary["home"] =  press_xbox_home_button
            dictionary["rx"] =  random_axis
            
            dictionary["jlc"] =  set_left_stick_neutral
            dictionary["jln"] =  set_left_stick_up
            dictionary["jlne"] =  set_left_stick_up_right
            dictionary["jlen"] =  set_left_stick_up_right
            
            dictionary["jle"] =  set_left_stick_right
            dictionary["jlse"] =  set_left_stick_down_right
            dictionary["jles"] =  set_left_stick_down_right
            dictionary["jls"] =  set_left_stick_down
            dictionary["jlsw"] =  set_left_stick_down_left
            dictionary["jlws"] =  set_left_stick_down_left
            dictionary["jlw"] =  set_left_stick_left
            dictionary["jlnw"] =  set_left_stick_up_left
            dictionary["jlwn"] =  set_left_stick_up_left
            dictionary["jrc"] =  set_right_stick_neutral
            dictionary["jrn"] =  set_right_stick_up
            dictionary["jrne"] =  set_right_stick_up_right
            dictionary["jren"] =  set_right_stick_up_right
            dictionary["jre"] =  set_right_stick_right
            dictionary["jrse"] =  set_right_stick_down_right
            dictionary["jres"] =  set_right_stick_down_right
            dictionary["jrs"] =  set_right_stick_down
            dictionary["jrsw"] =  set_right_stick_down_left
            dictionary["jrws"] =  set_right_stick_down_left
            dictionary["jrw"] =  set_right_stick_left
            dictionary["jrnw"] =  set_right_stick_up_left
            dictionary["jrwn"] =  set_right_stick_up_left

            
            # Steath Bastar
            # dictionary["left"] =  set_left_stick_left
            # dictionary["right"] =  set_left_stick_down
            # dictionary["down"] =  set_left_stick_down
            # dictionary["up"] =  set_left_stick_up
            # dictionary["jump"] =  press_a
            # dictionary["crouch"] =  press_b
            # dictionary["release"] = 1399
            
            dictionary["jlh+100"]=set_left_stick_horizontal_100
            dictionary["jlh-100"]=set_left_stick_horizontal_neg_100
            dictionary["jlv+100"]=set_left_stick_vertical_100
            dictionary["jlv-100"]=set_left_stick_vertical_neg_100
            dictionary["jrh+100"]=set_right_stick_horizontal_100
            dictionary["jrh-100"]=set_right_stick_horizontal_neg_100
            dictionary["jrv+100"]=set_right_stick_vertical_100
            dictionary["jrv-100"]=set_right_stick_vertical_neg_100
            dictionary["lt+100"]=set_left_trigger_100
            dictionary["rt+100"]=set_right_trigger_100
            dictionary["jlh+075"]=set_left_stick_horizontal_075
            dictionary["jlh-075"]=set_left_stick_horizontal_neg_075
            dictionary["jlv+075"]=set_left_stick_vertical_075
            dictionary["jlv-075"]=set_left_stick_vertical_neg_075
            dictionary["jrh+075"]=set_right_stick_horizontal_075
            dictionary["jrh-075"]=set_right_stick_horizontal_neg_075
            dictionary["jrv+075"]=set_right_stick_vertical_075
            dictionary["jrv-075"]=set_right_stick_vertical_neg_075
            dictionary["lt+075"]=set_left_trigger_075
            dictionary["rt+075"]=set_right_trigger_075
            dictionary["jlh+050"]=set_left_stick_horizontal_050
            dictionary["jlh-050"]=set_left_stick_horizontal_neg_050
            dictionary["jlv+050"]=set_left_stick_vertical_050
            dictionary["jlv-050"]=set_left_stick_vertical_neg_050
            dictionary["jrh+050"]=set_right_stick_horizontal_050
            dictionary["jrh-050"]=set_right_stick_horizontal_neg_050
            dictionary["jrv+050"]=set_right_stick_vertical_050
            dictionary["jrv-050"]=set_right_stick_vertical_neg_050
            dictionary["lt+050"]=set_left_trigger_050
            dictionary["rt+050"]=set_right_trigger_050
            dictionary["jlh+025"]=set_left_stick_horizontal_025
            dictionary["jlh-025"]=set_left_stick_horizontal_neg_025
            dictionary["jlv+025"]=set_left_stick_vertical_025
            dictionary["jlv-025"]=set_left_stick_vertical_neg_025
            dictionary["jrh+025"]=set_right_stick_horizontal_025
            dictionary["jrh-025"]=set_right_stick_horizontal_neg_025
            dictionary["jrv+025"]=set_right_stick_vertical_025
            dictionary["jrv-025"]=set_right_stick_vertical_neg_025
            dictionary["lt+025"]=set_left_trigger_025
            dictionary["rt+025"]=set_right_trigger_025
            
            dictionary["r1"] =press_right_side_button
            dictionary["r2"] =set_right_trigger_100
            dictionary["l1"] =press_left_side_button
            dictionary["l2"] =set_left_trigger_100
            
            dictionary["al"]=press_arrow_west
            dictionary["ar"]=press_arrow_east
            dictionary["au"]=press_arrow_north
            dictionary["ad"]=press_arrow_south
            dictionary["ac"]=release_dpad
            
            dictionary["br"]= press_b
            dictionary["bd"]= press_a
            dictionary["bl"]= press_x
            dictionary["bu"]= press_y
            
            dictionary["jlr"]= set_left_stick_right 
            dictionary["jll"]= set_left_stick_left
            dictionary["jlu"]= set_left_stick_up
            dictionary["jld"]= set_left_stick_down
            
            dictionary["jrr"]= set_right_stick_right
            dictionary["jrl"]= set_right_stick_left
            dictionary["jru"]= set_right_stick_up
            dictionary["jrd"]= set_right_stick_down
            
            dictionary["jr"]= press_right_stick
            dictionary["jl"]= press_left_stick
            
            dictionary["tl"]= set_left_trigger_100
            dictionary["tr"]= set_right_trigger_100
            dictionary["lt"]= set_left_trigger_100
            dictionary["rt"]= set_right_trigger_100
            
            
def select_character():
    # Validate character selection
    push_all_debug("A", XboxIntegerAction.press_a)
    time.sleep(2)
    push_all_debug("A", XboxIntegerAction.press_a)
    time.sleep(2)
    ii_pr(1, XboxIntegerAction.press_a)
    ii_pr(2, XboxIntegerAction.press_arrow_north)
    ii_pr(2, XboxIntegerAction.press_a)
            
            

def push_text_to_interpretor(text):
        time= get_time_in_milliseconds()
        delay=0 
        print (f"Humm: ({text})")
        #print ("------------------------------: ")
        
        tokens = text.split(" ")
        ssh_print("Tokens: ", tokens)
        for t in tokens:
            
            if len(t)==1:
                ssh_print("Char CMD:", t)
                
            text=text.lower()
            if push_conditional_key_to_shortcut(t):
                continue
            
            if t.lower()== "clear":
                ssh_print("Clearing the queue")
                in_queue_shortcut.clear()
                continue
            if t.endswith(">"):
                t= t.replace(">", "")
                try :
                    int_ms = int(t)
                    delay += int_ms
                except ValueError:
                    continue
                ssh_print("Delay: ", t)
                continue
            else:
                if delay==0:
                    push_shortcut_to_interpretor(t)
                else :
                    push_shortcut_to_queue_at_localTime(t, time, delay)
            
    
def push_shortcut_to_interpretor(shorcut):
            ssh_print("Executing: ", shorcut)
            #print ("############ ")
            #ssh_print("\n\n\nToken: ", t)
            try:
                int_value = int(shorcut)
                ssh_print("Found: ", int_value)
                i(int_value)
            except ValueError:
                pass
            
            bool_p1 = shorcut.find("_1")>-1
            bool_p2 = shorcut.find("_2")>-1
            bool_p3 = shorcut.find("_3")>-1
            bool_p4 = shorcut.find("_4")>-1
            bool_all = not bool_p1 and not bool_p2 and not bool_p3 and not bool_p4
            bool_pressed = shorcut.find("+")>-1 or shorcut.find("*")>-1
            bool_release = shorcut.find("-")>-1 or shorcut.find("*")>-1
            
            #print (f"PR: {bool_pressed},{bool_release}")
    
            shorcut= shorcut.replace("+", "")
            shorcut= shorcut.replace("-", "")
            shorcut= shorcut.replace("*", "")
            if bool_p1:
                shorcut = shorcut.replace("_1", "")
            if bool_p2:
                shorcut = shorcut.replace("_2", "")
            if bool_p3:
                shorcut = shorcut.replace("_3", "")
            if bool_p4:
                shorcut = shorcut.replace("_4", "")
            
            
            if not bool_pressed and not bool_release:
                bool_pressed = True
                bool_release = True
                
            shorcut = XboxIntegerAction.dictionary.get(shorcut, None)
            if shorcut is not None:    
                ssh_print("Found: ", shorcut)
                
                if bool_pressed:
                    if bool_all:
                        i(shorcut)
                    else :
                        if bool_p1:
                            ii(1, shorcut)
                        if bool_p2:
                            ii(2, shorcut)
                        if bool_p3:
                            ii(3, shorcut)
                        if bool_p4:
                            ii(4, shorcut)
                if bool_release:
                    if bool_all:
                        i(shorcut+1000)
                    else :
                        if bool_p1:
                            ii(1, shorcut+1000)
                        if bool_p2:
                            ii(2, shorcut+1000)
                        if bool_p3:
                            ii(3, shorcut+1000)
                        if bool_p4:
                            ii(4, shorcut+1000)
                            
                            

dico_key_to_shortcut = {}
dico_key_to_shortcut["z"] = "jlu+ 200> jlu-"
dico_key_to_shortcut["i"] = "jlu+ 200> jlu-"
dico_key_to_shortcut["s"] = "jld+ 200> jld-"
dico_key_to_shortcut["k"] = "jld+ 200> jld-"
dico_key_to_shortcut["q"] = "jll+ 200> jll-"
dico_key_to_shortcut["j"] = "jll+ 200> jll-"
dico_key_to_shortcut["d"] = "jlr+ 200> jlr-"
dico_key_to_shortcut["l"] = "jlr+ 200> jlr-"
dico_key_to_shortcut["e"] = "R1+ 200> R1-"
dico_key_to_shortcut["o"] = "R1+ 200> R1-"
dico_key_to_shortcut["i"] = "a"
dico_key_to_shortcut["w"] = ""
dico_key_to_shortcut["c"] = ""
dico_key_to_shortcut["r"] = "sbl+ 200> sbl-"
dico_key_to_shortcut["f"] = "sbr+ 200> sbr-"

dico_key_to_shortcut["Z"] = "jlu+ 50> jlu-"
dico_key_to_shortcut["S"] = "jld+ 50> jld-"
dico_key_to_shortcut["Q"] = "jll+ 50> jll-"
dico_key_to_shortcut["D"] = "jlr+ 50> jlr-"
dico_key_to_shortcut["E"] = "R1+ 50> R1-"
dico_key_to_shortcut["W"] = ""
dico_key_to_shortcut["C"] = ""
dico_key_to_shortcut["R"] = "sbl+ 50> sbl-"
dico_key_to_shortcut["F"] = "sbr+ 50> sbr-"

dico_key_to_shortcut["roll"] = "B+ 100> B-"
dico_key_to_shortcut["attack"] = "sbr+ 100> sbr-"

dico_key_to_shortcut["è"]  = "A+ 100> A-"
dico_key_to_shortcut["7"]  = "A+ 100> A-"
dico_key_to_shortcut["!"]  = "X+ 100> X-"
dico_key_to_shortcut["8"]  = "X+ 100> X-"
dico_key_to_shortcut["ç"]  = "B+ 100> B-"
dico_key_to_shortcut["9"]  = "B+ 100> B-"
dico_key_to_shortcut["à"]  = "y+ 100> Y-"
dico_key_to_shortcut["0"]  = "y+ 100> Y-"

dico_key_to_shortcut["&"]  = "au+ 100> au-"
dico_key_to_shortcut["1"]  = "ad+ 100> ad-"
dico_key_to_shortcut["é"]  = "al+ 100> al-"
dico_key_to_shortcut["é"]  = "al+ 100> al-"
dico_key_to_shortcut["\""] = "ar+ 100> ar-"
dico_key_to_shortcut["3"] = "ar+ 100> ar-"
dico_key_to_shortcut["'"]  = "ad+ 100> ad-"
dico_key_to_shortcut["4"]  = "ad+ 100> ad-"


dico_key_to_shortcut["("] = "jl+ 100> jl-"
dico_key_to_shortcut["5"] = "jl+ 100> jl-"
dico_key_to_shortcut["§"] = "jr+ 100> jr-"
dico_key_to_shortcut["6"] = "jl+ 100> jl-"

dico_key_to_shortcut["è"] = "sbl+ 100> sbl-"
dico_key_to_shortcut["!"] = "sbr2+ 100> sbr-"

#Clear
dico_key_to_shortcut["c"] = "clear+ 100> clear-"
dico_key_to_shortcut["clear"] = "clear+ 100> clear-"

#Release
dico_key_to_shortcut["r"] = "clear+ 100> clear-"
dico_key_to_shortcut["release"] = "clear+ 100> clear-"
                   
                            
def push_conditional_key_to_shortcut(text):
    shortcut = dico_key_to_shortcut.get(text, None)
    if shortcut is not None:
        push_text_to_interpretor(shortcut)
        return True
    return False

                            
import random                           
if __name__ == "__main__":
    
    
    # select_character()
    
    def listen_udp_messages():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((LISTEN_TEXT_IPV4, LISTEN_TEXT_PORT))
        while True:
            data, addr = sock.recvfrom(1024)
            text = data.decode()
            print ("Received: ", text)
            push_text_to_interpretor(text)

    listener_thread = threading.Thread(target=listen_udp_messages)
    listener_thread.daemon = True
    listener_thread.start()

    bool_use_while_true = False
    if bool_use_while_true:
        while True:
            list = ["a","b","x", "y"] 
            random.shuffle(list)
            for item in list:
                push_text_to_interpretor(item)
                time.sleep(2)
    
    
    bool_use_console=False
    if bool_use_console:
        while True:
            text = input("Enter text: ")
            push_text_to_interpretor(text)
        
    
    while True:
        check_the_queue_for_shortcuts()
        time.sleep(1)
    
            
            
            
            

            