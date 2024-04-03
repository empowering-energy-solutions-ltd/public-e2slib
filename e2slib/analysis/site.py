import collections
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd

from e2slib.analysis import location
from e2slib.common import common
from e2slib.structures import enums, protocols, site_schema
from e2slib.utillib import functions


def sum_dict(list_dict: list[dict[Any, float]]) -> dict[Any, float]:
  counter = collections.Counter()
  for d in list_dict:
    counter.update(d)
  return dict(counter)


@dataclass
class Site:
  """
  A class used to represent a site.

  Attributes:
      name (str): The name of the site.
      geolocation (location.GeoLocation): The geolocation of the site.
      list_asset_aggregator (list[protocols.AssetAggregator]): The list of asset aggregators in the site.
      site_electricity_demand (pd.DataFrame): The site electricity demand (default is an empty DataFrame).
      saving_path (Path): The path to save the results (default is the parent directory of the current directory).

  Methods:
      timezone(): Get the timezone of the site.
      size_system(): Get the size of the systems in the site.
      capital_cost(): Get the capital cost of the systems in the site.
      annual_maintenance_cost(): Get the annual maintenance cost of the systems in the site.
      add_asset_aggregator(asset_aggregator: protocols.AssetAggregator): Add an asset aggregator to the site.
      format_site_electricity_demand_data(): Format the site electricity demand data.
      get_total_capacity_installed(): Get the total capacity installed in the site.
      get_import_and_export_demand(dataf: pd.DataFrame): Get the import and export demand from the site electricity demand.
      aggregators_additional_demand(): Get the additional demand from the asset aggregators.
      total_additional_demand(): Get the total additional demand from the asset aggregators.
      get_dict_assets(): Get the dictionary of assets in the site.
      aggregators_onsite_generation(): Get the onsite generation from the asset aggregators.
      total_onsite_generation(): Get the total onsite generation from the asset aggregators.
      get_avoided_electricity_import(onsite_gen: pd.DataFrame, export_demand: pd.DataFrame): Get the avoided electricity import from the onsite generation and export demand.
      export_results(): Export the results of the site analysis.
  """
  name: str
  geolocation: location.GeoLocation
  list_asset_aggregator: list[protocols.AssetAggregator]
  site_electricity_demand: pd.DataFrame = field(default_factory=pd.DataFrame)
  saving_path: Path = Path(r"../")

  def __post_init__(self):
    self.format_site_electricity_demand_data()
    print(f"The results will be stored at:\n{self.saving_path.resolve()}")

  @property
  def timezone(self) -> str:
    return self.geolocation.timezone

  @property
  def size_system(self) -> dict[enums.TechnologyType, float]:
    frames: list[dict[enums.TechnologyType, float]] = []
    for temp_asset_aggregator in self.list_asset_aggregator:
      frames.append(temp_asset_aggregator.size_system)
    return sum_dict(frames)

  @property
  def capital_cost(self) -> dict[enums.TechnologyType, float]:
    frames: list[dict[enums.TechnologyType, float]] = []
    for temp_asset_aggregator in self.list_asset_aggregator:
      frames.append(temp_asset_aggregator.capital_cost)
    return sum_dict(frames)

  @property
  def annual_maintenance_cost(self) -> dict[enums.TechnologyType, float]:
    frames: list[dict[enums.TechnologyType, float]] = []
    for temp_asset_aggregator in self.list_asset_aggregator:
      frames.append(temp_asset_aggregator.annual_maintenance_cost)
    return sum_dict(frames)

  def add_asset_aggregator(
      self, asset_aggregator: protocols.AssetAggregator) -> None:
    self.list_asset_aggregator.append(asset_aggregator)

  def format_site_electricity_demand_data(self) -> None:
    if self.site_electricity_demand.shape[1] == 1:
      self.site_electricity_demand = functions.resample_and_fill_missing_data(
          self.site_electricity_demand, freq="30min")

      demand_datetimeindex: pd.DatetimeIndex = self.site_electricity_demand.index
      if demand_datetimeindex.tzinfo is None:
        self.site_electricity_demand.index = demand_datetimeindex.tz_localize(
            self.geolocation.timezone)
      else:
        self.site_electricity_demand.index = demand_datetimeindex.tz_convert(
            self.geolocation.timezone)

      self.site_electricity_demand.index.name = site_schema.SiteDataSchema.INDEX
      self.site_electricity_demand.columns = common.get_multiindex_single_column(
          site_schema.SiteDataSchema.INIT_SITE_ELECTRICITY_DEMAND)
    else:
      print(
          'The site_electricity_demand dataframe has too many columns or was not provided. Some functions of this class may not work.'
      )

  def get_import_and_export_demand(
      self, dataf: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Get the import and export demand from the site electricity demand.

    Args:
      dataf (pd.DataFrame): The site electricity demand.

    Returns:
      tuple[pd.DataFrame, pd.DataFrame]: The import and export demand from the site electricity demand.
    """
    import_dataf = dataf.copy()

    filt = import_dataf.values < 0
    import_dataf.loc[filt] = 0

    export_dataf = dataf.copy()
    filt = export_dataf.values > 0
    export_dataf.loc[filt] = 0
    export_dataf = -export_dataf

    import_dataf.columns = common.get_multiindex_single_column(
        site_schema.SiteDataSchema.IMPORT_ELECTRICITY_DEMAND)
    export_dataf.columns = common.get_multiindex_single_column(
        site_schema.SiteDataSchema.EXPORT_ELECTRICITY_DEMAND)
    return import_dataf, export_dataf

  def aggregators_additional_demand(self) -> pd.DataFrame:
    """
    Get the additional demand from the asset aggregators.
    
    Returns:
        pd.DataFrame: The additional demand from the asset aggregators.
    """
    frames = []
    additional_demand = pd.DataFrame()
    for temp_aggregator in self.list_asset_aggregator:
      temp_dataf = pd.concat(
          {temp_aggregator.name: temp_aggregator.additional_demand}, axis=1)
      frames.append(temp_dataf)
      additional_demand = pd.concat(frames, axis=1)
    return additional_demand

  def total_additional_demand(self) -> pd.DataFrame:
    """Total site additional demand from EV chargers, etc.
    
    Returns:
        pd.DataFrame: The total additional demand from the asset aggregators.
    """
    col_name = common.get_multiindex_single_column(
        site_schema.SiteDataSchema.ADDITIONAL_ELECTRICITY_DEMAND)
    systems_demand = self.aggregators_additional_demand()
    if len(systems_demand) == 0:
      systems_demand = pd.DataFrame(index=self.site_electricity_demand.index,
                                    columns=col_name)
      systems_demand.iloc[:, 0] = 0
    else:
      systems_demand = systems_demand.sum(axis=1).to_frame()
      systems_demand.columns = col_name
    return systems_demand.astype(float)

  def aggregators_onsite_generation(self) -> pd.DataFrame:
    """Get the onsite generation from the asset aggregators.
    
    Returns:
        pd.DataFrame: The onsite generation from the asset aggregators.
    """
    frames = []
    onsite_gen = pd.DataFrame()
    for temp_aggregator in self.list_asset_aggregator:
      temp_dataf = pd.concat(
          {temp_aggregator.name: temp_aggregator.onsite_generation}, axis=1)
      frames.append(temp_dataf)
      onsite_gen = pd.concat(frames, axis=1)
    return onsite_gen

  def total_onsite_generation(self) -> pd.DataFrame:
    """Total site electricity generation.
    
    Returns:
        pd.DataFrame: The total onsite generation from the asset aggregators.
    """
    col_name = common.get_multiindex_single_column(
        site_schema.SiteDataSchema.ELECTRICITY_GENERATION)
    onsite_gen = self.aggregators_onsite_generation()
    if len(onsite_gen) == 0:
      onsite_gen = pd.DataFrame(index=self.site_electricity_demand.index,
                                columns=col_name)
      onsite_gen.iloc[:, 0] = 0
    else:
      onsite_gen = onsite_gen.sum(axis=1).to_frame()
      onsite_gen.columns = col_name
    return onsite_gen.astype(float)

  def get_avoided_electricity_import(
      self, onsite_gen: pd.DataFrame,
      export_demand: pd.DataFrame) -> pd.DataFrame:
    """
    Get the avoided electricity import from the onsite generation and export demand.

    This method calculates the avoided electricity import by comparing the onsite generation
    with the export demand.

    Args:
        onsite_gen (pd.DataFrame): The onsite generation DataFrame.
        export_demand (pd.DataFrame): The export demand DataFrame.

    Returns:
        pd.DataFrame: The avoided electricity import from the onsite generation and export demand.
    """
    avoided_import = onsite_gen.copy()
    filt = export_demand.values > 0
    avoided_import.loc[filt] = self.site_electricity_demand.loc[filt]
    avoided_import.columns = common.get_multiindex_single_column(
        site_schema.SiteDataSchema.SELF_CONSUMED_ELECTRICITY)
    return avoided_import

  def export_results(self) -> pd.DataFrame:
    """Export the results of the site analysis.
    
    Returns:
        pd.DataFrame: The results of the site analysis.
    """
    additional_demand = self.total_additional_demand()
    on_site_gen = self.total_onsite_generation()
    total_elec_demand = self.site_electricity_demand.copy()
    total_elec_demand = total_elec_demand + additional_demand.values
    net_elec_demand = total_elec_demand.copy()
    net_elec_demand = total_elec_demand - on_site_gen.values
    import_demand, export_demand = self.get_import_and_export_demand(
        net_elec_demand)
    avoided_import_electricity = self.get_avoided_electricity_import(
        on_site_gen, export_demand)
    return pd.concat([
        import_demand, export_demand, on_site_gen, additional_demand,
        self.site_electricity_demand, avoided_import_electricity
    ],
                     axis=1).astype(float)
