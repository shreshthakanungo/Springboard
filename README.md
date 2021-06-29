# Springboard Cpaestone project:

Here is the link to my Amze_bot which is chatbot created by using different AWS services and which is deployed on Slack applocation.

https://app.slack.com/client/T01Q4EZ9J5R/D01Q4F0JYFL

A Chatbot is an Artificial Intelligence software that can simulate human conversations with a user in natural language. A Chatbot returns a response based on input from user.
Why do we need Chatbot ? The modern E-Commerce sites are constantly seeking to expand their technologies, both to improve customer service and increase delivery of services through advancement in technology and to expand the customer base.

Datasets : Here I am using the dataset of amazon-ecommerce which is downloaded from https://www.data.gov . This dataset contains 10,000 rows. It contains colomns such as: product_name, Manufacturer, price, number_available in stock, number_of_reviews, Product_information, etc. Through this dataset thw chatbot will be able to answer questions such as :
    1. What is the price of the product
    2. Is the product available in the stock
    3. Can I get all the products of manufacturer (If you dont provide the manufacturer name then the chatbot will ask you for the manufacturer name and then answer the question)
    4. What are th ratings of that product
    
To build this bot I have used several AWS services such as Amazon Lex, Amazon Lambda Function, Amazon S3 bucket, Amazon CloudWatch. Amazon Lex is a conversational interface for applications using voice and text. An amazon Lex is powered by Atomatic Speech Recognition and Natural Language Understanding capabilities. NLU is a branch of Natural Langugae Processing (NLP), which helps computers understand and interpret human language by breaking down the elemental pieces of speech.

The basic terminology used in Amazon Lex are:
    1. Bot -> A bot performs automated tasks such as ordering a pizza, booking a hotel, ordering flowers, Answering user's Question and so on. Amazon Lex bots can understand user inputs provided with text or speech and converse them in Natural language.
    2. Intent -> An intent represents an action that the user wants to perform. There can be one or intents of a bot. Each Intent contains the foloowing requirement:
        i. Intent name - Name of the intent
       ii. Sample utterances - How a user might convey the intent. These utterances can be used to train our bot.
      iii. How to fulfill the intent - How to fulfill the intent after the user provides the necessary information. This can be done by creating Lambda Functions or you can configure the intnent so that it returns the information to the user.
       iv. Slot - An intent can require zero or more slots or parameters. Slots can be added as a part of intent configuration. The user must provide values of all required slots before amazon lex fulfill the intent.
        v. Slot Type - Each slot has a slot type. You can create your own custom slot types or use build-in slot types. Each slot type must have a unique name within the account.
        
    
    
