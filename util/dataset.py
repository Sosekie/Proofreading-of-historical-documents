import re

def load_and_process_text(filename):
    # 打开文件并读取内容
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # 去除换行符
    content = content.replace('\n', '')

    # 去除所有空格
    content = content.replace(' ', '')

    # 去除除了逗号和句号之外的所有标点符号
    content = re.sub(r'[^\w\s,。]', '', content)

    # 使用句号分割字符串
    doc_array = content.split('。')

    # 移除空字符串
    doc_array = [sentence for sentence in doc_array if sentence]

    return doc_array

# # 调用函数
# if __name__ == "__main__":
#     filename = 'dataset/art_and_science_simple_txt.txt'
#     document_array = load_and_process_text(filename)
#     for sentence in document_array:
#         print(sentence)
