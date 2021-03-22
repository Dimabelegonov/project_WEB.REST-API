from requests import get, post, delete

print(post('http://localhost:8000/api/jobs',
           json={'team_leader': 'Nick',
                 'job': 'do home work',
                 'work_size': 150,
                 'collaborators': "1, 3, 4",
                 'is_finished': False}).json())

print(post('http://localhost:8000/api/jobs',
           json={'team_leader': 'Nick',
                 'job': 'do home work',
                 'work_size': 150,
                 'collaborators': "1, 3, 4",
                 'is_finished': False}).json())

print(post('http://localhost:8000/api/jobs',
           json={'team_leader': 'Nick',
                 'job': 'do home work',
                 'work_size': 150,
                 'collaborators': "1, 3, 4",
                 'is_finished': False}).json())

print(post('http://localhost:8000/api/jobs',
           json={'team_leader': 'Nick',
                 'job': 'do home work',
                 'work_size': 150,
                 'collaborators': "1, 3, 4",
                 'is_finished': False}).json())

print(get('http://localhost:8000/api/jobs').json())

print(delete('http://localhost:8000/api/jobs/5').json())

print(delete('http://localhost:8000/api/jobs/77').json())

print(delete('http://localhost:8000/api/jobs/3').json())

print(delete('http://localhost:8000/api/jobs/4').json())

print(get('http://localhost:8000/api/jobs').json())
