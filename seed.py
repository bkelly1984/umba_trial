import logging
import requests

from db import Db
from user_dao import UserDao

total = 150
git_username = "bkelly1984"
#git_password = ""
url = 'https://api.github.com/users?accept=application/vnd.github.v3+json&per_page=100'

#logging.basicConfig(level=logging.INFO)

# Instantiate the database objects
db = Db()
user_dao = UserDao()

# Create or clean the database
user_dao.create_or_clear_table(db)

# Prepare to make many requests to the database
count = 0
last_id = 0
while count < total:

    # Get 100 user records
    try :
        response = requests.get(url + f'&since={last_id}', f'auth=({git_username}, {git_password})')
    except NameError:
        response = requests.get(url + f'&since={last_id}')

    # Add each user to the database
    for user in response.json():
        user_dao.create(db, user)
        last_id = user['id']
        count += 1

        if count >= total:
            break

    # Commit this round of users and provide an update
    db.commit()
    logging.info(f"Seed is {(100 * count) // total}% complete")
