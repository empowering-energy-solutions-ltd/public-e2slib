from pathlib import Path

import pandas as pd


def create_path(path_to_create: Path) -> None:
  path_to_create.mkdir(parents=True, exist_ok=True)


def get_multiindex_single_column(
    schema_column: tuple[str, str]) -> pd.MultiIndex:
  """
  Create a multiindex with a column schema.

  Args:
      schema_column (tuple[str, str]): The column schema.

  Returns:
      pd.MultiIndex: The multiindex with the column schema.
  """
  return get_multiindex_multiple_columns([schema_column])


def get_multiindex_multiple_columns(
    list_columns: list[tuple[str, str]]) -> pd.MultiIndex:
  """
  Create a multiindex with the given list of columns.

  Args:
      list_columns (list[tuple[str, str]]): The list of columns.

  Returns:
      pd.MultiIndex: The multiindex with the list of columns.
  """
  return pd.MultiIndex.from_tuples(list_columns, names=['Parameters', 'Units'])
