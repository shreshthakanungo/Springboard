import json
import csv
import boto3
import json
import dateutil.parser
import datetime
import time
import os
import math
import random
import logging
import re

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    return response
    
def generic():
    s3=boto3.client("s3")
    filename='amazon_co-ecommerce_modified.csv'
    csvfile = s3.get_object(Bucket='myspringboardfirst', Key=filename)
    rows = csvfile['Body'].read().decode("utf-8").split('\n')
    reader = csv.reader(rows)
    header = next(reader)
    return(reader)

""" --- Function that return Price of product --- """
def productPrice(productName):
    dataFromS3 = generic()
    output=[]
    for row in dataFromS3:
        for column in row:
            if column==productName:
                output.append(row[3])
                print('output---',output)
    if not output :
        return ("There is no Product by this name")
    else:
        return ('Product prices are {}'.format(output))


""" --- Function that return List of product of a given Manufacturer --- """ 

def ListOfProduct(manufacturerName):
    dataFromS3 = generic()
    product_list = []
    for row in dataFromS3:
        for column in row:    
            if column ==  manufacturerName:
                product_list.append(row[1])
    if not product_list :
        return ("There is no Product from this manufacturer")
    else:
        return (product_list[:1])
        # topList = sorted(product_list, key=lambda i: product_list[i], reverse=True)[:5]
        # return(topList)
        

""" --- Function that return if the given product is in the stock --- """ 

def availableInStock(productName):
    dataFromS3 = generic()
    avail_stocks=[]
    for row in dataFromS3:
        for column in row:
            if column==productName:
                avail_stocks.append(row[5])
                #print('output---',output)
    if not avail_stocks :
        return ("There is no Product in the stock")
    else:
        return ('There are {} products'.format(avail_stocks))


def return_ProductPrice(intent_request):
    """
    Performs dialog management and fulfillment for returning Product’s price.
    """
    pro_name = intent_request['currentIntent']['slots']['Product_name'] 
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    
    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        slots = intent_request['currentIntent']['slots']
    return close(
        output_session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Hello! {}'.format(productPrice(pro_name))
        }
    )
    
def return_ListOfProduct(intent_request):
    """
    Performs dialog management and fulfillment for returning Product’s price.
    """
    manufac_name = intent_request['currentIntent']['slots']['Manufacturer_name'] 
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    
    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        slots = intent_request['currentIntent']['slots']
    return close(
        output_session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Hello list of Products are: {}'.format(ListOfProduct(manufac_name))
        }
    )  
    
    
def intent_AvailabilityInStock(intent_request):
    """
    Performs dialog management and fulfillment for returning Product’s price.
    """
    availableStock = intent_request['currentIntent']['slots']['product_name'] 
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    
    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        slots = intent_request['currentIntent']['slots']
    return close(
        output_session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Hello! : {}'.format(availableInStock(availableStock))
        }
    )  
    

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    logger.debug('dispatch intentName={}'.format(intent_request['currentIntent']['name']))
    intent_name=intent_request['currentIntent']['name']
    
    # Dispatch to your bot's intent handlers
    if intent_name == 'ReturnPriceForProduct':
        return return_ProductPrice(intent_request)

    elif intent_name == 'ReturnListOfProduct':
        return return_ListOfProduct(intent_request)
    
    elif intent_name == 'ReturnAvailabilityInStock':
        return intent_AvailabilityInStock(intent_request)
        
    raise Exception('Intent with name ' + intent_name + ' not supported')


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    # os.environ['TZ'] = 'America/New_York'
    # time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    print('event ---',event)
    return dispatch(event)
