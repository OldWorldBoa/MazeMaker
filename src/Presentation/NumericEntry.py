from tkinter import Entry


class NumericEntry(Entry):
    def __init__(self, master, initial_value, **kw):
        validate = (master.register(NumericEntry.ensure_numeric_input), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        super().__init__(master, None, validate='key', validatecommand=validate, **kw)

        self.insert(0, initial_value)

    @staticmethod
    def ensure_numeric_input(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type,
                             widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
