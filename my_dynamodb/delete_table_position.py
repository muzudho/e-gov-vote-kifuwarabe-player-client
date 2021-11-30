"""
# Run
python.exe -m my_dynamodb.delete_table_position
"""

import boto3
from app import app

TABLE_NAME = 'Position'


def delete_position_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',
                                  region_name="us-east-2")
        # ↓ region_name に変えて、ローカルのDynamoDBも指せます
        # endpoint_url="http://localhost:8000"

    table = dynamodb.Table(TABLE_NAME)
    table.delete()


if __name__ == '__main__':
    # テーブルを削除します
    try:
        app.log.init()
        delete_position_table()
        app.log.write_by_internal(f"{TABLE_NAME} table deleted.")

    except Exception as e:
        app.log.write_by_internal(f"(Err.158) テーブル削除できなかった [{e}]")
