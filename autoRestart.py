import os
import sys
import signal
import subprocess


def get_pid_by_port(port):
  """
  此脚本用于自动化劫持3.39.2版本小袁口算
  默认将清除7778端口占用并自动挂载mitmproxy脚本
  """
  try:
    # 根据系统类型执行不同的命令
    if os.name == 'nt':  # Windows
      command = f'netstat -ano | findstr :{port}'
      result = subprocess.check_output(command, shell=True).decode('utf-8')
      for line in result.splitlines():
        if f":{port}" in line:
          return int(line.split()[-1])  # PID 通常是最后一列
    else:  # Linux/macOS
      command = f'lsof -i :{port}'
      result = subprocess.check_output(command, shell=True).decode('utf-8')
      for line in result.splitlines():
        if f":{port}" in line:
          return int(line.split()[1])  # PID 通常是第二列
  except subprocess.CalledProcessError:
    return None  # 如果没有找到进程，返回 None


def kill_process(pid):
  """
  释放指定PID进程
  """
  try:
    if os.name == 'nt':  # Windows
      subprocess.call(['taskkill', '/PID', str(pid), '/F'])
    else:  # Linux/macOS
      os.kill(pid, signal.SIGKILL)
    print(f"Successfully killed process with PID: {pid}")
  except Exception as e:
    print(f"Failed to kill process with PID: {pid}. Error: {e}")


def start_mitmdump():
  """
  启动 mitmdump 并挂载 replace.py 脚本
  """
  # 获取当前脚本所在目录
  current_dir = os.path.dirname(os.path.abspath(__file__))

  # 切换到当前目录
  print(f"Changing directory to: {current_dir}")
  os.chdir(current_dir)

  # 查找 mitmdump 的路径
  # 如果 mitmdump 没有在环境变量 PATH 中，你可以手动指定路径
  mitmdump_path = 'mitmdump'  # 默认假设 mitmdump 在环境变量中

  # 替换成 mitmdump 的绝对路径，假如 mitmproxy 是通过 pip 安装的，将路径改为你系统上的实际路径
  if os.name == 'nt':  # Windows 系统
    python_path = os.path.dirname(sys.executable)  # 获取 Python 安装路径
    mitmdump_path = os.path.join(python_path, 'Scripts', 'mitmdump.exe')

  print(f"Using mitmdump path: {mitmdump_path}")

  # 启动 mitmdump
  try:
    # 构造 mitmdump 命令
    #mitmdump_command = [mitmdump_path, '-s', 'replace.py', '--listen-port', '7778']
    mitmdump_command = ['mitmdump', '-s', 'replace.py', '--listen-port', '7778']

    # 启动 mitmdump
    subprocess.call(mitmdump_command)

  except Exception as e:
    print(f"Failed to start mitmdump. Error: {e}")
    sys.exit(1)

if __name__ == "__main__":
  port = 7778
  # 启动 mitmdump
  print("Starting mitmdump on port 7778...")
  start_mitmdump()



