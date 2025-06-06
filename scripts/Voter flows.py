from ElectionPoland.data_loader import DataLoader
from ElectionPoland.experiments import PredictSecondRound

# Conditate: (flows to Nawrocki, flows to Trzaskowski, non-participation) - values between 0 and 1, have to sum to 1
"""
Flows based on IPSOS exit polls.
In candidate not included in the flow, it is assumed that all voters will not participate in the second round.
"""
VOTER_FLOWS = {
    "Bartoszewicz": (0, 0, 1),
    "Biejat": (0.902, 0.098, 0),
    "Braun": (0.925, 0.075, 0),
    "Hołownia": (0.138, 0.862, 0),
    "Jakubiak": (0, 0, 1),
    "Maciak": (0, 0, 1),
    "Mentzen": (0.881, 0.119, 0),
    "Nawrocki": (0.993, 0.007, 0),
    "Senyszyn": (0.189, 0.811, 0),
    "Stanowski": (0.512, 0.488, 0),
    "Trzaskowski": (0.01, 0.99, 0),
    "Woch": (0, 0, 1),
    "Zandberg": (0.162, 0.838, 0),
}


def main():
    data_loader = DataLoader()
    experiment = PredictSecondRound(
        first_round_results=data_loader.first_round, voter_flows=VOTER_FLOWS
    )
    experiment.predict_second_round()
    experiment.validate_results(data_loader.second_round)


if __name__ == "__main__":
    main()
