from flaskr.backend import Backend


def mock_blob_kesi(blob_data):

    class MockBlobKesi:
        input = blob_data

        def __init__(self, name=input, mode=""):
            self.name = name

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            pass

        def open(self, open):
            return self

        def read(self):
            return blob_data

    return MockBlobKesi()


def mock_bucket_kesi(bucket_data):

    class MockBucketKesi:
        input = bucket_data

        def __init__(self):
            pass

        def blob(self, blob):
            fake_blob = mock_blob_kesi(bucket_data)
            return fake_blob

    return MockBucketKesi()


def mock_storage_kesi(storage_data):

    class MockStorageKesi:
        input = storage_data
        pages_list = []

        def __init__(self):
            pass

        def bucket(self, bucket):
            fake_bucket = mock_bucket_kesi(storage_data)
            return fake_bucket
        def list_blobs(self, bucket_name):
            fake_blob = mock_blob_kesi(storage_data)
            fake_list = [fake_blob]
            return fake_list

    return MockStorageKesi()


""" Test for get_wiki_page """


def test_get_wiki_page():
    mocker = mock_storage_kesi("This is a page about Mario kart.")
    backend = Backend(mocker)
    result = backend.get_wiki_page("This is a page about Mario kart.")
    assert result == "This is a page about Mario kart."


""" Test for get_all_page_names """


def test_get_all_page_names():
    mocker = mock_storage_kesi("pacman")
    backend = Backend(mocker)
    result = backend.get_all_page_names()
    assert result == ["pacman"]


""" Test for get_image """


def test_get_image():
    mocker = mock_storage_kesi("image.jpg")
    backend = Backend(mocker)
    result = backend.get_image("image.jpg")
    assert result == "image.jpg"


def mock_photo_blob(blob_name):

    class MockBlob:
        input = blob_name

        def __init__(self, name=input, mode="", data=None):
            self.name = name
            self.data = data

        def upload_from_file(self, file):
            self.data = file

    return MockBlob()


def mock_photo_bucket(bucket_name):

    class MockBucket:
        input = bucket_name

        def __init__(self, name=input, mode=""):
            self.name = name
            self.data = mock_photo_blob('mock')

        def blob(self, blob_name):
            return self.data
        def get_blob(self, blob_name):
            return self.data

    return MockBucket()


def mock_photo_storage():

    class MockStorage:

        def __init__(self):
            self._bucket = mock_photo_bucket('mock')

        def bucket(self, bucket_name):
            return self._bucket

        def get_blob(self, blob_name):
            return self.get_blob
        
        def list_blobs(self, bucket_name):
            fake_list = [mock_photo_blob('mock')]
            return fake_list

    return MockStorage()
            

''' Test for upload '''


def test_upload():
    mock_client = mock_photo_storage()
    backend = Backend(mock_client)
    backend.upload('photo', 'test_photo')
    assert mock_client.bucket('mock').blob('mock').data == 'test_photo'

''' init related pages'''
def test_init_related_pages():
    mock_client = mock_photo_storage()
    backend = Backend(mock_client)
    backend.init_related_pages()
    mock_client.bucket('mock').blob('mock').data = 'test'
    mock_client.get_blob('mock')
    assert mock_client.bucket('mock').blob('mock').data == 'test'


# ''' Test for sign up '''


# def test_sign_up(_password, _username):
#     mocker = mock_sign_up("Password", "Username")
#     backend = Backend(mocker)
#     results = backend.sign_up
#     print(results)

''' test for sign in'''


# def test_sign_in():
#     mocker = mock_sign_in("Password", "Username")
#     backend = Backend(mocker)
#     results = backend.sign_in
#     assert results == True
