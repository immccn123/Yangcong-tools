import time

from api import *

INTRO_S = R"""
    Yangcong-tools: A tool to Complete home work on Onion School.
    Copyright (C) 2023 Imken Luo

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    This program is a part of Yangcong-tools.
"""

print(INTRO_S)


def bug_report(msg, **kwargs):
    print("\n\n\n")
    print("Oops! 程序出现了一些问题：\n\t%s" % msg)
    print("正在准备生成日志文件和调试信息，请稍后。")
    filename = "YCT-Error-%d.json.log" % time.time_ns()
    logfile = open(filename, "w", encoding="utf-8")
    logfile.write(json.dumps(kwargs))
    logfile.close()
    print("日志文件已生成，位于当前工作目录下的 %s" % filename)
    print(
        "请前往我们的GitHub仓库提出issue: https://github.com/immccn123/Yangcong-tools/issues/new/choose 。"
    )
    exit(3)


def complete_topic(homework_id, topic):
    if topic["state"] != "unfinished":
        return

    topic_id = topic["id"]
    print("\t获取话题", topic["name"], "的详细信息...", end="")
    topic_detail = get_topic_detail(topic_id)
    print(" 完成")
    if topic["videoState"] == "unfinished":
        print("\t\t正在完成视频...", end="")
        submit_video(
            topic_id,
            homework_id,
            topic_detail["video"]["id"],
            int(topic_detail["video"]["duration"]),
        )
        print(" 完成")
    if topic["practiceState"] != "unfinished":
        return
    if topic_detail["practices"] == None:
        print("\t无习题")
        return
    problem_count = len(topic_detail["practices"])
    done_count = 0
    for pc in topic_detail["practices"]:
        problem = pc[0]
        problem_id = problem["problemId"]
        problem_type = problem["type"]
        if problem_type in ["multi_choice", "single_choice"]:
            ans = []
            for choice in problem["choices"][0]:
                if choice["correct"] == True:
                    ans.append(choice["body"])
            submit_video_problem(problem_id, homework_id, topic_id, ans)
        elif problem_type in ["multi_blank", "single_blank", "hybrid"]:
            submit_video_problem(problem_id, homework_id, topic_id, problem["blanks"])
        elif problem_type in ["exam"]:
            submit_video_problem(problem_id, homework_id, topic_id, ["我答对了", "答:"])
        else:
            bug_report(
                "未知问题类型 10001",
                break_point="complete_topic",
                problem=problem,
                topic_name=topic["name"],
                ptype=problem_type,
            )
        done_count += 1
        print(f"\t完成习题 ({done_count}/{problem_count})")


def complete_practice(homework_id, problem_list):
    for index, problem in enumerate(problem_list):
        ans = []
        problem_type = problem["type"]
        if problem_type in ["single_choice", "exam", "multi_choice"]:
            for choice in problem["choices"][0]:
                if choice["correct"] == True:
                    ans.append({"body": choice["body"], "no": 0})
        elif problem_type in ["multi_blank", "single_blank", "hybrid"]:
            for s in problem["blanks"]:
                ans.append({"body": s, "no": 0})
        else:
            bug_report(
                "未知问题类型 10001",
                break_point="complete_practice",
                problem=problem,
                ptype=problem_type,
            )
        submit_practice_problem(
            homework_id,
            [
                {
                    "problemId": problem["id"],
                    "answer": ans,
                    "duration": randint(1, 12),
                }
            ],
            "finished" if index == len(problem_list) - 1 else "unfinished",
        )


def complete_exam(group_id, problem_list):
    problem_count = len(problem_list)
    for index, problem in enumerate(problem_list):
        ans = []
        problem_type = problem["type"]
        if problem_type in ["single_choice", "exam", "multi_choice"]:
            for choice in problem["choices"][0]:
                if choice["correct"] == True:
                    ans.append({"body": choice["body"], "no": 0})
        elif problem_type in ["multi_blank", "single_blank", "hybrid"]:
            for s in problem["blanks"]:
                ans.append({"body": s, "no": 0})
        else:
            bug_report(
                "未知问题类型 10001",
                break_point="complete_exam",
                problem=problem,
                ptype=problem_type,
            )
        commit_problem_progress(
            group_id,
            index == len(problem_list) - 1,
            [
                {
                    "problemId": problem["id"],
                    "answer": ans,
                    "type": problem_type,
                    "duration": randint(1, 120),
                }
            ],
        )
        print(f"\t\t已完成 ({index + 1}/{problem_count})")


