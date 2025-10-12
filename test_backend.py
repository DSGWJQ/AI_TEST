import requests
import json

def test_backend_api():
    """测试后端AI聊天接口"""
    url = "http://127.0.0.1:8000/ai/chat"
    headers = {"Content-Type": "application/json"}
    
    # 测试数据 - 使用OpenRouter官方示例中的模型
    test_data = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",  # 使用官方示例中的模型
        "messages": [{"role": "user", "content": "Hello, please respond with a simple greeting."}],
        "api_key": "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"
    }
    
    print("正在测试后端接口...")
    print(f"URL: {url}")
    print(f"请求数据: {json.dumps(test_data, indent=2)}")
    print("-" * 50)
    
    try:
        # 发送请求，设置30秒超时
        response = requests.post(url, headers=headers, json=test_data, timeout=30)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应时间: {response.elapsed.total_seconds():.2f}秒")
        print("-" * 50)
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("✅ 请求成功!")
                print(f"AI响应内容: {result.get('content', '无内容')}")
            except json.JSONDecodeError:
                print("⚠️ 响应不是有效的JSON格式")
                print(f"原始响应: {response.text}")
        else:
            print("❌ 请求失败!")
            try:
                error_detail = response.json()
                print(f"错误详情: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"错误响应: {response.text}")
                
    except requests.exceptions.Timeout:
        print("❌ 请求超时 (30秒)")
        print("可能原因:")
        print("- AI模型响应慢")
        print("- 网络连接问题")
        print("- OpenRouter服务响应慢")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败")
        print("可能原因:")
        print("- 后端服务未启动 (请运行: python backend/main.py)")
        print("- 端口8000被占用")
        print("- 防火墙阻止连接")
        
    except Exception as e:
        print(f"❌ 未知错误: {e}")

def test_simple_endpoint():
    """测试简单的根路径接口"""
    url = "http://127.0.0.1:8000/"
    print("\n正在测试根路径接口...")
    
    try:
        response = requests.get(url, timeout=5)
        print(f"根路径状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 后端服务正常运行")
        else:
            print("⚠️ 后端服务响应异常")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务")
        print("请确保后端服务已启动: python backend/main.py")
    except Exception as e:
        print(f"❌ 测试根路径失败: {e}")

if __name__ == "__main__":
    print("=== 后端接口测试工具 ===")
    
    # 先测试根路径
    test_simple_endpoint()
    
    # 再测试AI接口
    test_backend_api()
    
    print("\n=== 测试完成 ===")
    print("\n如果遇到问题，请检查:")
    print("1. 后端服务是否启动: python backend/main.py")
    print("2. 网络连接是否正常")
    print("3. OpenRouter API Key是否有效")
    print("4. 防火墙设置")