"""
python.exe e_gov_get_bestmove_item.py
"""

from pprint import pprint
import boto3
from botocore.exceptions import ClientError


def get_bestmove(your_name, secret, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',
                                  region_name="us-east-2")
        # ↓ region_name に変えて、ローカルのDynamoDBも指せます
        # endpoint_url="http://localhost:8000"

    table = dynamodb.Table('Bestmove')

    try:
        response = table.get_item(Key={'yourName': your_name, 'secret': secret})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


if __name__ == '__main__':
    movie = get_bestmove("Muzudho","abc1234")
    if movie:
        print("Get bestmove table succeeded:")
        pprint(movie, sort_dicts=False)
