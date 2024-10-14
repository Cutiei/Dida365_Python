import json
import requests

def login_dida365(username, password):
    url = 'https://api.dida365.com/api/v2/user/signon?wc=true&remember=true'
    headers = {
        'X-Device': '{"platform":"web","os":"Windows 10","device":"Chrome 102.0.0.0","name":"","version":4226,"id":"628774331068e7035ea5950b","channel":"website","campaign":"","websocket":""}'
    }
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        token = data.get('token')
        return token if token else False
    else:
        print(f"错误: {response.status_code}")
        return False

def action_dida365(token, action):
    url = f'https://api.dida365.com/api/v2/{action}'
    cookies = {'t': token}
    response = requests.get(url, cookies=cookies)
    if response.status_code == 200:
        return response.text
    else:
        print(f"错误: {response.status_code}")
        return None

def main():
    token = login_dida365('email', 'password')
    if token:
        action = input("请输入操作 (trash/completed/list/comments): ")
        if action == 'trash':
            print(action_dida365(token, 'project/all/trash/pagination'))
        elif action == 'completed':
            print(action_dida365(token, 'project/all/completed'))
        elif action == 'list':
            print(action_dida365(token, 'batch/check/0'))
        elif action == 'comments':
            project_id = input("请输入项目ID: ")
            task_id = input("请输入任务ID: ")
            if not project_id or not task_id:
                print(json.dumps({'error': True, 'message': 'projectId与taskId不能为空'}))
            else:
                print(action_dida365(token, f'project/{project_id}/task/{task_id}/comments'))
        else:
            print(json.dumps({
                'error': True,
                'message': {
                    'list': {
                        'info': '获取任务组与任务列表',
                        'method': 'GET',
                        'params': 'action=list'
                    },
                    'comments': {
                        'info': '获取任务清单的评论内容',
                        'method': 'GET',
                        'params': 'action=comments&project={projectId}&task={taskId}'
                    },
                    'completed': {
                        'info': '获取已完成的任务清单',
                        'method': 'GET',
                        'params': 'action=completed'
                    },
                    'trash': {
                        'info': '获取垃圾箱内的任务清单',
                        'method': 'GET',
                        'params': 'action=trash'
                    }
                }
            }))

if __name__ == "__main__":
    main()
