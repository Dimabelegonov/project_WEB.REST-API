from flask import Flask, url_for, request, render_template, Blueprint, jsonify
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
            'jobs': jobs.to_dict()
        }
    )


@blueprint.route("/api/jobs", methods=["POST"])
def create_job():
    print(1)
    if not request.json:
        print(1)
        return jsonify({"error": "Empty request"})
    elif not all(key in request.json for key in ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    else:
        db_sess = db_session.create_session()
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


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
