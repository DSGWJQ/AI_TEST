# ============== 一、import（仅一次） ==============
import asyncio
import hashlib
import json
import uvicorn
import subprocess
import tempfile
import textwrap
import shutil
import requests
import sys
import os
from datetime import datetime
from typing import Any, Optional
from concurrent.futures import ThreadPoolExecutor
import time

from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request, Body, Header
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel

# 导入自定义清理工具模块
from app.sanitizer import clean_code_content, validate_chinese_ratio
from app.script_executor import get_script_executor, ExecutionStatus, cleanup_executor
from sqlalchemy.orm import Session

# 在文件最开头添加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import get_db, User, create_tables
from backend.app.mail import send_code, random_code
from backend.app.redis_client import r
from backend.app.crypto import hash_password, verify_password, encrypt_code, decrypt_code

app = FastAPI()

# ============== 三、统一响应模型 + 全局异常 ==============
class BaseResponse(BaseModel):
    code: int = 200
    msg: str = "success"
    data: Optional[Any] = None

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    print(f"异常详情: {type(exc).__name__}: {str(exc)}")  # 添加日志
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=200,
                            content=BaseResponse(code=exc.status_code, msg=exc.detail).dict())
    return JSONResponse(status_code=200,
                        content=BaseResponse(code=500, msg=f"服务器异常: {str(exc)}").dict())

# ============== 四、线程池工具 ==============
executor = ThreadPoolExecutor(max_workers=4)

