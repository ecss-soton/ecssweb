from elections.models import Election, Position, Vote, Nomination, VoteRecord

election_name = 'agm-2021'

# Get the election and positions available
election = Election.objects.get(codename=election_name)
positions = Position.objects.filter(election=election)

for position in positions:
    nominees = Nomination.objects.filter(position=position)
    num_nominees = len(nominees) + 1
    
    # This will store the number of each priority vote
    scores = {"RON": [0] * num_nominees}
    for nominee in nominees:
        scores[nominee] = [0] * num_nominees

    # Go through each user's votes for this position
    votes = Vote.objects.filter(position=position)
    for vote in votes:
        seen = set()
        vote_records = VoteRecord.objects.filter(vote=vote)

        # Add each vote for each nominee to accumulators
        for record in vote_records:
            seen.add(record.rank)
            scores[record.nomination][record.rank-1] +=1

        # Find out RON's ranking
        for i in range(1, num_nominees + 1):
            if i not in seen:
                scores["RON"][i-1] +=1

    print(position.name)
    # Calculate each round
    for i in range(num_nominees - 1):
        actual = i + 1
        print("Round " + actual)
        for nominee, acc in d.items():
            if nominee == "RON":
                name = nominee
            else:
                name = nominee.name

            print(name + " scores " + sum(acc[:actual]))
