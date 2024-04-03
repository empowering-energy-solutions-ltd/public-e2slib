import numpy as np
import pandas as pd

from e2slib.structures import datetime_schema, enums


def get_season(month: int) -> str:
  """
  Get the season for a given month.
  
  Args:
      month (int): The month for which to get the season.
      
  Returns:
      str: The season of the given month.
  """
  if 3 <= month <= 5:  #April and May
    return enums.Season.SPRING.name
  elif 6 <= month <= 8:  # June, July, August
    return enums.Season.SUMMER.name
  elif 9 <= month <= 11:  # September, October and November
    return enums.Season.AUTUMN.name
  else:
    return enums.Season.WINTER.name


def add_time_features(dataf: pd.DataFrame) -> pd.DataFrame:
  """
  Add time features to a DataFrame.
  
  Args:
      dataf (pd.DataFrame): The DataFrame to which to add the time features.

  Returns:
      pd.DataFrame: The DataFrame with added time features.
  """
  new_dataf = dataf.copy()
  new_dataf_index: pd.DatetimeIndex = new_dataf.index
  new_dataf[datetime_schema.DateTimeSchema.HOUR] = new_dataf_index.hour
  new_dataf[
      datetime_schema.DateTimeSchema.DAYOFWEEK] = new_dataf_index.dayofweek
  new_dataf[
      datetime_schema.DateTimeSchema.DAYOFYEAR] = new_dataf_index.dayofyear
  new_dataf[datetime_schema.DateTimeSchema.MONTH] = new_dataf_index.month
  new_dataf[datetime_schema.DateTimeSchema.YEAR] = new_dataf_index.year
  new_dataf[datetime_schema.DateTimeSchema.WEEKDAYFLAG] = [
      'weekday' if x < 5 else 'weekend' for x in new_dataf_index.dayofweek
  ]
  new_dataf[datetime_schema.DateTimeSchema.
            HALFHOUR] = new_dataf_index.hour * 2 + new_dataf_index.minute // 30
  new_dataf[datetime_schema.DateTimeSchema.HALFHOUR] = new_dataf[
      datetime_schema.DateTimeSchema.HALFHOUR].astype(int)
  new_dataf[datetime_schema.DateTimeSchema.DATE] = new_dataf_index.date
  new_dataf[
      datetime_schema.DateTimeSchema.WEEK] = new_dataf_index.isocalendar().week
  new_dataf[datetime_schema.DateTimeSchema.SEASON] = new_dataf[
      datetime_schema.DateTimeSchema.MONTH].map(get_season)

  season_dict = {
      enums.Season.WINTER.name: 1,
      enums.Season.SPRING.name: 2,
      enums.Season.SUMMER.name: 3,
      enums.Season.AUTUMN.name: 4
  }
  new_dataf[datetime_schema.DateTimeSchema.SEASON_NUM] = new_dataf[
      datetime_schema.DateTimeSchema.SEASON].map(lambda x: season_dict[x])

  return new_dataf


def remove_zero_values(dataf: pd.DataFrame) -> pd.DataFrame:
  """
  Replace zero values with NaN in a DataFrame.
  
  Args:
      dataf (pd.DataFrame): The DataFrame to process.

  Returns:
      pd.DataFrame: The DataFrame with zero values replaced by NaN.
  """
  filt = dataf.values == 0
  dataf.loc[filt] = np.nan
  return dataf


def fill_missing_data(dataf: pd.DataFrame) -> pd.DataFrame:
  """
  Fill a dataframe using linear interpolation.
  
  Args:
      dataf (pd.DataFrame): The DataFrame to process.

  Returns:
      pd.DataFrame: The DataFrame with missing data filled.
  """
  return dataf.fillna(dataf.interpolate())


def resample_and_fill_missing_data(input_dataf: pd.DataFrame,
                                   freq: str = '30min') -> pd.DataFrame:
  """
  Resample a DataFrame and fill missing data.

  Args:
      input_dataf (pd.DataFrame): The DataFrame to process.
      freq (str, optional): The frequency to resample to, by default '30min'

  Returns:
      pd.DataFrame: The resampled DataFrame with missing data filled.
  """
  dataf = input_dataf.copy()
  dataf = dataf.resample(freq).mean()
  return fill_missing_data(dataf)


def get_avg_week_by_season_df(
    dataf: pd.DataFrame,
    target_col: str,
    timestep: datetime_schema.DateTimeSchema = datetime_schema.DateTimeSchema.
    HOUR,
    func=np.mean) -> pd.DataFrame:
  """
  Get the average demand for each season and day of the week.

  Args:
      dataf (pd.DataFrame): The DataFrame to process.
      target_col (str): The column to aggregate.
      timestep (enums.TimeStep, optional): The timestep of the data, by default enums.TimeStep.HALFHOUR
      func (function, optional): The aggregation function, by default np.mean
  
  Returns:
      pd.DataFrame: The DataFrame with the average demand for each season and day of the week.
  """
  groupby_cols = [
      datetime_schema.DateTimeSchema.SEASON,
      datetime_schema.DateTimeSchema.DAYOFWEEK, timestep
  ]
  gb_dataf = dataf.groupby(groupby_cols).agg({target_col: func}).unstack(0)
  gb_dataf.columns = [c[1] for c in gb_dataf.columns]
  gb_dataf = gb_dataf[[c.name for c in enums.Season]]
  return gb_dataf


def format_avg_week_index(
    dataf: pd.DataFrame, timestep: datetime_schema.DateTimeSchema) -> pd.Index:
  """
  Format the index of an average week DataFrame.
  
  Args:
      dataf (pd.DataFrame): The DataFrame to process.
      timestep (enums.TimeStep): The timestep of the data.

  Returns:
      pd.Index: The formatted index of the DataFrame.
  """
  if timestep is datetime_schema.DateTimeSchema.HALFHOUR:
    return dataf.index.get_level_values(0) + (
        (1 / 48) * dataf.index.get_level_values(1))
  else:
    return dataf.index.get_level_values(0) + (
        (1 / 24) * dataf.index.get_level_values(1))
