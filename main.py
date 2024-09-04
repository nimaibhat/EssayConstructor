import sys
from collections import defaultdict
from typing import List, Dict

def build_corpus(file_path: str) -> Dict[str, int]:
    print("Building corpus from file")
    word_sequence = defaultdict(int)
    with open(file_path, 'r', encoding='utf-8') as f:
        sequence = ""
        prev_char = f.read(1)
        sequence += prev_char
        for _ in range(3):
            current_char = f.read(1)
            if prev_char == ' ' and current_char == ' ':
                while True:
                    current_char = f.read(1)
                    if current_char != prev_char:
                        break
            sequence += current_char
            prev_char = current_char
        word_sequence[sequence] += 1
        word_sequence["total"] += 1

        while True:
            current_char = f.read(1)
            if not current_char:
                break
            if prev_char == ' ' and current_char == ' ':
                while True:
                    current_char = f.read(1)
                    if current_char != prev_char:
                        break
            prev_char = current_char
            sequence += current_char
            sequence = sequence[1:]
            word_sequence[sequence] += 1
            word_sequence["total"] += 1

    print("Corpus built successfully")
    return word_sequence

def calculate_probability(word_sequence: Dict[str, int], seq: str) -> float:
    return float(word_sequence[seq] + 1) / float(len(word_sequence) + word_sequence["total"])

def load_input(file_path: str) -> List[List[str]]:
    matrix = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            elements = line.strip().split('|')[1:-1]
            matrix.append(elements)
    return matrix

def compute_joint_probability(word_sequence: Dict[str, int], left_seq: List[str], right_seq: List[str]) -> float:
    joint_prob = 1.0
    for l_seq, r_seq in zip(left_seq, right_seq):
        joint_prob *= calculate_probability(word_sequence, l_seq + r_seq)
    return joint_prob

def display_matrix(matrix: List[List[str]]):
    for row in matrix:
        print(' '.join(f"({element})" for element in row))

def print_result(matrix: List[List[str]]):
    for row in matrix:
        print(''.join(row))

def rearrange(word_sequence: Dict[str, int], matrix: List[List[str]]) -> List[List[str]]:
    idx1, idx2 = 0, 0
    highest_prob = -float('inf')
    ordered_strips = []

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i != j:
                joint_prob = compute_joint_probability(word_sequence, matrix[i], matrix[j])
                if joint_prob > highest_prob:
                    idx1, idx2 = i, j
                    highest_prob = joint_prob

    ordered_strips.append(matrix[idx1])
    ordered_strips.append(matrix[idx2])

    if idx1 > idx2:
        matrix.pop(idx1)
        matrix.pop(idx2)
    else:
        matrix.pop(idx2)
        matrix.pop(idx1)

    while matrix:
        left_prob_max = right_prob_max = -float('inf')
        right_pos = left_pos = 0

        for i in range(len(matrix)):
            left_prob = compute_joint_probability(word_sequence, matrix[i], ordered_strips[0])
            if left_prob > left_prob_max:
                left_pos = i
                left_prob_max = left_prob

            right_prob = compute_joint_probability(word_sequence, ordered_strips[-1], matrix[i])
            if right_prob > right_prob_max:
                right_pos = i
                right_prob_max = right_prob

        if right_prob_max >= left_prob_max:
            ordered_strips.append(matrix[right_pos])
            del_pos = right_pos
        else:
            ordered_strips.insert(0, matrix[left_pos])
            del_pos = left_pos

        matrix.pop(del_pos)

    return ordered_strips

def transpose(matrix: List[List[str]]) -> List[List[str]]:
    return [list(row) for row in zip(*matrix)]

def main():
    corpus = build_corpus('plrabn12.txt')

    input_matrix = load_input('input.txt')
    display_matrix(input_matrix)
    print()

    transposed_matrix = transpose(input_matrix)
    reordered_result = rearrange(corpus, transposed_matrix)

    print_result(transpose(reordered_result))

if __name__ == "__main__":
    main()
