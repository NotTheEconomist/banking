context = None

def get_context():
    if context:
        return context
    else:
        raise RuntimeError("No initialized context!")

def make_context():
    class __Context(object):
        '''a singleton FSM for banking app'''
        def __init__(self):
            self.user = None
            self.db = None
            self.quitting = False

    global context
    if context is None:
        context = __Context()  # singleton
    else:
        pass
