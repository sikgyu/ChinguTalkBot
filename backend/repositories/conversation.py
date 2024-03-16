import json
import os
from datetime import datetime
from decimal import Decimal as decimal

import boto3
from boto3.dynamodb.conditions import Key

from .model import ContentModel, ConversationModel, MessageModel

TABLE_NAME = os.environ.get("TABLE_NAME", "")
REGION = os.environ.get("REGION", "ap-northeast-1")

dynamodb = boto3.resource("dynamodb", region_name=REGION)


def store_conversation(user_id, conversation: ConversationModel):
    table = dynamodb.Table(TABLE_NAME)
    response = table.put_item(
        Item={
            "UserId": user_id,
            "ConversationId": conversation.id,
            "Title": conversation.title,
            "CreateTime": decimal(conversation.create_time),
            "Messages": json.dumps(
                [message.model_dump() for message in conversation.messages]
            ),
        }
    )
    return response


def find_conversation_by_user_id(user_id: str) -> list[ConversationModel]:
    table = dynamodb.Table(TABLE_NAME)
    response = table.query(KeyConditionExpression=Key("UserId").eq(user_id))

    return [
        ConversationModel(
            id=item["ConversationId"],
            create_time=float(item["CreateTime"]),
            title=item["Title"],
            messages=[
                MessageModel(
                    id=message["id"],
                    role=message["role"],
                    content=ContentModel(
                        content_type=message["content"]["content_type"],
                        body=message["content"]["body"],
                    ),
                    model=message["model"],
                    create_time=float(message["create_time"]),
                )
                for message in json.loads(item["Messages"])
            ],
        )
        for item in response["Items"]
    ]


def find_conversation_by_id(conversation_id: str) -> ConversationModel:
    table = dynamodb.Table(TABLE_NAME)
    response = table.query(
        IndexName="ConversationIdIndex",
        KeyConditionExpression=Key("ConversationId").eq(conversation_id),
    )
    if len(response["Items"]) == 0:
        raise ValueError(f"No conversation found with id: {conversation_id}")

    # NOTE: conversation is unique
    item = response["Items"][0]
    return ConversationModel(
        id=item["ConversationId"],
        create_time=float(item["CreateTime"]),
        title=item["Title"],
        messages=[
            MessageModel(
                id=message["id"],
                role=message["role"],
                content=ContentModel(
                    content_type=message["content"]["content_type"],
                    body=message["content"]["body"],
                ),
                model=message["model"],
                create_time=float(message["create_time"]),
            )
            for message in json.loads(item["Messages"])
        ],
    )


def delete_conversation_by_id(conversation_id: str):
    table = dynamodb.Table(TABLE_NAME)

    # Query the index
    response = table.query(
        IndexName="ConversationIdIndex",
        KeyConditionExpression=Key("ConversationId").eq(conversation_id),
    )

    # Check if conversation exists
    if response["Items"]:
        user_id = response["Items"][0]["UserId"]
        key = {"UserId": user_id, "ConversationId": conversation_id}
        delete_response = table.delete_item(Key=key)
        return delete_response
    else:
        raise ValueError(f"No conversation found with id: {conversation_id}")


def delete_conversation_by_user_id(user_id: str):
    # First, find all conversations for the user
    conversations = find_conversation_by_user_id(user_id)
    if conversations:
        table = dynamodb.Table(TABLE_NAME)
        responses = []
        for conversation in conversations:
            # Construct key to delete
            key = {"UserId": user_id, "ConversationId": conversation.id}
            response = table.delete_item(Key=key)
            responses.append(response)
        return responses
    else:
        raise ValueError(f"No conversations found for user id: {user_id}")


def change_conversation_title(conversation_id: str, new_title: str):
    table = dynamodb.Table(TABLE_NAME)

    # First, we need to find the item using the GSI
    response = table.query(
        IndexName="ConversationIdIndex",
        KeyConditionExpression=Key("ConversationId").eq(conversation_id),
    )

    items = response["Items"]
    if not items:
        raise ValueError(f"No conversation found with id {conversation_id}")

    # We'll just update the first item in case there are multiple matches
    item = items[0]
    user_id = item["UserId"]

    # Then, we update the item using its primary key
    response = table.update_item(
        Key={"UserId": user_id, "ConversationId": conversation_id},
        UpdateExpression="set Title=:t",
        ExpressionAttributeValues={":t": new_title},
        ReturnValues="UPDATED_NEW",
    )

    return response