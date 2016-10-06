from random import choice
import sys
from os import environ
import twitter


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path) as file_to_string:
        return file_to_string.read()


def make_chains(text_string, n):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """
    words = text_string.split()
    chains = {}

    for index in range(len(words) - n):
        tup = tuple(words[index:index + n])
        chains.setdefault(tup, []).append(words[index + n])
     
    return chains


def make_text(chains, max_chars):
    """Takes dictionary of markov chains; returns random text."""

    capital_keys = [key for key in chains.keys() if key[0].istitle()]
    tup = choice(capital_keys)
    text = list(tup)
    num_chars = 0
    
    while num_chars < max_chars and tup in chains: 
        new_word = choice(chains[tup])
        num_chars += len(new_word) + 1
        tup = tup[1:] + (new_word,) 
        text.append(new_word)
        
    # Goes through list in backward direction to find last instance of punctuation
    for index, word in reversed(list(enumerate(text))):
        if word[-1] in (".", "?", "!") or word[-2:] in (".\"", "?\"", "!\""):
            return " ".join(text[:index + 1])


def tweet(chains):
    api = twitter.Api(
        consumer_key=environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=environ['TWITTER_ACCESS_TOKEN_SECRET'])

    print api.VerifyCredentials()

    status = api.PostUpdate(chains)
    print(status.text)


input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, 2)

# Produce random text
random_text = make_text(chains, 140)

tweet(random_text)
