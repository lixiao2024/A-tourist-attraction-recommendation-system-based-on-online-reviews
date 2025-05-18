import os
from http import HTTPStatus
from dashscope import Application
from dotenv import load_dotenv

# 加载.env.local文件中的环境变量
load_dotenv('../.env.local')

def call_with_session():
    response = Application.call(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key='sk-b5e444efee24456898a9b1756994b0e5',
        app_id='a004749b7ab34735bd4c0574a0d8e2f2',  # 替换为实际的应用 ID
        prompt='你是谁，可以帮我做些什么？')

    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
        return response

    responseNext = Application.call(
                # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                api_key='sk-b5e444efee24456898a9b1756994b0e5',
                app_id='a004749b7ab34735bd4c0574a0d8e2f2',  # 替换为实际的应用 ID
                prompt='明天我要从上海去杭州玩帮我看看天气，规划一下路线',
                session_id=response.output.session_id)  # 上一轮response的session_id

    if responseNext.status_code != HTTPStatus.OK:
        print(f'request_id={responseNext.request_id}')
        print(f'code={responseNext.status_code}')
        print(f'message={responseNext.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        print('%s\n session_id=%s\n' % (responseNext.output.text, responseNext.output.session_id))
        # print('%s\n' % (response.usage))

if __name__ == '__main__':
    call_with_session()