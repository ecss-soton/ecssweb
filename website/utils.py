def is_committee(user):
    return user.groups.filter(name='committee').exists()