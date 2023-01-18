# import requests
from api import *

import os

INTRO_S = R'''
----------------------------------------------------------------------------------------
 __  __   ______   ___   ___             _________  ______   ______   __
/_/\/_/\ /_____/\ /__/\ /__/\           /________/\/_____/\ /_____/\ /_/\
\ \ \ \ \\:::__\/ \::\ \\  \ \   _______\__.::.__\/\:::_ \ \\:::_ \ \\:\ \
 \:\_\ \ \\:\ \  __\::\/_\ .\ \ /______/\  \::\ \   \:\ \ \ \\:\ \ \ \\:\ \
  \::::_\/ \:\ \/_/\\:: ___::\ \\__::::\/   \::\ \   \:\ \ \ \\:\ \ \ \\:\ \____
    \::\ \  \:\_\ \ \\: \ \\::\ \            \::\ \   \:\_\ \ \\:\_\ \ \\:\/___/\
     \__\/   \_____\/ \__\/ \::\/             \__\/    \_____\/ \_____\/ \_____\/
      Licensed under GPLv3.
      If the project violates your rights,
      please contact immccn123 (at) outlook.com for removal.
      https://github.com/immccn123/Yangcong-tools
----------------------------------------------------------------------------------------
'''

print(INTRO_S)

def run(username: str, password: str):
    login(username, password)
    homework = get_unfinish_homework()
    exp_hm = get_expired_homework()
    homework: list = homework['homeworkList'] + exp_hm['homeworkList']
    print('已获取到', homework.__len__(), '个作业')
    for hw in homework:
        hwid = hw['id']
        if hw['state'] != 2:
            print('undone')
            if hw['type'] == 0:
                print('[Video] 正在完成', hw['name'], hw['id'])
                topics: list = hw['topics']
                print('\t检测到', len(topics), '个 Topic')
                for topic in topics:
                    tpid = topic['id']
                    print('\t正在完成', topic['name'], topic['id'])
                    print('\t话题完成情况: ', topic['state'])
                    if topic['state'] == 'unfinished':
                        # 检测视频完成情况
                        print('\t视频完成情况: ', topic['videoState'])
                        topic_detail = get_detail(tpid)
                        if topic['videoState'] == 'unfinished':
                            print('\t\t正在完成视频')
                            submit_video(tpid, hwid, topic_detail['video']['id'], int(topic_detail['video']['duration']))
                            print('\t\tDone.')
                        print('\t练习完成情况: ', topic['practiceState'])
                        if topic['practiceState'] == 'unfinished':
                            print('\t\t正在完成练习')
                            # print(topic_detail)
                            if topic_detail['practices'] != None:
                                print('\t\t检测到', len(topic_detail['practices']), '个习题')
                                for pc in topic_detail['practices']:
                                    p = pc[0]
                                    # print(p)
                                    # 判断类型
                                    if p['type'] == 'single_choice':
                                        print('\t\tSingle choice')
                                        # print(p['choices'])
                                        for choice in p['choices'][0]:
                                            if choice['correct'] == 'true' or choice['correct'] == True:
                                                # Submit
                                                submit_problem(p['problemId'], hwid, tpid, [choice['body']])
                                                print('\t\tSubmitted.')
                                                break
                                    elif p['type'] == 'multi_choice':
                                        print('\t\tMulti Choices')
                                        ans = []
                                        for choice in p['choices'][0]:
                                            if choice['correct'] == True:
                                                ans.append(choice['body'])
                                        submit_problem(p['problemId'], hwid, tpid, ans)
                                        print('\n\nSubmitted.')
                                    elif p['type'] == 'multi_blank':
                                        print('\t\tMulti blank')
                                        # print(p['extendedBlanks'])
                                        submit_problem(p['problemId'], hwid, tpid, p['blanks'])
                                        print('\t\tSubmitted.')
                                    elif p['type'] == 'hybrid':
                                        print('\t\tHybrid Problem')
                                        submit_problem(p['problemId'], hwid, tpid, p['blanks'])
                                    else:
                                        print('=' * 10)
                                        print('检测到不支持的题目类型；请将下列内容拷贝发送至 immccn123@outlook.com。邮件主题中需要包含“YC BUG”')
                                        print(p)
                                        print('=' * 10)
                                        raise NameError()
                            else:
                                print('\t\t无习题。')
                    print('\t已完成', topic['name'], topic['id'])
            elif hw['type'] == 3:
                print('[Exam] 正在完成', hw['name'], hw['id'])
                print('\t正在获取试题列表')
                ctx = get_task_problem(hwid)
                problems = ctx['problems']
                grid = ctx['groupDetailId']
                print('\t获取到', len(problems), '个试题')
                for pi in range(len(problems)):
                    p = problems[pi]
                    ans = []
                    if p['type'] == 'single_choice':
                        print('\t\tSingle choice')
                        # print(p['choices'])
                        for choice in p['choices'][0]:
                            if choice['correct'] == 'true' or choice['correct'] == True:
                                # Submit
                                ans.append({'body': choice['body'], 'no': 0})
                                break
                    elif p['type'] == 'multi_choice':
                        print('\t\tMulti Choices')
                        ans = []
                        for choice in p['choices'][0]:
                            if choice['correct'] == True:
                                ans.append({'body': choice['body'], 'no': 0})
                    elif p['type'] == 'multi_blank' or p['type'] == 'hybrid':
                        print('\t\tMulti blank')
                        # print(p['extendedBlanks'])
                        for s in p['blanks']:
                            ans.append({'body': s, 'no': 0})
                    # elif p['type'] == 'hybrid':
                    #     print('\t\tHybrid Problem')
                    #     submit_problem(p['problemId'], hwid, tpid, p['blanks'])
                    else:
                        print('=' * 10)
                        print('检测到不支持的题目类型；请将下列内容拷贝发送至 immccn123@outlook.com。邮件主题中需要包含“YC BUG”')
                        print(p)
                        print('=' * 10)
                        raise NameError()
                    commit_problem_progress(grid, pi == (len(problems) - 1), [{
                        'problemId': p['id'],
                        'answer': ans,
                        'type': p['type'],
                        'duration': randint(1, 120),
                    }])
                    print('\t\tSubmitted', p['id'])
        print('已完成', hw['name'], hwid)

if os.path.exists('username') and os.path.exists('password'):
    usernameFile = open('username', 'r')
    passwordFile = open('password', 'r')
    while True:
        un = usernameFile.readline()[:-1]
        pw = passwordFile.readline()[:-1]
        if (not un) and (not pw):
            break
        print('[Multi User] 正在执行用户', un)
        run(un, pw)
else:
    un = input('用户名/手机号：')
    pw = input('密码：')
    run(un, pw)
