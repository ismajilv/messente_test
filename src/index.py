import json
import boto3

db_exceptions = boto3.client('dynamodb').exceptions


def get_blacklist(event, blacklist_table):
    userid = event['requestContext']['authorizer']['principalId']

    response = blacklist_table.get_item(Key={"userid": userid}, ProjectionExpression="blacklist")
    blacklist = response['Item']['blacklist']

    body = {
        'Blacklist': [int(n) for n in blacklist],
        'Count': len(blacklist),
        'Message': "All the numbers in your blacklist."
    }

    return {'statusCode': 200, 'body': json.dumps(body)}


def post_blacklist(event, blacklist_table):
    userid = event['requestContext']['authorizer']['principalId']
    number = json.loads(event['body'])['number']

    try:
        number = int(number)
        blacklist_table.update_item(
            Key={
                'userid': userid
            },
            UpdateExpression="SET blacklist = list_append(blacklist, :iList)",
            ConditionExpression="not contains (blacklist, :iStr)",
            ExpressionAttributeValues={
                ':iList': [number],
                ':iStr': number
            },
            ReturnValues="UPDATED_NEW"
        )

        body = {"message": f"Number: {number} is added to blacklist."}
    except db_exceptions.ConditionalCheckFailedException:
        body = {"message": f"Number: {number} is already in your blacklist."}

    return {'statusCode': 201, 'body': json.dumps(body)}


def delete_blacklist(event, blacklist_table):
    userid = event['requestContext']['authorizer']['principalId']
    number = event['pathParameters']['number']

    response = blacklist_table.get_item(Key={"userid": userid},
                                        ProjectionExpression="blacklist")  # No way to remove element from list with one call
    try:
        number = int(number)
        index_to_delete = response['Item']['blacklist'].index(number)

        blacklist_table.update_item(
            Key={
                'userid': userid
            },
            UpdateExpression='REMOVE blacklist[%d]' % (index_to_delete)
        )

        body = {
            "message": f"Number: {number} is deleted from blacklist."
        }
    except ValueError:
        body = {"message": f"Number: {number} is not found in your blacklist."}

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


