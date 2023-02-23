'''
    Copyright (C) 2023 Imken Luo <immccn123@outlook.com>
    Licensed under GNU General Public License
    version 3 or above <https://www.gnu.org/licenses/>.
    This program is a part of Yangcong-tools. See `main.py` for more details.
'''

from random import randint
import requests, json
AUTH_TOKEN = ''

headers={
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-store",
    "client-char": "true",
    "client-type": "pc",
    "client-version": "8.15.57",
    "content-type": "application/json",
    "expires": "0",
    "omvd": "31556461274455727",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Microsoft Edge\";v=\"109\", \"Chromium\";v=\"109\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "Referer": "https://school.yangcongxueyuan.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

def login(username, password):
    global AUTH_TOKEN
    ctx = requests.post(
        url='https://school-api.yangcong345.com/public/login',
        headers=headers,
        json={
            'name': username,
            'password': password,
        }
    )
    # print(password, 'endl')
    if ctx.status_code != 200:
        return None
    else:
        AUTH_TOKEN = ctx.headers.get('authorization')
        headers['authorization'] = AUTH_TOKEN
        return AUTH_TOKEN

def get_unfinished_homework():
    if AUTH_TOKEN != '':
        ctx = requests.get(
            url='https://school-api.yangcong345.com/student/ai-homework/all/unfinish',
            headers=headers
        )
        return json.loads(ctx.content.decode('utf-8'))

def get_expired_homework():
    if AUTH_TOKEN != '':
        ctx = requests.get(
            url='https://school-api.yangcong345.com/student/ai-homework/all/expired',
            headers=headers
        )
        return json.loads(ctx.content.decode('utf-8'))


def get_topic_detail(topic_id):
    if AUTH_TOKEN != '':
        ctx = requests.get(
            url=f'https://school-api.yangcong345.com/course/topics/{topic_id}/detail-universal',
            headers=headers
        )
        return json.loads(ctx.content.decode('utf-8'))


def submit_video(topic_id, homework_id, video_id, duration):
    if AUTH_TOKEN != '':
        ctx1 = requests.put(
            url='https://school-api.yangcong345.com/student/previews/video',
            headers=headers,
            json={
                "topicId": topic_id,
                "videoId": video_id,
                "homeworkId": homework_id,
                "duration": duration + 3,
                "timepoint": duration,
                "finished": True,
                "from": "",
                "videoRecords": [1] * duration,
            }
        )
        ctx2 = requests.post(
            url='https://api-v5-0.yangcong345.com/learn/video',
            headers=headers,
            json={
                "duration": duration + 3,
                "timepoint": duration,
                "finished": True,
                "homeworkId": homework_id,
                "videoId": video_id,
                "topicId": topic_id,
                "scene": "package"
            }
        )

# TODO: Rename -> `submit_video_problem`
def submit_problem(problem_id,  homework_id, topic_id, answers):
    if AUTH_TOKEN != '':
        return requests.post(
            url='https://api-v5-0.yangcong345.com/learn/practice',
            headers=headers,
            json={
                "problemId": problem_id,
                "topicId": topic_id,
                "correct": True,
                "duration": randint(20, 50),
                "answers": answers,
                "scene": "package",
                "homeworkId": homework_id,
                "subproblems": []
            }
        )

# def get_progress(homework_id)

def get_task_problem(homework_id):
    if AUTH_TOKEN != '':
        # requests.
        # Get user id
        uid = json.loads(requests.get(
            url='https://school-api.yangcong345.com/user-auths/order/auth',
            headers=headers
        ).content.decode('utf-8'))['userId']
        detail_id = json.loads(requests.post(
            url=f'https://school-api.yangcong345.com/student/tasks/{homework_id}/task-detail',
            headers=headers,
            json={ 'userId': uid }
        ).content.decode('utf-8'))['taskDetailId']
        return json.loads(requests.get(
            url=f'https://school-api.yangcong345.com/student/task-detail/{detail_id}/problems',
            headers=headers
        ).content.decode('utf-8'))

def commit_problem_progress(group_id, is_finished: bool, problems):
    if AUTH_TOKEN != '':
        return requests.put(
            url=f'https://school-api.yangcong345.com/student/group-detail/{group_id}/problems-progress',
            headers=headers,
            json={
                'isFinished': is_finished,
                'problems': problems
            }
        )

def get_practice_problems(homework_id):
    if AUTH_TOKEN != '':
        return json.loads(requests.get(
            url=f'https://school-api.yangcong345.com/student/practices/{homework_id}',
            headers=headers,
        ).content.decode('utf-8'))['problems']

'''
`state`: 'unfinished' | 'finished'
'''
def submit_practice_problem(homework_id, problems, state):
    if AUTH_TOKEN != '':
        requests.put(
            url='https://school-api.yangcong345.com/student/practices',
            headers=headers,
            json={
                'homeworkId': homework_id,
                'problems': problems,
                'state': state,
            }
        )

# 假期特殊作业

def get_vacations():
    if AUTH_TOKEN != '':
        ctx = requests.get(
            url='https://school-api.yangcong345.com/vacation/student/homework/list',
            headers=headers,
        )
        ctx = ctx.content.decode('utf-8')
        return json.loads(ctx)['vacations']

def get_vacation_timelines(vacation_id):
    if AUTH_TOKEN != '':
        ctx = requests.get(
            url=f'https://school-api.yangcong345.com/vacation/student/homework/timeline/task/list?measuringID={vacation_id}',
            headers=headers,
        )
        ctx = ctx.content.decode('utf-8')
        return json.loads(ctx)['timeLines']


def get_vacation_video_detail(topic_id, task_id):
    if AUTH_TOKEN != '':
        ctx = requests.get(
            url=f'https://school-api.yangcong345.com/course/topics/{topic_id}/detail-video?taskID=f{task_id}',
            headers=headers
        )
        return json.loads(ctx.content.decode('utf-8'))


def submit_vacation_video(topic_id, video_id, task_id, duration):
    if AUTH_TOKEN != '':
        requests.put(
            url='https://school-api.yangcong345.com/vacation/student/homework/user-topic-video-record',
            headers=headers,
            json={
                "taskID": task_id,
                "videoID": video_id,
                "topicID": topic_id,
                "duration": duration * 1000,
                "timePoint": duration,
                "finished": True
            }
        )

def submit_vacation_practice(problem_id, topic_id, task_id, pool, is_finished: bool, answers: list):
    if AUTH_TOKEN != '':
        requests.post(
            url='https://school-api.yangcong345.com/vacation/student/homework/user-topic-problem-record',
            headers=headers,
            json={
                "taskID": task_id,
                "problemId": problem_id,
                "topicId": topic_id,
                "correct": True,
                "duration": randint(1000, 10000),
                "answers": answers,
                "pool": pool,
                "finished": is_finished
            }
        )
