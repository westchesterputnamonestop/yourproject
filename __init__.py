from flask import Flask, Blueprint
routes = Blueprint('routes', __name__)

from .index import *
from .users import *
from .jobseeker import *
from .employers  import *

if __name__ == "__main__":
    application.run(host='192.168.110.4',debug=True, port=80)
