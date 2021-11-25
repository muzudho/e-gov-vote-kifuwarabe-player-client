"""
cd meta/about-dynamodb
python.exe e_gov_bestmove.py
"""

import random
from pprint import pprint
from my_dynamodb.e_gov_scan_bestmove_table import scan_bestmove_table


def get_bestmove():
    """
    Returns
    -------
    str
        該当がなければ None
    """

    # 指し手とその投票数のディクショナリー
    summary_dict = {}

    item_list = scan_bestmove_table()
    if item_list:
        print("Scan bestmove table succeeded:")
        pprint(item_list, sort_dicts=False)

        for item in item_list:
            # move
            m = item['bestmove']

            if m in summary_dict.keys():
                summary_dict[m] += 1
            else:
                summary_dict[m] = 1

    max_key_list = []
    max_value = 0

    for csa_move, vote_count in summary_dict.items():
        if max_value < vote_count:
            max_key_list = [csa_move]
            max_value = vote_count
        elif max_value == vote_count:
            max_key_list.append(csa_move)

    print(f"max_value=[{max_value}] max_key_list=[{max_key_list}]")

    if len(max_key_list) < 1:
        return None

    return random.choice(max_key_list)


# cd my_dynamodb
# python.exe e_gov_bestmove.py
if __name__ == '__main__':
    # move
    m = get_bestmove()
    print(f"bestmove=[{m}]")