def complete_homework(hw):
    homework_id = hw["id"]
    if hw["state"] == 2:
        return
    if hw["type"] == 0:
        print("[Video] 正在完成", hw["name"], homework_id)
        topics: list = hw["topics"]
        print("\t共", len(topics), "个话题")
        for topic in topics:
            complete_topic(homework_id, topic)
            print("\t已完成", topic["name"], topic["id"])
    elif hw["type"] == 1:
        print("[Practice] 正在完成", hw["name"], homework_id)
        print("\t正在获取试题列表...", end="")
        problems = get_practice_problems(homework_id)
        print(" 共", len(problems), "题")
        complete_practice(homework_id, problems)
    elif hw["type"] == 3:
        print("[Exam] 正在完成", hw["name"], homework_id)
        print("\t正在获取试题列表...", end="")
        ctx = get_task_problem(homework_id)
        problems = ctx["problems"]
        group_id = ctx["groupDetailId"]
        print(" 共", len(problems), "题")
        complete_exam(group_id, problems)
    print("已完成", hw["name"], homework_id)


def complete_vacation_task_video(t, tl):
    topic = get_vacation_video_detail(t["topicId"], t["id"])
    if t["videoState"] == 0:
        print("\t正在完成视频...", end="")
        submit_vacation_video(
            topic["id"],
            topic["video"]["id"],
            t["id"],
            int(topic["video"]["duration"]) + 1,
        )
        print(" 完成")
    if t["problemState"] != 0:
        return
    ans = []
    practices_count = len(topic["practices"])
    for index, problem in enumerate(topic["practices"]):
        problem = problem[0]
        if problem["type"] in ["single_choice", "exam", "multi_choice"]:
            for choice in problem["choices"][0]:
                if choice["correct"] == True:
                    ans.append(choice["body"])
        elif problem["type"] in ["multi_blank", "single_blank", "hybrid"]:
            ans = problem["blanks"]
        else:
            bug_report(
                "未知问题类型 10001",
                timeline_name=tl["name"],
                break_point="complete_vacation",
                problem=problem,
                ptype=problem["type"],
            )
        submit_vacation_practice(
            problem["problemId"],
            topic["id"],
            t["id"],
            problem["pool"],
            index == len(topic["practices"]) - 1,
            ans,
        )
        print(f"\t完成练习 ({index + 1}/{practices_count})")


def complete_vacation_task_stage(t, vc, subject_id, stage_id):
    problems = get_vacation_stage_problem(
        t["id"],
        stage_id,
        subject_id,
        vc["id"],
    )
    problem_details = []
    for index, problem in enumerate(problems):
        problem_type = problem["type"]
        ans = []
        if problem_type in ["single_choice", "exam", "multi_choice"]:
            for choice in problem["choices"][0]:
                if choice["correct"] == True:
                    ans.append(choice["body"])
        elif problem_type in ["multi_blank", "single_blank", "hybrid"]:
            for s in problem["blanks"]:
                ans.append(s)
        else:
            bug_report(
                "未知问题类型 10001",
                break_point="vacation",
                problem=problem,
                ptype=problem_type,
            )
        problem_details.append(
            submit_vacation_stage_problem(
                task_id=t["id"],
                stage_id=stage_id,
                subject_id=subject_id,
                homework_id=vc["id"],
                problem_id=problem["id"],
                problem_type=problem_type,
                answer=ans,
                is_complete=(index == len(problems) - 1),
            )
        )
        if index == len(problems) - 1:
            finalsubmit_vacation_stage_problem(t["id"], problem_details)


def complete_vacation(vc):
    print("正在完成", vc["name"])
    vacation = get_vacation_details(vc["id"])
    timelines = vacation["timeLines"]
    stage_id = vacation["stageId"]
    subject_id = vacation["subjectId"]
    print("\t共", len(timelines), "个时间节点")
    for tl in timelines:
        if not (tl["state"] == 0 and tl["unlock"]):
            continue
        if len(tl["tasks"]) == 0:
            continue
        print("\t节点", tl["name"], "已解锁但未完成")
        tasks = tl["tasks"]
        for t in tasks:
            if t["type"] == 1:
                complete_vacation_task_video(t, tl)
            elif t["type"] == 2:
                complete_vacation_task_stage(
                    t, vc, subject_id=subject_id, stage_id=stage_id
                )


def run():
    unfinished_homework = get_unfinished_homework()
    expired_homework = get_expired_homework()
    homework: list = (
        unfinished_homework["homeworkList"] + expired_homework["homeworkList"]
    )
    vacations = get_vacations()
    print("共", len(homework), "个作业")
    for homework in homework:
        complete_homework(homework)
    print("共", len(vacations), "个假期课程")
    for vacation in vacations:
        complete_vacation(vacation)


if __name__ == "__main__":
    userinfo = []
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            userinfo = json.load(f)
        for user in userinfo:
            if login(user["username"], user["password"]) is not None:
                print("[Multi User] 正在处理用户", user["username"])
                run()
            else:
                print("Warning:", user["username"], "的账号或密码错误！")
    except FileNotFoundError:
        un = input("用户名/手机号：")
        pw = input("密码：")
        login(un, pw)
        run()
    except json.decoder.JSONDecodeError as E:
        print(E)
        print("多用户配置文件格式有误。")
