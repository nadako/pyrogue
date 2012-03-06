"astar.py - A* pathfinding module for Pyro"

# This module assumes movement on a grid, rather than an arbitrary graph.

from util import *
from heapq import heappush, heappop
from math import sqrt

class NodeList(BASEOBJ):
    def __init__(self, name="nodelist"):
        self.nodes, self.idx = [], {}
        self.name = name
    def add(self, x, y, cost, h, parent_x, parent_y):
        if self.has(x, y):
            raise ValueError
        node = [cost+h, cost, h, x, y, (parent_x, parent_y)]
        heappush(self.nodes, node)
        self.idx[(x, y)] = node
    def best_path_so_far(self):
        # Return the path to the closest node we found (lowest heuristic):
        lowest = 99999
        for n in self.nodes:
            if n[2] < lowest:
                lowest = n[2]
                x, y = n[3], n[4]
        return self.path_from(x, y)

    def has(self, x, y):
        return self.idx.has_key((x, y))
    def node(self, x, y):
        return self.idx[(x, y)]
    def path_from(self, x, y):
        # Return a path from the given node back to the start:
        node = self.node(x, y)
        path = []
        while node[5] != (None, None):
            path.insert(0, (x, y))
            x, y = node[5]
            node = self.node(x, y)
        return path
    def pop(self):
        node = heappop(self.nodes)
        del self.idx[(node[3], node[4])]
        return node
    def remove(self, x, y):
        self.nodes = [n for n in self.nodes if (n[3], n[4]) != (x, y)]
        del self.idx[(x, y)]

def path(start_x, start_y, dest_x, dest_y, passable, max_length=99999):
    # passable is a function(x,y) returning whether a node is passable.
    open = NodeList("Open")
    h = max(abs(dest_x - start_x), abs(dest_y - start_y))
    open.add(start_x, start_y, 0, h, None, None)
    closed = NodeList("Closed")
    length=0
    while len(open.nodes) > 0:
        node = open.pop()
        node_cost_h, node_cost, node_h, node_x, node_y, node_parent = node
        if node_cost > max_length:
            # We've failed to find a short enough path; return the best we've got:
            break
        # Put the parent node in the closed set:
        closed.add(node_x, node_y, node_cost, node_h, node_parent[0], node_parent[1])        
        # See if we're at the destination:
        if (node_x, node_y) == (dest_x, dest_y):
            # We found the path; return it:
            p = closed.path_from(node_x, node_y)
            return p
        # Check adjacent nodes:
        for i in xrange(node_x -1 , node_x + 2):
            for j in xrange(node_y - 1, node_y + 2):
                dx, dy = i - node_x, j - node_y
                # Skip the current node:
                if (i, j) == (node_x, node_y): continue
                # If this node is impassable, disregard it:
                if not passable(i, j): continue
                # Calculate the heuristic:
                h = max(abs(dest_x - i), abs(dest_y - j))
                # Calculate the move cost; assign slightly more to diagonal moves
                # to discourage superfluous wandering:
                if dx==0 or dy==0:
                    move_cost = 1
                else:
                    move_cost = 1.001
                cost = node_cost + move_cost
                # See if it's already in the closed set:
                if closed.has(i, j):
                    c = closed.node(i, j)
                    if cost < c[1]:
                        open.add(i, j, cost, h, node_x, node_y)
                        closed.remove(i, j)
                else:
                    # It's not in the closed list, put it in the open list if it's not already:
                    if not open.has(i, j):
                        open.add(i, j, cost, h, node_x, node_y)
    # We ran out of open nodes; pathfinding failed:
    # Do the best we can:
    p = closed.best_path_so_far()
    return p
                    
     