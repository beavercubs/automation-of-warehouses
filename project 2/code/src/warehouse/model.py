import mesa
import random
import time
from warehouse.agents import palletbot, pallet, isle, CELLNUMBER

class warehouse(mesa.Model):
    """Model representing an automated warehouse."""

    def __init__(self, n_palletbot=100, n_pallet=600, n_isle=300, width=100, height=100):
        super().__init__()

        self.width = width
        self.height = height
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.running = True
        self.start_time = None

        # 1. Create PalletBots at the bottom rows
        for i in range(n_palletbot):
            while True:
                x = self.random.randint(0, width - 1)
                y = self.random.randint(height - 9, height - 6)  # the 3 rows visually below the pallets
                if self.grid.is_cell_empty((x, y)):
                    bot = palletbot(self.next_id(), (x, y), self)
                    self.schedule.add(bot)
                    self.grid.place_agent(bot, (x, y))
                    break


        # 2. Create Isles in clean vertical columns with 2 empty border columns
        isle_columns = list(range(2, width - 2, 3))  # leave 2 columns on both sides
        isle_rows = list(range(0, height - 10))
        max_isles = len(isle_columns) * len(isle_rows)
        actual_isle_count = min(n_isle, max_isles)  # make sure we don't exceed capacity

        isle_count = 0
        for x in isle_columns:
            for y in isle_rows:
                if isle_count >= actual_isle_count:
                    break
                if self.grid.is_cell_empty((x, y)):
                    i = isle(self.next_id(), (x, y), self)
                    self.schedule.add(i)
                    self.grid.place_agent(i, (x, y))
                    isle_count += 1


        # 3. Create Pallets at the top (y = 0 to 4)
        for i in range(n_pallet):
            while True:
                x = self.random.randint(0, width - 1)
                y = self.random.randint(self.height - 5, self.height - 1)
                if self.grid.is_cell_empty((x, y)):
                    p = pallet(self.next_id(), (x, y), self)
                    self.schedule.add(p)
                    self.grid.place_agent(p, (x, y))
                    break

    def step(self):
        self.schedule.step()

        # Stop model once all pallets are delivered
        all_done = all(
            isinstance(agent, pallet) and agent.state == 0
            for agent in self.schedule.agents if isinstance(agent, pallet)
        )
        if all_done:
            self.running = False
            duration = time.time() - self.start_time if self.start_time else 0
            print(f"Simulation completed in {self.schedule.steps} steps and {duration:.2f} seconds.")
