from dataclasses import dataclass

import pandas as pd

from e2slib.structures import datetime_schema


@dataclass
class OccupancySchedule:
  """
  A class used to represent an occupancy schedule for each day of the week for each hour.

  Attributes:
      occupancy_dict (dict[int, list[tuple[int, int]]] | None): A dictionary where the keys are the days of the week (0-6) and the values are lists of tuples representing the start and end times of occupancy.
      timestep (enums.TimeStep): The timestep of the occupancy schedule.

  Methods:
      or_operator(list_1: list[bool], list_2: list[bool]) -> list[bool]: Perform a logical OR operation on two lists of boolean values.
      and_operator(list_1: list[bool], list_2: list[bool]) -> list[bool]: Perform a logical AND operation on two lists of boolean values.
      get_filter(dataf: pd.DataFrame) -> list[bool]: Get a filter for a DataFrame based on the occupancy schedule.
      filter_df(dataf: pd.DataFrame, occupied: bool = True): Filter a DataFrame with datetimeindex based on the occupancy schedule.
  """
  occupancy_dict: dict[int, list[tuple[int, int]]] | None = None
  timestep: datetime_schema.DateTimeSchema = datetime_schema.DateTimeSchema.HALFHOUR

  def __post_init__(self):
    if self.occupancy_dict is None:
      default_occupancy: dict[int, list[tuple[int, int]]] = {
          0: [(16, 34)],
          1: [(16, 34)],
          2: [(16, 34)],
          3: [(16, 34)],
          4: [(16, 34)],
          5: [],
          6: []
      }
      self.occupancy_dict = default_occupancy

  def or_operator(self, list_1: list[bool], list_2: list[bool]) -> list[bool]:
    return [a or b for a, b in zip(list_1, list_2)]

  def and_operator(self, list_1: list[bool], list_2: list[bool]) -> list[bool]:
    return [a and b for a, b in zip(list_1, list_2)]

  def get_filter(self, dataf: pd.DataFrame) -> list[bool]:
    """
    Get a filter for a DataFrame based on the occupancy schedule.

    Args:
        dataf (pd.DataFrame): The DataFrame to filter.

    Returns:
        list[bool]: The filter for the DataFrame.
    """
    temp_filt = [False] * len(dataf)
    temp_day_filt = [False] * len(dataf)
    time_col = self.timestep
    assert self.occupancy_dict is not None
    for temp_day, temp_hours in self.occupancy_dict.items():
      print(temp_day)
      temp_day_filt = list(
          (dataf[datetime_schema.DateTimeSchema.DAYOFWEEK] == temp_day))
      temp_final_time_filt = [False] * len(dataf)
      for start_time, end_time in temp_hours:
        start_time_filt = list(start_time <= dataf[time_col])
        end_time_filt = list(dataf[time_col] <= end_time)
        temp_time_filt = self.and_operator(start_time_filt, end_time_filt)
        temp_final_time_filt = self.or_operator(temp_final_time_filt,
                                                temp_time_filt)

      temp_day_filt = self.and_operator(temp_day_filt, temp_final_time_filt)
      temp_filt = self.or_operator(temp_filt, temp_day_filt)
    return temp_filt

  def filter_df(self, dataf: pd.DataFrame, occupied: bool = True):
    """
    Filter a DataFrame with datetimeindex based on the occupancy schedule.

    Args:
        dataf (pd.DataFrame): The DataFrame to filter.
        occupied (bool, optional): Whether to filter for occupied or unoccupied times. Defaults to True.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    filt = self.get_filter(dataf)
    if occupied:
      return dataf[filt]
    else:
      filt = [not a for a in filt]
      return dataf[filt]