def run_sync(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(executor, func, *args, **kwargs)

# ============== 五、请求/响应 DTO ==============
class Login(BaseModel):
    username: str
    password: str

class EmailRequest(BaseModel):
    email: str

class VerifyRequest(BaseModel):
    email: str
    code: str

class CodeRunRequest(BaseModel):
    code: str
    runner: Optional[str] = "python"
    timeout: Optional[int] = 20

# ============== 六、生命周期 ==============
@app.on_event("startup")
def startup():
    create_tables()

# ============== 七、路由蓝图 ==============
auth_router = APIRouter(tags=["auth"])
core_router = APIRouter(tags=["core"])

# 7.1 核心路由
@core_router.get("/", response_model=BaseResponse)
async def root():
    return BaseResponse(data={"hello": "world"})

# 7.2 认证路由
@auth_router.post("/register", response_model=BaseResponse)
async def register(user_data: Login, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    new_user = User(username=user_data.username,
                    password=hash_password(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return BaseResponse(msg="注册成功", data={"id": new_user.id,
                                            "username": new_user.username,
                                            "created_at": new_user.created_at.isoformat()})

@auth_router.post("/login", response_model=BaseResponse)
async def login(user_data: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 生成简单的 token（实际项目中应使用 JWT）
    import secrets
    access_token = secrets.token_urlsafe(32)
    
    return BaseResponse(msg="登录成功", data={
        "user_id": user.id, 
        "username": user.username,
        "access_token": access_token
    })

@auth_router.post("/send-code", response_model=BaseResponse)
async def send_code_api(req: EmailRequest):
    key = f"code:{req.email}"
    if r.exists(key):
        return BaseResponse(code=400, msg="1 分钟内只能发送一次")
    code = random_code()
    r.setex(key, 300, encrypt_code(code))
    await run_sync(send_code, req.email, code)
    return BaseResponse(msg="验证码已发送")

@auth_router.post("/verify-code", response_model=BaseResponse)
async def verify_code_api(req: VerifyRequest):
    key = f"code:{req.email}"
    real_code = decrypt_code(r.get(key))
    if real_code != req.code:
        raise HTTPException(status_code=400, detail="验证码错误或已过期")
    r.delete(key)
    return BaseResponse(msg="验证成功")

# 代码执行路由 - 使用异步非阻塞执行器
@core_router.post("/run-code", response_model=BaseResponse)
async def run_code(req: CodeRunRequest):
    """
    异步执行代码接口
    使用线程池隔离执行，避免主进程阻塞
    """
    try:
        print(f"[代码执行] 收到执行请求: runner={req.runner}, timeout={req.timeout}")
        
        # 参数验证
        if not req.code or not req.code.strip():
            raise ValueError("代码内容不能为空")
        
        runner = req.runner or "python"
        if runner not in ["python", "pytest"]:
            raise ValueError(f"不支持的执行器: {runner}")
        
        print(f"[run_code接口] 开始处理代码执行请求")
        print(f"[run_code接口] 原始代码长度: {len(req.code)} 字符")
        print(f"[run_code接口] 执行器类型: {runner}")
        print(f"[run_code接口] 超时设置: {req.timeout or 30} 秒")
        
        # 检查代码中的中文字符比例
        is_valid, chinese_ratio = validate_chinese_ratio(req.code)
        print(f"[run_code接口] 中文字符比例检查: {chinese_ratio:.2%} ({'通过' if is_valid else '未通过'})")
        if not is_valid:
            raise ValueError(f"代码中中文字符比例过高: {chinese_ratio:.2%}")

        # 写入文件前先清理代码
        cleaned_code = clean_code_content(req.code)
        print(f"[run_code接口] 代码清理完成，清理后长度: {len(cleaned_code)} 字符")
        print(f"[run_code接口] 清理后代码预览: {cleaned_code[:200]}...")
        # 预编译检查语法错误，提前给出明确提示
        try:
            compile(cleaned_code, "<submitted_code>", "exec")
        except SyntaxError as e:
            err_msg = f"语法错误: {e.msg} (第{e.lineno}行, 第{e.offset}列)"
            print(f"[run_code接口] 预编译失败: {err_msg}")
            return BaseResponse(code=400, msg=err_msg, data={
                "stdout": "",
                "stderr": e.text or "",
                "exit_code": -1,
                "status": "error"
            })
        
        # 获取脚本执行器
        executor = get_script_executor()
        
        # 异步执行脚本
        timeout_value = max(5, req.timeout or 30)  # 默认30秒超时
        print(f"[run_code接口] 开始异步执行，最终超时时间: {timeout_value}秒")
        
        result = await executor.execute_script_async(
            code=cleaned_code,
            runner=runner,
            timeout=timeout_value
        )
        
        print(f"[run_code接口] 执行完成总结:")
        print(f"  - 状态: {result.status.value}")
        print(f"  - 退出码: {result.exit_code}")
        print(f"  - 执行时间: {result.execution_time:.2f}秒")
        print(f"  - 文件路径: {result.file_path}")
        print(f"  - STDOUT前200字符: {result.stdout[:200]}")
        print(f"  - STDERR前200字符: {result.stderr[:200]}")
        
        # 构建返回结果
        response_data = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.exit_code,
            "runner": result.runner,
            "file_path": result.file_path,
            "timeout": result.timeout,
            "execution_time": result.execution_time,
            "status": result.status.value
        }
        
        # 根据执行状态返回不同的响应
        if result.status == ExecutionStatus.COMPLETED:
            if result.exit_code == 0:
                print(f"[run_code接口] 返回成功响应")
                return BaseResponse(data=response_data, msg="执行成功")
            else:
                print(f"[run_code接口] 返回失败响应 (退出码: {result.exit_code})")
                return BaseResponse(code=400, data=response_data, msg="执行失败")
        elif result.status == ExecutionStatus.TIMEOUT:
            print(f"[run_code接口] 返回超时响应")
            return BaseResponse(code=408, data=response_data, msg=f"执行超时 ({timeout_value}秒)")
        else:
            print(f"[run_code接口] 返回异常响应: {result.error_message}")
            return BaseResponse(code=500, data=response_data, msg=f"执行异常: {result.error_message}")
        
    except (ValueError, IOError) as e:
        error_msg = f"参数错误: {str(e)}"
        print(f"[run_code接口] 参数错误: {error_msg}")
        return BaseResponse(code=400, msg=error_msg, data={
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "error": "parameter_error",
            "status": "error"
        })
    except Exception as e:
        error_msg = f"执行失败: {str(e)}"
        print(f"[代码执行] 异常错误: {error_msg}")
        import traceback
        print(f"[代码执行] 异常堆栈: {traceback.format_exc()}")
        
        return BaseResponse(code=500, msg=error_msg, data={
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "error": "execution_error",
            "status": "error"
        })



# AI聊天路由 - 修复变量名冲突
@core_router.post("/ai/chat")
async def ai_chat(payload: dict = Body(...), x_openrouter_key: Optional[str] = Header(None)):
    """
    AI聊天接口，支持 OpenRouter API
    期望 payload:
    {
      "model": "deepseek/deepseek-r1-0528:free",
      "messages": [{"role": "user", "content": "prompt..."}],
      "api_key": "sk-or-v1-xxx" (可选)
    }
    """
    try:
        print(f"收到AI聊天请求: {payload}")  # 添加日志
        
        # 获取API Key
        api_key = x_openrouter_key or payload.get("api_key") or os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            return JSONResponse({"error": "API Key 未提供"}, status_code=400)

        # 验证API Key格式
        if not api_key.startswith('sk-or-v1-'):
            return JSONResponse({"error": "API Key 格式错误，应以 sk-or-v1- 开头"}, status_code=400)

        # 验证必需参数
        model = payload.get("model")
        messages = payload.get("messages", [])
        
        if not model:
            return JSONResponse({"error": "model 参数缺失"}, status_code=400)
        if not messages:
            return JSONResponse({"error": "messages 参数缺失"}, status_code=400)

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "FIRST_MIX"
        }
        
        data = {
            "model": model,
            "messages": messages,
        }
        
        print(f"发送到OpenRouter: {data}")  # 添加日志
        print(f"使用API Key: {api_key[:20]}...")  # 只显示前20个字符
        
        # 使用不同的变量名避免冲突
        response = requests.post(url, headers=headers, json=data, timeout=90)  # 从60秒增加到90秒
        
        print(f"OpenRouter响应状态: {response.status_code}")  # 添加日志
        print(f"响应时间: {response.elapsed.total_seconds():.2f}秒")  # 添加响应时间日志
        
        # 详细的错误处理
        if response.status_code == 401:
            return JSONResponse({"error": "API Key 无效或已过期，请检查后重试"}, status_code=401)
        elif response.status_code == 403:
            return JSONResponse({"error": "API Key 权限不足或余额不足"}, status_code=403)
        elif response.status_code == 429:
            return JSONResponse({"error": "请求过于频繁，请稍后重试"}, status_code=429)
        elif response.status_code != 200:
            try:
                error_detail = response.json()
                error_msg = error_detail.get('error', {}).get('message', response.text)
            except:
                error_msg = response.text
            return JSONResponse({"error": f"OpenRouter错误: {error_msg}"}, status_code=response.status_code)
        
        response_json = response.json()
        print(f"OpenRouter响应内容: {response_json}")  # 添加日志
        
        # 安全地提取内容
        if 'choices' not in response_json or not response_json['choices']:
            return JSONResponse({"error": "OpenRouter响应格式异常：缺少choices"}, status_code=500)
        
        choice = response_json['choices'][0]
        if 'message' not in choice or 'content' not in choice['message']:
            return JSONResponse({"error": "OpenRouter响应格式异常：缺少message内容"}, status_code=500)
        
        content = choice['message']['content']
        return JSONResponse({"content": content})
        
    except requests.exceptions.Timeout:
        error_msg = "请求超时，请检查网络连接"
        print(error_msg)
        return JSONResponse({"error": error_msg}, status_code=408)
    except requests.exceptions.ConnectionError:
        error_msg = "网络连接失败，请检查网络或代理设置"
        print(error_msg)
        return JSONResponse({"error": error_msg}, status_code=503)
    except requests.exceptions.RequestException as e:
        error_msg = f"网络请求异常: {str(e)}"
        print(error_msg)
        return JSONResponse({"error": error_msg}, status_code=500)
    except KeyError as e:
        error_msg = f"响应格式异常: {str(e)}"
        print(error_msg)
        return JSONResponse({"error": error_msg}, status_code=500)
    except Exception as e:
        error_msg = f"未知异常: {str(e)}"
        print(error_msg)
        return JSONResponse({"error": error_msg}, status_code=500)

# ============== 八、挂载蓝图 ==============
app.include_router(core_router)
app.include_router(auth_router)

# ============== 九、启动入口 ==============
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


@app.on_event("shutdown")
def shutdown():
    cleanup_executor()


