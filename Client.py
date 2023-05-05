import socket
import pygame
import sys
import Protocol
import time
import math

SAVED_PHOTO_LOCATION = 'img.png'
BASE_PORT = 20000
HOST = "127.0.0.1"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
SENTENCE_POS = (0, 0)


# A function that blits any text (or 3 connected texts) on the screen. The text could be longer than a row.
def blit_text(screen, pos, font, text1, color1, text2=None, color2=None, text3=None, color3=None):
    lines = [word.split(' ') for word in text1.splitlines()] # Creating a list of the lines
    space = font.size(' ')[0] # The size of a space
    max_width, max_height = screen.get_size()
    x, y = pos
    # Going over every word in every line
    for line in lines:
        for word in line:
            txt_surface = font.render(word, 0, color1)
            word_width, word_height = txt_surface.get_size()
            # Checking if there is a need for a new line
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            # Bliting the text
            screen.blit(txt_surface, (x, y))
            x += word_width + space
        # Creating a new line for every line except the last one
        if lines.index(line) != len(lines) - 1:
            x = pos[0]
            y += word_height
    if text2 is not None and color2 is not None:
        x -= space
        lines = [word.split(' ') for word in text2.splitlines()] # Creating a list of the lines in text2
        # Going over every word in every line
        for line in lines:
            for word in line:
                txt_surface = font.render(word, 0, color2)
                word_width, word_height = txt_surface.get_size()
                # Checking if there is a need for a new line
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                # Bliting the text
                screen.blit(txt_surface, (x, y))
                x += word_width + space
            # Creating a new line for every line except the last one
            if lines.index(line) != len(lines) - 1:
                x = pos[0]
                y += word_height
    if text3 is not None and color3 is not None:
        x -= space
        lines = [word.split(' ') for word in text3.splitlines()]  # Creating a list of the lines in text3
        # Going over every word in every line
        for line in lines:
            for word in line:
                txt_surface = font.render(word, 0, color3)
                word_width, word_height = txt_surface.get_size()
                # Checking if there is a need for a new line
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                # Bliting the text
                screen.blit(txt_surface, (x, y))
                x += word_width + space
            # Creating a new line for every line except the last one
            if lines.index(line) != len(lines) - 1:
                x = pos[0]
                y += word_height


# A function that returns first letters that match in 2 strings
def find_matches(text, sentence):
    count = 0
    for i in range(len(text)):
        if text[i] != sentence[i]:
            return count
        count += 1
    return count


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, BASE_PORT))

    get_name = True

    pygame.init()
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 32)
    sen_font = pygame.font.SysFont('Ariel', 32)
    big_font = pygame.font.SysFont('comicsansms', 48)

    box = pygame.Rect(200, 230, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive

    text = ''
    active = False
    sentence = ''
    occupied = False

    while get_name:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            # If user closed the program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If the user clicked on the text input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            color = color_active if active else color_passive
            # If the user types
            if event.type == pygame.KEYDOWN:
                # If the text box is toggled
                if active:
                    # If user pressed 'Enter', sending the text to the server
                    if event.key == pygame.K_RETURN:
                        client.send(Protocol.create_msg(text))
                        data = ''
                        while data == '':
                            data = Protocol.get_msg(client)[1]
                            if data == "Invalid Name":
                                text = ""
                                occupied = True
                            elif data == "Connected":
                                get_name = False
                    # If the user removed a letter, erasing that letter
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    # Adding the user's text to the text
                    else:
                        text += event.unicode
            if occupied:
                blit_text(screen, (180, 50), big_font, "Enter another name!", "burlywood1")
            else:
                blit_text(screen, (180, 50), big_font, "Enter your\nname below:", "burlywood1")
            txt_surface = font.render(text, True, color)
            # Increasing text box size if the name is too long
            width = max(200, txt_surface.get_width() + 10)
            box.w = width
            # Showing the text
            screen.blit(txt_surface, (box.x + 5, box.y + 5))
            # Showing the input_box rect.
            pygame.draw.rect(screen, color, box, 2)

            pygame.display.flip()
            clock.tick(30)

    running = True
    client.setblocking(False)
    # Client won't wait for server message
    text = ''

    waiting = True
    game_over = False
    got_sentece = False
    song_name = ''
    img = ''
    future = sys.maxsize
    int_time = 0
    wpm = 0

    while running:
        if time.time() > future:
            waiting = False
        data = ''
        try:
            data = Protocol.get_msg(client)[1]
        except BlockingIOError:
            pass
        if type(data) == str:
            if data.startswith("time-"):
                future = float(data[5:])
            elif data.startswith("sen-"):
                sentence = data[4:]
                got_sentece = True
            elif data.startswith("song-"):
                song_name = data[5:]
        elif type(data) == bytes:
            with open(SAVED_PHOTO_LOCATION, 'wb') as img:
                img.write(data)
            img = pygame.image.load(SAVED_PHOTO_LOCATION).convert()
        if game_over:
            for event in pygame.event.get():
                # If user closed the program
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                screen.fill((30, 30, 30))
                blit_text(screen, (201, 0), big_font, "  You have just written a song by:", 'green4')
                blit_text(screen, (0, 300), big_font, f"Words per minute: {wpm}", 'green4')
                blit_text(screen, (201, 160), sen_font, song_name, 'green4')
                if img != '':
                    screen.blit(img, (0, 0))
        elif got_sentece:
            for event in pygame.event.get():
                # If user closed the program
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # If user pressed 'Enter', creating a new line
                    if event.key == pygame.K_EQUALS:
                        text = sentence[:-1]
                    elif event.key == pygame.K_RETURN:
                        text += '\n'
                    # If the user removed a letter, erasing that letter
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    # Adding the user's text to the text
                    else:
                        text += event.unicode

                screen.fill((30, 30, 30))
                num_matches = find_matches(text, sentence)
                blit_text(screen, SENTENCE_POS, sen_font, text[:num_matches], 'green4',
                          text[num_matches:], 'red2', sentence[len(text):], 'lightsteelblue4')
                if num_matches == len(sentence):
                    game_over = True
                    wpm = math.floor(len(sentence.split(" ")) * 60 / (time.time() - future))
                    client.send(Protocol.create_msg("FINISH"))
        elif waiting:
            for event in pygame.event.get():
                screen.fill((30, 30, 30))
                # If user closed the program
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if time.time() > future:
                    waiting = False
                if int_time != math.floor(future - time.time()):
                    int_time = math.floor(future - time.time())
                blit_text(screen, (120, 100), big_font, f"Game begins in:\n  {str(int_time)} seconds!", "green4")

        # Trying to get the sentence
        else:
            for event in pygame.event.get():
                screen.fill((30, 30, 30))
                # If user closed the program
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()