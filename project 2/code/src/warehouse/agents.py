import random
import time
import mesa

# Constants
CELLNUMBER = 20
UNDONE = 1
DONE = 0
BLOCKED = 4

# Global dictionaries
isle_ids = {}           # Maps isle ID to (x, y) position
pallet_to_isle = {}     # Maps pallet ID to isle ID
bot_to_pallet = {}      # Maps palletbot ID to pallet ID


class palletbot(mesa.Agent):
    """
    PalletBot agent that continuously retrieves pallets, delivers them to isles,
    and drops the pallet ON the isle while stopping to the left or right of it.
    """
    def __init__(self, id, pos, model, init_state=UNDONE):
        super().__init__(id, model)
        self.pos = pos
        self.state = init_state  # UNDONE, DONE
        self.target = None
        self.dragging = None
        self.drop_position = None

    def step(self):
        if self.model.start_time is None:
            self.model.start_time = time.time()

        if self.state == BLOCKED:
            return

        if self.state == DONE and self.dragging is None:
            if any(isinstance(a, pallet) and a.state == UNDONE for a in self.model.schedule.agents):
                self.state = UNDONE
                bot_to_pallet.pop(self.unique_id, None)
                self.target = None

        if self.state == UNDONE and self.unique_id not in bot_to_pallet:
            self.assign_pallet()

        if self.target:
            self.move_to_target()

    def assign_pallet(self):
        closest, min_dist = None, float('inf')
        for agent in self.model.schedule.agents:
            if isinstance(agent, pallet) and agent.state == UNDONE and agent.claimed_by is None:
                dist = self.manhattan_dist(self.pos, (agent.x, agent.y))
                if dist < min_dist:
                    closest, min_dist = agent, dist

        if closest:
            bot_to_pallet[self.unique_id] = closest.unique_id
            closest.claimed_by = self.unique_id
            self.target = (closest.x, closest.y)
            print(f"Bot {self.unique_id} claimed Pallet {closest.unique_id}")

    def move_to_target(self):
        if self.pos == self.target:
            if self.state == UNDONE:
                pallet_id = bot_to_pallet[self.unique_id]
                for agent in list(self.model.schedule.agents):
                    if agent.unique_id == pallet_id:
                        self.dragging = agent
                        self.model.grid.remove_agent(agent)
                        print(f"Bot {self.unique_id} picked up Pallet {pallet_id}")
                        isle_id = pallet_to_isle.get(pallet_id)
                        if isle_id in isle_ids:
                            isle_pos = isle_ids[isle_id]
                            self.drop_position = isle_pos
                            self.target = (isle_pos[0] + 1, isle_pos[1])
                        self.state = DONE
            elif self.state == DONE:
                if self.dragging and self.drop_position:
                    self.dragging.x, self.dragging.y = self.drop_position
                    self.model.grid.place_agent(self.dragging, self.drop_position)
                    self.dragging.state = DONE
                    print(f"Bot {self.unique_id} delivered pallet to {self.drop_position}")
                    self.dragging = None
                    self.drop_position = None
                self.target = None

                if all(isinstance(a, pallet) and a.state == DONE for a in self.model.schedule.agents if isinstance(a, pallet)):
                    self.model.running = False
                    duration = time.time() - self.model.start_time
                    print(f"Simulation completed in {self.model.schedule.steps} steps and {duration:.2f} seconds.")

        else:
            x, y = self.pos
            tx, ty = self.target
            dx = 1 if tx > x else -1 if tx < x else 0
            dy = 1 if ty > y else -1 if ty < y else 0
            next_pos_x = (x + dx, y)
            next_pos_y = (x, y + dy)

            moved = False

            if dx != 0 and not self.check_collision_with_isle(next_pos_x):
                next_pos = next_pos_x
                moved = True
            elif dy != 0 and not self.check_collision_with_isle(next_pos_y):
                next_pos = next_pos_y
                moved = True
            else:
                next_pos = self.pos

            if moved:
                self.model.grid.move_agent(self, next_pos)
                self.pos = next_pos
                if self.dragging:
                    self.dragging.x, self.dragging.y = self.pos

    def check_collision_with_isle(self, pos):
        return pos in isle_ids.values()

    @staticmethod
    def manhattan_dist(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

class isle(mesa.Agent):
    def __init__(self, id, pos, model):
        super().__init__(id, model)
        self.x, self.y = pos
        isle_ids[id] = (self.x, self.y)

class pallet(mesa.Agent):
    def __init__(self, id, pos, model, init_state=UNDONE):
        super().__init__(id, model)
        self.x, self.y = pos
        self.state = init_state
        self.claimed_by = None
        if isle_ids:
            pallet_to_isle[id] = random.choice(list(isle_ids.keys()))
