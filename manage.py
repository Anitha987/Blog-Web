from app import create_app,db
from app.models import User,Pitch,Category,Comment,Vote
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager,Server

# app = create_app('production')
# app = create_app('test')
app = create_app('development')
migrate=Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)
manager.add_command('server',Server)
@manager.command
def test():
    '''
    run the unit tests.
    '''
    import unittest
    tests= unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run('tests')
@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User,Pitch = Pitch,Comment = Comment,Vote = Vote )
if __name__ == '__main__':
    manager.run()