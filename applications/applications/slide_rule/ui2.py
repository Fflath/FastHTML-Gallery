from fasthtml.common import *
from fasthtml.svg import *
from lines import *
from constants import *
import json


# Build the Frame of the ruler. 

class Skeleton():
    def __init__(self,topArm,slider,botArm):
        self.arms = Arms(self)
        self.slider = Slider(self)
        self.indicator = Indicator(self)

        self.topArmHeight = topArm * SCALE_SPACE
        self.sliderHeight = slider * SCALE_SPACE
        self.botArmHeight = botArm * SCALE_SPACE
        self.height = self.topArmHeight + self.sliderHeight + self.botArmHeight

        [{f"top-arm-{count}":{"y": START_Y + self.topArmHeight - (count*SCALE_SPACE) - .1,"up": True}} for count in range(self.topArm)]
        [{f"slider-{count}" :{"y": START_Y + self.topArmHeight + (count*SCALE_SPACE) + .1,"up": False}} for count in range(self.slider)]
        [{f"bot-arm-{count}":{"y": START_Y + self.topArmHeight + self.sliderHeight + (count*SCALE_SPACE)+ .1,"up": False}} for count in range(self.botArm)]
        
        # setting_map =

    def mk(self): 
        return (c.mk() for c in [self.slider, self.arms, self.indicator])
    
    # def setting_map(self,placement):


class Indicator():
    def __init__(self,skelly):
        self.skelly = skelly

    def mk(self):
        return G(
            Line(x1=f"{START_X + WIDTH/2}", y1=f"{START_Y - SBUFFER}", x2=f"{START_X + WIDTH/2}", y2=f"{START_Y + self.skelly.height + SBUFFER}", stroke="black", stroke_width=".1"),
            Rect(
            x=f"{START_X + WIDTH/2-WIDTH/20}",  # Center the indicator on the slider
            y=f"{START_Y - SBUFFER}",
            width=f"{WIDTH/10}",
            height=f"{SBUFFER + self.skelly.height + SBUFFER}",
            fill="rgba(200, 100, 100, 0.5)"),id=f"indicator",x=f"{START_X + WIDTH/2-WIDTH/20}",width=f"{WIDTH/10}")

class Slider():
    def __init__(self,skelly):
        self.skelly = skelly

    def mk(self):
        return G(
            Rect(
            x=f"{START_X-BUFFER}", y=f"{START_Y+self.skelly.topArmHeight}", width=f"{WIDTH+SBUFFER*BUFFER}", height=f"{self.skelly.sliderHeight}", 
            fill="#007bff", id="slider", stroke="black", stroke_width=".1"),
            *[G(id=f"slider-{count}") for count in range(self.skelly.slider)],
            id=f"slider-group",x=f"{START_X}",width=f"{WIDTH+SBUFFER*BUFFER}")

class Arms():
    def __init__(self, skelly):
        self.skelly = skelly
    def mk(self, y = START_Y):
        return G(
        Rect(x=f"{START_X-BUFFER}", y=f"{y}", width=f"{WIDTH+SBUFFER*BUFFER}", height=f"{self.top_arm_height}", fill="pearl", id="arm-top"),
        Rect(x=f"{START_X-BUFFER}", y=f"{y+self.top_arm_height+self.slider_height}", width=f"{WIDTH+SBUFFER*BUFFER}", height=f"{self.bot_arm_height}", fill="pearl", id="arm-bottom"),
        Rect(x=f"{START_X-BUFFER}", y=f"{y}", width=f"{BUFFER-SBUFFER}", height=f"{self.slider_height+self.top_arm_height + self.bot_arm_height}", fill="#B77729", id="end-left"),
        Rect(x=f"{START_X+WIDTH+SBUFFER}", y=f"{y}", width=f"{BUFFER-SBUFFER}", height=f"{self.slider_height+self.top_arm_height + self.bot_arm_height}", fill="#B77729", id="end-right"),
        *[G(id=f"top-arm-{count}") for count in range(self.topArm)],
        *[G(id=f"bot-arm-{count}") for count in range(self.botArm)],

        *[G(id=f"label-top-arm-{count}-l") for count in range(self.topArm)],
        *[G(id=f"label-top-arm-{count}-r") for count in range(self.topArm)],

        *[G(id=f"label-bot-arm-{count}-l") for count in range(self.botArm)],
        *[G(id=f"label-bot-arm-{count}-r") for count in range(self.botArm)],

        *[G(id=f"label-slider-arm-{count}-l") for count in range(self.slider)],
        *[G(id=f"label-slider-arm-{count}-r") for count in range(self.slider)]
        )
    

class NL():
    def __init__(self,ticks, name, placement):
        self.ticks = ticks
        self.name = name
        self.placement = placement

    def mk(self):
        y = setting_map[placement]["y"] + (0 if not zoom else 45)
        up = setting_map[placement]["up"]
        zoomlabel = "zoom-" if zoom else ""
        d = 1 if up else -1
        return [
            SvgOob(
                G(Line(x1=f"{x}", y1=f"{y}", x2=f"{x+width}", y2=f"{y}", stroke="black", stroke_width=".2"),
                *[mk_tick(y,tick,up,x,zoom=zoom) for tick in ticks],id="lines",line=name), hx_swap_oob=f"innerHTML:#{zoomlabel}{placement}"),
            SvgOob(
                Text(name, x=f"{x - 3.5}", y=f"{y-2.5*d}", fill="black", font_size="1", text_anchor="middle", alignment_baseline="middle", font_family="sans-serif", font_weight="bold"),
                hx_swap_oob=f"innerHTML:#{zoomlabel}label-{placement}-l"),
            SvgOob(
                Text(name, x=f"{x+width+3.5}", y=f"{y-2.5*d}", fill="black", font_size="1", text_anchor="middle", alignment_baseline="middle", font_family="sans-serif", font_weight="normal"),
                hx_swap_oob=f"innerHTML:#{zoomlabel}label-{placement}-r")]
