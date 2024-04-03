from enum import Enum, StrEnum, auto


class SiteData(Enum):
  """
  An enumeration class for site data.

  Attributes:
      TIMESTEP (Enum): An enumeration member representing the timestep.
      ENERGY_INPUT (Enum): An enumeration member representing the energy input.
  """

  @staticmethod
  def _generate_next_value_(name: str, start: int, count: int, last_values):
    return count

  TIMESTEP = auto()
  ENERGY_INPUT = auto()


### Good source about how to use Enum:: https://codereview.stackexchange.com/questions/267948/using-python-enums-to-define-physical-units


class SimParameters(Enum):
  """
  An enumeration class for simulation parameters.

  Attributes:
      COST (Enum): An enumeration member representing the cost.
      TIMESTEP (Enum): An enumeration member representing the timestep.
      SIMULATION_UNIT (Enum): An enumeration member representing the simulation unit.
      PRICE_UNIT (Enum): An enumeration member representing the price unit.
      EMISSION_UNIT (Enum): An enumeration member representing the emission unit.
  """
  COST = 1, "GBP"
  TIMESTEP = 30, "minutes"
  SIMULATION_UNIT = 1, "kW"
  PRICE_UNIT = 1, "GBP/kWh"
  EMISSION_UNIT = 1, "kgCO2e/kWh"

  @property
  def magnitude(self) -> str:
    """Get the magnitude which is most commonly used for this unit."""
    return str(self.value[0])

  @property
  def units(self) -> str:
    """Get the units for which this unit is relevant."""
    return self.value[1]


class PhysicalQuantity(Enum):
  """
  An enumeration class for physical quantities.

  Attributes:
      TEMPERATURE (Enum): An enumeration member representing the temperature.
      ENERGY (Enum): An enumeration member representing the energy.
      TIME (Enum): An enumeration member representing the time.
      MASS (Enum): An enumeration member representing the mass.
      LENGTH (Enum): An enumeration member representing the length.
      POWER (Enum): An enumeration member representing the power.
      UNCATEGORIZED (Enum): An enumeration member representing an uncategorized quantity.
  """
  TEMPERATURE = auto()
  ENERGY = auto()
  TIME = auto()
  MASS = auto()
  LENGTH = auto()
  POWER = auto()
  UNCATEGORIZED = auto()

  @classmethod
  def _missing_(cls, value):
    return cls.UNCATEGORIZED


class EnergyCarrier(Enum):
  """
  An enumeration class for energy carriers.

  Attributes:
      ELECTRICITY (Enum): An enumeration member representing electricity.
      GAS (Enum): An enumeration member representing gas.
      HEAT (Enum): An enumeration member representing heat.
      COOLING (Enum): An enumeration member representing cooling.
      UNCATEGORIZED (Enum): An enumeration member representing an uncategorized energy carrier.

  Methods:
      _missing_: A method to handle missing values.
  """

  ELECTRICITY = auto()
  NATURALGAS = auto()
  HEATING = auto()
  COOLING = auto()
  UNCATEGORIZED = auto()
  NONE = auto()

  @classmethod
  def _missing_(cls, value):
    return cls.NONE


class Destination(Enum):
  """
  An enumeration class for energy carriers.

  Attributes:
      ELECTRICITY (Enum): An enumeration member representing electricity.
      GAS (Enum): An enumeration member representing gas.
      HEAT (Enum): An enumeration member representing heat.
      COOLING (Enum): An enumeration member representing cooling.
      UNCATEGORIZED (Enum): An enumeration member representing an uncategorized energy carrier.
  """

  IMPORT = auto()
  EXPORT = auto()
  ONSITE = auto()
  INPUT = auto()
  OUTPUT = auto()
  DEMAND = auto()


class TechnologyType(Enum):
  """
  An enumeration class for technology types.

  Attributes:
      PV (Enum): An enumeration member representing photovoltaic technology.
      WIND (Enum): An enumeration member representing wind technology.
      BATTERY (Enum): An enumeration member representing battery technology.
      CHP (Enum): An enumeration member representing combined heat and power technology.
      BOILER (Enum): An enumeration member representing boiler technology.
      HEATPUMP (Enum): An enumeration member representing heat pump technology.
      UNCATEGORIZED (Enum): An enumeration member representing an uncategorized technology type.
  """

  PV = "Photovoltaics panels"
  EV = "Electric vehicle chargers"
  WINDTURBINE = "Wind turbine"
  CHPPLANT = "Combined heat and power plant"
  BOILERPLANT = "Boiler"
  UNCATEGORIZED = "Uncategorized"
  HEATPUMP = "Heat-pump"
  GRID = "Main grid"
  SITE = "Site"


class DispatchStrategy(Enum):
  """
  An enumeration class for dispatch strategies.

  Attributes:
    ELECTRICITYLED (Enum): An enumeration member representing the electricity-led strategy.
    THERMALLED (Enum): An enumeration member representing the thermal-led strategy.
    CUSTOM (Enum): An enumeration member representing a custom strategy.
    ACTUAL (Enum): An enumeration member representing an actual strategy.
  """
  ELECTRICITYLED = auto()
  THERMALLED = auto()
  CUSTOM = auto()
  ACTUAL = auto()


class EnergyCharge(Enum):
  """
  An enumeration class for energy charges.

  Attributes:
    DUOS (Enum): An enumeration member representing the distribution use of system charge.
    CCL (Enum): An enumeration member representing the climate change levy charge.
    ENERGY_CHARGE (Enum): An enumeration member representing the energy charge.
    NIGHT_CHARGE (Enum): An enumeration member representing the night charge.
    DAY_CHARGE (Enum): An enumeration member representing the day charge.
    DUOS_AMBER (Enum): An enumeration member representing the distribution use of system charge for amber periods.
    DUOS_RED (Enum): An enumeration member representing the distribution use of system charge for red periods.
    DUOS_GREEN (Enum): An enumeration member representing the distribution use of system charge for green periods.
  """
  DUOS = auto()
  CCL = auto()
  ENERGY_CHARGE = auto()
  NIGHT_CHARGE = auto()
  DAY_CHARGE = auto()
  DUOS_AMBER = auto()
  DUOS_RED = auto()
  DUOS_GREEN = auto()


class Charts(Enum):
  """
  An enumeration class for charts.

  Attributes:
    HH_LABEL (Enum): An enumeration member representing the half-hourly chart.
    DAILY_LABEL (Enum): An enumeration member representing the daily chart.
    WEEKLY_LABEL (Enum): An enumeration member representing the weekly chart.
  """
  HH_LABEL = "half-hourly"
  DAILY_LABEL = "daily"
  WEEKLY_LABEL = "weekly"


class Season(Enum):
  """
  An enumeration class for seasons.

  Attributes:
    WINTER (Enum): An enumeration member representing the winter season.
    SUMMER (Enum): An enumeration member representing the summer season.
    SPRING (Enum): An enumeration member representing the spring season.
    AUTUMN (Enum): An enumeration member representing the autumn season.
  """
  WINTER = auto()
  SUMMER = auto()
  SPRING = auto()
  AUTUMN = auto()
