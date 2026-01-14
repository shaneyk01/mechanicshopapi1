import unittest
from app import create_app
from app.models import db, Mechanic
from app.utils.auth import encode_token


class TestMechanics(unittest.TestCase):

	def setUp(self):
		self.app = create_app('TestingConfig')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.drop_all()
		db.create_all()
		self.mechanic = Mechanic(
			name='seed',
			email='seed@shop.com',
			salary=50000,
			password='secret'
		)
		db.session.add(self.mechanic)
		db.session.commit()
		self.client = self.app.test_client()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_create_mechanic(self):
		payload = {
			"name": "New Mech",
			"email": "new@shop.com",
			"salary": 60000,
			"password": "newpass"
		}
		response = self.client.post('/mechanics/', json=payload)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.get_json()['name'], 'New Mech')

	def test_get_mechanics(self):
		response = self.client.get('/mechanics/')
		self.assertEqual(response.status_code, 200)
		data = response.get_json()
		self.assertIsInstance(data, list)
		self.assertGreaterEqual(len(data), 1)
		self.assertEqual(data[0]['name'], 'seed')

	def test_update_mechanic(self):
		payload = {
			"name": "Updated Seed",
			"email": "seed@shop.com",
			"salary": 55000,
			"password": "secret"
		}
		response = self.client.put(
			f'/mechanics/{self.mechanic.id}',
			json=payload
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json()['name'], 'Updated Seed')

	def test_update_mechanic_not_found(self):
		payload = {
			"name": "Ghost",
			"email": "ghost@shop.com",
			"salary": 50000,
			"password": "secret"
		}
		response = self.client.put(
			'/mechanics/999999',
			json=payload
		)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.get_json()['message'], 'Mechanic not found')

	def test_delete_mechanic(self):
		to_delete = Mechanic(name='deleteme', email='deleteme@shop.com', salary=40000, password='pw')
		db.session.add(to_delete)
		db.session.commit()
		response = self.client.delete(f'/mechanics/{to_delete.id}')
		self.assertEqual(response.status_code, 200)
		self.assertIn('deleted successfully', response.get_json()['message'])
		list_resp = self.client.get('/mechanics/')
		emails = [m['email'] for m in list_resp.get_json()]
		self.assertNotIn('deleteme@shop.com', emails)

	def test_delete_mechanic_not_found(self):
		response = self.client.delete('/mechanics/999999')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.get_json()['message'], 'Mechanic not found')
