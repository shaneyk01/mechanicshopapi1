import unittest
from app import create_app
from app.models import db, Inventory


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.item = Inventory(name='bolt', price=1.99)
        db.session.add(self.item)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_create_inventory_item(self):
        payload = {
            'name': 'nut',
            'price': 0.99
        }
        resp = self.client.post('/inventory/', json=payload)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.get_json()['name'], 'nut')

    def test_get_all_items(self):
        resp = self.client.get('/inventory/')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        names = [d['name'] for d in data]
        self.assertIn('bolt', names)

    def test_update_inventory_item(self):
        payload = {
            'name': 'bolt-strong',
            'price': 2.49
        }
        resp = self.client.put(f'/inventory/{self.item.id}', json=payload)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['name'], 'bolt-strong')

    def test_delete_inventory_item(self):
        new_item = Inventory(name='washer', price=0.49)
        db.session.add(new_item)
        db.session.commit()
        resp = self.client.delete(f'/inventory/{new_item.id}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('deleted successfully', resp.get_json()['message'])
        list_resp = self.client.get('/inventory/')
        names = [d['name'] for d in list_resp.get_json()]
        self.assertNotIn('washer', names)

    def test_update_inventory_item_not_found(self):
        payload = {
            'name': 'ghost',
            'price': 9.99
        }
        resp = self.client.put('/inventory/999999', json=payload)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.get_json()['message'], 'Inventory item not found')
