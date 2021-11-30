"""
# Run
cd my_dynamodb
python.exe scan_table_bestmove.py
"""

from pprint import pprint
import boto3
from botocore.exceptions import ClientError
from app import app


def scan_bestmove_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',
                                  region_name="us-east-2")
        # ↓ region_name に変えて、ローカルのDynamoDBも指せます
        # endpoint_url="http://localhost:8000"

    table = dynamodb.Table('Bestmove')

    try:
        response = table.scan()
    except ClientError as e:
        app.log.write_by_internal(e.response['Error']['Message'])
    else:
        return response['Items']


if __name__ == '__main__':
    app.log.init()
    items = scan_bestmove_table()
    if items:
        app.log.write_by_internal("Scan bestmove table succeeded:")
        pprint(items, sort_dicts=False)
