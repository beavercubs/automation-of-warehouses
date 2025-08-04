from warehouse.agents import palletbot
from warehouse.agents import pallet
from warehouse.agents import isle
from warehouse.agents import UNDONE, DONE



def warehouse_portrayal(agent):
   """
   Determine which portrayal to use according to the type of agent.
   """
   #print(type(agent))
   if isinstance(agent,palletbot):
        return palletbot_portrayal(agent)
   elif isinstance(agent, pallet):
       return pallet_portrayal(agent) 
   else:
        return isle_portrayal(agent)

def palletbot_portrayal(palletbot):

    if palletbot is None:
        raise AssertionError
    return {
        "Shape": "arrowHead",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": palletbot.pos[0],
        "y": palletbot.pos[1],
        "scale": 1,
        "heading_x":1,
        "heading_y":0,
        # "r":4,
        "Color": "red",
    }


def pallet_portrayal(pallet):

    if pallet is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "scale": 1,
        "x": pallet.x,
        "y": pallet.y,
        "Color": "lightgrey" if pallet.state == UNDONE else "green",

    }


def isle_portrayal(isle):

    if isle is None:
        raise AssertionError
    return{
        "Shape": "circle",
        "w":1,
        "h":1,
        "Filled": "true",
        "Layer": 0,
        "r":1,
        "scale": 1,
        "x": isle.x,
        "y": isle.y,
        "Color": "purple",
    }
