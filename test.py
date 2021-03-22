from requests import get, post

print(post('http://localhost:8000/api/jobs').json())

print(post('http://localhost:8000/api/jobs',
           json={'team_leader': 'Nick'}).json())

print(post('http://localhost:8000/api/jobs',
           json={'team_leader': 'Nick',
                 'job': 'do home work',
                 'work_size': 150,
                 'collaborators': "1, 3, 4",
                 'is_finished': False}).json())

print(get('http://localhost:8000/api/jobs').json())
