import json as js
import random

def generate_linear(size, nlines, ll, ru):
    arr = []
    if size < nlines:
        nlines = size
        
    onlines = size // nlines
    
    for _ in range(nlines):
        side = random.choice((0, 1))
        x = random.uniform(ll[0], ru[0])
        y = random.uniform(ll[1], ru[1])
        if side == 0:
            for __ in range(onlines):
                arr.append((x, random.uniform(ll[1], ru[1])))
        else:
            for __ in range(onlines):
                arr.append((random.uniform(ll[0], ru[0]), y))
    return arr

def generate_square(size, ll, ru):
    arr = []
    for i in range(size):
        side = random.choice((0, 1, 2, 3))
        if side == 0: # górna
            x = random.uniform(ll[0], ru[0])
            y = ru[1]
        elif side == 1: # prawa
            x = ru[0]
            y = random.uniform(ll[1], ru[1])
        elif side == 2: # lewa
            x = ll[0]
            y = random.uniform(ll[1], ru[1])
        elif side == 3: # dolna
            x = random.uniform(ll[0], ru[0])
            y = ll[1]
        arr.append((x, y))
    return arr

def generate_square_diagonal(nside, ndiagonal, ll, ru):
    arr = [ll, (ll[0], ru[1]), (ru[0], ll[1]), ru]
    for _ in range(nside):
        arr.append((ll[0], random.uniform(ll[1],ru[1])))
        arr.append((random.uniform(ll[0], ru[0]), ll[1]))
    for _ in range(ndiagonal):
        x = random.uniform(ll[0], ru[0])
        arr.append((x, x))
        arr.append((x, ru[1]-x))
    return arr

def generate_random(n, ll, ru):
    arr = []
    for _ in range(n):
        arr.append((random.uniform(ll[0], ru[0]), random.uniform(ll[1], ru[1])))
    return arr

def points_to_file(points, name):
    with open(name, 'w') as file:
        file.write(js.dumps(points))

def file_to_points(file_points):
    with open(file_points, 'r') as file:
        points = js.loads(file.read())
    return points

def plot_to_points(plot):
    return plot.get_added_points()[0].points

