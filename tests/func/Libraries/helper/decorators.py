import inspect


def checkargs(function):
    def _f(*arguments):
        for index, argument in enumerate(inspect.getfullargspec(function)[0]):
            if not isinstance(arguments[index],
                              function.__annotations__[argument]):
                raise TypeError("{} is not of type {}"
                                .format(arguments[index],
                                        function.__annotations__[argument]))
        return function(*arguments)

    _f.__doc__ = function.__doc__
    return _f


def coerceargs(function):
    def _f(*arguments):
        new_arguments = []
        for index, argument in enumerate(inspect.getfullargspec(function)[0]):
            new_arguments.append(
                function.__annotations__[argument](arguments[index]))
        return function(*new_arguments)

    _f.__doc__ = function.__doc__
    return _f
