from dataclasses import dataclass


@dataclass
class SimParameters:
  """
  A class used to store the simulation parameters.

  Attributes:
      simulation_year (int): The simulation year.
      timesteps (str): The time steps of the simulation. Defaults to "30min".
      energy_units (str): The energy units of the simulation. Defaults to "kWh".
      power_units (str): The power units of the simulation. Defaults to "kW".
  """
  simulation_year: int
  timesteps: str = "30min"
  energy_units: str = "kWh"
  power_units: str = "kW"
