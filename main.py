# import requests
from api import *

INTRO_S = R'''
----------------------------------------------------------------------------------------
 __  __   ______   ___   ___             _________  ______   ______   __
/_/\/_/\ /_____/\ /__/\ /__/\           /________/\/_____/\ /_____/\ /_/\
\ \ \ \ \\:::__\/ \::\ \\  \ \   _______\__.::.__\/\:::_ \ \\:::_ \ \\:\ \
 \:\_\ \ \\:\ \  __\::\/_\ .\ \ /______/\  \::\ \   \:\ \ \ \\:\ \ \ \\:\ \
  \::::_\/ \:\ \/_/\\:: ___::\ \\__::::\/   \::\ \   \:\ \ \ \\:\ \ \ \\:\ \____
    \::\ \  \:\_\ \ \\: \ \\::\ \            \::\ \   \:\_\ \ \\:\_\ \ \\:\/___/\
     \__\/   \_____\/ \__\/ \::\/             \__\/    \_____\/ \_____\/ \_____\/  s
      Licensed under GPLv3.
      If the project violates your rights,
      please contact immccn123 (at) outlook.com for removal.
      https://github.com/immccn123/Yangcong-tools
----------------------------------------------------------------------------------------
'''

print(INTRO_S)

def bug_report_ukp(msg):
    print('\n\n\n')
    print('Error with code 10001')
    print('检测到不支持的题目类型；请将下列内容拷贝发送至 immccn123（at）outlook.com，\n或者前往我们的GitHub仓库提出issue: https://github.com/immccn123/Yangcong-tools/issues/new/choose')
    print('务必将下列内容拷贝并粘贴在issue里。')
    print('---------- BEGIN ----------')
    print(msg)
    print('----------- END -----------')
    exit(3)

def complete_topic(hwid, topic):
    tpid = topic['id']
    print('\t正在完成', topic['name'], topic['id'])
    print('\t话题完成情况: ', topic['state'])
    if topic['state'] == 'unfinished':
        # 检测视频完成情况
        print('\t视频完成情况: ', topic['videoState'])
        topic_detail = get_topic_detail(tpid)
        if topic['videoState'] == 'unfinished':
            print('\t\t正在完成视频')
            submit_video(tpid, hwid, topic_detail['video']['id'], int(topic_detail['video']['duration']))
            print('\t\tDone.')
        print('\t练习完成情况: ', topic['practiceState'])
        if topic['practiceState'] == 'unfinished':
            print('\t\t正在完成练习')
            if topic_detail['practices'] != None:
                print('\t\t检测到', len(topic_detail['practices']), '个习题')
                for pc in topic_detail['practices']:
                    p = pc[0]
                    # 判断类型
                    if p['type'] == 'single_choice':
                        print('\t\tSingle choice')
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
                    elif p['type'] == 'multi_blank' or p['type'] == 'single_blank':
                        print('\t\tMulti blank')
                        submit_problem(p['problemId'], hwid, tpid, p['blanks'])
                        print('\t\tSubmitted.')
                    elif p['type'] == 'hybrid':
                        print('\t\tHybrid Problem')
                        submit_problem(p['problemId'], hwid, tpid, p['blanks'])
                    else:
                        bug_report_ukp(p)
            else:
                print('\t\t无习题。')


def complete_practice(hwid, probs):
    for pi in range(len(probs)):
        p = probs[pi]
        ans = []
        if p['type'] == 'single_choice' or p['type'] == 'exam':
            print('\t\tSingle choice')
            for choice in p['choices'][0]:
                if choice['correct'] == True:
                    ans.append({'body': choice['body'], 'no': 0})
                    break
        elif p['type'] == 'multi_choice':
            print('\t\tMulti Choices')
            ans = []
            for choice in p['choices'][0]:
                if choice['correct'] == True:
                    ans.append({'body': choice['body'], 'no': 0})
        elif p['type'] == 'multi_blank' or p['type'] == 'single_blank' or p['type'] == 'hybrid':
            print('\t\tMulti blank')
            for s in p['blanks']:
                ans.append({'body': s, 'no': 0})
        else:
            bug_report_ukp(p)
        if pi == len(probs) - 1:
            submit_practice_problem(hwid, [{
                'problemId': p['id'],
                'answer': ans,
                'duration': randint(1, 12),
            }], 'finished')
        else:
            submit_practice_problem(hwid, [{
                'problemId': p['id'],
                'answer': ans,
                'duration': randint(1, 12),
            }], 'unfinished')


