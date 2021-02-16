import carla
from npc_planner import _create_speed_points_npc_planner_inner


def test_create_speed_points_npc_planner_inner():
    fun = _create_speed_points_npc_planner_inner([
        [0, 0, 10],
        [1, 0, 10],
        [2, 0, 10],
        [3, 0, 10],
    ])

    assert [[2, 0, 10], 0.0] == fun(carla.Location(1.5, 0.1, 0))
    assert [[2, 0, 10], 0.0] == fun(carla.Location(2.0, 0.1, 0))
    assert [[3, 0, 10], 0.0] == fun(carla.Location(3.0, 0.1, 0))
    assert [[3, 0, 10], 0.0] == fun(carla.Location(3.5, 0.1, 0))

    fun2 = _create_speed_points_npc_planner_inner([
        [0, 0, 10],
        [1, 1, 10],
        [2, 2, 10],
        [3, 3, 10],
    ])
    assert [[2, 2, 10], 45.0] == fun2(carla.Location(1.5, 1.5, 0))
