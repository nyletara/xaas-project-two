from pymongo import MongoClient
import boto3
import json
import jwt


def lambda_handler(event, context):
    print ("THIS IS THE EVENT!")
    print (event)
    print("THESE ARE THE KEYS")
    print(event.keys())
    print("THESE ARE THE CONTEXT KEYS")
    print(event['context'].keys())
    print("THIS IS THE resource-path")
    print(event['context']['resource-path'])



    method = event['context']['resource-path']
    userEventInfo = event['body-json']
    sns_client = boto3.client('sns')
    if method == "/login":
        connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
        aid = str(connectdb.loginAttempts.insert_one({"status" : "undefined"}).inserted_id);
        userEventInfo["aid"] = aid
        response = sns_client.publish(TopicArn='arn:aws:sns:us-east-1:648812771825:login', Message=str(json.dumps(userEventInfo)))
        return aid
    elif method == "/signup":
        client = boto3.client('stepfunctions')
        connectdb = MongoClient('mongodb://user1:user1password@ds149040.mlab.com:49040/user_db')["user_db"]
        aid = str(connectdb.signupAttempts.insert_one({"status": "undefined"}).inserted_id);
        userEventInfo["aid"] = aid
        response = client.start_execution(
            stateMachineArn='arn:aws:states:us-east-1:648812771825:stateMachine:HelloWorld098098',
            name=aid,
            input=str(json.dumps(userEventInfo))
        )
        return aid
    elif method == "/charge":
        chargeDb = MongoClient('mongodb://user1:user1password@ds149030.mlab.com:49030/charge_db')["charge_db"]
        aid = str(chargeDb.caids.insert_one({"status": "undefined"}).inserted_id);
        userEventInfo["aid"] = aid
        response = sns_client.publish(
            TopicArn='arn:aws:sns:us-east-1:648812771825:payments',
            Message=str(json.dumps(userEventInfo)))
        return aid
    else:
        # return event
        return "not supported"
    return str(event)
