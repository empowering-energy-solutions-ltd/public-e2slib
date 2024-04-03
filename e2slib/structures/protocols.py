from dataclasses import dataclass
from typing import Protocol

import pandas as pd

from e2slib.structures import enums


@dataclass
class AssetAggregator(Protocol):
  """
  A class used to represent an asset aggregator.

  Attributes:
      name (str): The name of the asset aggregator.

  Methods:
      size_system() -> dict[enums.TechnologyType, float]:
          Get the size of the system for each technology type.
      capital_cost() -> dict[enums.TechnologyType, float]:
          Get the capital cost for each technology type.
      annual_maintenance_cost() -> dict[enums.TechnologyType, float]:
          Get the annual maintenance cost for each technology type.
      lifetime() -> int:
          Get the lifetime of the asset aggregator.
      additional_demand() -> pd.DataFrame:
          Get the additional demand as a DataFrame.
      onsite_generation() -> pd.DataFrame:
          Get the onsite generation as a DataFrame.
      export_results() -> pd.DataFrame:
          Export the results as a DataFrame.
  """

  name: str

  @property
  def size_system(self) -> dict[enums.TechnologyType, float]:
    """
    Get the size of the system for each technology type.

    Returns:
        dict[enums.TechnologyType, float]: The size of the system for each technology type.
    """
    ...

  @property
  def capital_cost(self) -> dict[enums.TechnologyType, float]:
    """
    Get the capital cost for each technology type.

    Returns:
        dict[enums.TechnologyType, float]: The capital cost for each technology type.
    """
    ...

  @property
  def annual_maintenance_cost(self) -> dict[enums.TechnologyType, float]:
    """
    Get the annual maintenance cost for each technology type.

    Returns:
        dict[enums.TechnologyType, float]: The annual maintenance cost for each technology type.
    """
    ...

  @property
  def lifetime(self) -> int:
    """
    Get the lifetime of the asset aggregator.

    Returns:
        int: The lifetime of the asset aggregator.
    """
    ...

  @property
  def additional_demand(self) -> pd.DataFrame:
    """
    Get the additional demand as a DataFrame.

    Returns:
        pd.DataFrame: The additional demand as a DataFrame.
    """
    ...

  @property
  def onsite_generation(self) -> pd.DataFrame:
    """
    Get the onsite generation as a DataFrame.

    Returns:
        pd.DataFrame: The onsite generation as a DataFrame.
    """
    ...

  def export_results(self) -> pd.DataFrame:
    """
    Export the results as a DataFrame.

    Returns:
        pd.DataFrame: The results as a DataFrame.
    """
    ...


@dataclass
class SiteModel(Protocol):
  """
  A class used to represent a site model.

  Methods:
      size_sysem() -> dict[enums.TechnologyType, float]:
          Get the size of the system for each technology type.
      capital_cost() -> dict[enums.TechnologyType, float]:
          Get the capital cost for each technology type.
      annual_maintenance_cost() -> dict[enums.TechnologyType, float]:
          Get the annual maintenance cost for each technology type.
      export_results() -> pd.DataFrame:
          Export the results as a DataFrame.
      timezone() -> str:
          Get the timezone of the site model.
      add_asset_aggregator(asset_aggregator: AssetAggregator) -> None:
          Add an asset aggregator to the site model.
  """

  @property
  def size_sysem(self) -> dict[enums.TechnologyType, float]:
    """
    Get the size of the system for each technology type.

    Returns:
        dict[enums.TechnologyType, float]: The size of the system for each technology type.
    """
    ...

  @property
  def capital_cost(self) -> dict[enums.TechnologyType, float]:
    """
    Get the capital cost for each technology type.

    Returns:
        dict[enums.TechnologyType, float]: The capital cost for each technology type.
    """
    ...

  @property
  def annual_maintenance_cost(self) -> dict[enums.TechnologyType, float]:
    """
    Get the annual maintenance cost for each technology type.

    Returns:
        dict[enums.TechnologyType, float]: The annual maintenance cost for each technology type.
    """
    ...

  def export_results(self) -> pd.DataFrame:
    """
    Export the results as a DataFrame.

    Returns:
        pd.DataFrame: The results as a DataFrame.
    """
    ...

  @property
  def timezone(self) -> str:
    """
    Get the timezone of the site model.

    Returns:
        str: The timezone of the site model.
    """
    ...

  def add_asset_aggregator(self, asset_aggregator: AssetAggregator) -> None:
    """
    Add an asset aggregator to the site model.

    Args:
        asset_aggregator (AssetAggregator): The asset aggregator to add.
    """
    ...
