import subprocess
import tkinter as tk


def get_connections_for_port(port):
  """
  使用该脚本查询代理地址ip与端口
  获取指定端口的网络连接信息，使用 netstat 和 findstr 过滤连接状态
  """
  try:
    # 调用 netstat 并过滤端口
    result = subprocess.run(
      ['netstat', '-an'], capture_output=True, text=True, shell=True
    )

    # 提取包含特定端口的行
    lines = result.stdout.splitlines()
    connections = [line for line in lines if f":{port}" in line]

    if connections:
      return connections
    else:
      return ["没有找到端口相关的连接."]
  except Exception as e:
    return [f"发生错误: {e}"]


def update_connections(text_area, port):
  """
  更新 GUI 中的连接信息
  """
  # 清空文本区域
  text_area.config(state=tk.NORMAL)  # 允许编辑
  text_area.delete(1.0, tk.END)  # 删除现有内容

  # 获取新的连接信息
  connections = get_connections_for_port(port)

  # 插入新内容
  for connection in connections:
    text_area.insert(tk.END, connection + "\n")

  # 设置为只读
  text_area.config(state=tk.DISABLED)

  # 每秒 (1000ms) 调用一次该函数
  text_area.after(1000, update_connections, text_area, port)


def display_ip_in_gui():
  """
  显示通过 netstat 获取的 TCP 连接信息，并提供一个模板化的 GUI 界面
  """
  # 创建主窗口
  root = tk.Tk()
  root.title("端口 7778 的连接信息")

  # 设置窗口大小
  root.geometry("500x400")

  # 创建标题标签
  title_label = tk.Label(root, text="连接查询面板", font=("Arial", 16))
  title_label.pack(pady=10)

  # 设置端口号
  port = 7778

  # 显示连接信息的标签
  connection_label = tk.Label(root, text="当前连接:", font=("Arial", 12))
  connection_label.pack(pady=5)

  # 使用 Text 小部件来展示多行内容
  text_area = tk.Text(root, height=15, width=60, font=("Arial", 10))
  text_area.pack(pady=10)

  # 初次调用更新连接信息的函数
  update_connections(text_area, port)

  # 用户指导内容（模板化部分）
  guide_label = tk.Label(root, text="用户指导：\n请根据查询ip和端口设置被监听机代理", font=("Arial", 10))
  guide_label.pack(pady=10)

  # 一个按钮示例：退出
  exit_button = tk.Button(root, text="退出", command=root.quit, font=("Arial", 12))
  exit_button.pack(pady=20)

  # 运行主循环
  root.mainloop()


if __name__ == "__main__":
  display_ip_in_gui()

