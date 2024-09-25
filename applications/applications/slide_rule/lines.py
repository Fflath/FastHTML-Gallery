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
    _,e = m_e(max_x-min_x)
    step_size = 10**e
    x = round(min_x,e-1)
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
            if mx >= min_x and c == 5: style = "medium"
            elif mx >= min_x: style = "small"
            ticks.append(Tick(x=mx,y=fx(mx), position=pos(mx), label=x if label=="x" else y, style=style))
            mx += m_step
            c += 1
        
    return ticks


C = Scale(ticks=ticks(lambda x: x, 1, 10, 125), name="C", description="I am a line")
D = Scale(ticks=ticks(lambda x: x, 1, 10, 125), name="D", description="I am a line")
CF = Scale(ticks=ticks(lambda x: x, pi, 10*pi, 125), name="CF", description="I am a line")
DF = Scale(ticks=ticks(lambda x: x, pi, 10*pi, 125), name="CF", description="I am a line")

CI = Scale(ticks=ticks(lambda x: 1/x, 1, 10, 125, label="x",reverse=True), name="CI", description="I am a line")
S = Scale(ticks=ticks(lambda x: np.sin(np.deg2rad(x)), 5.74, 90, 125), name="S", description="I am a line")
S2 = Scale(ticks=ticks(lambda x: np.sin(np.deg2rad(x)), 0.57, 5.74, 125), name="S", description="I am a line")
K = Scale(ticks=ticks(lambda x: x**3, 1, 1000, 125), name="K", description="I am a line")
A = Scale(ticks=ticks(lambda x: x**2, 1, 100, 125), name="A", description="I am a line")
B = Scale(ticks=ticks(lambda x: x**2, 1, 100, 125), name="B", description="I am a line")


acuman_600 = {
    "name": "Acuman 600",
    "description": "A 600 series slide rule.",
    "scales": [
        {"scale": K, "position": "top-arm-2"},
        {"scale": A, "position": "top-arm-3"},
        {"scale": B, "position": "slider-1"},
        {"scale": S, "position": "slider-2"},
        # {"scale": I, "position": "slider-3"},
        {"scale": CI, "position": "slider-4"},
        {"scale": C, "position": "slider-5"},
        {"scale": D, "position": "bottom-arm-1"},
        # {"scale": L, "position": "bottom-arm-2"},
        # {"scale": T, "position": "bottom-arm-3"}
    ]
}
ruler_options = {"default":acuman_600}

class Tick:
    def __init__(self, x, y, position, label, style):
        self.x = x
        self.y = y
        self.position = position
        self.label = label
        self.style = style

class Scale:
    def __init__(self, fx, min_x, max_x, size, name, description, label_func = lambda tick: tick.x):
        self.ticks = []
        self.name = name
        self.description = description
        self.min_x = min_x
        self.max_x = max_x
        self.size = size
        self.fx = fx
        self.px = np.log10(fx)
        self.scale_factor = size/(self.px(max_x)-self.px(min_x))
        self.shift_factor = self.px(min_x)*self.scale_factor
        self.pos = lambda x: self.px(x)*self.scale_factor-self.shift_factor
        self.label_func = label_func

    def genx(self):
        x = self.min_x
        _,e = m_e(self.min_x)
        self.step_size = 1**e
        while x <= self.max_x:
            yield x,"big"
            if self.pos(x+self.step_size) - self.pos(x) < 2: self.step_size *= 10
            m_step = self.step_size/10
            mx = x + m_step
            x += self.step_size
            while (mx <= x) and (mx <= self.max_x):
                mm,_ = m_e(mx)
                if mx >= self.min_x and mm==5 : yield mx,"medium"
                elif mx >= self.min_x: yield mx,"small"
                mx += m_step

            x += self.step_size
    
    def ticks(self):
        self.ticks = [Tick(x=x,y=self.fx(x), position=self.pos(x), label=self.label_func, style=style) for x,style in self.genx()]
        return self.ticks
