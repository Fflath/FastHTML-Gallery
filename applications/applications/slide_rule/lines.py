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

def ticks(fx, min_x, max_x, size=WIDTH, label="x",reverse=False,zoom=False):
    if min_x > max_x: 
        min_x,max_x = max_x,min_x
    
    f = lambda x: np.log10(fx(x))
    scale_factor = size/(f(max_x)-f(min_x))
    shift_factor = f(min_x)*scale_factor

    scale_zoom = .1 if zoom else 1
    label_zoom = 1 if zoom else 0
    if reverse:
        pos = lambda x: size-(f(x)*scale_factor-shift_factor)
    else:   
        pos = lambda x: f(x)*scale_factor-shift_factor

    # big tick loop
    ticks = []
    _,e = m_e(min_x)
    step_size = scale_zoom*10**e
    x = round(min_x,e)

    if x < min_x: x += step_size
    if x > min_x:
        mx = round(min_x,e+1)
        m_step = step_size/10
        while (mx <= x) and (mx <= max_x):
            if mx < min_x or mx > max_x:
                mx += m_step
                next
            style = SMALL + label_zoom
            if (mx>=min_x) and (mx <= max_x):ticks.append(Tick(x=mx,y=fx(mx), position=pos(mx), label=x if label=="x" else y, style=style))
            mx += m_step

    while x <= max_x:
        if x < min_x:
            x += step_size
            next
        y=fx(x)
        p = pos(x)

        m,e = m_e(x)
        step_size = scale_zoom*10**e
        if label == "y": m,_=m_e(y)
        if (x>=min_x) and (x <= max_x): ticks.append(Tick(x=x,y=y, position=p, label=m, style=BIG + label_zoom))

        m_step = step_size/10
        mx = x + m_step
        x += step_size
        c = 1
        while (mx <= x) and (mx <= max_x):
            if mx < min_x or mx > max_x:
                mx += m_step
                next
            if mx >= min_x and c == 5: style = MEDIUM + label_zoom
            else: style = SMALL
            m,e = m_e(mx)
            if label == "y": m,_=m_e(y)

            if (mx>=min_x) and (mx <= max_x):ticks.append(Tick(x=mx,y=fx(mx), position=pos(mx), label=m, style=style))
            mx += m_step
            c += 1
    if reverse: ticks.reverse()
    return ticks

def ticks2(fx, min_x, max_x, size=WIDTH, label="x",reverse=False,zoom=False):

    f = lambda x: np.log10(fx(x))
    scale_factor = size/(f(max_x)-f(min_x))
    shift_factor = f(min_x)*scale_factor
    scale_zoom = .1 if zoom else 1
    label_zoom = 1 if zoom else 0
    if reverse:
        pos = lambda x: size-f(x)*scale_factor-shift_factor
    else:   
        pos = lambda x: f(x)*scale_factor-shift_factor
    ticks = []

    def helper(x0, x1, tick_size, step_size):
        ret = []
        x=x0
        while x < x1:
            y=f(x)
            p = pos(x)
            m,e = m_e(x)
            if label == "y": m,_=m_e(y)
            if (x >= min_x) and (x <= max_x): 
                ret.append(Tick(x=x,y=y, position=p, label=m, style=tick_size))

            pxn = pos(x+step_size)
            if pxn - p > 4: ret += helper(x,x+step_size,tick_size-2,step_size/10)
            x += step_size
        return ret
    
    _,e = m_e(min_x)
    step_size = scale_zoom*10**e
    x = round(min_x,e)

    while x <= max_x:
        ticks += helper(x,x+step_size,BIG,step_size)
        x += step_size
    return ticks




def C(xmin=1,xmax=10,zoom=False): return Scale(ticks=ticks(lambda x: x, xmin, xmax,zoom=zoom), name="C", description="Fundamental scale of all slide rules. Identical to the D scale. They are used together for multiplication and division.")
def D(xmin=1,xmax=10,zoom=False): return Scale(ticks=ticks(lambda x: x, xmin, xmax,zoom=zoom), name="D", description="Fundamental scale of all slide rules. Identical to the C scale. They are used together for multiplication and division.")
def CF(xmin=pi,xmax=10*pi,zoom=False): return Scale(ticks=ticks(lambda x: x, xmin, xmax,zoom=zoom), name="CF", description="Same as C but with a range of pi to 10pi.")
def DF(xmin=pi,xmax=10*pi,zoom=False): return Scale(ticks=ticks(lambda x: x, xmin, xmax,zoom=zoom), name="DF", description="Same as D but with a range of pi to 10pi.")

def CI(xmin=1,xmax=10,zoom=False): return Scale(ticks=ticks(lambda x: 1/x, xmin, xmax,reverse=True,zoom=zoom), name="CI", description="Inverse of C scale. Used to find the reciprocal of a number.")
def CIF(xmin=pi,xmax=10*pi,zoom=False): return Scale(ticks=ticks(lambda x: 1/x, xmin, xmax,reverse=True,zoom=zoom), name="CIF", description="I am a line")

def S(xmin=5.74,xmax=90,zoom=False): return Scale(ticks=ticks(lambda x: np.sin(np.deg2rad(x)), xmin, xmax,zoom=zoom), name="S", description="I am a line")
def ST(xmin=0.57,xmax=5.74,zoom=False): return Scale(ticks=ticks(lambda x: np.sin(np.deg2rad(x)), xmin, xmax,zoom=zoom), name="ST", description="I am a line")
def T(xmin=5.71,xmax=45,zoom=False): return Scale(ticks=ticks(lambda x: np.tan(np.deg2rad(x)), xmin, xmax,zoom=zoom), name="T", description="I am a line")

def K(xmin=1,xmax=1000,zoom=False): return Scale(ticks=ticks(lambda x: x**3, xmin, xmax,zoom=zoom), name="K", description="I am a line")
def A(xmin=1,xmax=100,zoom=False): return Scale(ticks=ticks(lambda x: x**2, xmin, xmax,zoom=zoom), name="A", description="I am a line")
def B(xmin=1,xmax=100,zoom=False): return Scale(ticks=ticks(lambda x: x**2, xmin, xmax,zoom=zoom), name="B", description="I am a line")

def L(xmin=0,xmax=10,zoom=False): return Scale(ticks=ticks(lambda x: 10**x, xmin, xmax,zoom=zoom), name="L", description="I am a line")



acuman_600 = {
    "name": "Acuman 600",
    "description": "A 600 series slide rule.",
    "scales": [
        {"scale": K, "position": "top-arm-1", "name": "K"},
        {"scale": A, "position": "top-arm-2", "name": "A"},
        {"scale": CF, "position": "top-arm-3", "name": "CF"},
        {"scale": DF, "position": "slider-1", "name": "DF"},
        # {"scale": B, "position": "slider-1", "name": "B"},
        {"scale": S, "position": "slider-2", "name": "S"},
        {"scale": ST, "position": "slider-3", "name": "ST"},
        {"scale": CI, "position": "slider-4", "name": "CI"},
        {"scale": C, "position": "slider-5", "name": "C"},
        {"scale": D, "position": "bottom-arm-1", "name": "D"},        
        {"scale": L, "position": "bottom-arm-2", "name": "L"},
        {"scale": T, "position": "bottom-arm-3", "name": "T"}
    ]
}

ruler_options = {"acuman_600": acuman_600}