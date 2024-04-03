import math
import random
from datetime import datetime, time

import numpy as np
import pandas as pd
import pytz

from e2slib.structures import site_schema

random.seed(42)


def generate_annual_timesteps(year: int) -> pd.DatetimeIndex:
  """
  Generate a DatetimeIndex for a year with a 30 minute frequency.
  
  Args:
      year (int): The year for which to generate the DatetimeIndex.

  Returns:
      pd.DatetimeIndex: The generated DatetimeIndex.
  """
  return pd.date_range(datetime(year, 1, 1, 0, 0, tzinfo=pytz.UTC),
                       datetime(year, 12, 31, 23, 59, 59, tzinfo=pytz.UTC),
                       freq="30min",
                       tz="UTC")


def generate_dummy_demand_values(timestamp) -> int:
  """
  Generate dummy demand values for a timestamp.
  
  Args:
      timestamp (pd.Timestamp): The timestamp for which to generate the demand value.

  Returns:
      int: The generated demand value.
  """
  if time(7, 0) <= timestamp.time() <= time(18,
                                            0) and timestamp.dayofweek <= 4:
    return random.randint(10, 40)
  else:
    return random.randint(0, 10)


def create_dummy_site_demand(year: int) -> pd.DataFrame:
  """
  Create a dummy site demand DataFrame for a year.
  
  Args:
      year (int): The year for which to generate the site demand.

  Returns:
      pd.DataFrame: The generated site demand DataFrame.
  """
  timesteps = generate_annual_timesteps(year=year)
  dummy_site_demand = pd.DataFrame(index=timesteps)
  dummy_site_demand['Site energy [kWh]'] = dummy_site_demand.index.to_series(
  ).apply(generate_dummy_demand_values)
  return dummy_site_demand


def dummy_duos_timetable(red: float, amber: float, green: float, day: float,
                         night: float) -> list:
  """
  Generate a dummy DUoS timetable.
  
  Args:
      red (float): The red charge.
      amber (float): The amber charge.
      green (float): The green charge.
      day (float): The day charge.
      night (float): The night charge.

  Returns:
      list: The generated DUoS timetable.
  """
  return [(time(16, 0), time(20, 0), red + day),
          (time(6, 0), time(16, 0), amber + day),
          (time(0, 0), time(6, 0), green + night),
          (time(20, 0), time(23, 59, 59), green + day)]


def dummy_duos_values(red: float = 0.0518,
                      amber: float = 0.00518,
                      green: float = 0.00051,
                      day: float = 0.1950,
                      night: float = 0.1430) -> list:
  """
  Generate dummy DUoS values.

  Args:
      red (float): The red charge.
      amber (float): The amber charge.
      green (float): The green charge.
      day (float): The day charge.
      night (float): The night charge.

  Returns:
      list: The generated DUoS values.
  """
  return dummy_duos_timetable(red, amber, green, day, night)


def generate_dummy_price_profile(year: int) -> pd.DataFrame:
  """
  Generate a dummy price profile for a year.
  
  Args:
      year (int): The year for which to generate the price profile.
  
  Returns:
      pd.DataFrame: The generated price profile DataFrame.
  """
  timesteps = generate_annual_timesteps(year)
  column = pd.MultiIndex.from_tuples(
      [site_schema.ResultsSchema.IMPORT_ELECTRICITY_PRICES])
  dummy_prices = pd.DataFrame(index=timesteps, columns=column)
  for timestamp in timesteps:
    time_of_day = timestamp.time()
    for start_time, end_time, charge in dummy_duos_values():
      if start_time <= time_of_day <= end_time:
        dummy_prices.loc[timestamp, column] = charge
        break
  return dummy_prices


def generate_dummy_carbon_profile(year: int) -> pd.DataFrame:
  """
  Generate a dummy carbon profile for a year.
  
  Args:
      year (int): The year for which to generate the carbon profile.
      
  Returns:
      pd.DataFrame: The generated carbon profile DataFrame.
  """
  dummy_carbon = pd.DataFrame(index=generate_annual_timesteps(year=year))
  # Set parameters
  length = len(dummy_carbon)
  amplitude = 20
  mean_value = 180
  randomness = 1
  wavelength = 36

  times = np.arange(length)
  random_noise = np.random.uniform(-randomness, randomness, length)
  sin_variable = 2 * np.pi * times / wavelength
  dummy_carbon['actual'] = amplitude * np.sin(sin_variable) + (
      mean_value + dummy_carbon.index.hour) + random_noise
  return dummy_carbon
