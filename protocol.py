import json


def msg_send_scores(id: int, date: str, time: str, motion: int, sound: int) -> str:
    message ={
        "request": "send_scores",
        "id": id,
        "date": date,
        "time": time,
        "motion_score": motion,
        "sound_score": sound
    }

    return json.dumps(message)
