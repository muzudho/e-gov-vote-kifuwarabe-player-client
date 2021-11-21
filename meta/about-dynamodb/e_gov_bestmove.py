"""
cd meta/about-dynamodb
python.exe e_gov_bestmove.py
"""

import random
from pprint import pprint
from e_gov_scan_bestmove_table import scan_bestmove_table


def get_bestmove():
    item_list = scan_bestmove_table()
    if item_list:
        print("Scan bestmove table succeeded:")
        pprint(item_list, sort_dicts=False)

        move_dict = {}

        for item in item_list:
            # move
            m = item['bestmove']

            if m in move_dict.keys():
                move_dict[m] += 1
            else:
                move_dict[m] = 1

    max_key_list = []
    max_value = 0

    for key, value in move_dict.items():
        if max_value < value:
            max_key_list = [key]
            max_value = value
        elif max_value == value:
            max_key_list.append(key)

    print(f"max_value=[{max_value}] max_key_list=[{max_key_list}]")

    return random.choice(max_key_list)


if __name__ == '__main__':
    # move
    m = get_bestmove()
    print(f"bestmove=[{m}]")
