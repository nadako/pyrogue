"dungeon_gen.py - Dungeon creation for Pyro"

from util import *

# Find temp tiles that won't interfere with the defined ones:
def temp_tiles(num):
    tiles = ""
    for L in letters:
        if L not in DUNGEON_CHARS:
            tiles += L
            if len(tiles) >= num:
                return tiles[:num]
(TEMP_ROOM, TEMP_CORRIDOR, CORRIDOR_FLOOR) = temp_tiles(3)

STEP = False

class Level(BASEOBJ):
    def __init__(self, level_width = 79, level_height = 20,
                 room_min_width = 5, room_max_width = 11,
                 room_min_height = 3, room_max_height = 6, 
                 room_separation = 1, max_passages = 3,
                 max_rooms = 25, room_tries = 50, passage_tries = 20):
        self.level_width, self.level_height = level_width, level_height
        self.room_min_width, self.room_max_width = room_min_width, room_max_width
        self.room_min_height, self.room_max_height = room_min_height, room_max_height
        self.room_separation, self.max_rooms = room_separation, max_rooms
        self.max_passages = max_passages
        self.room_tries, self.passage_tries = room_tries, passage_tries
        self.data = []
        for i in range(self.level_height):
            self.data.append([WALL]*self.level_width)
        self.rooms = []
        self.generate()
    def __str__(self):
        return "\n".join(["".join(row) for row in self.data])
    def add_doors(self):
        "Add doors where passages meet rooms"
        for i in range(self.level_width):
            for j in range(self.level_height):
                if self.data[j][i] == CORRIDOR_FLOOR and self.adjacent_to(i, j, FLOOR):
                    self.data[j][i] = DOOR
        for i in range(self.level_width):
            for j in range(self.level_height):
                if self.data[j][i] == DOOR and not self.adjacent_to(i, j, CORRIDOR_FLOOR):
                    self.data[j][i] = WALL
        
    def add_passage(self, rx, ry, rw, rh, dirs=[0,1,2,3]):
        "Add a passage from (x, y) till we hit a room or other passage"
        dx = (0, 1, 0, -1)
        dy = (-1, 0, 1, 0)
        done = False
        tries = 0
        while not done and tries < self.passage_tries:
            tries += 1
            # Remove any previous attempt:
            self.bake(TEMP_CORRIDOR, WALL)
            self.bake("x", WALL)
            # Go back to the start:
            x = irand(rx, rx+rw-1)
            y = irand(ry, ry+rh-1)
            start_dir = choice(dirs)
            dir = start_dir
            # First travel in the same dir till we escape this room:
            while self.data[y][x] == TEMP_ROOM:
                x += dx[dir]
                y += dy[dir]
            if self.data[y][x] != WALL:
                continue
            # Begin the passage:
            self.data[y][x] = TEMP_CORRIDOR
            if self.adjacent_to(x, y, CORRIDOR_FLOOR):
                continue
            twistiness = irand(5, 25)   # Percent chance of a turn per square
            if len(self.rooms) < 2:
                twistiness = 0
            ticker = 0
            length = 0
            while not (self.adjacent_to(x, y, FLOOR) or self.adjacent_to(x, y, CORRIDOR_FLOOR)):
                if STEP:
                    self.display()
                    raw_input()
                if self.adjacent_to(x, y, TEMP_ROOM) and length > 1:
                    break
                if self.adjacent_to(x, y, TEMP_CORRIDOR) > 1:
                    break
                if irand(0, 20) < ticker:
                    # If a room exists in one of the 2 L/R directions, turn:
                    ticker = 0
                    nx, ny, ndir = x, y, (dir+1) % 4
                    near = 999
                    while 0<nx<self.level_width-2 and 0<ny<self.level_height-2 and self.data[ny][nx] != FLOOR:
                        nx += dx[ndir]
                        ny += dy[ndir]
                    if 0<nx<self.level_width-2 and 0<ny<self.level_height-2 and self.data[ny][nx] == FLOOR:
                        near = abs(nx-x)+abs(ny-y)
                    nx, ny, ndir = x, y, (dir-1) % 4
                    while 0<nx<self.level_width-2 and 0<ny<self.level_height-2 and self.data[ny][nx] != FLOOR:
                        nx += dx[ndir]
                        ny += dy[ndir]
                    if 0<nx<self.level_width-2 and 0<ny<self.level_height-2 and self.data[ny][nx] == FLOOR and abs(nx-x)+abs(ny-y) < near:
                        dir = (dir-1) % 4
                    elif near < 999:
                        dir = (dir+1) % 4
                    else:
                        pass
                elif x<1 or x>self.level_width-2 or y<1 or y>self.level_height-2:
                    # Back up one space, then turn right or left:
                    if length < 2:
                        break
                    x -= dx[dir]
                    y -= dy[dir]
                    dir = (dir + choice((-1, 1))) % 4
                    #break
                elif irand(0, 99) < twistiness and length > 0:
                    # Possibly turn based on twistiness of the corridor:
                    dir = (dir + choice((-1, 1))) % 4
                x += dx[dir]
                y += dy[dir]
                ticker += 1
                length += 1
                # Abort if we touch the current room:
                if self.data[y][x] == FLOOR:
                    break
                # Disallow diagonally touching another corridor or room:
                for s in "._":
                    if not self.adjacent_to(x, y, s) and self.adjacent_or_diag(x, y, s):
                        break
                self.data[y][x] = TEMP_CORRIDOR
            else:
                self.data[y][x] = TEMP_CORRIDOR
                if length > 2:
                    done = True
                dl = (dir+1) % 4
                dr = (dir-1) % 4
                # disallow "sideswipe" connections of corridors to rooms:
                if (self.data[y+dy[dr]][x+dx[dr]] == FLOOR
                or self.data[y+dy[dl]][x+dx[dl]] == FLOOR):
                    done = False
        if self.adjacent_or_diag(x, y, TEMP_ROOM):
            done = False
        if done:
            self.bake(TEMP_CORRIDOR, CORRIDOR_FLOOR)
            return start_dir + 1
        else:
            self.bake(TEMP_CORRIDOR, WALL)
            return False
    def add_room(self):
        for t in range(self.room_tries):
            # Try at most X times to add a room, then give up:
            if len(self.rooms) >= self.max_rooms:
                break
            w = irand(self.room_min_width, self.room_max_width)
            h = irand(self.room_min_height, self.room_max_height)
            x = irand(1, self.level_width - w - 1)
            y = irand(1, self.level_height - h - 1)
            free = self.area_free(x, y, w, h)
            if STEP:
                print "Free is: %s" % free
            if free:
                # The area is free; dig out the room:
                for i in range(w):
                    for j in range(h):
                        self.data[y+j][x+i] = TEMP_ROOM                                
                passages_added = False
                if len(self.rooms) > 0 and free != "room":
                    if len(self.rooms) > 1:
                        num_passages = irand(1, self.max_passages)
                    else:
                        num_passages = 1
                    dirs = [0, 1, 2, 3]
                    for p in range(num_passages):
                        pdir = self.add_passage(x+1, y+1, w-1, h-1, dirs)
                        if pdir:
                            dirs.remove(pdir-1)
                            passages_added = True
                else:
                    passages_added = True
                if not passages_added:
                    # We were not able to attach this room to the level:
                    if free == "clear":
                        # The room didn't touch existing passages; undo it:
                        self.bake(TEMP_ROOM, WALL)
                        # ...and try again:
                        continue
                    elif free == "passage":
                        # There were passages, so it's connected; leave it:
                        self.rooms.append((x, y, w, h))
                        return True
                    elif free == "room":
                        # Overlies or adjoins another room; don't need passages:
                        self.rooms.append((x, y, w, h))
                        return True
                self.rooms.append((x, y, w, h))
                return True
        return False
    def adjacent_or_diag(self, x, y, what):
        "Return how many tiles of given type(s) are 8-way adjacent to (x, y)"
        num = 0
        for offset in ((-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)):
            i = max(0, min(self.level_width-1, x+offset[0]))
            j = max(0, min(self.level_height-1, y+offset[1]))
            if self.data[j][i] in what:
                    num += 1
        return num
    def adjacent_to(self, x, y, what):
        "Return how many tiles of given type(s) are 4-way adjacent to (x, y)"
        num = 0
        for offset in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            i = max(0, min(self.level_width-1, x+offset[0]))
            j = max(0, min(self.level_height-1, y+offset[1]))
            if self.data[j][i] in what:
                    num += 1
        return num
    def area_free(self, x, y, w, h):
        "return whether the area is free for a room"
        passage = False # whether the area overlies a passage
        room = False    # whether the area overlies a room
        for i in range(x-self.room_separation, x+w+1+self.room_separation):
            for j in range(y-self.room_separation, y+h+1+self.room_separation):
                ii = max(0, min(self.level_width-1, i))
                jj = max(0, min(self.level_height-1, j))
                if self.data[jj][ii] == FLOOR:
                    return False
                elif self.data[jj][ii] == CORRIDOR_FLOOR:
                    if x <= i < x+w and y <= j < y+h:
                        passage = True
        # Exclude rooms that are right along a corridor:
        for i in range(x-1, x+w+2):
            for j in range(y-1, y+h+2):
                ii = max(0, min(self.level_width-1, i))
                jj = max(0, min(self.level_height-1, j))
                if self.data[jj][ii] == CORRIDOR_FLOOR:
                    if self.adjacent_to(i, j, CORRIDOR_FLOOR) > 1:
                        return False
        if passage:
            return "passage"
        else:
            # See if it overlies or adjoins a room:
            if self.room_separation < 1:
                for i in range(x, x+w):
                    if self.adjacent_to(i, y, FLOOR):
                        return "room"
                    if self.adjacent_to(i, y+h-1, FLOOR):
                        return "room"
                for j in range(y, y+h):
                    if self.adjacent_to(x, j, FLOOR):
                        return "room"
                    if self.adjacent_to(x+w-1, j, FLOOR):
                        return "room"
            return "clear"
    def bake(self, old, new):
        "'bake' the fresh rooms/passages into the level"
        for i in range(self.level_width):
            for j in range(self.level_height):
                if self.data[j][i] == old:
                    self.data[j][i] = new
    def cosmetic(self):
        # Make it look like a gameplay screen by hiding walls:
        self.bake(CORRIDOR_FLOOR, FLOOR)
        self.bake(WALL, " ")
        for i in range(self.level_width):
            for j in range(self.level_height):
                if self.data[j][i] == " ":
                    if self.adjacent_or_diag(i, j, FLOOR):
                        self.data[j][i] = WALL

    def display(self):
        print "-" * 78
        for line in self.data:
            print ''.join(line)
        print "-" * 78
    def generate(self):
        "Add rooms, passages, doors, etc"
        while self.add_room():
            self.bake(TEMP_ROOM, FLOOR)
        self.add_doors()
        self.bake(CORRIDOR_FLOOR, FLOOR)

if __name__ == "__main__":
    # Generate and display one dungeon (test code):
    L = Level(room_separation=1)
    #L.cosmetic()
    L.display()