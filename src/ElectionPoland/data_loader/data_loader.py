import pandas as pd
from ElectionPoland.constants import DATA_DIR, important_columns_translated


class DataLoader:
    def __init__(self):
        self.first_round = pd.read_excel(
            DATA_DIR.joinpath("Voting/1st round.xlsx"),
            sheet_name="Arkusz",
            usecols=lambda col: col in important_columns_translated.keys(),
        ).rename(columns=important_columns_translated)

        self.second_round = pd.read_excel(
            DATA_DIR.joinpath("Voting/2nd round.xlsx"),
            sheet_name="Arkusz",
            usecols=lambda col: col in important_columns_translated.keys(),
        ).rename(columns=important_columns_translated)
