from flask import render_template, request, send_file, redirect, url_for, flash
from flaskr.backend import Backend
from flaskr.user import User
from google.cloud import storage
import io
import hashlib
import json
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename

def make_endpoints(app, login_manager):

    @login_manager.user_loader
    def load_user(user_id):
        """Returns an empty user with the id set as the name.
        
        Args:
            user_id: the id of a user.
        """
        return User(user_id)

    """ Routes to the main page. """
    @app.before_first_request
    def init():
        backend = Backend()
        backend.init_related_pages()

    @app.route("/")
    @app.route('/main')
    def home():
        backend = Backend()
        backend.init_related_pages()
        blobs = backend.storage_client.list_blobs('related_pages')
        page_names = backend.get_all_page_names()
        link_page = []
        for page in page_names:
            if page.endswith('.txt'):
                link_page.append(page)
        return render_template('main.html', page_names=link_page)

    """ Routes to RetroVideoGames.jpg. A picture for the main page. """

    @app.route('/RetroVideoGames.jpg')
    def retro_video_game_photo():
        backend = Backend()
        image_from_bucket = backend.get_image('RetroVideoGames.jpg')
        return send_file(io.BytesIO(image_from_bucket),
                         mimetype='image/jpg',
                         download_name='RetroVideoGames.jpg')

    """ Routes to the pages page. """

    @app.route('/pages')
    def index():
        backend = Backend()
        page_names = backend.get_all_page_names()
        link_page = []
        for page in page_names:
            if page.endswith('.txt'):
                link_page.append(page)
        return render_template("index.html", page_names=link_page)


    """ Routes to a specific page in pages. """

    @app.route('/pages/<page_name>')
    def display_text(page_name):
        backend = Backend()
        text_from_page = backend.get_wiki_page(page_name)
        related_titles = []
        blobs = backend.storage_client.list_blobs('related_pages')
        get_blob = page_name[:-4]
        for blob in blobs:
            if blob.name == get_blob:
                json_data = blob.download_as_string()
                print(str(json_data))
                related_pages_string = str(json_data)[2:-1]
                if len(related_pages_string) > 0:
                    related_pages_lst = related_pages_string.split('<AND>')
                    for page in related_pages_lst:
                        related_titles.append(page + '.txt')
        page_names = backend.get_all_page_names()
        link_page = []
        for page in page_names:
            if page.endswith('.txt'):
                link_page.append(page)
        return render_template("page.html",
                               page_name=page_name,
                               text_from_page=text_from_page, related_titles=related_titles, page_names=link_page)

    """ Routes to the about page. """

    @app.route('/about')
    def about():
        backend = Backend()
        page_names = backend.get_all_page_names()
        link_page = []
        for page in page_names:
            if page.endswith('.txt'):
                link_page.append(page)
        return render_template("about.html", page_names=link_page)

    """ Routes to KesiChapman.jpg. Kesi's picture for the about page. """

    @app.route('/KesiChapman.jpg')
    def kesi_photo():
        backend = Backend()
        image_from_bucket = backend.get_image('KesiChapman.jpg')
        return send_file(io.BytesIO(image_from_bucket),
                         mimetype='image/jpg',
                         download_name='KesiChapman.jpg')

    """ Routes to MarianoGarcia.jpg. Mariano's picture for the about page. """

    @app.route('/MarianoGarcia.jpg')
    def mariano_photo():
        backend = Backend()
        image_from_bucket = backend.get_image('MarianoGarcia.jpg')
        return send_file(io.BytesIO(image_from_bucket),
                         mimetype='image/jpg',
                         download_name='MarianoGarcia.jpg')

    """ Routes to ShaneMiller.jpg. Shane's picture for the about page. """

    @app.route('/ShaneMiller.jpg')
    def shane_photo():
        backend = Backend()
        image_from_bucket = backend.get_image('ShaneMiller.jpg')
        return send_file(io.BytesIO(image_from_bucket),
                         mimetype='image/jpg',
                         download_name='ShaneMiller.jpg')

    '''  Routes to the signup page'''

    @app.route('/signup')
    def sign_up_page():
        return render_template("signup.html")

    ''' after user enters information, will send the same information from the signup page and create a user for the bucket'''

    @app.route('/signup', methods=['POST'])
    def signUp():
        backend = Backend()
        try:
            _name = request.form['Username']
            _password = request.form['Password']
            if _name and _password:
                if not backend.sign_up(_password, _name):
                    return json.dumps(
                        {'html': 'Username already exists, try again'})
                login_user(User(_name))
            else:
                return json.dumps({'sign up': 'Enter the required fields'})

        except Exception as e:
            return render_template('error.html', error=str(e))

        return render_template("main.html")

    '''  Routes to the signin page'''

    @app.route('/signin')
    def sign_in():
        return render_template("signin.html")

    ''' After user enters information in signin, will gather the information and post it (checks if information is valid)'''

    @app.route('/signin', methods=["POST"])
    def sign_in_page():
        backend = Backend()
        try:
            _name = request.form['Username']
            _password = request.form['Password']
            if _name and _password:
                if not backend.sign_in(_password, _name):
                    return json.dumps(
                        {'Sign In': 'Wrong Username or Password Entered'})
            else:
                return json.dumps({'html': 'Enter the required fields'})
        except Exception as e:
            return json.dumps({'html': 'An Error Has Occured'})
        login_user(User(_name))
        return render_template("main.html")

    '''logs the user out and returns to the main.html'''

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return render_template("main.html")

    """Routes to the upload page, shows a form where you can upload"""

    @app.route('/upload')
    @login_required
    def upload():
        return render_template('upload.html')

    """Routes to the uploader, not a real page but the action for the upload page"""

    @app.route('/uploader', methods=['GET', 'POST'])
    @login_required
    def upload_file():
        backend = Backend()
        extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

        def allowed_file(filename):
            return '.' in filename and filename.rsplit(
                '.', 1)[1].lower() in extensions

        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            f = request.files['file']
            if f.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if f and allowed_file(f.filename):
                file_name = secure_filename(f.filename)
                backend.upload(file_name, f)
            flash('file uploaded succesfully')
            return redirect(url_for('upload'))
        return redirect(url_for('upload'))
