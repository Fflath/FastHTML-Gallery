import numpy as np
from collections import namedtuple
from math import pi
import math

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

# fx is monotonically increasing
def ticks(fx, min_x, max_x, size, delta_x=1e-6, debug=False):
    dx = lambda x: (fx(x+delta_x) - fx(x))/delta_x

    # fx(min_x) is the left most tick at position 0
    # fx(max_x) is the right most tick at position size
    # scale everything to fit the size and shift to the left
    scale_factor = size/(fx(max_x)-fx(min_x))
    shift_factor = fx(min_x)*scale_factor
    pos = lambda x: fx(x)*scale_factor-shift_factor

    # big tick loop
    ticks = []
    m,e = m_e(max_x-min_x)
    x = round(min_x,e-1)
    while x <= max_x:
        # x = round(x,2)
        y=fx(x)
        p = pos(x)

        step_size = 1**e

        while (pos(x+step_size) - pos(x)) < 2:
            step_size += step_size
        if between(x,min_x,max_x): ticks.append(Tick(x=x,y=y, position=p, label=x, style="big"))

        m_step = step_size/10
        mx = x + m_step
        x += step_size
        while (mx <= x) and (mx <= max_x):
            if mx >= min_x: ticks.append(Tick(x=mx,y=fx(mx), position=pos(mx), label=x, style="small"))
            mx += m_step
    return ticks


I = Scale(ticks=ticks(lambda x: x, 0, 10, 100), name="I", description="This is the basic number line with ticks spaced evenly on the integers.")
C = Scale(ticks=ticks(lambda x: np.log10(x), 1, 10, 125), name="C", description="I am a line")
D = Scale(ticks=ticks(lambda x: np.log10(x), 1, 10, 125), name="D", description="I am a line")
CF = Scale(ticks=ticks(lambda x: np.log10(x), pi, 10*pi, 125), name="CF", description="I am a line")
DF = Scale(ticks=ticks(lambda x: np.log10(x), pi, 10*pi, 125), name="CF", description="I am a line")

CI = Scale(ticks=ticks(lambda x: np.log10(x), 1, 10, 125), name="CI", description="I am a line")
S = Scale(ticks=ticks(lambda x: np.log10(np.sin(np.deg2rad(x))), 5.74, 90, 125), name="S", description="I am a line")
S2 = Scale(ticks=ticks(lambda x: np.log10(np.sin(np.deg2rad(x))), 0.57, 5.74, 125), name="S", description="I am a line")
K = Scale(ticks=ticks(lambda x: np.log10(x**3), 1, 1000, 125), name="K", description="I am a line")
A = Scale(ticks=ticks(lambda x: np.log10(x**2), 1, 100, 125), name="A", description="I am a line")
B = Scale(ticks=ticks(lambda x: np.log10(x**2), 1, 100, 125), name="A", description="I am a line")

acuman_600 = {
    "name": "Acuman 600",
    "description": "A 600 series slide rule.",
    "scales": [
        {"scale": K, "position": "top-arm-2"},
        {"scale": A, "position": "top-arm-3"},
        {"scale": B, "position": "slider-1"},
        {"scale": S, "position": "slider-2"},
        {"scale": I, "position": "slider-3"},
        {"scale": CI, "position": "slider-4"},
        {"scale": C, "position": "slider-5"},
        {"scale": D, "position": "bottom-arm-1"},
        # {"scale": L, "position": "bottom-arm-2"},
        # {"scale": T, "position": "bottom-arm-3"}
    ]
}
ruler_options = {"default":acuman_600}



