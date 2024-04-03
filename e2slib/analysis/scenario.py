from dataclasses import dataclass, field

import pandas as pd

from e2slib.common import common
from e2slib.structures import protocols, site_schema


@dataclass
class Scenario:
  """
  A class used to represent a scenario.

  Attributes:
      name (str): The name of the scenario.
      site_model (protocols.SiteModel): The site model of the scenario.
      site_energy_demand (pd.DataFrame): The site energy demand of the scenario (default is an empty DataFrame).
      description (str): The description of the scenario (default is an empty string).
      import_electricity_emission_factor (pd.DataFrame): The import electricity emission factor of the scenario (default is an empty DataFrame).
      import_electricity_prices (pd.DataFrame): The import electricity prices of the scenario (default is an empty DataFrame).
      export_electricity_prices (pd.DataFrame): The export electricity prices of the scenario (default is an empty DataFrame).
      discount_rate (float): The discount rate of the scenario (default is 0.0).
      summary_results (pd.DataFrame): The summary results of the scenario (default is an empty DataFrame).
      cashflow_data (pd.DataFrame): The cashflow data of the scenario (default is an empty DataFrame).

  Methods:
      __post_init__(): Initialize the scenario.
      add_asset_aggregator(asset): Add an asset aggregator to the site model of the scenario.
      update_results(): Update the site energy demand and the summary results of the scenario.
      set_default_export_electricity_prices(value): Set a default value if no export electricity prices are provided.
      set_default_import_electricity_emission_factor(): Set a default import electricity emission factor.
  """
  name: str
  site_model: protocols.SiteModel
  site_energy_demand: pd.DataFrame = field(
      default_factory=pd.DataFrame)  #See site_schema.SiteDataSchema for format
  description: str = ''
  import_electricity_emission_factor: pd.DataFrame = field(
      default_factory=pd.DataFrame)  #kgCO2e/kWh
  import_electricity_prices: pd.DataFrame = field(default_factory=pd.DataFrame)
  export_electricity_prices: pd.DataFrame = field(default_factory=pd.DataFrame)
  discount_rate: float = 0.  #for investment
  summary_results: pd.DataFrame = field(default_factory=pd.DataFrame)
  cashflow_data: pd.DataFrame = field(default_factory=pd.DataFrame)

  def __post_init__(self) -> None:
    self.format_site_import_electricity_prices()
    self.set_default_import_electricity_emission_factor()
    self.set_default_export_electricity_prices()
    self.update_results()

  def add_asset_aggregator(self, asset: protocols.AssetAggregator) -> None:
    """Add an asset aggregator to the scenario."""
    self.site_model.add_asset_aggregator(asset)

  def update_results(self) -> None:
    """Update the results of the scenario."""
    self.site_energy_demand = self.site_model.export_results()
    self.summary_results = self.export_results()

  def set_default_export_electricity_prices(self, value: float = 0):
    """
    Set a default value if no export electricity prices are provided.

    If the export electricity prices DataFrame is empty, this method will copy the import electricity prices DataFrame,
    rename its columns to 'EXPORT_ELECTRICITY_REVENUES', and set all its values to the provided default value.

    Args:
        value (float, optional): The default value to set for export electricity prices. Defaults to 0.
    """
    if len(self.export_electricity_prices) == 0:
      self.export_electricity_prices = self.import_electricity_prices.copy()
      self.export_electricity_prices.columns = common.get_multiindex_single_column(
          site_schema.ResultsSchema.EXPORT_ELECTRICITY_REVENUES)
      self.export_electricity_prices.iloc[:, 0] = value

  def set_default_import_electricity_emission_factor(self,
                                                     value: float = 0.150):
    """
    Set a default value if no import electricity emission factor is provided.

    If the import electricity emission factor DataFrame is empty, this method will copy the import electricity prices DataFrame,
    rename its columns to 'GHG_INTENSITY_IMPORT_ELECTRICITY', and set all its values to the provided default value.

    Args:
        value (float, optional): The default value to set for import electricity emission factor. Defaults to 0.150.
    """
    if len(self.import_electricity_emission_factor) == 0:
      self.import_electricity_emission_factor = self.import_electricity_prices.copy(
      )
      self.import_electricity_emission_factor.columns = common.get_multiindex_single_column(
          site_schema.ResultsSchema.GHG_INTENSITY_IMPORT_ELECTRICITY)
      self.import_electricity_emission_factor.iloc[:, 0] = value

  @property
  def export_demand(self) -> pd.DataFrame:
    col_name = site_schema.SiteDataSchema.EXPORT_ELECTRICITY_DEMAND
    return self.site_energy_demand[col_name].to_frame().copy()

  @property
  def import_demand(self) -> pd.DataFrame:
    col_name = site_schema.SiteDataSchema.IMPORT_ELECTRICITY_DEMAND
    return self.site_energy_demand[col_name].to_frame().copy()

  @property
  def avoided_import(self) -> pd.DataFrame:
    col_name = site_schema.SiteDataSchema.SELF_CONSUMED_ELECTRICITY
    return self.site_energy_demand[col_name].to_frame().copy()

  @property
  def onsite_generation(self) -> pd.DataFrame:
    col_name = site_schema.SiteDataSchema.ELECTRICITY_GENERATION
    return self.site_energy_demand[col_name].to_frame().copy()

  @property
  def timezone(self) -> str:
    return self.site_model.timezone

  def get_col_name(self, col: tuple[str, ...]) -> tuple[str, ...]:
    return common.get_multiindex_single_column(col)[0]

  def format_site_import_electricity_prices(self) -> None:
    """
    Format the import electricity prices DataFrame.
    """
    if self.import_electricity_prices.shape[1] == 1:
      price_datetimeindex: pd.DatetimeIndex = self.import_electricity_prices.index
      if price_datetimeindex.tzinfo is None:
        self.import_electricity_prices.index = price_datetimeindex.tz_localize(
            self.timezone)
      else:
        self.import_electricity_prices.index = price_datetimeindex.tz_convert(
            self.timezone)
      self.import_electricity_prices.index.name = site_schema.ResultsSchema.INDEX
      self.import_electricity_prices.columns = common.get_multiindex_single_column(
          site_schema.ResultsSchema.IMPORT_ELECTRICITY_PRICES)
    else:
      print(
          'The import_electricity_prices dataframe has too many columns or was not provided. Some functions of this class may not work.'
      )

  def calculate_electricity_import_operation_cost(self) -> pd.DataFrame:
    """Calculate the electricity import operation cost based on a dataframe
    where first column is import electricity and second column export electricity
    
    Returns:
      pd.DataFrame: A DataFrame with the electricity import operation cost."""
    dataf = self.import_demand.mul(self.import_electricity_prices.values,
                                   axis=0)
    dataf.columns = common.get_multiindex_single_column(
        site_schema.ResultsSchema.IMPORT_ELECTRICITY_COSTS)
    return dataf

  def calculate_electricity_export_operation_cost(self) -> pd.DataFrame:
    """Calculate the electricity export operation cost based on a dataframe
    where first column is import electricity and second column export electricity.
    
    Returns:
      pd.DataFrame: A DataFrame with the electricity export operation cost."""
    dataf = self.export_demand.mul(self.export_electricity_prices.values,
                                   axis=0)
    dataf.columns = common.get_multiindex_single_column(
        site_schema.ResultsSchema.EXPORT_ELECTRICITY_REVENUES)
    return dataf

  def calculate_electricity_associated_emissions(self) -> pd.DataFrame:
    """
    Calculate the electricity associated emissions from the site.

    This method calculates the emissions by multiplying the import electricity emissions by the import electricity emission factor.

    Returns:
        pd.DataFrame: A DataFrame containing the electricity associated emissions.
    """
    dataf = self.import_demand.mul(
        self.import_electricity_emission_factor.values, axis=0)
    dataf.columns = common.get_multiindex_single_column(
        site_schema.ResultsSchema.GHG_EMISSIONS_IMPORT_ELECTRICITY)
    return dataf

  def calculate_site_electricity_avoided_emissions(self) -> pd.DataFrame:
    """
    Calculate the site avoided emissions from self-consuming electricity from PV system.

    This method calculates the avoided emissions by multiplying the avoided import emissions by the import electricity emission factor.

    Returns:
        pd.DataFrame: A DataFrame containing the site avoided emissions.    
    
    """
    dataf = self.avoided_import.mul(
        self.import_electricity_emission_factor.values, axis=0)
    dataf.columns = common.get_multiindex_single_column(
        site_schema.ResultsSchema.SITE_GHG_EMISSIONS_DISPLACED)
    return dataf

  def calculate_total_electricity_avoided_emissions(self) -> pd.DataFrame:
    """
    Calculate the total avoided emissions from the site.

    This method calculates the total avoided emissions by summing the avoided import emissions and the onsite generation emissions.

    Returns:
        pd.DataFrame: A DataFrame containing the total avoided emissions.
    """
    dataf = self.onsite_generation.mul(
        self.import_electricity_emission_factor.values, axis=0)
    dataf.columns = common.get_multiindex_single_column(
        site_schema.ResultsSchema.TOTAL_GHG_EMISSIONS_DISPLACED)
    return dataf

  def calculate_electricity_operation_cost(self):
    """
    Calculate the electricity operation cost based on a dataframe
    where first column is import electricity and second column export electricity.

    This method calculates the import and export electricity operation costs and concatenates them into a single DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the electricity import and export operation costs.
    """
    import_cost = self.calculate_electricity_import_operation_cost()
    export_cost = self.calculate_electricity_export_operation_cost()
    return pd.concat([import_cost, export_cost], axis=1)

  def calculate_electricity_import_savings(self) -> pd.DataFrame:
    """
    Calculate the electricity import savings from self-consuming electricity from PV system.

    This method calculates the savings by multiplying the avoided import electricity by the import electricity prices.
    The result is a DataFrame with a single column named 'ELECTRICITY_SAVINGS'.

    Returns:
        pd.DataFrame: A DataFrame containing the electricity import savings.
    """
    dataf = self.avoided_import.mul(self.import_electricity_prices.values,
                                    axis=0)
    dataf.columns = common.get_multiindex_single_column(
        site_schema.ResultsSchema.ELECTRICITY_SAVINGS)
    return dataf

  def export_results(self) -> pd.DataFrame:
    """
    Export the results of the scenario.

    This method calculates the current cost, current emissions, site avoided emissions, total avoided emissions, and current cost savings. 
    It then concatenates these results along with the site energy demand into a single DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the site energy demand, current cost, current cost savings, current emissions, site avoided emissions, and total avoided emissions.
    """
    current_cost = self.calculate_electricity_operation_cost()
    current_emissions = self.calculate_electricity_associated_emissions()
    site_avoided_emissions = self.calculate_site_electricity_avoided_emissions(
    )
    total_avoided_emissions = self.calculate_total_electricity_avoided_emissions(
    )
    current_cost_savings = self.calculate_electricity_import_savings()
    return pd.concat([
        self.site_energy_demand, current_cost, current_cost_savings,
        current_emissions, site_avoided_emissions, total_avoided_emissions
    ],
                     axis=1)

  def calculate_total_opex(self,
                           summary_results: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the total operational expenditure (OPEX) for the scenario.

    Args:
        summary_results (pd.DataFrame): The summary results of the scenario.

    Returns:
        pd.DataFrame: The updated summary results with the total OPEX.
    """
    opex_col = self.get_col_name(site_schema.ResultsSchema.OPEX)
    summary_results.loc[opex_col, self.name] = sum(
        self.site_model.annual_maintenance_cost.values())

    import_costs = self.get_col_name(
        site_schema.ResultsSchema.IMPORT_ELECTRICITY_COSTS)
    export_revenues = self.get_col_name(
        site_schema.ResultsSchema.EXPORT_ELECTRICITY_REVENUES)
    summary_results.loc[opex_col, self.name] = summary_results.loc[
        opex_col, self.name] + summary_results.loc[
            import_costs, self.name] - summary_results.loc[export_revenues,
                                                           self.name]
    return summary_results

  def get_capex_by_technology(self,
                              summary_results: pd.DataFrame) -> pd.DataFrame:
    """
    Get the capital expenditure (CAPEX) by technology for the scenario.

    Args:
        summary_results (pd.DataFrame): The summary results of the scenario.

    Returns:
        pd.DataFrame: The updated summary results with the CAPEX by technology.
    """
    for tech_name, tech_capex in self.site_model.capital_cost.items():
      col_name = site_schema.ResultsSchema.CAPEX
      col_name = (f'{tech_name.name}_{col_name[0]}', ) + col_name[1:]
      summary_results.loc[col_name, self.name] = tech_capex
    return summary_results

  def get_capacity_by_technology(
      self, summary_results: pd.DataFrame) -> pd.DataFrame:
    """
    Get the installed capacity by technology for the scenario.

    Args:
        summary_results (pd.DataFrame): The summary results of the scenario.

    Returns:
        pd.DataFrame: The updated summary results with the installed capacity by technology.
    """
    for tech_name, tech_cap in self.site_model.size_system.items():
      col_name = site_schema.ResultsSchema.CAPACITY_INSTALLED
      col_name = (f'{tech_name.name}_{col_name[0]}', ) + col_name[1:]
      summary_results.loc[col_name, self.name] = tech_cap
    return summary_results

  def get_summary_results(self) -> pd.DataFrame:
    """
    Get the summary results for the scenario.

    Returns:
        pd.DataFrame: The summary results for the scenario.
    """
    summary_results = self.summary_results.sum().to_frame()
    summary_results.columns = [self.name]
    peak_import_col = self.get_col_name(
        site_schema.ResultsSchema.PEAK_ELECTRICITY_IMPORT)
    summary_results.loc[peak_import_col,
                        self.name] = self.import_demand.max().iloc[0] * 2
    peak_export_col = self.get_col_name(
        site_schema.ResultsSchema.PEAK_ELECTRICITY_EXPORT)
    summary_results.loc[peak_export_col,
                        self.name] = self.export_demand.max().iloc[0] * 2

    summary_results = self.get_capex_by_technology(summary_results)
    summary_results = self.calculate_total_opex(summary_results)
    summary_results = self.get_capacity_by_technology(summary_results)
    return summary_results.astype(float)
