# Apostle.py

Python bindings for [Apostle.io](http://apostle.io).


## Installation

```sh
pip install apostle
```

## Usage

### Domain Key
You will need to provide your apostle domain key to send emails. You can either place this value into your OS environment as `APOSTLE_DOMAIN_KEY`, or specify it in your code.

```python
apostle.domain_key = 'Your domain key';
```

### Sending Email

Sending an email is easy, a minimal example may look like this.

```python
apostle.deliver('welcome_email', {email: 'mal@apostle.io'});
```

You can pass any information that your Apostle.io template might need.

```python
order = {
	items: ['Widget frame', 'Widget chain', 'Widget seat'],
	id: "abc123"
}

apostle.deliver('order_complete', {
	'email': 'mal@apostle.io',
	'replyTo': 'support@apostle.io',
	'order': order
})
```

### Sending multiple emails

You can send multiple emails at once by using a queue. If any of the emails fail validation, no emails will be sent.

```python
queue = apostle.Queue()

queue.add('welcome_email', {'email': 'mal@apostle.io'});
queue.add('order_email', {'email': 'mal@apostle.io', 'order': order})

queue.deliver()
```

### Failure Responses

Failure to deliver will result in an exception being raised. All exceptions are namespaced under `apostle.exceptions`.

* `ValidationError` - Validation failed. One or more emails did not have a template id, or email address set (see error text).
* `UnauthorizedError` (HTTP 401) – Authorization failed. Either no domain key, or an invalid domain key was supplied.
* `ForbiddenError` (HTTP 403) – The domain key you used was not authorized to perform the action you have requested.
* `UnprocessableEntityError` (HTTP 422) – Unprocessable entitity. An invalid payload was supplied, usually a missing email or template id, or no recipients key. `apostle.py` should validate before sending, so it is unlikely you will see this response.
* `ServerError` (HTTP >= 500) – Server error. Something went wrong at the Apostle API, you should try again with exponential backoff.
* `DeliveryError` – Any response code that is not covered by the above exceptions.


## Who
Created with ♥ by [Mal Curtis](http://github.com/snikch) ([@snikchnz](http://twitter.com/snikchnz))


## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request









