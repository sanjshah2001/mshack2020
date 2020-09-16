import logging
import uuid
import datetime
import urllib
import requests
import json
import azure.functions as func


def main(req: func.HttpRequest, cosmos: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    
    # If data comes via GET
    userId = req.params.get('userId')
    productId = req.params.get('productId')
    locationName = req.params.get('locationName')
    rating = req.params.get('rating')
    userNotes = req.params.get('userNotes')

    # If data comes via POST
    if not userId: 
        req_body = req.get_json()
        userId = req_body.get('userId')
        productId = req_body.get('productId')
        locationName = req_body.get('locationName')
        rating = req_body.get('rating')
        userNotes = req_body.get('userNotes')



    #Validate userId and productID
    # The URL will need to be editted after service create.
    url_userid = "https://serverlessohuser.trafficmanager.net/api/GetUser"
    url_productid = "https://serverlessohproduct.trafficmanager.net/api/GetProduct"

    req = urllib.request.Request(url_userid + "?userId=" + userId)
    try:
        response = urllib.request.urlopen(req).read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return func.HttpResponse(f"Error: userId not found")

    req = urllib.request.Request(url_productid + "?productId=" + productId) 
    try:
        response = urllib.request.urlopen(req).read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return func.HttpResponse(f"Error: productId not found")

    # Validate rating is a integer 0-5
    if int(rating) in range(0, 6): pass
    else:
       return func.HttpResponse(f"Error: rating is not an integer between 0-5") 

    mydict = {
        "id":id,
        "timestamp": timestamp,
        "userId": userId,
        "productId": productId,
        "locationName": locationName,
        "rating": rating,
        "userNotes": userNotes
    }

    #Write to CosmosDF

    cosmos.set(func.Document.from_dict(mydict))

    return func.HttpResponse(json.dumps(mydict),status_code=200)

