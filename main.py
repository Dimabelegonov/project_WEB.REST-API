from flask import Flask, url_for, request, render_template, Blueprint, jsonify
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
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


@app.route('/')
@app.route('/index')
def index():
    return "Hello World!"


@blueprint.route('/api/jobs', methods=["GET"])
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


@blueprint.route('/api/jobs/<int:jobs_id>', methods=["GET"])
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


@blueprint.route("/api/jobs", methods=["POST"])
def create_job():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not all(key in request.json for key in ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    elif 'id' in request.json:
        jobs = db_sess.query(Jobs).all()
        for job in jobs:
            if job.id == request.json['id']:
                return jsonify({
                    'error': "Id already exists"
                })
    else:
        jobs = Jobs(
            team_leader=request.json['team_leader'],
            job=request.json['job'],
            work_size=request.json['work_size'],
            collaborators=request.json['collaborators'],
            is_finished=request.json['is_finished']
        )
        db_sess.add(jobs)
        db_sess.commit()
        return jsonify({'success': "OK"})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def update_job():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not Found'})
    for key in request.json:
        if key in ("id", "team_leader", "job", "work_size", "collaborators",
                                        "start_date", "end_date", "is_finished"):
            pass


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.register_blueprint(blueprint)
    app.run(port=8000, host='127.0.0.1')
