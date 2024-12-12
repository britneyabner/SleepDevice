import json


def msg_send_scores(id: int, date: str, time: str, motion: int, sound: int) -> str:
    message = {
        "request": "send_scores",
        "id": id,
        "date": date,
        "time": time,
        "motion_score": motion,
        "sound_score": sound
    }

    return json.dumps(message)


def msg_request_scores_on_date(id: int, date: str):
    message = {
        "request": "request_scores_on_date",
        "id": id,
        "date": date
    }

    return json.dumps(message)


def msg_send_scores_on_date(motion: int, sound: int):
    message = {
        "request": "send_scores_on_date",
        "motion_score": motion,
        "sound_score": sound
    }
    
    return json.dumps(message)
