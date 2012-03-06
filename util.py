"util.py - Pyro utility functions"
import curses
from copy import deepcopy
from random import choice, randint, uniform as rnd, normalvariate as norm, seed
from math import ceil, sqrt
from time import sleep
from strings import lang

class GameOver(Exception): pass

############################## GLOBALS ##########################
class Global(object):
    KeyBuffer = ""
    FullDungeonRefresh = True
    current_level = None
    pc = None

############################ CONSTANTS ##########################

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ANIMATION_DELAY = 0.00    # Sleep time in seconds between animation frames
MESSAGE_LOG_SIZE = 200    # Number of messages to keep in the log

# Dungeon layout characters (data, not display, though they may be the same)
# These are the characters used by the dungeon generator to represent each square
WALL = "#"
FLOOR = "."
DOOR = "+"
DUNGEON_CHARS = (WALL, FLOOR, DOOR)
OUTSIDE_LEVEL = " "

# Literal colors:
c_black = curses.COLOR_BLACK
c_blue = curses.COLOR_BLUE
c_cyan = curses.COLOR_CYAN
c_green = curses.COLOR_GREEN
c_magenta = curses.COLOR_MAGENTA
c_red = curses.COLOR_RED
c_white = curses.COLOR_WHITE
c_yellow = curses.COLOR_YELLOW
c_Black = curses.COLOR_BLACK + 8
c_Blue = curses.COLOR_BLUE + 8
c_Cyan = curses.COLOR_CYAN + 8
c_Green = curses.COLOR_GREEN + 8
c_Magenta = curses.COLOR_MAGENTA + 8
c_Red = curses.COLOR_RED + 8
c_White = curses.COLOR_WHITE + 8
c_Yellow = curses.COLOR_YELLOW + 8

colors = {
    'black':        c_black,
    'blue':         c_blue,
    'light blue':   c_Blue,
    'cyan':         c_cyan,
    'green':        c_green,
    'purple':       c_magenta,
    'red':          c_red,
    'gray':         c_white,
    'white':        c_White,
    'brown':        c_yellow,
    'yellow':       c_Yellow,
    'pink':         c_Red,
    'magenta':      c_Magenta,
    'shiny':        c_Cyan,
    'clear':        c_Cyan,
    'blood red':    c_red,
    'lime green':   c_Green,
}

msg_colors = {
    "k":    c_black,
    "b":     c_blue,
    "g":    c_green,
    "c":     c_cyan,
    "r":      c_red,
    "m":  c_magenta,
    "y":   c_yellow,
    "w":    c_white,
    "K":    c_Black,
    "B":     c_Blue,
    "G":    c_Green,
    "C":     c_Cyan,
    "R":      c_Red,
    "M":  c_Magenta,
    "Y":   c_Yellow,
    "W":    c_White,
}

# Keycodes:
k_up = 56
k_upright = 57
k_right = 54
k_downright = 51
k_down = 50
k_downleft = 49
k_left = 52
k_upleft = 55
k_center = 53

offsets = ((-1, 1), (0, 1), (1, 1), (-1 ,0),(0, 0),
           (1, 0), (-1, -1), (0, -1), (1, -1))

vi_offsets = {
    'h' : (-1, 0),
    'l' : ( 1, 0),
    'j' : ( 0, 1),
    'k' : ( 0,-1),
    'y' : (-1,-1),
    'u' : ( 1,-1),
    'b' : (-1, 1),
    'n' : ( 1, 1),
    '.' : ( 0, 0),
} 
####################### CLASS DEFINITIONS #######################

class Logger(object):
    def __init__(self, filename):
        try:
            self.file = open(filename, "w")
            self.AddEntry("Log initialized.")
        except IOError:
            # Couldn't open the log file:
            self.file = None            
    def __call__(self, entry):
        self.AddEntry(entry)
        #print(entry)
    def __del__(self):
        if self.file:
            self.file.close()
    def AddEntry(self, entry):
        if self.file:
            self.file.write("%s\n" % entry)

class Cycler(object):
    def __init__(self, iterable):
        try:
            iterable[0]
        except IndexError:
            raise TypeError
        self.iterable = iterable
        self.index = -1  # So first call to next() returns iterable[0]
    def next(self):
        self.index = (self.index + 1) % len(self.iterable)
        return self.iterable[self.index]
    def prev(self):
        self.index = (self.index - 1) % len(self.iterable)
        return self.iterable[self.index]
    
####################### GLOBAL FUNCTIONS ########################

def d(p1, p2=None):
    "Roll dice"
    try:
        num, kind, mod = p1+0, p2+0, 0  # Numeric parameters
    except TypeError:
        # String parameter in p1 like "1d3" or "2d6-1"
        num, kind = [s for s in p1.split("d")]
        num = int(num)
        L1 = kind.split("+")
        L2 = kind.split("-")
        if len(L1) > 1:
            kind = int(L1[0])
            mod = int(L1[1])
        elif len(L2) > 1:
            kind = int(L2[0])
            mod = -int(L2[1])
        else:
            kind = int(kind)
            mod = 0
    roll = 0
    for i in range(num):
        roll += irand(1, kind)
    return roll + mod

def seen(mob):
    "Return whether the mob is seen by the PC"
    return mob.is_pc or mob.pc_can_see

def delay(speed):
    "Return the delay for a given speed."
    # 100 is normal speed, resulting in 1000 delay.
    # 200 is twice as fast, 500 delay.
    # 50 is twice as slow, 2000 delay.
    return int(1000 * (100.0 / speed))

def irand(a, b, n=1):
    if a > b:
        a, b = b, a
    t = 0
    for i in xrange(n):
        t += randint(a, b)
    return int(round(t / n))

try:
    sum([])
except NameError:
    from operator import add
    def sum(data):
        if len(data) == 0:
            return 0
        return reduce(add, data)

def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    
    EDB: I didn't write this beast--I fear and respect it.
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 ).split('\n')

def weighted_choice(lst):
    """
    Given a list like [[item1, wieght1], ..., [itemN, weightN]], with weights
    given as real numbers, return one of the items randomly according to weights.
    """
    n = rnd(0, sum([x[1] for x in lst]))
    for item, weight in lst:
        if n < weight:
            break
        n -= weight
    return item

def adjacent(a, b):
    """
    Return whether a is 8-way adjacent to b.  a and b need to have 
    .x and .y members.  Sitting on the same spot counts as adjacent.
    """
    return abs(a.x - b.x) < 2 and abs(a.y - b.y) < 2

def quantize(r):
    "Quantize a real number.  Returns int(r), and adds 1 if rnd(0, 1) < frac(r)."
    return int(r + rnd(0, 1))

def int_range(mean, std_dev=None, max_std_dev=2):
    "Return an random integer normally distributed around mean, with the given std dev."
    if std_dev is None:
        std_dev = mean / 4.0
    mean += 0.5
    return int(min(mean+std_dev*max_std_dev, max(norm(mean, std_dev), mean-std_dev*max_std_dev)))

def hit_chance(differential, level=1):
    "Return the chance to hit a target."
    # differential is attacker's to-hit bonus minus defender's evade bonus
    # level is the target's level; bonuses are diminished in effectiveness with higher levels
    # decay controls how fast the effectiveness of a hit/evade differential diminishes
    # with level.  
    # 0.933 = 1/2 at 10 and 1/4 at 20
    # 0.966 = 71% at 10, 1/2 at 20
    decay = 0.933
    mod = decay ** (level - 1) * 0.05 * (0.9 ** abs(differential) - 1) / -0.1
    if differential >= 0:
        return 0.5 + mod
    else:
        return 0.5 - mod
    
def successful_hit(differential, level=1):
    return rnd(0, 1) < hit_chance(differential, level)

def clen(s):
    "Return the length of a string, excluding embedded color codes."
    for c in msg_colors.keys() + ["0"]:
        s = s.replace("^"+c+"^", "")
    return len(s)

def bresenham(x1, y1, x2, y2, initial_error=0):
    "Bresenham's famous algorithm."
    # initial_error can be varied from -0.5 to 0.5 to alter the
    # spots at which the line jumps (to get different valid paths).
    path = []
    steep = abs(y2 - y1) > abs(x2 - x1)
    if steep:
        x1, y1, x2, y2 = y1, x1, y2, x2
    reversed = x1 > x2
    if reversed:
        x1, y1, x2, y2 = x2, y2, x1, y1
    dx, dy = x2 - x1, abs(y2 - y1)
    error, derror = initial_error, float(dy) / dx
    y = y1
    if y1 < y2: ystep = 1
    else: ystep = -1
    for x in xrange(x1, x2+1):
        if steep: path.append((y, x))
        else: path.append((x, y))
        error += derror
        if error > 0.5:
            y += ystep
            error -= 1
    if reversed:
        path.reverse()
    return path

def path_clear(path, blocked):
    for x, y in path:
        if blocked(x, y): return False
    return True
    
def linear_path(x1, y1, x2, y2, blocked):
    "Return a list of (x, y) tuples along a line from (x1, y1) to (x2, y2)."
    # blocked is a function that returns whether (x, y) is blocked
    # Try to find a linear path that does not contain any blocked squares.
    dx, dy = x2 - x1, y2 - y1
    path = []
    # Try the special cases first:
    if dx == dy == 0:
        return [(x1, y1)], True
    elif dx == 0:
        inc = dy / abs(dy)
        x, y = x1, y1
        while y != y2:
            path.append((x, y))
            y += inc
        path.append((x2, y2))
        return path, path_clear(path[1:-1], blocked)
    elif dy == 0:
        inc = dx / abs(dx)
        x, y = x1, y1
        while x != x2:
            path.append((x, y))
            x += inc
        path.append((x2, y2))
        return path, path_clear(path[1:-1], blocked)
    elif abs(dy) == abs(dx):
        inc_x, inc_y = dx / abs(dx), dy / abs(dy)
        x, y = x1, y1
        while x != x2:
            path.append((x, y))
            x += inc_x
            y += inc_y
        path.append((x2, y2))
        return path, path_clear(path[1:-1], blocked)
    else:
        # Not orthogonal or diagonal; use Bresenham's:
        pretty_path = bresenham(x1, y1, x2, y2)
        if path_clear(pretty_path[1:-1], blocked):
            return pretty_path, True
        # The prettiest path isn't clear; try others:
        path = bresenham(x1, y1, x2, y2, -0.4999)
        if path_clear(path[1:-1], blocked):
            return path, True
        path = bresenham(x1, y1, x2, y2, 0.4999)
        if path_clear(path[1:-1], blocked):
            return path, True
        tune = max(abs(dx), abs(dy))
        for error in xrange(1, tune):
            path = bresenham(x1, y1, x2, y2, 0.5-float(error)/tune)
            if path_clear(path[1:-1], blocked):
                return path, True
        # If we got here, we couldn't find a clear path.
        # Return the pretty path.
        return pretty_path, False
        
def animation_delay():
    if ANIMATION_DELAY:
        sleep(ANIMATION_DELAY)
    
def bonus_str(bonus):
    "Return -1, +0, +1, etc. from a given bonus."
    if bonus < 0:
        return "-%s" % bonus
    else:
        return "+%s" % bonus
    
def report_combat_hit(attacker, target, damage_taken, 
                      verbs=["hits", "hits", "hits"], 
                      verbs_sp=["hit", "hit", "hit"]):
    "Display a text message about a successful attack."
    if not seen(attacker) and not seen(target): return
    if damage_taken > 0:
        if attacker.is_pc:
            Global.IO.Message(lang.combat_you_hit % (verbs_sp[1],
                lang.ArticleName("the", target), damage_taken))
            if target.dead:
                Global.IO.Message(lang.combat_you_killed % 
                                  (lang.ArticleName("the", target),target.kill_xp))
        elif target.is_pc:
            Global.IO.Message(lang.combat_mob_hit_you % 
                              (lang.ArticleName("The", attacker), verbs[1], damage_taken))
        else:
            Global.IO.Message(lang.combat_mob_hit_mob % (lang.ArticleName("The", attacker),
                verbs[1], lang.ArticleName("the", target)))
    elif damage_taken == 0:
        if attacker.is_pc:
            Global.IO.Message(lang.combat_you_hit_no_damage % (verbs_sp[0],
                lang.ArticleName("the", target)))
        elif target.is_pc:
            Global.IO.Message((lang.combat_mob_hit_you_no_damage %
                   (lang.ArticleName("The", attacker), verbs[0])))
        else:
            Global.IO.Message(lang.combat_mob_hit_mob % (lang.ArticleName("The", attacker),
                verbs[0], lang.ArticleName("the", target)))
    if target.is_pc:
        Global.IO.ShowStatus()
    return True
    
def report_combat_miss(attacker, target,
                       verbs=["hits", "hits", "hits"],
                       verbs_sp=["hit", "hit", "hit"]):
    if not seen(attacker) and not seen(target): return
    if attacker.is_pc:
        Global.IO.Message(lang.combat_you_miss % (verbs_sp[1],
            lang.ArticleName("the", target)))
    elif target.is_pc:
        Global.IO.Message((lang.combat_mob_misses_you %
               (lang.ArticleName("The", attacker), verbs_sp[1])))
    else:
        Global.IO.Message(lang.combat_mob_misses_mob % (lang.ArticleName("The", attacker),
              verbs_sp[1], lang.ArticleName("the", target)))
    return False
    
    
####################### INITIALIZATION ##########################

log = Logger("pyro.log")
overlay = {}   # For debugging purposes; characters to be drawn over the level map
