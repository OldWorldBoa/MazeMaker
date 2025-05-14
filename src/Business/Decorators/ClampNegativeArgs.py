import numbers


def clamp_negative_args(func):
    def wrapper_clamp_negative_args(*args, **kwargs):
        new_args = []
        for arg in args:
            if isinstance(arg, numbers.Number):
                new_args.append(max(0, arg))
            else:
                new_args.append(arg)

        return func(*new_args, **kwargs)

    return wrapper_clamp_negative_args
