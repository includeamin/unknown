from api.settings import storage_settings


class Storage:
    def __init__(self):
        self.raw: str
        self._bucket_name: str = storage_settings.RAW_FILES_BUCKET

    def move(self):
        pass

    def delete(self):
        pass
