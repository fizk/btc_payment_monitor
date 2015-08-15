# btc_payment_monitor

This is a microservice to enable callers to monitor payments to addresses on the Bitcoin network.

For instance, if you want to monitor payments to address 2NFePNEX3sYGnRozsvD47cq25vF4Sie5Vi4, anticipating 0.00500000 BTC, you might create a monitoring request with this microservice, and then poll it regularly to see if payment or payments have been sent to the address. When the amount you desire has been received by the address, a polled data will indicate so and how much was received. In addition, the microservice allows callers to specify at which block to start search for payments to the specified address, and what number of confirmations is required for each transaction giving payments to the address specified in order to be considered validated. 

This microservice is written in Python, using the Django-framework. To ask the webservice to monitor payments, callers must use RESTful HTTP requests, and the webservice will respond with JSON. To implement the webservice, rest_framework add-on is employed. 

## Examples ##

### List of addresses monitored 
To get a list of addresses being monitored, a request has to be performed:

```
GET /v1/monitor/?id=5,1
```

the id parameter here contains IDs of monitoring-objects created previously.

### Create a monitoring

To create a monitoring, perform a request like this:
```
POST /v1/monitor 
```

with data: 

```
{
        "address": "2NFePNEX3sYGnRozsvD47cq25vF4Sie5Vi4",
        "confirmations_required": 16,
        "block_number_start": 530583,
        "amount_desired": 500000
}
```

### Updating monitoring



