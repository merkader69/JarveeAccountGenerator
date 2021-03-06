from math import log


# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
words = open("txts/words-by-frequency.txt").read().split()
wordcost = dict((k, log((i+1)*log(len(words)))) for i, k in enumerate(words))
maxword = max(len(x) for x in words)


def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k, c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1, len(s)+1):
        c, k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i > 0:
        c, k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return list(reversed(out))


def profanityFilter(input):
    """
    :param input: username parameter
    :return: False if username does not contain a censored word, otherwise True
    """
    with open('txts/profanity_list.txt', 'r') as file_read:
        bad_words = file_read.read().splitlines()
    name_infer = infer_spaces(input.lower())
    t_f = bool(set(name_infer).intersection(bad_words))  # true or false
    return t_f


def nameFilter(input):
    """
    :param input: first name parameter
    :return: False if name does not contain a boys name(obviously), otherwise True
    """
    with open('txts/bad_names.txt', 'r') as file_read:
        bad_names = file_read.read().splitlines()
    name_infer = infer_spaces(input.lower())
    t_f = bool(set(name_infer).intersection(bad_names))  # true or false
    return t_f

