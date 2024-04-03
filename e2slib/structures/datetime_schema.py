from enum import StrEnum


class DateTimeSchema(StrEnum):
  """A class used to represent a schema for datetime-related constants.

  Attributes:
    HOUR (str): Constant for hour.
    MINUTES (str): Constant for minutes.
    SECONDS (str): Constant for seconds.
    MONTH (str): Constant for month.
    DAYOFWEEK (str): Constant for day of the week.
    WEEKDAYFLAG (str): Constant for weekday flag.
    YEAR (str): Constant for year.
    HALFHOUR (str): Constant for half-hour.
    DATE (str): Constant for date.
    WEEK (str): Constant for week.
    DAYOFYEAR (str): Constant for day of the year.
    DATETIME (str): Constant for datetime.
    TIME (str): Constant for time.
    WEEKEND (str): Constant for weekend.
    SEASON (str): Constant for season.
    SEASON_NUM (str): Constant for season number.
  """

  HOUR = 'Hour'
  MINUTES = 'Minutes'
  SECONDS = 'Seconds'
  MONTH = 'Month'
  DAYOFWEEK = 'Day of week'
  WEEKDAYFLAG = 'Weekday flag'
  YEAR = 'Year'
  HALFHOUR = 'Half-hour'
  DATE = 'Date'
  WEEK = 'Week'
  DAYOFYEAR = 'Day of year'
  DATETIME = 'Datetime'
  TIME = 'time'
  WEEKEND = 'weekend'
  SEASON = 'season'
  SEASON_NUM = 'season_number'
