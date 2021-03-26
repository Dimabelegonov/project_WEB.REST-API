from flask import Flask, url_for, request, render_template, Blueprint, jsonify, make_response
from werkzeug.utils import redirect

from forms.user import RegisterForm, LoginForm
from sqlalchemy_serializer import SerializerMixin
from flask_login import LoginManager, login_user, login_required, logout_user
from data import db_session
from data.users import User
from data.jobs import Jobs

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandex_lyceum_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = db_sess.query(User).all()
    data = {}
    for user in users:
        data[user.id] = user.surname + " " +  user.name
    return render_template("index.html", jobs=jobs, data=data)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@blueprint.route('/api/jobs', methods=["GET"])  # Получание всех работ
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            "jobs":
                [item.to_dict(only=("id", "team_leader", "job", "work_size", "collaborators",
                                    "start_date", "end_date", "is_finished"))
                 for item in jobs]

        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=["GET"])  # Получение работы по id
def get_one_job(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': [item.to_dict(only=("id", "team_leader", "job", "work_size", "collaborators",
                                        "start_date", "end_date", "is_finished"))
                     for item in jobs]
        }
    )


@blueprint.route("/api/jobs", methods=["POST"])  # Добавление новой работы
def create_job():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({"error": "Empty request"})
    if not all(key in request.json for key in ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    flag = False
    if 'id' in request.json:
        jobs = db_sess.query(Jobs).all()
        for job in jobs:
            if job.id == request.json['id']:
                return jsonify({
                    'error': "Id already exists"
                })
        flag = True
    jobs = Jobs(
        id=request.json['id'] if flag else None,
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': "OK"})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])  # Удаление работы по id
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])  # Редактирование работы
def update_job(jobs_id):
    if not request.json:
        return jsonify({"error": "Empty request"})
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not Found'})
    new_job = Jobs(
        id=jobs.id if "id" not in request.json else request.json["id"],
        team_leader=jobs.team_leader if "team_leader" not in request.json else request.json["team_leader"],
        job=jobs.job if "job" not in request.json else request.json["job"],
        work_size=jobs.work_size if "work_size" not in request.json else request.json["work_size"],
        collaborators=jobs.collaborators if "collaborators" not in request.json else request.json["collaborators"],
        start_date=jobs.start_date if "start_date" not in request.json else request.json["start_date"],
        end_date=jobs.end_date if "end_date" not in request.json else request.json["end_date"],
        is_finished=jobs.is_finished if "is_finished" not in request.json else request.json["is_finished"],
    )
    db_sess.delete(jobs)
    db_sess.add(new_job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users', methods=['GET'])  # Получение всех пользователей
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            "users": [item.to_dict(only=("id", "surname", "name", "age", "position", "speciality",
                                         "address", "email", "hashed_password", "modified_date")) for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])  # Получение пользователя по id
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    return jsonify(
        {
            "users": [user.to_dict(only=("id", "surname", "name", "age", "position", "speciality",
                                         "address", "email", "hashed_password", "modified_date"))]
        }
    )


@blueprint.route('/api/users', methods=['POST'])  # Создание пользователя
def create_user():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in ["surname", "name", "age", "position",
                                               "speciality", "address", "email"]):
        return jsonify({'error': 'Bad request'})
    flag = False
    if 'id' in request.json:
        users = db_sess.query(User).all()
        for item in users:
            if request.json['id'] == item.id:
                return jsonify({'error': 'Id already exists'})
        flag = True

    user = User(
        id=request.json['id'] if flag else None,
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email']
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])  # Удаление пользователя
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not Found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])  # Редактирование пользователя
def update_user(user_id):
    if not request.json:
        return jsonify({"error": "Empty request"})
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not Found'})
    new_user = User(
        id=user.id if "id" not in request.json else request.json["id"],
        surname=user.surname if "surname" not in request.json else request.json["surname"],
        name=user.name if "name" not in request.json else request.json["name"],
        age=user.age if "age" not in request.json else request.json["age"],
        position=user.position if "position" not in request.json else request.json["position"],
        speciality=user.speciality if "speciality" not in request.json else request.json["speciality"],
        address=user.address if "address" not in request.json else request.json["address"],
        email=user.email if "email" not in request.json else request.json["email"],
        hashed_password=user.hashed_password if "hashed_password" not in request.json else request.json["hashed_password"],
        modified_date=user.modified_date if "modified_date" not in request.json else request.json["modified_date"],
    )
    db_sess.delete(user)
    db_sess.add(new_user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.register_blueprint(blueprint)
    app.run(port=8000, host='127.0.0.1')
