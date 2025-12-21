import unittest
from app import create_app
from app.models import db, Customer, ServiceTickets
from app.utils.auth import encode_token
from datetime import date


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = Customer(name='test',email ='test@test.com',phone='8907865430',password='1234')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        db.session.add(self.customer)
        db.session.commit()
        self.client = self.app.test_client()
        

    def tearDown(self):
        self.app_context.pop()

    def test_create_customer(self):
        payload ={
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "8087654321",
            "password": "pass1234"
        }
        response = self.client.post('/customers/', json = payload)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.get_json()['name'], 'John Doe')

    def test_get_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'test')

    def test_login_success(self):
        payload = {
            "email": "test@test.com",
            "password": "1234"
        }
        response = self.client.post('/customers/login', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

    def test_login_invalid_credentials(self):
        payload = {
            "email": "test@test.com",
            "password": "wrong"
        }
        response = self.client.post('/customers/login', json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['message'], 'Invalid email or password')

    def test_get_customer_by_id(self):
        response = self.client.get(f'/customers/{self.customer.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], self.customer.id)
        self.assertEqual(response.get_json()['name'], 'test')

    def test_get_customer_not_found(self):
        response = self.client.get('/customers/999999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['message'], 'Customer not found')

    def test_update_customer(self):
        payload = {
            "name": "Updated Name",
            "email": "test@test.com",
            "phone": "1234567890",
            "password": "1234"
        }
        response = self.client.put(f'/customers/{self.customer.id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Updated Name')

    def test_delete_customer(self):
        # create a fresh customer to delete
        to_delete = Customer(name='delete me', email='deleteme@test.com', phone='1111111111', password='pw')
        db.session.add(to_delete)
        db.session.commit()
        response = self.client.delete(f'/customers/{to_delete.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('deleted successfully', response.get_json()['message'])
        # confirm it's gone
        get_resp = self.client.get(f'/customers/{to_delete.id}')
        self.assertEqual(get_resp.status_code, 404)

    def test_get_customer_service_tickets(self):
        # create a service ticket for seeded customer
        ticket = ServiceTickets(date=date.today(), customer_id=self.customer.id, service_descr='Oil change')
        db.session.add(ticket)
        db.session.commit()
        token = encode_token(self.customer.id, role='customer')
        response = self.client.get(
            f'/customers/{self.customer.id}/service_tickets',
            headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]['service_descr'], 'Oil change')

  