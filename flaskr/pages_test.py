from flaskr import create_app

import pytest


# See https://flask.palletsprojects.com/en/2.2.x/testing/
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()


""" Test for home. Routes to 'main' page. """


# def test_home_page(client):
#     resp = client.get("/")
#     assert resp.status_code == 200
#     assert b"Welcome to our page!" in resp.data


# """ Test for retro_video_game_photo. Routes to 'RetroVideoGames.jpg' photo. """


# def test_retro_video_game_photo(client):
#     resp = client.get("/RetroVideoGames.jpg")
#     assert resp.status_code == 200


# """Tests for both the sign up/in pages  """


# def test_sign_in_page(client):
#     resp = client.get('/signin')
#     assert resp.status_code == 200


# def test_sign_up_page(client):
#     resp = client.get('/signup')
#     assert resp.status_code == 200


# """ Test for page. Routes to 'pages' page. """


# def test_page(client):
#     resp = client.get("/pages")
#     assert resp.status_code == 200
#     assert b"Pages included" in resp.data


# """ Test for display_text. Routes to 'pages/Tetrix.txt' page. """


# def test_display_text(client):
#     resp = client.get("/pages/Tetris.txt")
#     assert resp.status_code == 200
#     assert b"developed in 1984" in resp.data


# """ Test for about. Routes to 'about' page. """


# def test_about(client):
#     resp = client.get("/about")
#     assert resp.status_code == 200
#     assert b"We hope you enjoy exploring the content!" in resp.data


# """ Test for kesi_photo. Routes to 'KesiChapman.jpg' photo."""


# def test_kesi_photo(client):
#     resp = client.get("/KesiChapman.jpg")
#     assert resp.status_code == 200


# """ Test for mariano_photo. Routes to 'MarianoGarcia.jpg' photo."""


# def test_mariano_photo(client):
#     resp = client.get("/MarianoGarcia.jpg")
#     assert resp.status_code == 200


# """ Test for shane_photo. Routes to 'ShaneMiller.jpg' photo."""


# def test_shane_photo(client):
#     resp = client.get("/ShaneMiller.jpg")
#     assert resp.status_code == 200


# ''' Test for Upload, routes to the upload.html'''


# def test_upload(client):
#     resp = client.get("/upload")
#     assert resp.status_code == 200
#     assert b"Upload your file here!" in resp.data


# ''' Test for Uploader, routes an action, ensures its active'''


# def test_uploader(client):
#     resp = client.get("/uploader")
#     assert resp.status_code == 302
