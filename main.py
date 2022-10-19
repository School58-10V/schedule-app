import controllers
import web
from schedule_app import app

import mimetypes

mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

app.run(debug=True)
