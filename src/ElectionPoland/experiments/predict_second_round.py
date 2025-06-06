import pandas as pd
from ElectionPoland.constants import candidates_per_lastname, commission_info
from ElectionPoland.constants import RESULTS_DIR


class PredictSecondRound:
    def __init__(
        self,
        first_round_results: pd.DataFrame,
        voter_flows: dict[str, tuple[float, float]],
    ):

        if not all(
            isinstance(flow, tuple)
            and len(flow) == 3
            and all(0 <= f <= 1 for f in flow)
            and sum(flow) == 1
            for flow in voter_flows.values()
        ):
            raise ValueError(
                "All voter flows must be tuples of two floats between 0 and 1 and have to sum to 1."
            )
        if not all(
            candidates_per_lastname[candidate] in first_round_results.columns
            for candidate in voter_flows.keys()
        ):
            raise ValueError(
                "All candidates in voter_flows must be present in the first_round_results DataFrame."
            )

        self.first_round_results = first_round_results
        self.voter_flows = voter_flows

        self.predicted_second_round = None

    def predict_second_round(self):
        second_round_results = self.first_round_results.copy()
        second_round_results = second_round_results.drop(
            columns=[
                candidates_per_lastname[candidate]
                for candidate in self.voter_flows.keys()
            ]
        )
        second_round_results.loc[
            :,
            [
                candidates_per_lastname["Nawrocki"],
                candidates_per_lastname["Trzaskowski"],
            ],
        ] = 0
        for candidate, flow in self.voter_flows.items():
            second_round_results[candidates_per_lastname["Nawrocki"]] += (
                self.first_round_results[candidates_per_lastname[candidate]] * flow[0]
            )
            second_round_results[candidates_per_lastname["Trzaskowski"]] += (
                self.first_round_results[candidates_per_lastname[candidate]] * flow[1]
            )
        self.predicted_second_round = second_round_results

    def validate_results(self, true_second_round_results: pd.DataFrame):
        if self.predicted_second_round is None:
            raise ValueError("Second round results have not been predicted yet.")

        self.predicted_second_round = self._calculate_percentage_results(
            self.predicted_second_round
        )

        true_second_round_results = self._calculate_percentage_results(
            true_second_round_results
        )

        self._different_winer(self.predicted_second_round, true_second_round_results)

        return True

    @staticmethod
    def _calculate_percentage_results(df: pd.DataFrame) -> pd.DataFrame:
        """
        Negative Difference [%pt.] means that Nawrocki has more votes than Trzaskowski.
        Positive Difference [%pt.] means that Trzaskowski has more votes than Nawrocki.
        """
        df_new = df.copy()
        df_new.loc[:, "Number of predicted voters"] = df_new.loc[
            :,
            [
                candidates_per_lastname["Nawrocki"],
                candidates_per_lastname["Trzaskowski"],
            ],
        ].sum(axis=1)
        df_new.loc[:, "Nawrocki [%]"] = (
            df_new.loc[:, candidates_per_lastname["Nawrocki"]]
            / df_new["Number of predicted voters"]
            * 100
        )
        df_new.loc[:, "Trzaskowski [%]"] = (
            df_new.loc[:, candidates_per_lastname["Trzaskowski"]]
            / df_new["Number of predicted voters"]
            * 100
        )
        df_new.loc[:, "Difference [%pt.]"] = (
            df_new.loc[:, "Trzaskowski [%]"] - df_new.loc[:, "Nawrocki [%]"]
        )
        return df_new

    @staticmethod
    def _different_winer(df_pred: pd.DataFrame, df_true: pd.DataFrame) -> pd.DataFrame:
        needed_columns = commission_info + [
            "Number of predicted voters",
            "Nawrocki [%]",
            "Trzaskowski [%]",
            "Difference [%pt.]",
        ]

        combined_df = pd.merge(
            df_pred.loc[:, needed_columns],
            df_true.loc[:, needed_columns],
            on=commission_info,
            suffixes=(" (1st round)", " (2nd round)"),
        )
        suspected_different_winner = (
            combined_df["Difference [%pt.] (1st round)"]
            * combined_df["Difference [%pt.] (2nd round)"]
            < 0
        )
        combined_df[suspected_different_winner].to_excel(
            RESULTS_DIR.joinpath("suspected_different_winner.xlsx"), index=False
        )
