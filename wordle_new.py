import sys
from enum import Enum


class Char:
    def __init__(self, char, status, position):
        self.char = char
        self.status = status
        self.positions = [position]

    def __str__(self):
        return self.char + ": " + str(self.status) + " " + str(self.positions)


class Status(Enum):
    EXCLUDED = 1
    ANOTHER_PLACE = 2
    FOUND = 3


def contains(char_list, char):
    for letter in char_list:
        if letter.char == char:
            return True
    return False


def to_status(num):
    if num not in [1, 2, 3]:
        return -1
    elif num == 1:
        return Status.EXCLUDED
    elif num == 2:
        return Status.ANOTHER_PLACE
    else:
        return Status.FOUND


def find_index(char_list, char):
    for i in range(len(char_list)):
        if char_list[i].char == char:
            return i
    return -1


chars = []
first_word = "икота"
right_chars_count = 0
predicted_chars_count = 0
predicted_word = 'икота'


def check(results):
    c = 0
    global right_chars_count
    char_count = 0
    global predicted_chars_count
    global chars
    for i in results:
        i = int(i)
        current_status = to_status(i)
        if current_status not in [Status.FOUND, Status.ANOTHER_PLACE, Status.EXCLUDED]:
            return False
        current_char = predicted_word[char_count]
        if not contains(chars, current_char):
            chars.append(Char(current_char, current_status, char_count))
            if current_status == Status.ANOTHER_PLACE:
                predicted_chars_count += 1
            elif current_status == Status.FOUND:
                right_chars_count += 1
        else:
            index = find_index(chars, current_char)
            if current_status == Status.ANOTHER_PLACE == chars[index].status:
                chars[index].positions.append(char_count)
            elif current_status == Status.FOUND:
                if chars[index].status == Status.ANOTHER_PLACE:
                    chars[index].status = Status.FOUND
                    chars[index].positions = [char_count]
                    predicted_chars_count -= 1
                    right_chars_count += 1
                elif chars[index].status == Status.FOUND and \
                        char_count not in chars[index].positions:
                    c = index
                    chars[index].positions.append(char_count)
                    right_chars_count += 1
        char_count += 1
    if right_chars_count == 5:
        print('Правильное слово: ', predicted_word)
        sys.exit()
    return True


def predict():
    if len(chars) == 0:
        return first_word
    dictionary = open('dictionary.txt', encoding='utf-8')
    for word in dictionary:
        word = word.strip('\n')
        char_count = 0
        right_count = 0
        predicted_count = 0
        for letter in word:
            if contains(chars, letter):
                current_char = chars[find_index(chars, letter)]
                if current_char.status == Status.FOUND:
                    if char_count in current_char.positions:
                        right_count += 1
                elif current_char.status == Status.ANOTHER_PLACE and char_count not in current_char.positions:
                    predicted_count += 1
                else:
                    break
            char_count += 1
        if right_chars_count == right_count and predicted_chars_count == predicted_count \
                and word != predicted_word:
            dictionary.close()
            return word
    dictionary.close()
    print('No such word')
    sys.exit()


if __name__ == '__main__':
    print(predict())
    while True:
        results = list(input())
        if check(results):
            predicted_word = predict()
            print(predicted_word)
        else:
            print('Некорректный ввод, попробуй снова')
