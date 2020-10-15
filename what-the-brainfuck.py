r = [',', '>', ',', '>', '<', '[', '<', '[', '>', '>', '+', '>', '+', '<', '<', '<', '-', ']', '>', '>', '>', '[', '<', '<', '<', '+', '>', '>', '>', '-', ']', '<', '<', '-', ']', '>', '.']
c = [4, 9]
l, s, n = [1, 4, 2]


import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
looping = True
printed = False
out = ''
l, s, n = [int(i) for i in input().split()]
c = []
r = []
arr = [0] * s
data_pointer = 0
input_pointer = 0
for i in range(l):
    r.extend([ch for ch in input() if ch in '><+-,.[]'])
for i in range(n):
    c.append(int(input()))
    if c[-1] > 255:
        printed = True
        looping = False

# Write an answer using print
# To debug:
# print(r, file=sys.stderr, flush=True)
# print(input_pointer, file=sys.stderr, flush=True)

while looping:
    # print(input_pointer, file=sys.stderr, flush=True)
    if input_pointer > len(r) - 1:
        looping = False
    elif r[input_pointer] == '>':
        data_pointer += 1
        if data_pointer > s - 1:
            print("POINTER OUT OF BOUNDS")
            printed = True
            looping = False
    elif r[input_pointer] == '<':
        data_pointer -= 1
        if data_pointer < 0:
            print("POINTER OUT OF BOUNDS")
            printed = True
            looping = False
    elif r[input_pointer] == '+':
        arr[data_pointer] += 1
        if arr[data_pointer] > 255:
            print("INCORRECT VALUE")
            printed = True
            looping = False
    elif r[input_pointer] == '-':
        arr[data_pointer] -= 1
        if arr[data_pointer] < 0:
            print("INCORRECT VALUE")
            printed = True
            looping = False
    elif r[input_pointer] == '.':
        out += chr(arr[data_pointer])
    elif r[input_pointer] == ',':
        if c == []:
            print("MISSING INPUT")
            printed = True
            looping = False
        arr[data_pointer] = c[0]
        if len(c) > 1:
            c = c[1:]
        else:
            c = []
    elif r[input_pointer] == '[' and arr[data_pointer] == 0:
        try:
            while r[input_pointer] != ']':
                input_pointer += 1
        except IndexError:
            printed = True
            print("SYNTAX ERROR")
            looping = False
    elif r[input_pointer] == ']' and arr[data_pointer] != 0:
        try:
            while r[input_pointer] != '[':
                input_pointer -= 1
        except IndexError:
            printed = True
            print("SYNTAX ERROR")
            looping = False

    input_pointer += 1

if not printed:
    print(out)