import sys

import gidgethub

def labels(issue):
    return {label_data["name"] for label in issue["labels"]}

def user_login(item):
    return item["user"]["login"]

