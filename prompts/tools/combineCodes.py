import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='将指定目录下的所有Python文件内容合并到输出文件中。')
    parser.add_argument('directory', help='要遍历的根目录')
    parser.add_argument('output_file', help='输出文件路径')
    args = parser.parse_args()

    start_dir = os.path.abspath(args.directory)
    output_content = []

    for root, dirs, files in os.walk(start_dir):
        if root == start_dir and '.conda' in dirs:
            dirs.remove('.conda')
        for filename in files:
            if filename.endswith('.py'):
                file_abs_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_abs_path, start_dir)
                
                # 格式化路径为以./开头的统一格式
                formatted_path = './' + rel_path.replace(os.sep, '/')
                
                try:
                    with open(file_abs_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                except Exception as e:
                    print(f"处理文件 {file_abs_path} 时出错: {e}")
                    continue
                
                # 构建条目并添加到输出内容
                entry = f"{formatted_path}:\n'''\n{content}\n'''\n"
                output_content.append(entry)

    # 将所有内容写入输出文件
    with open(args.output_file, 'w', encoding='utf-8') as out_file:
        out_file.writelines(output_content)

if __name__ == '__main__':
    main()