import os
import unittest
import airflow_ml.edinet.api as api


class TestAPI(unittest.TestCase):

    def test_metadata(self):
        client = api.MetaDataClient()
        metadata = client.get("2019-01-31")
        self.assertGreater(metadata.count, 0)

    def test_document(self):
        client = api.DocumentListClient()
        documents = client.get("2019-01-31")
        self.assertGreater(len(documents), 0)

    def test_get_document(self):
        _dir = os.path.dirname(__file__)
        client = api.DocumentClient()
        file_path = client.get("S100FGR9", response_type=1, save_dir=_dir)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)

        file_path = client.get("S100FGR9", response_type=2, save_dir=_dir)  # PDF
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)

    def test_document_get(self):
        client = api.DocumentListClient()
        documents = client.get("2019-01-31")
        self.assertGreater(len(documents), 0)

        d = documents[0]

        path = d.get_pdf()
        self.assertTrue(os.path.exists(path))
        self.assertTrue(str(path).endswith(".pdf"))
        os.remove(path)

        path = d.get_xbrl()
        self.assertTrue(os.path.exists(path))
        self.assertTrue(str(path).endswith(".xbrl"))
        os.remove(path)
