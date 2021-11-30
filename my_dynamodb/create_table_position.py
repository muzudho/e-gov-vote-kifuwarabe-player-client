"""
# Run
python.exe -m my_dynamodb.create_table_position
"""

import boto3
from app import app


def create_position_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',
                                  region_name="us-east-2")
        # ↓ region_name に変えて、ローカルのDynamoDBも指せます
        # endpoint_url="http://localhost:8000"

    table = dynamodb.create_table(
        # テーブル名
        TableName='Position',
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
    # テーブルを作成します
    try:
        app.log.init()
        position_table = create_position_table()
        app.log.write_by_internal(
            f"Table status:{position_table.table_status}")

    except Exception as e:
        app.log.write_by_internal(f"(Err.163) テーブル作成できなかった [{e}]")
