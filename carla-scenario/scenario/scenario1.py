import carla
from typing import List


class Scenario1:

    def __init__(self):
        self.description = "first scenario"
        self.mapName = "/Game/Carla/Maps/Town01_Opt"
        self.timeout = 20.0

        print("init")

    def make_ego_vehicle(self, world) -> carla.Vehicle:
        # blueprint
        # start_tf
        # controller, waypoint
        return None

    def make_other_vehicles(self, world) -> List[carla.Vehicle]:
        return []

    def make_other_walkers(self, world) -> List[carla.Walker]:
        return []
