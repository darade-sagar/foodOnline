from django.core.exceptions import PermissionDenied

# Restrict the customer from accessing vendor page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the vender from accessing customer page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied