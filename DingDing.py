import json
import requests
import ssl

# 关闭 SSL 验证（如有需要）
ssl._create_default_https_context = ssl._create_unverified_context

# 新的 webhook 地址
url = 'https://oapi.dingtalk.com/robot/send?access_token=00ed3a42e6cf2dc199bd3ce9e66f6b04cde9947fad152bfc88acf7d94753fa3f'

# 钉钉机器人安全设置中的加签 secret（你可以加签用，但此代码中未使用）
secret = 'SEC6a86bf49ccb3555b64a01e4b0c0b37273029772dc2a0b1e8106f9ff3e6ca4155'

def getDingMes(data, suggestion=None):
    HEADERS = {
        "Content-Type": "application/json; charset=utf-8"
    }

    if suggestion:
        message = f"{data}\n建议：{suggestion}"
    else:
        message = str(data)

    stringBody = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [""],
            "isAtAll": "false"
        }
    }

    MessageBody = json.dumps(stringBody)
    result = requests.post(url=url, data=MessageBody, headers=HEADERS)
    print(result.text)
