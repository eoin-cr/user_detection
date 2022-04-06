# User detection
Uses a keylogger to check whether
1. The person typing is typing slower than 60wpm
2. The person is attempting to type in qwerty (I don't use qwerty)

If either of these is true it will lock the computer.

---

## How it works
pynput.keyboard is used to take all the key inputs from the computer.  Several
values are set.  The main ones are as follows:
* Time started - tracks whether the program is currently tracking the time in
between keypresses
* Chars before check - the amount of characters that have to be typed before
the WPM will be tested.  A lower number will result in an intruder being locked
out more rapidly, but will also lead to more false positives.
* Time to recheck - time to wait after user stops typing to start tracking the
WPM again.  If a user starts typing, passes the user test, and continues typing,
they are almost definitely the same user, so there is no point checking whilst
they are still typing.  However, once they stop typing, there is a chance for
someone else to start using the computer.  So if a time limit of the user not
typing is exceeded, the user checks will be ran again.  The default time is
30 seconds.  This means if an intruder hops on the computer the moment you step
away, and starts typing in under 30 seconds from you stopping typing, they can
bypass the checks.  This can be avoided by setting the time to recheck to a
lower value, however, this means the user will be tested more often, producing
more possibilities for the user to fail their own tests, making the program
more annoying to keep running.
* Time to stop - how long between 2 characters being pressed the program stops
counting the time in the wpm.  Due to the way the program works—which I will
cover later on—without this, the program would continue counting the time between
key presses, even if you waited a minute after typing the last letter, which would
dramatically influence the WPM.  The default for this is 1 second, which seems to 
be a good value, as it doesn't change the wpm too much and also means waits that
are reasonably long between characters won't be counted.  However, you can increase
this value if you want, which would make the wpm slightly more accurate, as long
as you aren't stopping typing before you press space.
* Finished - after the check this value will be set as true, indicating the check
has been ran.  This value will remain true until the time between keypresses
exceeds the time to recheck value


The WPM counter works as follows.  If a (non-special, non-(back)space) character is
entered, a character count will go up.  When the first character is entered a timer
is started.  There are 3 counter values — a counter which keeps track of the total
time(self.time), and a variable which keeps track of the time a word was started
(self.start_time), and a variable which keeps track of whether it's tracking the
time in a word (self.time_started).  

Whenever a character is entered, if the start
tracker is false, it will initialise the start time to the current time (if the
start time variable is true, nothing will happen to the time).  Whenever the space
bar is pressed, the the current time minus the start time will be added to the total
time, and the time started variable will be set to false.  Essentially, a timer will
run whilst a word is being typed, and stop between words.  This is to prevent people
from stopping to think after hitting space, and having that get added to their time.
(Although this wouldn't be much of an issue anymore, as there is a check which will
remove any extra time you have stopped typing after exceeding one second, however,
most of the WPM code was written before that was introduced).  

Once the character before check value is hit, the program will calculate the WPM
by doing `self.count / self.time * 60 / 5`.  The self.count / self.time is to get
the amount of characters pressed per second, and then is multiplied by 60 to get
characters per minute, and then divided by 5 to get WPM.


Then several checks are run.
1. If finished is set as true, it will then check whether the time between 
key presses exceeds the time to recheck variable.  If it does, the finished value
is set to false, and the time is set to 0—thereby starting the user detection
program once again.  Otherwise, the last keypress value is simply set to the current
time
2. If the character count exceeds the characters before check value, call the check
function
3. If the time since the last keypress is greater than the value for time to stop
and the previous key was not a special key, and self.time_started is true, then
add `time.time() - self.last_press` to the start time, and set last_press to the
current time.  This basically just removes the time waited from the timer, so the
WPM is accurate.
4. If the previous key was a special key (see point 8), the key is simply ignored,
and `self.special_key` is set to false
5. If the value of the key press is a character—if the time hasn't already been
started, it gets started.  Then this character is added to `self.word` which keeps
track of the last word written (important for checking whether qwerty was entered),
the count is incremented, and `self.last_press` is set to the current time
6. If the space key was pressed, if time has started, add the current time minus
the start time to the total time, set `self.time_started` to false, and runs the 
qwerty check on the word.  If the word is recognised as a user attempting to type
in qwerty, the check function will be run (there's nothing to check really, we've
already determined that it is qwerty, it just is handy to have a function that
resets all the variables properly and the like).  Then `self.word` is set as an
empty string
7. If the last key pressed was backspace, remove the last character from the
`self.word` string
8. Otherwise, a special key must have been pressed.
If a special key is pressed, a value is set (`self.special_key`), which simply
   keeps track of every time a special key is counted.  The reason for this is so that
   whenever you do some sort of keyboard combination for example `ctrl + c` and the
   like, the ctrl and c keys are not counted in the time or character count.


---

## Notes on using this yourself
Regarding the obvious point—the keylogger.  Installing a keylogger on your own
computer may seem risky—because it usually is.  This program will be able to read
anything you type on your keyboard, including passwords, credit cards details, etc,
HOWEVER, **none of this data is sent anywhere.  There is not a single network call**
**in the program, nor are there even the modules required to make network calls**.
There is no reason to trust me, feel free to look through the code yourself.  Your key
inputs are also not stored in any file on the computer.  They are stored solely on
memory, so they should not be able to be read by other programs on your computer.
The only file I/O occurring is the reading of the qwerty typing attempts on colemak
list.

If your keyboard language is not colemak, the qwerty check won't be properly running,
*however*, if you have your keyboard set to qwerty, running the program will not lock
you out.  The program will only lock out people trying to use qwerty on a colemak layout.

If you do use some sort of unusual keyboard layout, such as dvorak or the like, you can
create your own word list which will lock out people trying to type in qwerty on your
layout.  All you need to do is take the wiki-100k.txt file, copy it, then do a search 
and replace on a character with what happens when you attempt to press that key in your
layout.  Take for example the word 'hello'.  On colemak the h key in qwerty is h in colemak
as well, the e key in colemak is actually an f, l in the qwerty position is i, o in
qwerty position is y.  So what we do is do a search and replace of e with f, l with i,
and o with y.  Do this for every letter in the alphabet (make sure to use a special
character or something as a temporary store for a character or obviously you will run out
of characters for switching).  Now when the user attempts to type hello what actually
comes out is 'hfiiy', which will match the word we just added to our word list, thereby
confirming the user is trying to type in qwerty on a non-qwerty layout.  After you
create this new file of all the ways trying to type qwerty words results in, you should
run the del_word.py script.  This will just ensure actual words don't end up on the list.

When you are running the program for the first time, it is advisable to set WPM limits
around 10-20WPM below what you usually type, setting it higher than this can lead to a
lot of false positives, and is not a great experience.  Currently I have no need for a 
max WPM limit, as it would be too annoying for trying to use vim and the like, however,
I will add one in the future for people who don't use any programs like that.  Most of
the other defaults should be fine though.