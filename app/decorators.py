from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def funcionario_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_funcionario:
            return function(request, *args, **kwargs)
        raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap