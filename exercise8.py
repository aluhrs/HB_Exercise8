#!/usr/bin/env python

# ???? order of operations???


# import the sys module
import sys
# import randint from the random module
from random import randint
# import the twitter module
import twitter
# import the os module
import os

def make_chains(input_text, n_gram_size):
    """Takes an input text as a string number of grams and returns a dictionary of
    markov chains."""
    
    # split the text by whitespace
    # assign it to a variable
    words = input_text.split()

    # create an empty dictionary
    d = {}

    # loop through the range of the length of the split text minus the number of grams
    # we do this because range starts at 0 and counts to the end
    # whie length starts at 1 and goes to the end
    # so it is one more than we need
    for i in range(len(words) - n_gram_size):
        # we are taking the text that has split into words
        # and pulling the item we are one and and the next n 
        # (number of grams as specified in the main function) amount of items
        # assign it to a variable
        n_gram = words[i:i + n_gram_size]
        # since n_gram is currently a list, we need to turn it into a tuple       
        key = tuple(n_gram)
        # if the touple/key is not already in the dictionary
        if not d.get(key):
            # add it
            d[key] = [words[i + n_gram_size]]
        else:
            # if the touple/key is already in the dict
            # add the value to the end of the list of existing values
            # for that touple/key
            d[key].append(words[i + n_gram_size])


    # return the dictionary
    return d

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    # calls the capitalized_words functions on the dictionary     
    key = capitalized_words(chains)

    # since the key is a touple, we want to make it into a list
    # assign the list to a variable    
    words = list(key)
    
    # in a while loop, while the key exists in the dictionary
    while chains.get(key):
        # get a random number between 0 and the length of the dictionary's capatilized key minus 1
        # we do minus one because ??? an out of bounds of the array error?
        # assign it to a variable
        random_number = randint(0, len(chains[key]) - 1)
        # ????get the capitalized touple's randomly selected letter????
        random_word = chains[key][random_number]

        # call the end_periods function
        # to verify the tweet ends in a period 
        # (the function returned true)
        # if it doesn't, exit the loop
        # ???? and???? get a new touple to start with?
        if end_on_period(words):
            break

        # call the tweet_sized function
        # if the function returned true
        # (it said the tweet was 140 chars or less)
        if tweet_sized(words, random_word):
            # add the string to random_word
            words.append(random_word)
        else:
            # ???otherwise, leave the loop and go ....???
            break

        # ??why do we go through these steps??    
        # get all of the items in the touple/key except for the first
        # and put it into a list
        # assign it a variable
        tmp = list(key[1:])
        # append the list to random_word
        tmp.append(random_word)
        # make the list back into a touple
        key = tuple(tmp)
    
    # ???? what is words actually right here?
    return ' '.join(words)

def capitalized_words(d):
    """Returns a tuple that starts with a capital letter."""

    # creates a list of the dictionary's capatilzed touple/key
    keys = d.keys()

    # in a while loop,
    while True:
        # get a random index (key) between the beginning
        # and the end of the list of keys
        # we do (len(keys) - 1) because length
        # will cause an index out of bounds of array error
        # because we're starts at zero, but length starts at 1
        # and we're trying to get the index
        # indexes start at 0
        random_index = randint(0, len(keys) - 1)

        # get the first letter of of the random key
        first_letter = keys[random_index][0][0]

        # check to see if the first letter is capitalized by checking
        # the ASCII decimal
        # ASCII ord(65) = A, ASCII (90) = Z
        if ord(first_letter) >= 65 and ord(first_letter) <= 90:
            # if the first letter is capitalized, return the key
            return keys[random_index]


def end_on_period(words):
    """Verifies the list of words ends in a period."""
    # get the last word of the of the capitalized touple/key
    # assign it to a variable
    last_word = words[-1]

    # get the last letter of the of the capitalized touple/key
    last_letter = last_word[-1]

    # if the last letter ends in a period or a questions mark or
    # exlamation point
    # return true
    # otherwise return false
    if last_letter == "." or last_letter == "?" or last_letter == "!":
        return True    

    return False

def tweet_end_on_period(chain_dict):
    """End the tweet on a period."""

    #in a while loop,
    while True:
        # call the make_text function
        # ??? what is the returned words as this point
        tweet = make_text(chain_dict)
        # split the text into words by whitespace
        split_words = tweet.split()
        # the tweet ends on a period, return the tweet
        # if it doesn't, return False
        # ??? and then do what?
        if end_on_period(split_words):
            return tweet


def tweet_sized(words, appended_word):
    """If longer than 140 characters return False, otherwise return True."""

    # get the capitalized and ends on period tweet
    # and join it into a string
    # assign it to a variable

    string = ' '.join(words)
    # get the lenght of the string
    # assign it to a variable
    length_of_string = len(string)

    # if the length of the tweet/string is greater than 140 chars
    if length_of_string > 140:
        # return false
        return False
    else:
        # otherwise return true
        return True    

def tweet(text):
    """Takes the text and tweets it on a twitter account using their API"""

    # keys for the twitter API to work and be able to work
    api_key = os.environ.get("TWITTER_API_KEY")    
    api_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    token_secret = os.environ.get("TWITTER_TOKEN_SECRET")

    # grants access to be able to tweet
    api=twitter.Api(api_key, api_secret, access_token, token_secret)
    
    #print api.VerifyCredentials()

    # send the tweet to twitter
    api.PostUpdate(text)

def main():
    # ????assign whatever sys.argv is to args?????
    args = sys.argv

    # assigning all of the source files we get into a variable filenames
    # we start at index 1 because the first filename will be the script name (markov.py)
    filenames = args[1:]

    # creating an empty string
    input_text = ""

    # looping through each source file
    for f in filenames:
        # open each file
        o = open(f)
        # read each file and add the contents to the empty string called input_text
        input_text += o.read()
        # close each file
        o.close()

    # prompt the user to assign how many items will be in the tuple
    # assign that number to input_number
    print "Enter size of n-gram"
    input_number = raw_input("> ")

    # in a while loop, check to see if the user is inputing a digit
    # if they are not, prompt them again
    while not input_number.isdigit():
        print "That's a not a digit. Please enter a digit."
        input_number = raw_input("> ")

    # once we are sure we have a digit
    # store the digit into a variable
    n_gram_size = int(input_number)

    # call the make_chains function that two arguments
    # store it into a variable
    chain_dict = make_chains(input_text, n_gram_size)
    # call the tweet_end_on_period function that takes one argument
    # store it into a variable
    random_text = tweet_end_on_period(chain_dict)
    print random_text

    # in a while loop, ask the user to confirm whether or not they want to send the completed tweet
    # also check if they want to quit, if they do, then quit the program
    # if they do not want to send the tweet, call the tweet_end_on_period function again to
    # generate a new tweet
    # continue this until the person verifies they want to send this tweet

    print "Do you want to tweet this? Press Y to select this tweet or press q to quit or press any other key to see another tweet"
    verify = raw_input("> ")
    while verify.lower() != "y":
        if verify == 'q':
            exit(0)
        random_text = tweet_end_on_period(chain_dict)
        print random_text
        print "Do you want to tweet this? Press Y to select this tweet or press q to quit or press any other key to see another tweet"
        verify = raw_input("> ")

    # if they confirmed they want to send the tweet, then send the tweet    
    tweet(random_text)
  
         

if __name__ == "__main__":
    main()