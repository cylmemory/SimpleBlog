#!/usr/bin/env python

import os
from flask_script import Manager, Server
from . import create_app


app = create_app(os.getenv('config') or 'default')
manager = Manager(app)

manager.add_command('runserver', Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=5000))

if __name__ == "__main__":
    manager.run()
