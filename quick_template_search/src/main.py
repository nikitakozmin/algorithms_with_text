def compute_prefix(text):
    rslt = [0] * len(text)
    for i in range(1, len(text)):
        cur_distance = rslt[i - 1]
        while cur_distance > 0 and text[i] != text[cur_distance]:
            cur_distance = rslt[cur_distance - 1]
        if text[i] == text[cur_distance]:
            cur_distance += 1
        rslt[i] = cur_distance
    return rslt


def kmp_search(pattern, text):
    text_len, pattern_len = len(text), len(pattern)
    pattern_prefix = compute_prefix(pattern)
    cur_distance = 0
    occurrences = []
    for i in range(text_len):
        while cur_distance > 0 and text[i] != pattern[cur_distance]:
            cur_distance = pattern_prefix[cur_distance - 1]
        if text[i] == pattern[cur_distance]:
            cur_distance += 1
        if cur_distance == pattern_len:
            occurrences.append(i - pattern_len + 1)
            cur_distance = pattern_prefix[cur_distance - 1]
    return occurrences if occurrences else [-1]


def cyclic_shift_check(text, pattern):
    text_len, pattern_len = len(text), len(pattern)
    if text_len != pattern_len:
        return -1
    pattern_prefix = compute_prefix(pattern)
    cur_distance = 0
    for i in range(text_len*2):
        char = text[i%text_len]
        while cur_distance > 0 and char != pattern[cur_distance]:
            cur_distance = pattern_prefix[cur_distance - 1]
        if char == pattern[cur_distance]:
            cur_distance += 1
        if cur_distance == pattern_len:
            return (i - pattern_len + 1) % text_len
    return -1


def main():
    fst_string = input()
    snd_string = input()
    print(",".join(map(str, kmp_search(fst_string, snd_string))))
    print(cyclic_shift_check(fst_string, snd_string))


if __name__ == "__main__":
    main()
