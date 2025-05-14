import numbers

def ClampNegativeArgs(func):
	def wrapperClampNegativeArgs(*args, **kwargs):
		newargs = []
		for arg in args:
			if isinstance(arg, numbers.Number):
				newargs.append(max(0, arg))
			else:
				newargs.append(arg)

		return func(*newargs, **kwargs)

	return wrapperClampNegativeArgs