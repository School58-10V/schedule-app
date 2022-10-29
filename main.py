import controllers
import frontend
import mimetypes
from schedule_app import app

app.run(debug=True)

mimetypes.add_type('application/javascript', ".js")
mimetypes.add_type('text/css', '.css')
