from flask import Blueprint, request
from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200

def search_users(id=None, name=None, age=None, occupation=None):
    id = id if id else request.args.get('id')
    name = name if name else request.args.get('name')
    age = age if age else request.args.get('age')
    occupation = occupation if occupation else request.args.get('occupation')

    results = []
    matched_by_id = []
    matched_by_name = []
    matched_by_age = []
    matched_by_occupation = []

    if id:
        for user in USERS:
            if user['id'] == id:
                matched_by_id.append(user)
                break  # Since IDs are unique, break after finding the match

    for user in USERS:
        if name and name.lower() in user['name'].lower():
            matched_by_name.append(user)
        if occupation and occupation.lower() in user['occupation'].lower():
            matched_by_occupation.append(user)
        if age:
            try:
                age = int(age)
                if abs(user['age'] - age) <= 1:
                    matched_by_age.append(user)
            except ValueError:
                pass

    results.extend(matched_by_id)
    results.extend([user for user in matched_by_name if user not in results])
    results.extend([user for user in matched_by_age if user not in results])
    results.extend([user for user in matched_by_occupation if user not in results])

    return sorted(results, key=lambda x: (x in matched_by_id, x in matched_by_name, x in matched_by_age, x in matched_by_occupation), reverse=True)
