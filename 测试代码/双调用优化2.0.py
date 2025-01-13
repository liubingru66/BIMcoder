# -*- coding: utf-8 -*-
import random
import pandas as pd
import requests
import json
import re
from tqdm import tqdm

def sanitize_string(s):
    """清理字符串，移除前后空格及引号，并转换为小写"""
    return re.sub(r'\s+|\'|\"', '', s).lower()

def sanitize_dict(d):
    """清理字典，仅移除字符串值内的前后空格"""
    return {k: sanitize_string(v) if isinstance(v, str) else v for k, v in d.items()}

def read_excel_data(file_path):
    """读取Excel文件并随机抽取样本"""
    df = pd.read_excel(file_path)
    sample_df = df.sample(n=20, replace=False)
    questions = sample_df['问题'].tolist()
    answers = sample_df['标准答案'].tolist()
    return questions, answers

def optimize_question(question, access_token):
    """优化问题"""
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"
    question_with_prompt = f"1.提供整个建筑的3D显示。2.单独展示建筑的‘墙’构件。3.同时显示建筑中的‘墙壁’和‘门’构件。4.使根据GUID：16M94jOxL3f8Bkl$7i8KQ$检索建筑中的具体构件。5.查询建筑结构中在‘123宽 x 123高 x 123深’空间内的构件。6.根据特定GUID:06gL_hkB14LhZ8gqCSCgQ_查询整个建筑构造中某构件的属性。7.检索建筑物内门构件的属性。8.展示所有墙类型及其子类型的构件，包括'OwnerHistory'、'Representation' 和 'ObjectPlacement' 属性。9.展示带有开口的所有‘墙’，包括子类型，展示相关填充物和关联‘楼梯’。10.找到具有特定’GUID:2udBPbKibCZ8zbfpJmtDTM‘的楼层，并展示该楼层包含的所有元素。11.只是呈现建筑外部的‘墙壁’。12.列出所有被归类为特定‘57.2’类型的'IfcProduct'及其衍生类型的构件。请根据用户的提问，理解提问的意图，将其转化为以上十二类精准问题中的一类,以同样的格式描绘。请只回答修改后的问题，不需要其它文字！不要带序号！问题是：{question}"
    payload = json.dumps({"messages": [{"role": "user", "content": question_with_prompt}]})
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        response_data = response.json()
        return response_data.get("result", question)  # 如果优化失败，使用原始问题
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")
        return question

def execute_query(question, access_token, temperature=0.1):
    """发送请求到API并返回结果"""
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/completions/ihong3dq_lbr_12345?access_token={access_token}"
    payload = json.dumps({"prompt":question})
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        response_data = response.json()
        return response_data.get("result", None)
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")
        return None

def compare_answers(question_answer_pair, access_token):
    """比较标准答案与生成的答案"""
    question, expected_answer = question_answer_pair
    optimized_question = optimize_question(question, access_token)
    actual_answer = execute_query(optimized_question, access_token)

    if actual_answer is None:
        return False

    # 预处理答案
    expected_answer_processed = sanitize_string(str(expected_answer))
    actual_answer_processed = sanitize_string(str(actual_answer))

    # 比较预处理后的答案
    is_correct = expected_answer_processed == actual_answer_processed

    print(f"原始问题：{question}")
    print(f"优化后问题：{optimized_question}")
    print(f"标准答案：{expected_answer}")
    print(f"模型生成答案：{actual_answer}")
    print(f"答案匹配情况：{'正确' if is_correct else '错误'}\n")

    return is_correct

def calculate_accuracy(questions, answers, access_token):
    """计算答案匹配的准确率"""
    correct_count = 0
    for question, answer in tqdm(zip(questions, answers), total=len(questions), desc="计算准确率"):
        if compare_answers((question, answer), access_token):
            correct_count += 1

    accuracy = correct_count / len(questions)
    return accuracy * 100  # 转换成百分比形式

def get_access_token():
    """获取访问令牌"""
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=cE86qPxYeHZiZg2LtfPWBn8k&client_secret=iMoh4aXlEF2BacCzabcd1JU7U4EDpkC2"
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps({}))
        response.raise_for_status()
        access_token = response.json().get("access_token")
        return access_token if access_token else None
    except requests.exceptions.RequestException as e:
        print(f"获取access_token失败：{e}")
        return None

def main():
    """主函数，执行整个流程"""
    access_token = get_access_token()
    if not access_token:
        print("未能成功获取access_token，请检查API密钥和secret_key")
        return

    questions, answers = read_excel_data(r'E:\Users\Administrator\Desktop\研三\现在数据集\测试代码\模糊测试集\7.xlsx')  # 替换为你的Excel文件路径

    # 存储每次迭代的准确率
    accuracy_list = []

    # 运行十次循环
    for _ in tqdm(range(5), desc="总体进度"):
        # 计算使用优化后的准确率
        accuracy = calculate_accuracy(questions, answers, access_token)
        accuracy_list.append(accuracy)

    # 计算平均准确率
    avg_accuracy = sum(accuracy_list) / len(accuracy_list)

    # 显示每次迭代的准确率
    print("\n每次使用后的准确率：")
    for i, accuracy in enumerate(accuracy_list, 1):
        print(f"第 {i} 次准确率：{accuracy}%")

    # 显示平均准确率
    print(f"\n平均准确率：{avg_accuracy}%")

if __name__ == '__main__':
    main()
