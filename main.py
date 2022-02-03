import subprocess
from pynput.keyboard import Key, Listener
# import logging
import time
# from datetime import datetime
# import os


class State:
    def __init__(self):
        self.keys_arr = []
        self.word = ""
        self.count = 0
        # self.time_start = time.time()
        self.start_time = time.time()
        self.time = 0
        self.time_started = False
        self.time_finished = 0
        self.running = True
        self.finished = False
        # self.keyboard = Controller()
        self.special_key = False
        self.last_press = time.time()
        self.min_wpm = 70
        self.chars_before_check = 25

    def on_press(self, key):
        if self.running:
            #             print(key)
            if time.time() - self.time_finished > 60:
                self.finished = False

            if not self.finished:
                if self.count > self.chars_before_check:
                    if self.time_started:
                        self.time += (time.time() - self.start_time)
                        # self.time += (time.time() - self.time_started) % 60

                    # self.count / self.time
                    print(f'start_time: {self.start_time}')
                    print(f'time.time(): {time.time()}')
                    print(f'WPM: {self.count / self.time * 60 / 5}')
                    print(f'self.time = {self.time}')
                    if self.count / self.time * 60 / 5 < self.min_wpm:
                        print("Warning: Type speed exceeded, locking")
                        subprocess.run("i3lock")

                    self.finished = True
                    self.time_finished = time.time()
                    self.count = 0
                    self.time_started = False

                elif time.time() - self.last_press > 3:
                    self.start_time += (time.time() - self.last_press)

                elif self.special_key:
                    print("Special key pressed")
                    self.special_key = False

                elif getattr(key, "char", None):
                    if not self.time_started:
                        self.start_time = time.time()
                        self.time_started = True
                    self.word += key.char
                    self.count += 1
                    self.last_press = time.time()
                elif key == Key.space:
                    print(self.word)
                    # keys_array += word
                    self.time_started = False
                    # self.time += (time.time() - self.time_started) % 60
                    self.time += (time.time() - self.start_time)
                    self.keys_arr.append(self.word)
                    self.word = ""
                elif key == Key.backspace:
                    self.word = self.word[:-1]
                elif not self.special_key:
                    self.special_key = True
                    self.time_started = False
                    self.time += time.time() - self.start_time


                print(self.count)


state = State()
with Listener(on_press=state.on_press) as listener:
    listener.join()
