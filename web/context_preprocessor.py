from schedule_app import app


@app.context_processor
def inject_stage_and_region():
    return {
        'user': 'clown',
        }
