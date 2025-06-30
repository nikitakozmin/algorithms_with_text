def min_diff_table(str_one, str_two, replace_val, insert_val, delete_val):
    result = [[0 for _ in range(len(str_two)+1)] for _ in range(len(str_one)+1)]
    for i in range(len(str_one)+1):
        for j in range(len(str_two)+1):
            if i == 0:
                result[i][j] = j*insert_val
            elif j == 0:
                result[i][j] = i*delete_val
            else:
                result[i][j] = min(
                    result[i-1][j-1]+(replace_val if str_one[i-1]!=str_two[j-1] else 0),
                    result[i-1][j]+delete_val,
                    result[i][j-1]+insert_val,
                )
    return result


def min_diff(str_one, str_two, replace_val, insert_val, delete_val):
    table = min_diff_table(str_one, str_two, replace_val, insert_val, delete_val)
    return table[len(str_one)][len(str_two)]


def min_diff_instruction(str_one, str_two, replace_val, insert_val, delete_val):
    table = min_diff_table(str_one, str_two, replace_val, insert_val, delete_val)
    cur_pos_i, cur_pos_j = len(str_one), len(str_two)
    result = ""
    while cur_pos_i != 0 or cur_pos_j != 0:
        _, add_i, add_j = min(
            (table[cur_pos_i-1][cur_pos_j], -1, 0) if cur_pos_i != 0 else (float("inf"), 0, 0),
            (table[cur_pos_i-1][cur_pos_j-1], -1, -1) if cur_pos_i != 0 and cur_pos_j != 0 else (float("inf"), 0, 0),
            (table[cur_pos_i][cur_pos_j-1], 0, -1) if cur_pos_j != 0 else (float("inf"), 0, 0)
        )
        if (add_i, add_j) == (-1, -1):
            if table[cur_pos_i][cur_pos_j] == table[cur_pos_i-1][cur_pos_j-1]:
                result = "M" + result
            else:
                result = "R" + result
        elif add_i == -1:
            result = "D" + result
        else:
            result = "I" + result
        cur_pos_i += add_i
        cur_pos_j += add_j
    return result


def main():
    replace_val, insert_val, delete_val = map(int, input().split())
    # replace_val, insert_val, delete_val = 1, 1, 1
    str_one = input()
    str_two = input()
    print(min_diff(str_one, str_two, replace_val, insert_val, delete_val))
    print(min_diff_instruction(str_one, str_two, replace_val, insert_val, delete_val))
    # print(str_one)
    # print(str_two)


if __name__ == "__main__":
    main()
