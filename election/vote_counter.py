from election.models import Election, Position, Vote, Nomination, VoteRecord
from collections import defaultdict

election_name = 'agm-2021'

# Get the election and positions available
election = Election.objects.get(codename=election_name)
positions = Position.objects.filter(election=election)

for position in positions:
    nominees = Nomination.objects.filter(position=position)
    num_nominees = len(nominees) + 1

    # Turn Django objects into mutable dicts
    usable_votes = []
    # Go through each user's votes for this position
    votes = Vote.objects.filter(position=position)
    for vote in votes:
        usable_vote = {}
        seen = set()

        vote_records = VoteRecord.objects.filter(vote=vote)
        # Add each vote to the new usable_vote dict
        for record in vote_records:
            usable_vote[record.nomination] = record.rank
            seen.add(record.rank)

        # Find out RON's ranking
        for i in range(1, num_nominees + 1):
            if i not in seen:
                usable_vote["RON"] = i

        usable_votes.append(usable_vote)

    print(position.name)
    previous_yeet = ""
    # Calculate each round
    for i in range(num_nominees - 1):
        round_num = i + 1
        print("Round {}".format(round_num))

        # Redistribute votes from previous rounds before starting
        for vote in usable_votes:
            yeeted_ranking = vote.pop(previous_yeet, None)

            # We have yeeted someone out of the election
            if yeeted_ranking:
                # Re-distribute the preferences of this voter
                for nominee, ranking in vote.items():
                    if ranking > yeeted_ranking:
                        vote[nominee] = ranking - 1

        # Count the votes
        scores = defaultdict(int)
        for vote in usable_votes:
            # Invert votes (Clunky as hell but it works)
            # Find the most favoured candidate for this round
            inverted_vote = dict((v, k) for k, v in vote.items())
            most_favoured = inverted_vote[1]

            # Add a vote for the most favoured candidate
            scores[most_favoured] += 1

        lowest_candidate = None
        lowest_score = 100000
        # Display the results
        for nominee, score in scores.items():
            if nominee == "RON":
                name = nominee
            else:
                name = nominee.name

            print("{} scores {}".format(name, score))

            # Track who performed the worst
            if score < lowest_score:
                lowest_score = score
                lowest_candidate = nominee

        # YEET the worst performing candidate
        previous_yeet = lowest_candidate
        print("\n")

    # If it's only RON then RIP
    if num_nominees == 1:
        print("RON scores {}".format(len(usable_votes)))
        print("\n")
