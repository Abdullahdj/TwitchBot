import socket
import time
import threading

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "moistmachine_420"
PASS = ""
CHAN = "flambr0s"

# Naughts and crosses stuff here
select = {"tl":'-', "tm":'-', "tr":'-', "ml":'-',
          "m":'-', "mr":'-', "bl":'-', "bm":'-', "br":'-'}



board = f"""| {select["tl"]} | {select["tm"]} | {select["tr"]} |
| {select["ml"]} | {select["m"]} | {select["mr"]} | 
| {select["bl"]} | {select["bm"]} | {select["br"]} | 
"""

turn = 'x'
new = 'o'

def clearBoard():
    global select
    select = {"tl":'-', "tm":'-', "tr":'-', "ml":'-',
          "m":'-', "mr":'-', "bl":'-', "bm":'-', "br":'-'}
    updateBoard()

def updateBoard():
    global board, select
    board = f"""| {select["tl"]} | {select["tm"]} | {select["tr"]} |
    | {select["ml"]} | {select["m"]} | {select["mr"]} | 
    | {select["bl"]} | {select["bm"]} | {select["br"]} | 
    """

# Rotate turn
def rotateTurn():
    global turn, new
    temp = turn
    turn = new
    new = temp

# Show the board
def printBoard(s):
    global board
    for line in str.splitlines(board):
        send_privmsg(s, line)

# Use a dictionary to reduce if statements
def makeTurn(s, location):
    global select, board
    try:
        if select[location] == '-':
            select[location] = turn
            rotateTurn()
        else:
            send_privmsg(s, "This place is already occupied!")
    except KeyError:
        send_privmsg(s, "Not a valid position. Stop trying to break me!")
    updateBoard()
    printBoard(s)
    finish = checkWin(s)
    if finish:
        clearBoard()
        select["tr"] = "-"
        printBoard(s)

# Check if there is a winner or draw
def checkWin(s):
    global select, new
    if select["tr"] == select["tm"] == select["tl"] != "-":
        send_privmsg(s, f"Congratulations, {new} wins!")
    elif select["ml"] == select["m"] == select["mr"] != "-":
        send_privmsg(s, f"Congratulations, {new} wins!")
    elif select["bl"] == select["bm"] == select["br"] != "-":
        send_privmsg(s, f"Congratulations, {new} wins!")
    elif select["tl"] == select["ml"] == select["bl"] != "-":
        send_privmsg(s, f"Congratulations, {new} wins!")
    elif select["tm"] == select["m"] == select["bm"] != "-":
        send_privmsg(s, f"Congratulations, {new} wins!")
    elif select["tr"] == select["mr"] == select["br"] != "-":
        send_privmsg(s, f"Congratulations, {new} wins!")
    elif select["br"] == select["m"] == select["tl"] != "-":
        send_privmsg(s, f"Congratulations, {new} wins!")
    elif select["bl"] == select["m"] == select["tr"] != "-":
        send_privmsg(s, f"Congratulations, {new} wins!")
    else:
        placesOccupied = 0
        for key in select:
            if select[key] != "-":
                placesOccupied+=1
        if placesOccupied == 9:
            send_privmsg(s, "Its a draw!")
        else:
            return False
    return True

def send_privmsg(s, text):
    send_command(s, f'PRIVMSG #{CHAN} :{text}')

def send_command(s, command):
    print(f'< {command}')
    s.send((command + '\r\n').encode())

def connect():
    irc = socket.socket()
    irc.connect((HOST, PORT))
    send_command(irc, f'PASS {PASS}')
    send_command(irc, f'NICK {NICK}')
    send_command(irc, f'JOIN #{CHAN}')
    send_privmsg(irc, 'BeepBoop I am online')
    waitThread = threading.Thread(target=sendOnPeriod, args=[irc])
    waitThread.start()
    loop_for_messages(irc)

def handle_message(s, received_msg):
    if len(received_msg) == 0:
        return
    print(f'> {received_msg}')
    if received_msg.split(':')[-1].lower() == 'moisturise me':
        send_privmsg(s, "I got you homie. Thats what bros are for!")
        time.sleep(1)
        send_privmsg(s, "*unzips pants*")
        send_privmsg(s, "Open wide")
    if received_msg == 'PING :tmi.twitch.tv':
        send_command(s, 'PONG :tmi.twitch.tv')
    if received_msg.split(':')[-1].lower()[0:5] == 'slap ':
        send_privmsg(s, "YO " + received_msg.split(':')[-1][5:] + " you just been SLAPPED DUDE.")
    if received_msg.split(':')[-1].lower() == '!discord':
        send_privmsg(s, "Be sure to join the discord on https://discord.com/invite/XFDWgnHceD or use the panels below")
    
    # Create a naughts and crosses bot game
    if received_msg.split(':')[-1].lower()[:6] == '!board':
        printBoard(s)
    if received_msg.split(':')[-1].lower()[:5] == '!turn':
        location = received_msg.split(':')[-1].lower()[5:]
        makeTurn(s, location.replace(" ", ""))
    if received_msg.split(':')[-1].lower()[:5] == '!help':
        send_privmsg(s, "To make a turn, type !turn followed by one of the following on the same line:")
        send_privmsg(s, "tl, tm, tr, ml, m, mr, bl, bm, br")
        send_privmsg(s, "Type !board to show the board.")

def loop_for_messages(s):
    while True:
        received_msgs = s.recv(2048).decode()
        for received_msg in received_msgs.split('\r\n'):
            handle_message(s, received_msg)

def sendMessage(sock, message):
    print(f"<{message}")
    sock.send((message + '\r\n').encode())

def sendOnPeriod(s):
    startTime = time.time()
    while True:
        send_privmsg(s, "Be sure to join the discord on https://discord.com/invite/XFDWgnHceD or use the panels below")
        time.sleep(60*30)

def main():
    s = connect()

if __name__ == "__main__":
    main()
