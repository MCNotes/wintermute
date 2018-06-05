import sys
import gidgethub

def labels(issue):
    return {label_data["name"] for label in issue["labels"]}

def user_login(item):
    return item["user"]["login"]

def label_name(event_data):
    """Get the label name from a label-related webhook event."""
    return event_data["label"]["name"]