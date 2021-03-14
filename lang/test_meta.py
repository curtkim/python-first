from scenario.base import Scenario
import scenario.scenario1
import scenario.scenario2

print([cls.__name__ for cls in Scenario.__subclasses__()])