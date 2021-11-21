"""
python.exe e_gov_create_bestmove_table.py
"""

import boto3


def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',
                                  region_name="us-east-2")
        # ↓ region_name に変えて、ローカルのDynamoDBも指せます
        # endpoint_url="http://localhost:8000"

    table = dynamodb.create_table(
        # テーブル名
        TableName='Bestmove',
        # キー列の設定
        KeySchema=[
            {
                'AttributeName': 'yourName',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'secret',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        # キー列定義（通常列は書きません）
        AttributeDefinitions=[
            {
                'AttributeName': 'yourName',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'secret',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == '__main__':
    bestmove_table = create_table()
    print("Table status:", bestmove_table.table_status)
