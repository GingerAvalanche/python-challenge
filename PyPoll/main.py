from csv import DictReader
from pathlib import Path
from typing import Dict


def main():
    """
    Script that calculates various election analyses based on input data from a static location

    total_votes - sum of votes for each candidate

    vote_data: Dict[str, int] - dict mapping every candidate to number of votes they won

    percent_data: Dict[str, float] - dict mapping every candidate to percentage of votes they won

    winner - winner of the election
    """
    vote_data: Dict[str, int] = {}

    with Path("Resources/election_data.csv").open(mode="r", encoding="utf-8", newline="") as csv:
        field_names = csv.readline().strip().split(',') # ["Ballot ID", "County", "Candidate"]
        csvreader = DictReader(csv, fieldnames=field_names)

        for line in csvreader:
            if not line["Candidate"] in vote_data:
                vote_data[line["Candidate"]] = 0

            vote_data[line["Candidate"]] += 1

    total_votes: int = sum(vote_data.values())

    percent_data: Dict[str, float] = {}
    for (candidate, votes) in vote_data.items():
        percent_data[candidate] = votes / total_votes * 100

    winner: str = [k for (k, v) in vote_data.items() if v == max(vote_data.values())][0]

    candidate_summary = '\n'.join(
        list(
            map(lambda c_v: f'{c_v[0]}: {percent_data[c_v[0]]:.3f}% ({c_v[1]})', vote_data.items())
        )
    )
    analysis: str = (
        "Election Results\n"
        "-------------------------\n"
        f"Total Votes: {total_votes}\n"
        "-------------------------\n"
        f"{candidate_summary}\n"
        "-------------------------\n"
        f"Winner: {winner}\n"
        "-------------------------\n"
    )

    print(analysis)

    Path("analysis/analysis.txt").write_text(analysis,encoding="utf-8")


if __name__ == "__main__":
    main()
