import numpy as np
from collections import namedtuple
from math import pi
import math
from constants import *

Tick = namedtuple("Tick", ["x", "y", "label", "position", "style"])
Scale = namedtuple("Scale", ["ticks", "name", "description"])

def m_e(number):
    if number == 0:
        return 0,0
    exponent = math.floor(math.log10(abs(number)))
    mantissa = number / (10 ** exponent)
    return mantissa,exponent

def between(value,lower,upper):
    return value > lower and value < upper

def ticks(fx, min_x, max_x, size, label="x",reverse=False):

    f = lambda x: np.log10(fx(x))
    scale_factor = size/(f(max_x)-f(min_x))
    shift_factor = f(min_x)*scale_factor
    if reverse:
        pos = lambda x: size-f(x)*scale_factor-shift_factor
    else:   
        pos = lambda x: f(x)*scale_factor-shift_factor

    # big tick loop
    ticks = []
    _,e = m_e(min_x)
    step_size = 10**e
    x = round(min_x,e)

    if x < min_x: x += step_size
    if x > min_x:
        mx = round(min_x,e+1)
        m_step = step_size/10
        while (mx <= x) and (mx <= max_x):
            if mx < min_x or mx > max_x:
                mx += m_step
                next
            style = "small"
            if (mx>=min_x) and (mx <= max_x):ticks.append(Tick(x=mx,y=fx(mx), position=pos(mx), label=x if label=="x" else y, style=style))
            mx += m_step

    while x <= max_x:
        if x < min_x:
            x += step_size
            next
        y=fx(x)
        p = pos(x)

        m,e = m_e(x)
        step_size = 10**e
        if label == "y": m,_=m_e(y)
        if (x>=min_x) and (x <= max_x): ticks.append(Tick(x=x,y=y, position=p, label=m, style="big"))

        m_step = step_size/10
        mx = x + m_step
        x += step_size
        c = 1
        while (mx <= x) and (mx <= max_x):
            if mx < min_x or mx > max_x:
                mx += m_step
                next
            if mx >= min_x and c == 5: style = "medium"
            else: style = "small"
            if (mx>=min_x) and (mx <= max_x):ticks.append(Tick(x=mx,y=fx(mx), position=pos(mx), label=x if label=="x" else y, style=style))
            mx += m_step
            c += 1
        
    return ticks


C = Scale(ticks=ticks(lambda x: x, 1, 10, WIDTH), name="C", description="Fundamental scale of all slide rules. Identical to the D scale. They are used together for multiplication and division.")
D = Scale(ticks=ticks(lambda x: x, 1, 10, WIDTH), name="D", description="Fundamental scale of all slide rules. Identical to the C scale. They are used together for multiplication and division.")
CF = Scale(ticks=ticks(lambda x: x, pi, 10*pi, WIDTH), name="CF", description="Same as C but with a range of pi to 10pi.")
DF = Scale(ticks=ticks(lambda x: x, pi, 10*pi, WIDTH), name="DF", description="Same as D but with a range of pi to 10pi.")

CI = Scale(ticks=ticks(lambda x: 1/x, 1, 10, WIDTH,reverse=True), name="CI", description="Inverse of C scale. Used to find the reciprocal of a number.")
CIF = Scale(ticks=ticks(lambda x: 1/x, pi, 10*pi, WIDTH,reverse=True), name="CIF", description="I am a line")

S = Scale(ticks=ticks(lambda x: np.sin(np.deg2rad(x)), 5.74, 90, WIDTH), name="S", description="I am a line")
ST = Scale(ticks=ticks(lambda x: np.sin(np.deg2rad(x)), 0.57, 5.74, WIDTH), name="ST", description="I am a line")
T = Scale(ticks=ticks(lambda x: np.tan(np.deg2rad(x)), 5.71, 45, WIDTH), name="T", description="I am a line")

K = Scale(ticks=ticks(lambda x: x**3, 1, 1000, WIDTH), name="K", description="I am a line")
A = Scale(ticks=ticks(lambda x: x**2, 1, 100, WIDTH), name="A", description="I am a line")
B = Scale(ticks=ticks(lambda x: x**2, 1, 100, WIDTH), name="B", description="I am a line")

L = Scale(ticks=ticks(lambda x: 10**x, 0, 10, WIDTH), name="L", description="I am a line")



acuman_600 = {
    "name": "Acuman 600",
    "description": "A 600 series slide rule.",
    "scales": [
        {"scale": K, "position": "top-arm-1"},
        {"scale": A, "position": "top-arm-2"},
        {"scale": B, "position": "slider-1"},
        {"scale": S, "position": "slider-2"},
        {"scale": ST, "position": "slider-3"},
        {"scale": CI, "position": "slider-4"},
        {"scale": C, "position": "slider-5"},
        {"scale": D, "position": "bottom-arm-1"},        
        {"scale": L, "position": "bottom-arm-2"},
        {"scale": T, "position": "bottom-arm-3"}
    ]
}

default = {
    "name": "Acuman 600",
    "description": "A 600 series slide rule.",
    "scales": [
        {"scale": K, "position": "top-arm-1"},
        {"scale": A, "position": "top-arm-2"},
        {"scale": CF, "position": "top-arm-3"},
        {"scale": DF, "position": "slider-1"},
        {"scale": S, "position": "slider-2"},
        {"scale": ST, "position": "slider-3"},
        {"scale": CI, "position": "slider-4"},
        {"scale": C, "position": "slider-5"},
        {"scale": D, "position": "bottom-arm-1"},
        {"scale": L, "position": "bottom-arm-2"},
        {"scale": T, "position": "bottom-arm-3"}
    ]
}

ruler_options = {"default":default, "acuman_600": acuman_600}

# def position2x(ind_x, arm_x, slider_x):
#     scale_factor = WIDTH/(f(max_x)-f(min_x))
#     shift_factor = f(min_x)*scale_factor

#     tx = (ind_x - arm_x)
