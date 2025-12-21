import unittest
from datetime import date
from app import create_app
from app.models import db, Customer, Mechanic, ServiceTickets


class TestServiceTickets(unittest.TestCase):

	def setUp(self):
		self.app = create_app('TestingConfig')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.drop_all()
		db.create_all()
		# seed a customer and a mechanic
		self.customer = Customer(name='cust', email='cust@test.com', phone='1234567890', password='pw')
		self.mechanic = Mechanic(name='mech', email='mech@test.com', salary=45000, password='pw')
		db.session.add_all([self.customer, self.mechanic])
		db.session.commit()
		self.client = self.app.test_client()

	def tearDown(self):
		db.session.remove()
		self.app_context.pop()

	def test_create_ticket(self):
		payload = {
			'date': date.today().isoformat(),
			'customer_id': self.customer.id,
			'service_descr': 'Oil change'
		}
		resp = self.client.post('/service_tickets/', json=payload)
		self.assertEqual(resp.status_code, 201)
		data = resp.get_json()
		self.assertEqual(data['service_descr'], 'Oil change')
		self.assertEqual(data['customer_id'], self.customer.id)

	def test_get_tickets(self):
		# seed one ticket
		t = ServiceTickets(date=date.today(), customer_id=self.customer.id, service_descr='Check brakes')
		db.session.add(t)
		db.session.commit()
		resp = self.client.get('/service_tickets/')
		self.assertEqual(resp.status_code, 200)
		data = resp.get_json()
		self.assertIsInstance(data, list)
		self.assertGreaterEqual(len(data), 1)

	def test_create_ticket_validation_error(self):
		# missing service_descr should trigger 400 from schema
		bad_payload = {
			'date': date.today().isoformat(),
			'customer_id': self.customer.id
		}
		resp = self.client.post('/service_tickets/', json=bad_payload)
		self.assertEqual(resp.status_code, 400)

	def test_edit_ticket_add_remove_mechanic(self):
		# create a ticket
		t = ServiceTickets(date=date.today(), customer_id=self.customer.id, service_descr='Tune up')
		db.session.add(t)
		db.session.commit()
		# add the mechanic (use single id to match current route behavior)
		edit_payload = {
			'add_mechanic_ids': [self.mechanic.id],
			'remove_mechanic_ids': []
		}
		resp = self.client.put(f'/service_tickets/{t.id}', json=edit_payload)
		self.assertEqual(resp.status_code, 200)
		data = resp.get_json()
		self.assertIn('mechanics', data)
		self.assertGreaterEqual(len(data['mechanics']), 1)
		self.assertEqual(data['mechanics'][0]['id'], self.mechanic.id)

	def test_delete_ticket(self):
		# create a ticket
		t = ServiceTickets(date=date.today(), customer_id=self.customer.id, service_descr='Alignment')
		db.session.add(t)
		db.session.commit()
		resp = self.client.delete(f'/service_tickets/{t.id}')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('deleted successfully', resp.get_json()['message'])