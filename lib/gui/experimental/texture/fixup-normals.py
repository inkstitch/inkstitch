#!/bin/python3

import pathlib

import PIL
import PIL.Image

directory = pathlib.Path(__file__).parent

image = PIL.Image.open(directory / "normals-rounded.png")
px = image.load()
assert px

for x in range(image.width):
    ref = 0
    while (orig := px[x, ref])[3] == 0:
        ref += 1

    val = (orig[0], orig[1], orig[2], 0)
    for y in range(ref):
        px[x,y] = val

for x in range(image.width):
    ref = image.height-1
    while (orig := px[x, ref])[3] == 0:
        ref -= 1

    val = (orig[0], orig[1], orig[2], 0)
    for y in range(ref+1, image.height):
        px[x,y] = val

image.save(directory / "normals-rounded-fixed.png")
    
