from dataclasses import dataclass


@dataclass
class GeoLocation:
  """
  A class used to store the geographical location.
  
  Attributes:
      name (str): The name of the location.
      latitude (float): The latitude of the location.
      longitude (float): The longitude of the location.
      altitude (float): The altitude of the location.
      timezone (str): The timezone of the location.
    
  """
  name: str
  latitude: float
  longitude: float
  altitude: float
  timezone: str
