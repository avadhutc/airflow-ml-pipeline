import json
from tempfile import NamedTemporaryFile
from google.cloud import storage


class Storage():

    def __init__(self, root, credential_path=None):
        self.root = root
        self.credential_path = credential_path

    def upload_file(self, path, content_path="", content=None):
        _content_path = content_path
        if not _content_path:
            if content is not None:
                _content = content
                if isinstance(_content, dict):
                    _content = json.dumps(_content)

                with NamedTemporaryFile(delete=False, mode="w",
                                        encoding="utf-8") as ntf:
                    ntf.write(_content)
                    ntf.flush()
                    _content_path = ntf.name
            else:
                raise Exception("Target content is not spefified")

        blob = self.get_blob(path, check_existance=False)
        blob.upload_from_filename(filename=str(_content_path))

    def download_file(self, path, save_path):
        with open(path, "wb") as f:
            self.get_blob(path).download_to_file(f)

    def download_conent(self, path, encoding="utf-8"):
        return self.get_blob(path).download_as_string().decode(encoding)

    def exists(self, path):
        return self.get_blob(path, check_existance=False).exists()

    def get_blob(self, path, check_existance=True):
        blob = self._get_client().get_bucket(self.root).blob(path)

        if check_existance and not blob.exists():
            raise Exception("{} does not exist at {}.".format(path, self.root))
        return blob

    def list_blobs(self, prefix=None, delimiter=None):
        bucket = self._get_client().get_bucket(self.root)
        blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
        return blobs

    def _get_client(self):
        if self.credential_path is not None:
            client = storage.Client.from_service_account_json(
                        self.credential_path)
        else:
            client = storage.Client()
        return client

    def delete(self, path):
        self.get_blob(path).delete()
