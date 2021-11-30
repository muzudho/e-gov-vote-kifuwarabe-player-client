"""
# Run
cd my_dynamodb
python.exe get_item_from_bestmove.py
"""

from pprint import pprint
import boto3
from botocore.exceptions import ClientError
from app import app


def get_item_from_bestmove(your_name, secret, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',
                                  region_name="us-east-2")
        # ↓ region_name に変えて、ローカルのDynamoDBも指せます
        # endpoint_url="http://localhost:8000"

    table = dynamodb.Table('Bestmove')

    try:
        response = table.get_item(
            Key={'yourName': your_name, 'secret': secret})
    except ClientError as e:
        app.log.write_by_internal(e.response['Error']['Message'])
    else:
        return response['Item']


if __name__ == '__main__':
    app.log.init()
    movie = get_item_from_bestmove("Muzudho", "abc1234")
    if movie:
        app.log.write_by_internal("Get bestmove table succeeded:")
        pprint(movie, sort_dicts=False)
