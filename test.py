from requests import get, post, delete, put

print(get('http://localhost:8000/api/users').json())

print(delete('http://localhost:8000/api/users/1').json())

print(get('http://localhost:8000/api/users').json())

print(post('http://localhost:8000/api/users',
           json={'address': 'module_1',
                 'age': 12,
                 'email': 'scott_chief@mars.com',
                 'hashed_password': None,
                 'id': 1,
                 'modified_date': None,
                 'name': 'Rid',
                 'position': 'capt',
                 'speciality': 'research engineer',
                 'surname': 'Sctt'}).json())

print(get('http://localhost:8000/api/users').json())

print(put('http://localhost:8000/api/users/1',
          json={'address': 'module_1',
                'age': 56,
                'email': 'scott_chief@mars.com',
                'hashed_password': None,
                'id': 1,
                'modified_date': None,
                'name': 'Ridley',
                'position': 'captain',
                'speciality': 'research engineer',
                'surname': 'Scott'}).json())

print(get('http://localhost:8000/api/users').json())
