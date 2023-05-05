import socket
import sys
from _thread import *
import threading
import random
import os
import Protocol
import pygame
import time
import math
from Player import *

IMAGE = ""
READ_CHUNK = 2048
BASE_PORT = 20000
HOST = "0.0.0.0"

PARENT_DIR = os.getcwd()


players_dict = {}
sentences = [
    ("Memories consume like opening the wound, I'm picking me apart again. You all assume, I'm safe here in my room, unless I try to start again.",
     "Linkin Park - Breaking the Habit", os.path.join(PARENT_DIR, "Pictures\\Meteora.png")),
    ("The enemy ascended beyond your control, or was that all your intention? They have managed to demolish whatever we made, but you're failing to comprehend.",
     "DM DOKURO - Roar of the Jungle Dragon", os.path.join(PARENT_DIR, "Pictures\\The Tale of a Cruel World.png")),
    ("I'm so tired of being here, suppressed by all my childish fears, and if you have to leave, I wish that you would just leave, 'cause your presence still lingers here, and it won't leave me alone.",
     "Evanescence - My Immortal", os.path.join(PARENT_DIR, "Pictures\\Fallen.png")),
    ("All of my hate cannot be found, I will not be drowned by your thoughtless scheming. So you can try to tear me down, beat me to the ground, I will see you screaming.",
     "Korn - Thoughtless", os.path.join(PARENT_DIR, "Pictures\\Untouchable.png")),
    ("First comes the blessing of all that you've dreamed, but then comes the curses of diamonds and rings. Only at first did it have its appeal, But now you can't tell the false from the real.",
     "Imagine Dragons - Gold", os.path.join(PARENT_DIR, "Pictures\\Smokes + Mirrors.png")),
    ("Master of puppets, I'm pulling your strings, twisting your mind and smashing your dreams. Blinded by me, you can't see a thing, just call my name 'cause I'll hear you scream.",
     "Metallica - Master Of Puppets", os.path.join(PARENT_DIR, "Pictures\\Master Of Puppets.png")),
    ("Where are you now? Atlantis, under the sea, under the sea. Where are you now? Another dream, the monster running wild inside of me, I'm faded.",
     "Alan Walker - Faded", os.path.join(PARENT_DIR, "Pictures\\Different World.png")),
    ("Crawling back to you, ever thought of calling when you've had a few? Cause I always do. Maybe I'm too busy being yours to fall for somebody new, now I've thought it through. Crawling back to you.",
     "Arctic Monkeys - Do I Wanna Know?", os.path.join(PARENT_DIR, "Pictures\\AM.png")),
    ("Just the two of us, we can make it if we try, just the two of us. Just the two of us, building castles in the sky, just the two of us, You and I.",
     "Grover Washington Jr. - Just the Two of Us", os.path.join(PARENT_DIR, "Pictures\\Winelight.png")),
    ("You, what do you own the world? How do you own disorder, disorder? Now, somewhere between the sacred silence, sacred silence and sleep. Somewhere, between the sacred silence and sleep. disorder, disorder, disorder.",
     "System Of A Down - Toxicity", os.path.join(PARENT_DIR, "Pictures\\Toxicity.png")),
    ("Something's getting in the way, something's just about to break. I will try to find my place in the diary of Jane, so tell me how it should be.",
     "Breaking Benjamin - The Diary of Jane", os.path.join(PARENT_DIR, "Pictures\\Phobia.png")),
    ("So what if you can see the darkest side of me? No one would ever change this animal I have become. Help me believe it's not the real me, somebody help me tame this animal.",
     "Three Days Grace - Animal I Have Become", os.path.join(PARENT_DIR, "Pictures\\One-X.png")),
    ("I don't wanna live, I don't wanna breathe, 'less I feel you next to me. You take the pain I feel, waking up to you never felt so real.",
     "Skillet - Comatose", os.path.join(PARENT_DIR, "Pictures\\Comatose.png")),
    ("Welcome to the jungle, we've got fun and games. We got everything you want honey, we know the names. We are the people that can find whatever you may need. If you got the money, honey, we got your disease.",
     "Guns N' Roses - Welcome To The Jungle", os.path.join(PARENT_DIR, "Pictures\\Appetite For Destruction.png")),
    ("Joy, beautiful spark of Divinity. Daughter of Elysium, we enter, drunk with fire, heavenly one, thy sanctuary! Thy magic binds again, what custom strictly divided; all people become brothers, where thy gentle wing abides.",
     "Ludwig van Beethoven - Ode to Joy", os.path.join(PARENT_DIR, "Pictures\\Beethoven.png")),
    ("Don't you know I'm still standin' better than I ever did? Lookin' like a true survivor, feelin' like a little kid. And I'm still standin' after all this time. Pickin' up the pieces of my life without you on mind.",
     "Elton John - I'm Still Standing", os.path.join(PARENT_DIR, "Pictures\\Too Low For Zero.png")),
    ("Psychic spies from China try to steal your mind's elation. And little girls from Sweden dream of silver screen quotation. And if you want these kind of dreams it's Californication.",
     "Red Hot Chili Peppers- Californication", os.path.join(PARENT_DIR, "Pictures\\Californication.png")),
    ("With the lights out, it's less dangerous, here we are now, entertain us. I feel stupid, and contagious, here we are now, entertain us. A mulatto, an albino, a mosquito, my libido. Yeah!",
     "Nirvana - Smells Like Teen Spirit", os.path.join(PARENT_DIR, "Pictures\\Nevermind.png"))
]

CHOICE = random.choice(sentences)
FUTURE = sys.maxsize
WAIT_TIME = 20


def handle_client(player,):
    """
    Using Threading to handle each client
    """
    global FUTURE
    # Checking if the name is occupied
    valid_name = False
    name = ''
    while not valid_name:
        name = player.get_msg()
        if name != "":
            valid_name = True
            for key in players_dict.keys():
                if name == key:
                    valid_name = False
                    player.send_msg("Invalid Name")
    player.send_msg("Connected")
    player.set_name(name)
    players_dict[name] = player
    print(f"{name} has connected")

    if FUTURE == sys.maxsize:
        FUTURE = time.time() + WAIT_TIME
    player.send_msg(f'time-{FUTURE}')
    while time.time() < FUTURE:
        pass

    player.send_msg(f'sen-{CHOICE[0]}')
    while True:
        data = ""
        try:
            data = player.get_msg()
            if data == "FINISH":
                player.send_msg(f'song-{CHOICE[1]}')
                player.send_msg(IMAGE)
                data = ""
        except:
            pass


def main():
    global IMAGE
    with open(CHOICE[2], 'rb') as img:
        data = img.read(READ_CHUNK)
        IMAGE = data
        while data:
            data = img.read(READ_CHUNK)
            IMAGE += data
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, BASE_PORT))
    server.listen(4)
    server.settimeout(None)
    getting_clients = True

    while getting_clients:
        server.settimeout(1)
        try:
            client, addr = server.accept()
            player = Player(client)
            start_new_thread(handle_client, (player,))
        except:
            pass
        if time.time() > FUTURE:
            getting_clients = False
    """for client in clients_dict.keys():
        msg = Protocol.create_msg(f"sen-{CHOICE[0]}")
        client.send(msg)"""
    while True:
        pass
    server.close()


if __name__ == '__main__':
    main()