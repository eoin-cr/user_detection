import subprocess
from pynput.keyboard import Key, Listener
# import logging
import time


# from datetime import datetime
# import os


class State:
    def __init__(self):
        # The word bit will be used for checking if they're trying to use qwerty
        self.keys_arr = []
        self.word = ""

        # Adds some more variables
        self.count = 0  # Counts how many characters have been pressed
        self.start_time = time.time()  # Gets time the user started typing
        self.time = 0  # Time it's taken to type however many characters
        self.time_started = False  # Tracks whether it's started tracking the time
        self.time_finished = 0  # Time the user finished typing last
        self.running = True  # In case something goes wrong with the script and it keeps locking you out, change
        # this to false
        self.finished = False  # After chars before check is reached this will
        # become true to stop checking for another time
        self.special_key = False  # Whether the last key pressed was a special character
        self.last_press = time.time()  # The last time a key was pressed
        self.min_wpm = 55  # The minimum wpm that must be reached
        self.chars_before_check = 50  # The characters before the check will be implemented
        self.time_to_recheck = 120  # How long after the user stops typing before it rechecks their speed
        self.time_to_stop = 1  # How long between characters does it stop counting the time

    def on_press(self, key):
        if self.running:
            # print(key)
            # print(self.finished)
            # If the time between now and the last time the user entered
            # input is greater than the set time to recheck, start the script
            # again
            if self.finished and time.time() - self.time_finished > self.time_to_recheck:
                self.time = 0
                self.finished = False
                print("first")

            if not self.finished:
                # If the count is greater than the amount of characters set
                # to check, do the check
                if self.count > self.chars_before_check:
                    # If the time has started, stop it, and get get the total
                    # time the user was typing for
                    if self.time_started:
                        self.time += (time.time() - self.start_time)
                        # self.time += (time.time() - self.time_started) % 60

                    # Just prints some stats, helpful for debugging
                    print(f'start_time: {self.start_time}')
                    print(f'time.time(): {time.time()}')
                    print(f'WPM: {self.count / self.time * 60 / 5}')
                    print(f'self.time = {self.time}')

                    # If the calculated wpm is less than the minimum wpm, lock
                    # the system
                    if (self.count / self.time * 60 / 5) < self.min_wpm:
                        print("Warning: Type speed exceeded, locking")
                        subprocess.run("i3lock")

                    # Resets variables
                    self.finished = True
                    self.time_finished = time.time()
                    self.count = 0
                    self.time_started = False
                    self.time = 0

                # Else if the time since the last press is greater than the
                # chosen time to stop, remove the time since the last press
                # from the time.  i.e. if you are typing and then stop for
                # 5 seconds to think, this will not be incorporated into the
                # wpm calculation
                elif time.time() - self.last_press > self.time_to_stop and not self.special_key and self.time_started:
                    print(time.time())
                    print(self.last_press)
                    print(self.start_time)
                    self.start_time += (time.time() - self.last_press)
                    print(self.start_time)
                    self.last_press = time.time()
                    print("Time issue")

                # If the last key pressed was a special key, ignore the next one
                elif self.special_key:
                    print("Key ignored - special before")
                    self.special_key = False

                # Else get the character of the key pressed
                elif getattr(key, "char", None):
                    print("Key accepted")
                    # If the time hasn't started, start it
                    if not self.time_started:
                        self.start_time = time.time()
                        self.time_started = True

                    # Add the charcter just pressed to the word, this will be
                    # useful when we add in the keyboard check later
                    self.word += key.char

                    # Increase count by 1
                    self.count += 1

                    # Set the last time pressed to the current time
                    self.last_press = time.time()

                # Checks if a space was pressed
                elif key == Key.space:
                    print("Space")
                    # print(self.word)
                    # keys_array += word

                    # Before implementing this check, if you hit space, stopped, and then hit space again,
                    # time.time() - self.start_time would be added to self.time both times you hit the
                    # space bar, leading to the wpm to be wildly incorrect
                    if self.time_started:
                        # Add the time to the total time
                        self.time += (time.time() - self.start_time)

                    # Stop the timer
                    self.time_started = False

                    # Append the word to the array, will be handy when we
                    # add the keyboard check
                    self.keys_arr.append(self.word)
                    self.word = ""

                # If the last key pressed was backspace, remove the last char
                # from the word
                elif key == Key.backspace:
                    print("Backspace")
                    self.word = self.word[:-1]

                # Otherwise, the key pressed must be a special key, so we check
                # if the last key pressed was also a special key.  If not, we
                # set the special key value and do the same stuff as when we
                # hit spacebar with the timer
                elif not self.special_key:
                    print("Special key")
                    self.special_key = True
                    self.time_started = False
                    self.time += time.time() - self.start_time

                # Prints the current count (useful for debugging)
                print(self.count)


# Calls the State class
state = State()
# Upon a key being pressed call the function
with Listener(on_press=state.on_press) as listener:
    listener.join()
