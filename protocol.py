def send_scores(id: int, time: str, motion: int, sound: int) -> str:
    return f"send_scores: {id} {time} {motion} {sound}"


def request_name(id: int) -> str:
    return f"request_name: {id}"


def request_average_scores(id: int) -> str:
    return f"request_average_scores: {id}"
