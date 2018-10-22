#!/usr/bin/env python
import os, sys
from flask_script import Manager, Server
from app import create_app
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = create_app(os.getenv('config') or 'default')
manager = Manager(app)

manager.add_command('runserver', Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=5052))

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
