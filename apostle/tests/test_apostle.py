import json

import unittest

from mock import patch
from mock import Mock

import apostle
from apostle import exceptions


class ApostleTest(unittest.TestCase):
	def testMissingTemplateIdRaisesException(self):
		self.assertRaises(
			exceptions.ValidationError,
			apostle.deliver, None, None
		)

	def testMissingEmailRaisesException(self):
		self.assertRaises(
			exceptions.ValidationError,
			apostle.deliver, "template_id", {}
		)

	def testDeliverCreatesQueueAddsAndRuns(self):
		queue_mock = Mock()
		queue_add = queue_mock.add = Mock()
		queue_deliver = queue_mock.deliver = Mock()

		with patch('apostle.get_queue', return_value=queue_mock) as queue:
			apostle.deliver("template_id", {'email': "user@example.org"})

		self.assertTrue(queue.called)
		self.assertTrue(queue_add.called)
		self.assertTrue(queue_deliver.called)



class MailTest(unittest.TestCase):
	def testMailSetters(self):
		mail = apostle.Mail("template slug", {
			'email': 'user@example.org',
			'name': 'Example User',
			'foo': 'bar'
		})

		mail.headers['Client'] = 'Test'
		mail.bar = 'baz'

		self.assertEquals(mail.data, {'foo': 'bar', 'bar': 'baz'})
		self.assertEquals(mail.headers, {'Client': 'Test'})
		self.assertEquals(mail.template_id, 'template slug')
		self.assertEquals(mail.email, 'user@example.org')
		self.assertEquals(mail.name, 'Example User')

	def testMailToRecipientDict(self):
		mail = apostle.Mail("template slug", {
			'email': 'user2@example.org',
			'name': 'This User',
			'foo': 'bar'
		})
		self.assertDictEqual(mail.to_recipient_dict(), {
			'user2@example.org' : {
				'name': 'This User',
				'data': { 'foo': 'bar' },
				'template_id': 'template slug'
			}
		})


class QueueTest(unittest.TestCase):
	def setUp(self):
		self.queue = apostle.Queue()

	def tearDown(self):
		apostle.domain_key = None

	def testAddingMailToQueue(self):
		queue = self.queue
		self.assertEquals(len(queue.emails), 0)
		queue.add(True)
		queue.add(True)
		queue.add(True)
		self.assertEquals(len(queue.emails), 3)

	def testDeliverWithoutDomainKeyRaisesException(self):
		self.assertRaises(
			apostle.exceptions.UnauthorizedError,
			self.queue.deliver
		)

class QueueDeliveryTest(unittest.TestCase):

	def assertDeliverRaisesException(self, code, exception):
		request_mock = Mock()
		request_mock.status_code = code
		with patch('requests.post', return_value=request_mock) as request:
			self.assertRaises(exception, self.queue.deliver)

	def setUp(self):
		self.queue = apostle.Queue()
		apostle.domain_key = 'abc123'

	def tearDown(self):
		apostle.domain_key = None

	def testDeliverWithInvalidMailRaisesException(self):
		bad_mail = apostle.Mail(None, None)
		self.queue.add(bad_mail)

		self.assertRaises(
			apostle.exceptions.ValidationError,
			self.queue.deliver
		)

	def testDeliverSendsPayloadToApostle(self):
		request_mock = Mock()
		request_mock.status_code = 202

		self.queue.add(apostle.Mail('slug', { 'email': 'user@example.org' }))

		with patch('requests.post', return_value=request_mock) as request:
			self.queue.deliver()

		request.assert_called_with('https://deliver.apostle.io',
			headers={
				'Apostle-Client': "Python/{0}".format(apostle.__version__),
				'Authorization': 'Bearer abc123',
				'Content-Type': 'application/json'
			},
			data='{"recipients": {"user@example.org": {"template_id": "slug"}}}'
		)

	def testDeliverRaisesExceptionOn401(self):
		self.assertDeliverRaisesException(401, exceptions.UnauthorizedError)

	def testDeliverRaisesExceptionOn403(self):
		self.assertDeliverRaisesException(403, exceptions.ForbiddenError)

	def testDeliverRaisesExceptionOn422(self):
		self.assertDeliverRaisesException(422, exceptions.UnprocessableEntityError)

	def testDeliverRaisesExceptionOn500(self):
		self.assertDeliverRaisesException(500, exceptions.ServerError)


def main():
    unittest.main()

if __name__ == '__main__':
    main()


