# BTC Payment Monitor

This is a microservice to enable callers to monitor payments to addresses on the Bitcoin network.

For instance, if you want to monitor payments to address 2NFePNEX3sYGnRozsvD47cq25vF4Sie5Vi4, anticipating 0.00500000 BTC, you might create a monitoring request with this microservice, and then poll it regularly to see if payment or payments have been sent to the address. When the amount you desire has been received by the address, polled data will indicate so and how much was received. In addition, the microservice allows callers to specify at which block to start search for payments, and what number of confirmations is required for each transaction giving payments to the address specified in order to be considered validated. 

This microservice is written in Python, using the Django framework. To ask the webservice to monitor payments, callers must use REST-ful HTTP requests, and the webservice will respond with JSON. To implement the webservice, the rest_framework add-on is employed. 

Access is controlled by authenticating once, and then using cookies to create and poll monitorings.

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

which will result in a response like this one

```
{
    "id": 9,
    "created_at": "2015-08-15T17:52:59.546344Z",
    "address": "BPMAddress object",
    "confirmations_required": 16,
    "cancelled": false,
    "block_number_start": 530583,
    "block_number_scanned": 0,
    "amount_desired": 500000,
    "amount_paid": 0,
    "goal_reached": false,
    "goal_reached_at": null
}
```

### Updating monitoring

Already registered monitors cannot be edited, except for the 'cancelled' field. Setting this field to 'true' will cause monitoring to be cancelled.

For instance, to edit the monitor above, a request like this one can be issued:

```
PUT /v1/monitor/9/
``` 

with the following data submitted:

```
{
    "id" : 9,
    "cancelled": true
}
```

and this will cause the object be updated, and subsequently monitoring will cease.

### Authentication

# FIXME: pk --> id
# FIXME: Implement PUT
# FIXME: Implement authentication
# FIXME: Write unit-tests
# FIXME: Logging facility ! Preferably something that is system-wide to our platform.


