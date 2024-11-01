import numpy as np
from collections import namedtuple
from math import pi
import math
from constants import *
import fastcore.all as fc

Tick = namedtuple("Tick", ["x", "y", "label", "position", "style"])
# Scale = namedtuple("Scale", ["ticks", "name", "description"])

def m_e(number):
    if number == 0:
        return 0,0
    exponent = math.floor(math.log10(abs(number)))
    mantissa = number / (10 ** exponent)
    return mantissa,exponent

def between(value,lower,upper):
    return value > lower and value < upper


def p2x(p,fxi,scale_factor,shift_factor,reverse=False,size=WIDTH): 
    if reverse:
        return fxi((size-p+shift_factor)/scale_factor)  
    else:   
        return fxi((p + shift_factor)/scale_factor)
    

class Scale:
    def __init__(self, fx, min_x,max_x,name,description,size=WIDTH, label="x",reverse=False,deltax=0.00001):
        self.size = size
        self.fx = fx
        self.name = name
        self.description = description
        self.label = label
        self.deltax = deltax
        self.reverse = reverse
        self.set_pos(min_x,max_x)
        

    def set_pos(self,min_x,max_x):
        self.min_x = min_x
        self.max_x = max_x
        f = lambda x: np.log10(self.fx(x))
        self.scale_factor = self.size/(f(max_x)-f(min_x))
        self.shift_factor = f(min_x)*self.scale_factor

        if self.reverse:
            self.pos = lambda x: self.size-(f(x)*self.scale_factor-self.shift_factor)
        else:   
            self.pos = lambda x: f(x)*self.scale_factor-self.shift_factor

    def invert(self,atx,guess):
        dx = lambda f: lambda x: (f(x+self.deltax)-f(x))/self.deltax
        fxi = lambda x: self.pos(x)-atx

        xn = lambda x: x-(fxi(x)/dx(fxi)(x))
        x0 = guess
        x1 = xn(x0)
        while x0-x1 > 0.00001:
            x0=x1
            x1=xn(x0)
        return x1
 
    def ticks(self,xmin=None,xmax=None,zoom=False):
        
        xmin=self.min_x if xmin is None else xmin
        xmax=self.max_x if xmax is None else xmax
        scale_zoom = .1 if zoom else 1
        label_zoom = 1 if zoom else 0
        # big tick loop
        ticks = []
        _,e = m_e(xmin)
        step_size = scale_zoom*10**e
        x = round(xmin,e)

        if x < xmin: x += step_size
        if x > xmin:
            mx = round(xmin,e+1)
            m_step = step_size/10
            while (mx <= x) and (mx <= xmax):
                if mx < xmin or mx > xmax:
                    mx += m_step
                    next
                style = SMALL + label_zoom
                if (mx>=xmin) and (mx <= xmax):ticks.append(Tick(x=mx,y=self.fx(mx), position=self.pos(mx), label=x if self.label=="x" else y, style=style))
                mx += m_step

        while x <= xmax:
            if x < xmin:
                x += step_size
                next
            y=self.fx(x)
            p = self.pos(x)

            m,e = m_e(x)
            step_size = scale_zoom*10**e
            if self.label == "y": m,_=m_e(y)
            if (x>=xmin) and (x <= xmax): ticks.append(Tick(x=x,y=y, position=p, label=m, style=BIG + label_zoom))

            m_step = step_size/10
            mx = x + m_step
            x += step_size
            c = 1
            while (mx <= x) and (mx <= xmax):
                if mx < xmin or mx > xmax:
                    mx += m_step
                    next
                if mx >= xmin and c == 5: style = MEDIUM + label_zoom
                else: style = SMALL
                m,e = m_e(mx)

                if (mx>=xmin) and (mx <= xmax):ticks.append(Tick(x=mx,y=self.fx(mx), position=self.pos(mx), label=m, style=style))
                mx += m_step
                c += 1
        if self.reverse: ticks.reverse()
        return ticks
    
    def zoom(self,lx,lguess,rx,rguess):
        xmin = self.invert(lx,lguess)
        xmax = self.invert(rx,rguess)
        self.set_pos(min(xmin,xmax),max(xmin,xmax))
        return self.zoom_ticks()
    
    def zoom_ticks(self):
        xmin=self.min_x
        xmax=self.max_x
        diff = xmax - xmin
        m,e = m_e(diff)
        rounder = -1*e
        x = round(xmin,rounder)
        step_size = 10**(e-1)
        ticks = []
        if x > xmin: x -= 10*step_size
        while x < xmax:
            y=self.fx(x)
            p = self.pos(x)
            m,e = m_e(x)
            if (x>=xmin) and (x <= xmax): ticks.append(Tick(x=x,y=y, position=p, label=m, style=ZOOM_BIG))
            m_step = step_size/10
            mx = x + m_step
            x += step_size
            c = 1
            while (mx <= x) and (mx <= xmax):
                if mx >= xmin and c == 5: style = MEDIUM
                else: style = SMALL
                m,e = m_e(mx)

                if (mx>=xmin) and (mx <= xmax):ticks.append(Tick(x=mx,y=self.fx(mx), position=self.pos(mx), label=m, style=style))
                mx += m_step
                c += 1
        if self.reverse: ticks.reverse()

        return ticks

def C(): return Scale(fx=lambda x:x, min_x=1,max_x=10, name="C", description="Fundamental scale of all slide rules. Identical to the D scale. They are used together for multiplication and division.")
def D(): return Scale(fx=lambda x: x, min_x=1,max_x=10, name="D", description="Fundamental scale of all slide rules. Identical to the C scale. They are used together for multiplication and division.")
def CF(): return Scale(fx=lambda x: x, min_x=pi,max_x=10*pi, name="CF", description="Same as C but with a range of pi to 10pi.")
def DF(): return Scale(fx=lambda x: x, min_x=pi,max_x=10*pi, name="DF", description="Same as D but with a range of pi to 10pi.")

def CI(): return Scale(fx=lambda x: x, min_x=1,max_x=10, reverse=True,name="CI", description="Inverse of C scale. Used to find the reciprocal of a number.")
def CIF(): return Scale(fx=lambda x: x, min_x=pi,max_x=10*pi, reverse=True, name="CIF", description="I am a line")

def S(): return Scale(fx=lambda x: np.sin(np.deg2rad(x)), min_x=5.74,max_x=90, name="S", description="I am a line")
def ST(): return Scale(fx=lambda x: np.sin(np.deg2rad(x)), min_x=0.57,max_x=5.74, name="ST", description="I am a line")
def T(): return Scale(fx=lambda x: np.tan(np.deg2rad(x)), min_x=5.71,max_x=45, name="T", description="I am a line")

def K(): return Scale(fx=lambda x: x**3, min_x=1,max_x=1000, name="K", description="I am a line")
def A(): return Scale(fx=lambda x: x**2, min_x=1,max_x=100, name="A", description="I am a line")
def B(): return Scale(fx=lambda x: x**2, min_x=1,max_x=100, name="B", description="I am a line")

def L(): return Scale(fx=lambda x: 10**x, min_x=0,max_x=10, name="L", description="I am a line")

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
