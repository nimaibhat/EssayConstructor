import sys
from collections import defaultdict
from typing import List, Dict

def create_dict(dict_path: str) -> Dict[str, int]:
    print("Creating a dictionary")
    corpus = defaultdict(int)
    with open(dict_path, 'r', encoding='utf-8') as file:
        strng = ""
        prev = file.read(1)
        strng += prev
        for _ in range(3):
            c = file.read(1)
            if prev == ' ' and c == ' ':
                while True:
                    c = file.read(1)
                    if c != prev:
                        break
            strng += c
            prev = c
        corpus[strng] += 1
        corpus["count"] += 1

        while True:
            c = file.read(1)
            if not c:
                break
            if prev == ' ' and c == ' ':
                while True:
                    c = file.read(1)
                    if c != prev:
                        break
            prev = c
            strng += c
            strng = strng[1:]
            corpus[strng] += 1
            corpus["count"] += 1

    print("Done with the dictionary")
    return corpus

def probability(corpus: Dict[str, int], strng: str) -> float:
    return float(corpus[strng] + 1) / float(len(corpus) + corpus["count"])

def read_input(input_path: str) -> List[List[str]]:
    input_matrix = []
    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')[1:-1]
            input_matrix.append(parts)
    return input_matrix

def strip_correction(corpus: Dict[str, int], left: List[str], right: List[str]) -> float:
    prod = 1.0
    for l, r in zip(left, right):
        prod *= probability(corpus, l + r)
    return prod

def print_matrix(matrix: List[List[str]]):
    for row in matrix:
        print(' '.join(f"({elem})" for elem in row))

def display_output(matrix: List[List[str]]):
    for row in matrix:
        print(''.join(row))

def reorder(corpus: Dict[str, int], input_matrix: List[List[str]]) -> List[List[str]]:
    ele1, ele2 = 0, 0
    max_pair_prob = -float('inf')
    correct_strips = []
    for i in range(len(input_matrix)):
        for j in range(len(input_matrix)):
            if i != j:
                pair_prob = strip_correction(corpus, input_matrix[i], input_matrix[j])
                if pair_prob > max_pair_prob:
                    ele1, ele2 = i, j
                    max_pair_prob = pair_prob

    correct_strips.append(input_matrix[ele1])
    correct_strips.append(input_matrix[ele2])

    if ele1 > ele2:
        input_matrix.pop(ele1)
        input_matrix.pop(ele2)
    else:
        input_matrix.pop(ele2)
        input_matrix.pop(ele1)

    while input_matrix:
        max_left = max_right = -float('inf')
        right_index = left_index = 0

        for i in range(len(input_matrix)):
            left_prob = strip_correction(corpus, input_matrix[i], correct_strips[0])
            if left_prob > max_left:
                left_index = i
                max_left = left_prob

            right_prob = strip_correction(corpus, correct_strips[-1], input_matrix[i])
            if right_prob > max_right:
                right_index = i
                max_right = right_prob

        if max_right >= max_left:
            correct_strips.append(input_matrix[right_index])
            del_index = right_index
        else:
            correct_strips.insert(0, input_matrix[left_index])
            del_index = left_index

        input_matrix.pop(del_index)

    return correct_strips

def transpose_matrix(matrix: List[List[str]]) -> List[List[str]]:
    return [list(row) for row in zip(*matrix)]

def main():
    corpus = create_dict('plrabn12.txt')

    input_matrix = read_input('input.txt')
    print_matrix(input_matrix)
    print()

    input_transposed = transpose_matrix(input_matrix)
    result = reorder(corpus, input_transposed)

    display_output(transpose_matrix(result))

if __name__ == "__main__":
    main()
