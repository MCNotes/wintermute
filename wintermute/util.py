""" Set of utilitie4s to perform common actions """


def labels(issue):
    """Get the label from an issue"""
    return {label["name"] for label in issue["labels"]}


def user_login(item):
    """Extract the user login name from an item.
    This item can be anything like an issue, PR, etc"""
    return item["user"]["login"]