def complete_exam(grid, problems):
    for pi in range(len(problems)):
        p = problems[pi]
        ans = []
        print('\t\t', p['type'])
        if p['type'] in ['single_choice', 'exam', 'multi_choice']:
            for choice in p['choices'][0]:
                if choice['correct'] == True:
                    # Submit
                    ans.append({'body': choice['body'], 'no': 0})
        elif p['type'] in ['multi_blank', 'single_blank', 'hybrid']:
            for s in p['blanks']:
                ans.append({'body': s, 'no': 0})
        else:
            bug_report_ukp(p)
        commit_problem_progress(grid, pi == (len(problems) - 1), [{
            'problemId': p['id'],
            'answer': ans,
            'type': p['type'],
            'duration': randint(1, 120),
        }])
        print('\t\tSubmitted', p['id'])


def complete_homework(hw):
    hwid = hw['id']
    if hw['state'] != 2:
        if hw['type'] == 0:
            print('[Video] 正在完成', hw['name'], hw['id'])
            topics: list = hw['topics']
            print('\t检测到', len(topics), '个 Topic')
            for topic in topics:
                complete_topic(hwid, topic)
                print('\t已完成', topic['name'], topic['id'])
        elif hw['type'] == 1:
            print('[Practice] 正在完成', hw['name'], hw['id'])
            print('\t正在获取试题列表')
            probs = get_practice_problems(hwid)
            print('\t获取到', len(probs), '个试题')
            complete_practice(hwid, probs)
        elif hw['type'] == 3:
            print('[Exam] 正在完成', hw['name'], hw['id'])
            print('\t正在获取试题列表')
            ctx = get_task_problem(hwid)
            problems = ctx['problems']
            grid = ctx['groupDetailId']
            print('\t获取到', len(problems), '个试题')
            complete_exam(grid, problems)
    print('已完成', hw['name'], hwid)


def complete_vacation(vc):
    print('正在完成', vc['name'])
    timelines = get_vacation_timelines(vc['id'])
    print('\t已获取到', len(timelines), '个时间节点')
    for tl in timelines:
        if tl['state'] == 0 and tl['unlock']:
            print('\t节点', tl['name'], '已解锁但未完成')
            tasks = tl['tasks']
            for t in tasks:
                # print(t)
                if t['type'] == 1:
                    topic = get_vacation_video_detail(t['topicId'], t['id'])
                    if t['videoState'] == 0:
                        submit_vacation_video(
                            topic['id'],
                            topic['video']['id'],
                            t['id'],
                            int(topic['video']['duration']) + 1,
                        )
                        print('\t\t已完成视频')
                    if t['problemState'] == 0:
                        ans = []
                        for pi in range(len(topic['practices'])):
                            p = topic['practices'][pi][0]
                            print('\t\t', p['type'])
                            if p['type'] in ['single_choice', 'exam', 'multi_choice']:
                                for choice in p['choices'][0]:
                                    if choice['correct'] == True:
                                        ans.append(choice['body'])
                            elif p['type'] in ['multi_blank', 'single_blank', 'hybrid']:
                                ans = p['blanks']
                            else:
                                bug_report_ukp(p)
                            # print(p)
                            submit_vacation_practice(
                                p['problemId'],
                                topic['id'],
                                t['id'],
                                p['pool'],
                                pi == len(topic['practices']) - 1,
                                ans
                            )


def run():
    homework = get_unfinished_homework()
    exp_hm = get_expired_homework()
    homework: list = homework['homeworkList'] + exp_hm['homeworkList']
    print('已获取到', homework.__len__(), '个作业')
    for hw in homework:
        complete_homework(hw)
    # return
    print('下列功能正在调试中！！！不保证可用性！！！')
    input('按下回车继续')
    vacations = get_vacations()
    print('检测到', len(vacations), '个假期课程')
    for vc in vacations:
        complete_vacation(vc)



if __name__ == '__main__':
    userinfo = []
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            userinfo = json.load(f)
        for user in userinfo:
            if login(user['username'], user['password']) is not None:
                print('[Multi User] 正在处理用户', user['username'])
                run()
            else:
                print('Error:', user['username'], '的账号或密码错误！')
                if input('是否继续？[y/N]') not in ['Y', 'y']:
                    print('Aborted.')
                    exit(3)
    except FileNotFoundError:
        un = input('用户名/手机号：')
        pw = input('密码：')
        login(un, pw)
        run()
    except (json.decoder.JSONDecodeError) as E:
        print(E)
        print('多用户配置文件格式有误。')
