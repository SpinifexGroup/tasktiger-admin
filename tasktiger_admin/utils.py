import click
import redis
from flask import Flask
from flask_admin import Admin
from tasktiger import TaskTiger
from tasktiger_admin import TaskTigerView


@click.command()
@click.option('-h', '--host', help='Redis server hostname')
@click.option('-p', '--port', help='Redis server port')
@click.option('-a', '--password', help='Redis password')
@click.option('-n', '--db', help='Redis database number')
@click.option('-l', '--listen', help='Admin port to listen on')
@click.option('-i', '--interface', help='Admin interface to listen on',
              default='127.0.0.1')
def run_admin(host, port, db, password, listen, interface):
    conn = redis.Redis(
        host, int(port or 6379), int(db or 0), password, decode_responses=True
    )
    tiger = TaskTiger(setup_structlog=True, connection=conn)
    app = Flask(__name__)
    admin = Admin(app, url='/')
    admin.add_view(
        TaskTigerView(tiger, name='TaskTiger', endpoint='tasktiger', integration_config={})
    )
    app.run(debug=True, port=int(listen or 5000), host=interface)
