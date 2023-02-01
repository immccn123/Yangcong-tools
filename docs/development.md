# 开发文档

首先，您应该已经知晓，仓库作者 immccn123 的代码风格和英文拼写跟依托答辩一样。

## 基础方法

本节不包括完成作业的相关内容。

### 登录
`login(username, password)`

必须要先登录，才能进行接下来的操作，例如获取作业、完成作业。~~（废话~~

### 获取作业

有两个方法。
`get_unfinished_homework()` & `get_expired_homework()`

返回以下对象：
```json
{
    "homeworkList": [
        {
            "id": "<homework_id>",
            "name": "几何中的动点问题",
            "stageId": 2,
            "subjectId": 1,
            "publisherId": -1,
            "semesterId": -1,
            "judgmentMethod": "student",
            "createdTime": "[Private]T[Private]Z",
            "expiredTime": "[Private]T[Private]Z",
            "leaveMessage": "",
            "creator": "[Private]",
            "specialCourseId": "[Private]",
            "startTime": "[Private]T[Private]Z",
            "source": "",
            "state": -1,
            "showWarnExpiredTime": true,
            "roomStudentTotal": 48,
            "finishedStudentTotal": 12,
            "itemCount": 3,
            "finishedItemCount": 0,
            "accuracy": 0,
            "type": 0,
            "topics": [
                {
                    "id": "<topic_id>",
                    "_id": "",
                    "name": "动点与面积问题",
                    "pay": true,
                    "isFreeTime": false,
                    "state": "unfinished",
                    "videoState": "unfinished",
                    "practiceState": "unfinished",
                    "topicOrder": 1
                }
            ],
            "subsections": []
        }
    ]
}
```

## 作业完成流程说明

### 视频作业 (Type 0)

一个基本的作业长这样：
```
Homework
  |- Topic A
    |- Video A (只有一个)
      |- Practice Problem A-1
      |- Practice Problem A-2
      |- Practice Problem A-3
  |- Topic B
    |- ...
```

完成作业的基本流程是：
1. 获取作业id（即`homework_id`，在获取未完成作业时获取到作业id）
2. 得到作业的详细信息。遍历`topic`。
    1. 通过`topic_id`获取`topic`的相关信息（`get_detail(topic_id)`），其中包含了视频的基本信息以及课后试题（含答案）。会保存视频时长。
    2. 伪造客户端的信息（纯明文），向服务器发送观看的视频市场，即原视频时长。提交视频完成信息。
    3. 遍历试题。判断类型并对于每个试题分别向服务器提交完成信息（`submit_problem(problem_id,  homework_id, topic_id, answers)`）。正确性是服务端+客户端双重检验。
3. 完成作业。

### 课后习题/练习任务 (Type 1)
作业完成流程：
1. 获得作业id
2. 通过作业id获取试题列表（含答案，`get_practice_problems(homework_id)`）。
3. 对于每一个试题，判断类型并逐个上传完成情况（`submit_practice_problem(homework_id, problems, state)`）。

### [Unknown] (Type 2)

### 精测作业 (Type 3)
TODO: 将代码里的task改为exam。

作业完成流程：
1. 获得作业id
2. 通过作业id获取试题列表（含答案，`get_task_problem(homework_id)`）。
3. 对于每一个试题，判断类型并逐个上传完成情况（`commit_problem_progress(group_id, is_finished: bool, problems)`）。

## 试题题型

### 单选题 `single_choice`

答案位于选项内`choices`。例如：
```json
{
    "choices": [[
        {
            "body": "$选A$",
            "correct": true
        },
        {
            "body": "$不选B$",
            "correct": false
        }
    ]] // 注意这是二维数组
}
```

### 多选题 `multi_choice`

```json
{
    "choices": [[
        {
            "body": "$选A$",
            "correct": true
        },
        {
            "body": "$也选B$",
            "correct": true
        }
    ]] // 注意这是二维数组
}
```

### 填空题 `multi_blank`
```json
{
    "blanks": ["第一个空"]
}
```

### 杂交大题（？） `hybrid`

无论里面有没有选择，都可以直接提交`blanks`。
```json
{
    "blanks": [
        "第一个空",
        "第二个空，但是单选",
        "$LaTeX yyds$"
    ]
}
```
