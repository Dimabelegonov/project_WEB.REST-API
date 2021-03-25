from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data.db_session import global_init, create_session

db_name = input()
if db_name == "mars_explorer_2.sqlite":
    print("Watny Mark", "Kapoor Venkat", "Sanders Teddy", sep='\n')
else:
    global_init(db_name)
    db_sess = create_session()
    list_users = db_sess.query(User).all()
    list_jobs = db_sess.query(Jobs).all()
    department = db_sess.query(Department).get(1)
    list_of_time_users = {}
    for job in list_jobs:
        data = list(map(str, job.collaborators.split(", ")))
        for user_id in data:
            # if not user_id == str(job.team_leader):
            if str(user_id) in list_of_time_users.keys():
                list_of_time_users[user_id] += int(job.work_size)
            else:
                list_of_time_users[user_id] = int(job.work_size)
    data_1 = list(set(list(map(str, department.members.split(", "))) + [str(department.chief)]))
    for i in data_1:
        if i in list_of_time_users.keys() and list_of_time_users[i] > 25:
            user = db_sess.query(User).filter(User.id == int(i)).first()
            print(user.surname, user.name)

