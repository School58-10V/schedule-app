from __future__ import annotations
from typing import TYPE_CHECKING

from flask import jsonify, g

from schedule_app import app

if TYPE_CHECKING:
    from flask import Response


@app.route('/api/v1/profile', methods=['GET'])
def profile() -> Response:
    user = g.user

    user_information = user.get_profile_information()

    return jsonify(user_information), 200
