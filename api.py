"""
    Copyright (C) 2023 Imken Luo <me@imken.moe>
    Licensed under GNU General Public License
    version 3 or above <https://www.gnu.org/licenses/>.
    This program is a part of Yangcong-tools. See `main.py` for more details.
"""

import json
from random import randint

import requests

AUTH_TOKEN = ""

headers = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-store",
    "client-char": "true",
    "client-type": "pc",
    "client-version": "8.16.04",
    "content-type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200",
    "expires": "0",
    "omvd": "yangcong345aTZ5ZmFpYTBwaQ==",
    "pragma": "no-cache",
    "sec-ch-ua": '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "Referer": "https://school.yangcongxueyuan.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}

session = requests.session()


def login(username, password):
    global AUTH_TOKEN
    ctx = session.post(
        "https://school-api.yangcong345.com/public/login",
        headers=headers,
        json={
            "name": username,
            "password": password,
        },
    )
    if ctx.status_code != 200:
        return None
    AUTH_TOKEN = ctx.headers.get("authorization")
    headers["authorization"] = AUTH_TOKEN
    session.headers = headers
    return AUTH_TOKEN


def get_unfinished_homework():
    if AUTH_TOKEN == "":
        return
    ctx = session.get(
        "https://school-api.yangcong345.com/student/ai-homework/all/unfinish",
    )
    return json.loads(ctx.content.decode("utf-8"))


def get_expired_homework():
    if AUTH_TOKEN == "":
        return
    ctx = session.get(
        "https://school-api.yangcong345.com/student/ai-homework/all/expired",
    )
    return json.loads(ctx.content.decode("utf-8"))


def get_topic_detail(topic_id):
    if AUTH_TOKEN == "":
        return
    ctx = session.get(
        f"https://school-api.yangcong345.com/course/topics/{topic_id}/detail-universal",
    )
    return json.loads(ctx.content.decode("utf-8"))


def submit_video(topic_id, homework_id, video_id, duration):
    if AUTH_TOKEN == "":
        return
    session.put(
        "https://school-api.yangcong345.com/student/previews/video",
        json={
            "topicId": topic_id,
            "videoId": video_id,
            "homeworkId": homework_id,
            "duration": duration + 3,
            "timepoint": duration,
            "finished": True,
            "from": "",
            "videoRecords": [1] * duration,
        },
    )
    session.post(
        "https://api-v5-0.yangcong345.com/learn/video",
        json={
            "duration": duration + 3,
            "timepoint": duration,
            "finished": True,
            "homeworkId": homework_id,
            "videoId": video_id,
            "topicId": topic_id,
            "scene": "package",
        },
    )


def submit_video_problem(problem_id, homework_id, topic_id, answers):
    if AUTH_TOKEN == "":
        return
    return session.post(
        "https://api-v5-0.yangcong345.com/learn/practice",
        json={
            "problemId": problem_id,
            "topicId": topic_id,
            "correct": True,
            "duration": randint(20, 50),
            "answers": answers,
            "scene": "package",
            "homeworkId": homework_id,
            "subproblems": [],
        },
    )


def get_task_problem(homework_id):
    if AUTH_TOKEN == "":
        return
    uid = json.loads(
        session.get(
            "https://school-api.yangcong345.com/user-auths/order/auth",
        ).content.decode("utf-8")
    )["userId"]
    detail_id = json.loads(
        session.post(
            f"https://school-api.yangcong345.com/student/tasks/{homework_id}/task-detail",
            json={"userId": uid},
        ).content.decode("utf-8")
    )["taskDetailId"]
    return json.loads(
        session.get(
            f"https://school-api.yangcong345.com/student/task-detail/{detail_id}/problems",
        ).content.decode("utf-8")
    )


def commit_problem_progress(group_id, is_finished: bool, problems):
    if AUTH_TOKEN == "":
        return
    return session.put(
        f"https://school-api.yangcong345.com/student/group-detail/{group_id}/problems-progress",
        json={"isFinished": is_finished, "problems": problems},
    )


