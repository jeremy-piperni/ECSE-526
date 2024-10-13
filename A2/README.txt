README for A2 by Jeremy Piperni

Part 1

To run, write in terminal:
python3 part1.py

Output: generated sentence using a markov model, sources for each word generated (unigram, bigram, trigram).


Part 2

To run, write in terminal:
python3 part2.py

Variables that can be changed by the user:
test_sentence: string in array, change to whatever test sentence you'd like to correct.
use_test_sentence: True = correct the written test sentence above
		   False (default) = correct the 5 given sentences in the assignment 2 instructions

Output: corrected sentence(s) using a hidden markov model.


Levenshtein distances calculated using the following code:
https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python