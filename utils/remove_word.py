import re

remove_words = []
stop_words = open('resources/stop_word.txt', 'r', encoding='utf8')
for row in stop_words:
    remove_words.append(row[:-1])


def remove_word(words):
    result = []
    for word in words:
        if (word not in remove_words):
            result.append(word)
    return result
