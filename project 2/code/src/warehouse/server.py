# Make a world that is 50x50, on a 250x250 display.
import mesa
from warehouse.model import warehouse
from warehouse.portrayal import warehouse_portrayal
from warehouse.agents import CELLNUMBER

SIZE_OF_CANVAS_IN_PIXELS_X = 400
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

# TODO Add a parameter named "n_boxes" for the number of boxes to include in the model.
simulation_params = {
    "height": CELLNUMBER, 
    "width": CELLNUMBER,

    "n_palletbot": mesa.visualization.Slider(
        'number of palletbot',
        10, #default
        10, #min
        30, #max
        1, #step
           
        "choose how many Pallet robots are to be included in the simulation"
    ),
    "n_pallet": mesa.visualization.Slider(
        'number of pallet',
        50, #default
        50, #min
        200, #max
        1, #step
        "choose how many pallets to include in the simulation"
    )
    # TODO implement
    }
grid = mesa.visualization.CanvasGrid(warehouse_portrayal, CELLNUMBER, CELLNUMBER, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)


server = mesa.visualization.ModularServer(
    warehouse, [grid], " Sorting warehouse", simulation_params
)
