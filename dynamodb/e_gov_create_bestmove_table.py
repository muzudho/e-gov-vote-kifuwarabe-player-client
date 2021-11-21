"""
python.exe e_gov_create_bestmove_table.py
"""

import boto3


def create_bestmove_table(dynamodb=None):
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


# cd dynamodb
# python.exe e_gov_create_bestmove_table.py
if __name__ == '__main__':
    # テーブルを作成します
    try:
        bestmove_table = create_bestmove_table()
        print(f"Table status:{bestmove_table.table_status}")

    except Exception as e:
        print(f"(Err.163) テーブル作成できなかった [{e}]")
