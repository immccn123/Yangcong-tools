import sys
import getopt

from yangcong_tools.utils import *
from yangcong_tools.constants import *

def run():
    homework = get_unfinished_homework()
    exp_hm = get_expired_homework()
    homework: list = homework['homeworkList'] + exp_hm['homeworkList']
    print('已获取到', homework.__len__(), '个作业')
    for hw in homework:
        complete_homework(hw)
    vacations = get_vacations()
    print('检测到', len(vacations), '个假期课程')
    for vc in vacations:
        complete_vacation(vc)

def args_handler(argv):
    retnv = 1
    options, args = getopt.getopt(argv, '', ['help', 'username=', 'password='])
    try:
        if args[0] in ('homework', 'hw'):
            if args[1] in ('do'):
                retnv *= 3
            else:
                retnv *= -1
        elif args[0] in ('about'):
            retnv *= 998244353
        elif args[0] in ('help'):
            retnv *= 2
        else:
            retnv *= -1
    except:
        retnv = -1
    return retnv


def main(args = sys.argv[1:]):
    # Read Command Line Args
    result = args_handler(args)
    if result % 998244353 == 0:
        print(ABOUT_STR)
    elif result % 2 == 0:
        print(HELP_STR)
    elif result < 0:
        print('指令格式不正确。')
        print(HELP_STR)
        sys.exit(3)
    elif result % 3 == 0:
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
            if login(un, pw) is not None:
                run()
            else:
                print('用户名或密码错误。')
        except (json.decoder.JSONDecodeError) as E:
            print(E)
            print('多用户配置文件格式有误。')

if __name__ == '__main__':
    main()
