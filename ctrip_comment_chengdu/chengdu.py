# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# def fetch_ca_narrative(ca_address):
#     # 配置 Chrome 无头模式（无需界面）
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")  # 隐藏浏览器界面
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
#
#     # 初始化 WebDriver（需安装 ChromeDriver）
#     driver = webdriver.Chrome(options=options)
#
#     try:
#         # 直接访问带 CA 地址的 URL
#         target_url = f"https://aiphago.com/#/{ca_address}"
#         driver.get(target_url)
#
#         # 显式等待叙事内容加载（最多等10秒）
#         narrative_element = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "div.text-gray-300.text-sm.font-mono.whitespace-pre-wrap"))
#         )
#
#         # 提取文本并清理空白字符
#         narrative = narrative_element.text.strip()
#         return narrative if narrative else "叙事内容为空。"
#
#     except TimeoutException:
#         return "错误：页面加载超时，未找到叙事内容。"
#     except NoSuchElementException:
#         return "错误：页面结构不符，叙事标签不存在。"
#     except Exception as e:
#         return f"未知错误: {str(e)}"
#     finally:
#         driver.quit()
#
# # 示例使用
# ca = "AT9tnZ5tfY8fVFGj3bw4j9g2dWKX5Rx6RN5hNTf1pump"
# result = fetch_ca_narrative(ca)
# print("查询结果:", result)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import translators as ts

def translate_text(text, from_lang='auto', to_lang='zh'):
    """使用谷歌翻译引擎进行文本翻译"""
    try:
        return ts.translate_text(text, translator='google',
                                from_language=from_lang,
                                to_language=to_lang)
    except Exception as e:
        print(f"翻译失败: {str(e)}")
        return None

def fetch_ca_narrative_with_translation(ca_address):
    # 获取原始叙事内容
    original_text = fetch_ca_narrative(ca_address)

    # 如果内容为错误信息则不翻译
    if any(keyword in original_text for keyword in ["错误", "失败", "无效"]):
        return original_text

    # 执行翻译
    translated_text = translate_text(original_text)

    # 构建返回结果
    result = "=== 原始内容 ===\n" + original_text
    if translated_text:
        result += "\n\n=== 中文翻译 ===\n" + translated_text
    else:
        result += "\n\n(翻译服务暂不可用)"

    return result

# 修改原函数名为私有函数
def fetch_ca_narrative(ca_address):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(f"https://aiphago.com/#/{ca_address}")
        narrative_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.text-gray-300.text-sm.font-mono.whitespace-pre-wrap")))
        return narrative_element.text.strip() or "叙事内容为空。"

    except TimeoutException:
        return "错误：页面加载超时，未找到叙事内容。"
    except NoSuchElementException:
        return "错误：页面结构不符，叙事标签不存在。"
    except Exception as e:
        return f"未知错误: {str(e)}"
    finally:
        driver.quit()

# 示例使用
if __name__ == "__main__":
    ca = "AT9tnZ5tfY8fVFGj3bw4j9g2dWKX5Rx6RN5hNTf1pump"
    print("正在查询并翻译...")
    result = fetch_ca_narrative_with_translation(ca)

    # 处理Windows控制台编码问题
    try:
        print(result)
    except UnicodeEncodeError:
        print(result.encode('gbk', errors='replace').decode('gbk'))