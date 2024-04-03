import pandas as pd

from e2slib.structures import site_schema


def create_cashflow_data_skeleton() -> pd.DataFrame:
  """
  Create a skeleton DataFrame for the cashflow data.
  
  Returns:
      pd.DataFrame: The cashflow data skeleton.
  """
  columns = pd.MultiIndex.from_tuples([], names=['Parameters', 'Units'])
  cashflow_dataf = pd.DataFrame(index=list(range(0, 50)), columns=columns)
  cashflow_dataf.index.name = site_schema.ResultsSchema.INDEX
  return cashflow_dataf
