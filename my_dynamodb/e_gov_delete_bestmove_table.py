"""
python.exe e_gov_delete_bestmove_table.py
"""

import boto3


def delete_bestmove_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',
                                  region_name="us-east-2")
        # ↓ region_name に変えて、ローカルのDynamoDBも指せます
        # endpoint_url="http://localhost:8000"

    table = dynamodb.Table('Bestmove')
    table.delete()


# cd my_dynamodb
# python.exe e_gov_delete_bestmove_table.py
if __name__ == '__main__':
    # テーブルを削除します
    try:
        delete_bestmove_table()
        print("Bestmove table deleted.")

    except Exception as e:
        print(f"(Err.158) テーブル削除できなかった [{e}]")
