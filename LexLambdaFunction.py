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
import numpy

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
                output = row[3]
                
                print('output---', output)
    if not output :
        return ("There is no Product by this name")
    else:
        return ('Product price is; {}'.format(output))



# """ --- Function that return list of product given age group --- """
# def productByAge(age_group):
#     dataFromS3 = generic()
#     output=[]
#     product_list =[]
#     for row in dataFromS3:
#         for column in row:
#             if column==product_information:
#                 print(column[:2])
#                 product_list.append(row[1])
#                 for description in column:
#                     re.findall(r'[0-9]+', description)
#                     output.append(newlist)
#                 # print('output---',output)
#     if not output :
#         return ("There is no Product by this name")
#     else:
#         return ('Product prices are {}'.format(output))



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
        return (', '.join(product_list[:3]))
        
        

""" --- Function that return if the given product is in the stock --- """ 

def availableInStock(productName):
    dataFromS3 = generic()
    avail_stocks=[]
    for row in dataFromS3:
        for column in row:
            if column==productName:
                avail_stocks=(row[4])
                #print('output---',output)
    if not avail_stocks :
        return ("There is no Product in the stock")
    else:
        return ('There are {} products by this name'.format(avail_stocks))
        
        
# def return_productByAge(ageGroup):
#     """
#     Performs dialog management and fulfillment for returning Product’s price.
#     """
#     age_group = intent_request['currentIntent']['slots']['Age_group'] 
#     source = intent_request['invocationSource']
#     output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    
#     if source == 'DialogCodeHook':
#         # Perform basic validation on the supplied input slots.
#         slots = intent_request['currentIntent']['slots']
#     return close(
#         output_session_attributes,
#         'Fulfilled',
#         {
#             'contentType': 'PlainText',
#             'content': 'Hello! {}'.format(productByAge(age_group))
#         }
#     )


"""
Performs dialog management and fulfillment for returning Product’s price.
"""
def return_ProductPrice(intent_request):
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
    
    manufac_name = intent_request['currentIntent']['slots']['manufacturer_name'] 
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
            'content': 'Hello the diffferent Products are: {}'.format(ListOfProduct(manufac_name))
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
            'content': '{}'.format(availableInStock(availableStock))
        }
    )  
    

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    logger.debug('dispatch intentName={}'.format(intent_request['currentIntent']['name']))
    intent_name=intent_request['currentIntent']['name']
    
    print ('the intent name is ----', intent_name)
    # Dispatch to your bot's intent handlers
    if intent_name == 'ReturnPriceForProduct':
        return return_ProductPrice(intent_request)

    elif intent_name == 'ReturnListOfProduct':
        return return_ListOfProduct(intent_request)
    
    elif intent_name == 'ReturnAvailabilityInStock':
        return intent_AvailabilityInStock(intent_request)
        
    elif intent_name == 'ReturnProductByAge':
        return intent_AvailabilityInStock(intent_request)
        
    raise Exception('Intent with name ' + intent_name + ' not supported')


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    nameIntent = event['currentIntent']['name']
    nluIntentConfidenceScore = event['currentIntent']['nluIntentConfidenceScore']
    # print('nluIntentConfidenceScore --', nluIntentConfidenceScore)
    
    Strings = nameIntent + '       ' + str(nluIntentConfidenceScore)
    
    bucket_name = 'myspringboardfirst'
    filename = "Lambda_logs_file.csv"
    
    s3_path = "output/" + filename
    
    s3=boto3.client("s3")
    filename='Lambda_logs_file.csv'
    lambda_path = "/tmp/"+ filename
    txtfile = s3.get_object(Bucket='myspringboardfirst', Key=filename)
    reading = txtfile['Body'].read().decode("utf-8").split('\n')
    print ('reading ---', reading)
    reading1 = str(reading) + '  ' + Strings
    
    
    # print('txtfile --', txtfile);
        
    with open(lambda_path, 'w+') as file:
        file.write(str(reading1))
        file.close()
        
    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(lambda_path, bucket_name, filename)
    
    # By default, treat the user request as coming from the America/New_York time zone.
    # os.environ['TZ'] = 'America/New_York'
    # time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    print('event ---',event)
    return dispatch(event)
    