def get_practice_problems(homework_id):
    if AUTH_TOKEN == "":
        return
    return json.loads(
        session.get(
            f"https://school-api.yangcong345.com/student/practices/{homework_id}",
        ).content.decode("utf-8")
    )["problems"]


"""
`state`: 'unfinished' | 'finished'
"""


def submit_practice_problem(homework_id, problems, state):
    if AUTH_TOKEN == "":
        return
    session.put(
        "https://school-api.yangcong345.com/student/practices",
        json={
            "homeworkId": homework_id,
            "problems": problems,
            "state": state,
        },
    )


def get_vacations():
    if AUTH_TOKEN == "":
        return
    ctx = session.get(
        "https://school-api.yangcong345.com/vacation/student/homework/list",
    )
    ctx = ctx.content.decode("utf-8")
    return json.loads(ctx)["vacations"]


def get_vacation_details(vacation_id):
    if AUTH_TOKEN == "":
        return
    ctx = session.get(
        "https://school-api.yangcong345.com/vacation/student/homework/timeline/task/list"
        + f"?measuringID={vacation_id}",
    )
    ctx = ctx.content.decode("utf-8")
    return json.loads(ctx)


def get_vacation_video_detail(topic_id, task_id):
    if AUTH_TOKEN == "":
        return
    ctx = session.get(
        f"https://school-api.yangcong345.com/course/topics/{topic_id}/detail-video"
        + f"?taskID=f{task_id}"
    )
    return json.loads(ctx.content.decode("utf-8"))


def submit_vacation_video(topic_id, video_id, task_id, duration):
    if AUTH_TOKEN == "":
        return
    session.put(
        "https://school-api.yangcong345.com/vacation/student/homework/user-topic-video-record",
        json={
            "taskID": task_id,
            "videoID": video_id,
            "topicID": topic_id,
            "duration": duration * 1000,
            "timePoint": duration,
            "finished": True,
        },
    )


def submit_vacation_practice(
    problem_id, topic_id, task_id, pool, is_finished: bool, answers: list
):
    if AUTH_TOKEN == "":
        return
    session.post(
        "https://school-api.yangcong345.com/vacation/student/homework/user-topic-problem-record",
        json={
            "taskID": task_id,
            "problemId": problem_id,
            "topicId": topic_id,
            "correct": True,
            "duration": randint(1000, 10000),
            "answers": answers,
            "pool": pool,
            "finished": is_finished,
        },
    )


def get_vacation_stage_problem(task_id, stage_id, subject_id, homework_id):
    if AUTH_TOKEN == "":
        return
    return json.loads(
        session.get(
            "https://school-api.yangcong345.com/vacation/student/homework/stage-practise"
            + f"?taskID={task_id}&stageId={stage_id}&subjectId={subject_id}&homeworkId={homework_id}"
        ).content.decode("utf-8")
    )["problems"]


def submit_vacation_stage_problem(
    task_id,
    stage_id,
    subject_id,
    homework_id,
    answer,
    problem_id,
    problem_type,
    is_complete,
):
    if AUTH_TOKEN == "":
        return
    session.post(
        "https://school-api.yangcong345.com/vacation/student/homework/user-stage-problem-record",
        json={
            "taskID": str(task_id),
            "stageId": str(stage_id),
            "subjectId": str(subject_id),
            "homeworkId": str(homework_id),
            "problemId": problem_id,
            "problemType": problem_type,
            "answers": answer,
            "correct": True,
            "partCorrect": False,
            "isComplete": is_complete,
            "score": 0,
            "duration": randint(114514, 1919810),
        },
    )
    return {
        "problemId": problem_id,
        "problemType": problem_type,
        "answers": answer,
        "correct": True,
        "partCorrect": False,
        "isComplete": is_complete,
        "score": 0,
        "duration": randint(114514, 1919810),
    }


def finalsubmit_vacation_stage_problem(task_id, problem_records):
    if AUTH_TOKEN == "":
        return
    session.post(
        "https://school-api.yangcong345.com/vacation/student/homework/user-stage-problem-record",
        json={
            "taskID": task_id,
            "finished": True,
            "stageProblemRecords": problem_records,
        },
    )
