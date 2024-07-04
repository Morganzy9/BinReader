
from django.test import TestCase
from bin_service.bin_service.bin_lookup.models import BinInfo  # Corrected import path

class BINInfoTestCase(TestCase):
    def setUp(self):
        BinInfo.objects.create(bin="123456", bank_name="Test Bank")

    def test_bin_info_retrieval(self):
        bin_info = BinInfo.objects.get(bin="123456")
        self.assertEqual(bin_info.bank_name, "Test Bank")

    def test_fetch_and_store_bin_info(self):
        response = self.client.get('/bin/6543217890123456/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('bank_name', data)

