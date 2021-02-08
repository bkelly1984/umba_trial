from flask import Flask, jsonify, request, send_file, send_from_directory
import logging

from db import Db
from user_dao import UserDao

app = Flask("user_api")
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def get_index():
    """
    Root Flask route to serve index.html

    Parameters: None

    Returns:
        Response: A Flask Response object containing index.html
    """

    logging.info("Serving file index.html")
    return send_file('index.html')


@app.route("/images/<filename>")
def get_image(filename):
    """
    Flask route to serve the files located in the image directory

    Parameters:
        filename (str): The name of the file to access.

    Returns:
        Response: A Flask Response object containing the requested file
    """

    logging.info(f"Serving file images/{filename}")
    return send_from_directory("images", filename)


@app.route('/user')
def get_user():
    """
    Flask route that reads a DataTable request string and returns records in JSON format

    Parameters: None

    Returns:
        Response: A Flask Response object containing requested users encoded in the DataTable expected JSON format
    """

    error_list = []
    user_dao = UserDao()

    # Get the parameters from the request URL
    draw = request.args.get('draw', default=1, type=int)
    start = request.args.get('start', default=0, type=int)
    length = request.args.get('length', default=25, type=int)
    sort_index = request.args.get('order[0][column]', default=0, type=str)
    sort_by = request.args.get('columns[' + sort_index + '][name]', type=str).lower()

    # Verify the order string
    if sort_by not in user_dao.columns:
        error_list.append(f"Unable to sort on column {sort_by} as it was not found")
        order_string = user_dao.columns[0]

    # Sort in descending order when requested
    desc_flag = False
    if request.args.get('order[0][dir]', type=str) == "desc":
        desc_flag = True

    # Return the requested data in json format
    logging.info(f"Serving user data (start={start}, length={length}, sort_by={sort_by})")
    db = Db()
    count = user_dao.get_count(db)

    payload = {
        "draw": draw,
        "recordsTotal": count,
        "recordsFiltered": count
    }

    if len(error_list) == 0:
        payload["data"] = user_dao.read(db, start, length, sort_by, desc_flag)
    else:
        payload["error"] = '; '.join(error_list)

    return jsonify(payload)
