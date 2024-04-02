import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequences.txt")
        sys.exit(1)

    # TODO: Read database file into a variable
    with open(sys.argv[1], "r") as DNA_DBFile:
        reader = csv.DictReader(DNA_DBFile)
        DNA_database = [row for row in reader]

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as file:
        DNA_sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    strCounts = {}
    for key in DNA_database[0].keys():
        if key != "name":
            strCounts[key] = longest_match(DNA_sequence, key)

    # TODO: Check database for matching profiles
    for p in DNA_database:
        match = person_match(p, strCounts)
        if match == True:
            print(p['name'])
            return

    print("No match")
    return


def person_match(person, strCounts):
    for key in strCounts.keys():
        if int(person[key]) != strCounts[key]:
            return False
    return True


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
