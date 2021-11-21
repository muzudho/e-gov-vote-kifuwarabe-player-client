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


if __name__ == '__main__':
    delete_bestmove_table()
    print("Bestmove table deleted.")