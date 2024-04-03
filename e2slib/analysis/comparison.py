from dataclasses import dataclass, field

import pandas as pd

from e2slib.analysis import scenario


@dataclass
class ScenarioComparison:
  """
  A class used to compare different scenarios.

  Attributes:
      reference_scenario (scenario.Scenario): The reference scenario to compare with.
      list_scenarios (list[scenario.Scenario]): The list of scenarios to compare.
      _summary_results (pd.DataFrame): The summary results of the comparison (default is an empty DataFrame).

  Methods:
      summary_results: Get the summary results of the comparison.
      comparison_results: Get the comparison results of the scenarios with the reference scenario.
  """

  reference_scenario: scenario.Scenario
  list_scenarios: list[scenario.Scenario]
  _summary_results: pd.DataFrame = field(default_factory=pd.DataFrame)

  @property
  def summary_results(self) -> pd.DataFrame:
    """
    Get the summary results of the comparison.

    Returns:
        pd.DataFrame: The summary results of the comparison.
    """
    frames: list[pd.DataFrame] = []
    for sc in self.list_scenarios:
      frames.append(sc.get_summary_results())
    self._summary_results = pd.concat(frames, axis=1)
    sorted_cols: list[str] = sorted(self._summary_results.columns)
    self._summary_results = self._summary_results[sorted_cols]
    return self._summary_results

  def comparison_results(self) -> pd.DataFrame:
    """
    Get the comparison results of the scenarios with the reference scenario.

    Returns:
        pd.DataFrame: The comparison results of the scenarios with the reference scenario.
    """
    ref_summary = self.reference_scenario.get_summary_results()
    return (self.summary_results - ref_summary.values) / ref_summary.values
