"""
脚本执行器模块
提供异步代码执行功能，支持Python和pytest
"""

import asyncio
import subprocess
import tempfile
import os
import time
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple
import uuid


class ExecutionStatus(Enum):
    """执行状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class ExecutionResult:
    """执行结果数据类"""
    stdout: str
    stderr: str
    exit_code: int
    runner: str
    file_path: str
    timeout: int
    execution_time: float
    status: ExecutionStatus
    error_message: Optional[str] = None


class ScriptExecutor:
    """脚本执行器类"""
    
    def __init__(self, temp_dir: str = None):
        """
        初始化脚本执行器
        
        Args:
            temp_dir (str): 临时文件目录，默认使用系统临时目录
        """
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.running_processes = {}
    
    async def execute_script_async(
        self, 
        code: str, 
        runner: str = "python", 
        timeout: int = 30
    ) -> ExecutionResult:
        """
        异步执行脚本代码
        
        Args:
            code (str): 要执行的代码
            runner (str): 执行器类型 ("python" 或 "pytest")
            timeout (int): 超时时间（秒）
            
        Returns:
            ExecutionResult: 执行结果
        """
        start_time = time.time()
        
        # 生成唯一的文件名
        script_id = str(uuid.uuid4())[:8]
        file_extension = ".py"
        script_filename = f"script_{script_id}{file_extension}"
        script_path = os.path.join(self.temp_dir, script_filename)
        
        print(f"[脚本执行器] 开始执行 - ID: {script_id}, Runner: {runner}, 超时: {timeout}秒")
        print(f"[脚本执行器] 临时文件路径: {script_path}")
        
        try:
            # 写入代码到临时文件，使用严格的编码处理
            with open(script_path, 'w', encoding='utf-8', errors='replace') as f:
                # 确保代码内容是有效的UTF-8
                clean_code = code.encode('utf-8', errors='replace').decode('utf-8')
                f.write(clean_code)
            print(f"[脚本执行器] 代码已写入文件，大小: {len(code)} 字符")
            
            # 根据runner类型构建命令（新增：pytest测试检测与回退）
            if runner == "pytest":
                if not self._contains_pytest_tests(code):
                    print("[脚本执行器] 未检测到pytest测试，自动改用python运行")
                    runner = "python"
            if runner == "pytest":
                cmd = ["python", "-m", "pytest", script_path, "-v", "--tb=short"]
            else:
                cmd = ["python", script_path]
            
            print(f"[脚本执行器] 执行命令: {' '.join(cmd)}")
            
            # 执行命令（非阻塞，禁用交互输入，按平台创建进程组）
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.path.dirname(script_path),
                creationflags=(subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0),
                start_new_session=(os.name != 'nt')
            )
            self.running_processes[script_id] = process
            
            try:
                # 等待执行完成或超时
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=timeout
                )
                
                execution_time = time.time() - start_time
                
                # 解码输出
                stdout_str = stdout.decode('utf-8', errors='replace') if stdout else ""
                stderr_str = stderr.decode('utf-8', errors='replace') if stderr else ""
                
                # 详细日志输出
                print(f"[脚本执行器] 执行完成 - 退出码: {process.returncode}, 耗时: {execution_time:.2f}秒")
                print(f"[脚本执行器] STDOUT前200字符: {stdout_str[:200]}")
                print(f"[脚本执行器] STDERR前200字符: {stderr_str[:200]}")
                
                return ExecutionResult(
                    stdout=stdout_str,
                    stderr=stderr_str,
                    exit_code=process.returncode,
                    runner=runner,
                    file_path=script_path,
                    timeout=timeout,
                    execution_time=execution_time,
                    status=ExecutionStatus.COMPLETED
                )
                
            except asyncio.TimeoutError:
                # 超时处理，按平台优雅终止，失败后强杀
                try:
                    if os.name == 'nt':
                        import signal
                        os.kill(process.pid, signal.CTRL_BREAK_EVENT)
                    else:
                        process.terminate()
                    await asyncio.wait_for(process.wait(), timeout=5)
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()
                
                execution_time = time.time() - start_time
                
                return ExecutionResult(
                    stdout="",
                    stderr=f"执行超时 ({timeout}秒)",
                    exit_code=-1,
                    runner=runner,
                    file_path=script_path,
                    timeout=timeout,
                    execution_time=execution_time,
                    status=ExecutionStatus.TIMEOUT,
                    error_message=f"执行超时 ({timeout}秒)"
                )
            
            finally:
                # 清理进程记录
                self.running_processes.pop(script_id, None)
        
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"执行异常: {str(e)}"
            print(f"[脚本执行器] {error_msg}")
            
            return ExecutionResult(
                stdout="",
                stderr=error_msg,
                exit_code=-1,
                runner=runner,
                file_path=script_path,
                timeout=timeout,
                execution_time=execution_time,
                status=ExecutionStatus.ERROR,
                error_message=error_msg
            )
        
        finally:
            # 清理临时文件
            try:
                if os.path.exists(script_path):
                    os.remove(script_path)
                    print(f"[脚本执行器] 临时文件已清理: {script_path}")
            except Exception as e:
                print(f"[脚本执行器] 清理临时文件失败: {e}")
    
    def stop_all_processes(self):
        """停止所有正在运行的进程"""
        for process_id, process in self.running_processes.items():
            try:
                if os.name == 'nt':
                    import signal
                    os.kill(process.pid, signal.CTRL_BREAK_EVENT)
                else:
                    process.terminate()
                print(f"[脚本执行器] 已终止进程: {process_id}")
            except Exception as e:
                print(f"[脚本执行器] 终止进程失败 {process_id}: {e}")
        self.running_processes.clear()
    
    def _contains_pytest_tests(self, code: str) -> bool:
        import re
        patterns = [
            r'^\s*def\s+test_',          # 测试函数
            r'^\s*class\s+Test',         # 测试类
            r'^\s*import\s+pytest',      # 显式导入pytest
            r'^\s*from\s+pytest\s+import'
        ]
        return any(re.search(p, code, re.MULTILINE) for p in patterns)


# 全局脚本执行器实例
_script_executor = None


def get_script_executor() -> ScriptExecutor:
    """
    获取全局脚本执行器实例
    
    Returns:
        ScriptExecutor: 脚本执行器实例
    """
    global _script_executor
    if _script_executor is None:
        _script_executor = ScriptExecutor()
    return _script_executor


def cleanup_executor():
    """清理执行器资源"""
    global _script_executor
    if _script_executor:
        _script_executor.stop_all_processes()
        _script_executor = None