import os

# 定义项目的根路径
PROJECT_ROOT = "/Users/yafei/workspace/AutoPrintFileFromEmail"

# 定义项目的目录结构
PROJECT_STRUCTURE = [
    "app/__init__.py",
    "app/email_client.py",
    "app/attachment_handler.py",
    "app/print_timer.py",
    "app/config.py",
    "tests/__init__.py",
    "tests/test_email_client.py",
    "tests/test_handler.py",
    "logs/",
    "attachments/",
    "README.md",
    "requirements.txt",
    ".env",
    "main.py"
]

def create_project_structure(root, structure):
    for path in structure:
        # 构建完整路径
        full_path = os.path.join(root, path)

        if path.endswith("/"):
            # 创建目录
            os.makedirs(full_path, exist_ok=True)
            print(f"Created directory: {full_path}")
        else:
            # 确保父目录存在，然后创建空文件
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write("")  # 写入空内容
            print(f"Created file: {full_path}")

if __name__ == "__main__":
    create_project_structure(PROJECT_ROOT, PROJECT_STRUCTURE)
    print("Project structure created successfully!")