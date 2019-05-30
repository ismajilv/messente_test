import json
import boto3

iam = boto3.client('iam')


def get_blacklist(event, blacklist_table):
    response = blacklist_table.scan(
        ProjectionExpression="numb",
    )

    body = {
        'Items': response['Items'],
        'Count': response['Count'],
        'Message': "All the numbers in the blacklist."
    }

    return {'statusCode': 200, 'body': json.dumps(body)}


def post_blacklist(event, blacklist_table):
    number = json.loads(event['body'])['number']

    blacklist_table.put_item(
        Item={
            'numb': int(number)
        }
    )

    body = {
        "message": f"Number: {number} is added to blacklist."
    }

    return {'statusCode': 201, 'body': json.dumps(body)}


def delete_blacklist(event, blacklist_table):
    number = event['pathParameters']['number']

    blacklist_table.delete_item(
        Key={
            'numb': int(number)
        },
        ConditionExpression='attribute_exists(numb)'
    )

    body = {
        "message": f"Number: {number} is deleted from blacklist."
    }

    return {'statusCode': 200, 'body': json.dumps(body)}


def blacklist(event, context):
    http_method = event['httpMethod']

    dynamodb = boto3.resource("dynamodb")
    blacklist_table = dynamodb.Table("blacklist_table")

    try:
        response = {'GET': get_blacklist, 'POST': post_blacklist, 'DELETE': delete_blacklist}[http_method](event,
                                                                                                          blacklist_table)
        return response

    except:
        return {'statusCode': 500, 'body': json.dumps({'statusDescriotion': "Internal Server Error"})}


