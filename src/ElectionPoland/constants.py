from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DATA_DIR = PROJECT_ROOT.joinpath("data")
RESULTS_DIR = PROJECT_ROOT.joinpath("results")

candidates_per_lastname = {
    "Bartoszewicz": "BARTOSZEWICZ Artur",
    "Biejat": "BIEJAT Magdalena Agnieszka",
    "Braun": "BRAUN Grzegorz Michał",
    "Hołownia": "HOŁOWNIA Szymon Franciszek",
    "Jakubiak": "JAKUBIAK Marek",
    "Maciak": "MACIAK Maciej",
    "Mentzen": "MENTZEN Sławomir Jerzy",
    "Nawrocki": "NAWROCKI Karol Tadeusz",
    "Senyszyn": "SENYSZYN Joanna",
    "Stanowski": "STANOWSKI Krzysztof Jakub",
    "Trzaskowski": "TRZASKOWSKI Rafał Kazimierz",
    "Woch": "WOCH Marek Marian",
    "Zandberg": "ZANDBERG Adrian Tadeusz",
}

important_columns_translated = {
    "Nr komisji": "Commission number",
    "Gmina": "Gmina",
    "Powiat": "Powiat",
    "Województwo": "Województwo",
    "Typ obwodu": "Type of precinct",
    "Typ obszaru": "Type of area",
    "Liczba kart do głosowania otrzymanych przez obwodową komisję wyborczą, ustalona po ich przeliczeniu przed rozpoczęciem głosowania z uwzględnieniem ewentualnych kart otrzymanych z rezerwy": "Number of ballots received",
    "Liczba wyborców uprawnionych do głosowania (umieszczonych w spisie, z uwzględnieniem dodatkowych formularzy) w chwili zakończenia głosowania": "Number of eligible voters",
    "Liczba kart wyjętych z urny": "Number of ballots",
    "Liczba kart nieważnych (bez pieczęci obwodowej komisji wyborczej lub inne niż urzędowo ustalone)": "Number of invalid ballots",
    "Liczba kart ważnych": "Number of valid ballots",
    "Liczba głosów nieważnych (z kart ważnych)": "Number of invalid votes",
    "Liczba głosów ważnych oddanych łącznie na wszystkich kandydatów (z kart ważnych)": "Number of valid votes",  # only in first round
    "Liczba głosów ważnych oddanych łącznie na obu kandydatów (z kart ważnych)": "Number of valid votes",  # only in second round
}

commission_info = [
    "Commission number",
    "Gmina",
    "Powiat",
    "Województwo",
    "Type of precinct",
    "Type of area",
]
important_columns_translated = important_columns_translated | {
    value: value for value in candidates_per_lastname.values()
}
