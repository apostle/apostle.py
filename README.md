# Apostle.py

Python bindings for [Apostle.io](http://apostle.io).


## Installation


## Usage

### Domain Key
OR IN TH ENV
You will need to provide your apostle domain key to send emails.

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
var order = {
	items: ['Widget frame', 'Widget chain', 'Widget seat'],
	id: "abc123"
};

apostle.deliver('order_complete', {
	email: 'mal@apostle.io',
	replyTo: 'support@apostle.io',
	order: order
});
```

### Sending multiple emails

You can send multiple emails at once by using a queue. If any of the emails fail validation, no emails will be sent.

```python
var queue = apostle.createQueue();

queue.push('welcome_email', {email: 'mal@apostle.io'});
queue.push('order_email', {email: 'mal@apostle.io', order: order})

queue.deliver().then(success, error);
```

### Failure Responses

When recieving an error callback with `message == 'error'`, it means that the delivery to Apostle.io has failed. There are several circumstances where this might occur. You should check the `response.status` value to determine your next action. Any 2xx status code is considered a success, and will resolve the returned promise. Shortcut methods are available for some responses. In all cases, except a server error,  you can check `response.body.message` for more information.

* `response.unauthorized`, `response.status == 401` – Authorization failed. Either no domain key, or an invalid domain key was supplied.
* `response.badRequest`, `response.status == 400` – Either no json, or invalid json was supplied to the delivery endpoint. This should not occur when using the library correctly.
* `response.status == 422` – Unprocessable entitity. An invalid payload was supplied, usually a missing email or template id, or no recipients key. `Apostle.js` should validate before sending, so it is unlikely you will see this response.
* `response.serverError`, `response.status == 500` – Server error occured. Something went wrong at the Apostle API, you should try again with exponential backoff.


## Who
Created with ♥ by [Mal Curtis](http://github.com/snikch) ([@snikchnz](http://twitter.com/snikchnz))


## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request









