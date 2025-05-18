import urllib.parse
import urllib.request
import random
import logging
import threading
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.user import User

# 设置日志
logger = logging.getLogger(__name__)

# SMS验证码过期时间（分钟）
SMS_CODE_EXPIRE_MINUTES = 5

# 全局存储验证码的字典，确保跨请求共享
# 格式: {phone: {"code": "1234", "expire_time": datetime}}
# 实际项目中应该使用Redis存储
VERIFICATION_CODES = {}

class SMSService:
    def __init__(self, db: Session):
        self.db = db
        
        # 接口配置
        self.sms_url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'
        self.account = 'C16140131'
        self.password = 'b47cd9d8d50b921c10d916c02da35ddd'
    
    def generate_verification_code(self) -> str:
        """生成6位随机验证码"""
        return ''.join(random.choices('0123456789', k=6))
    
    async def send_verification_code(self, phone: str) -> dict:
        """
        发送验证码到指定手机号
        
        Args:
            phone: 手机号
            
        Returns:
            发送结果
        """
        try:
            # 1. 生成验证码
            code = self.generate_verification_code()
            logger.info(f"为手机号 {phone} 生成验证码: {code}")
            
            # 2. 保存验证码及过期时间到全局字典
            expire_time = datetime.now() + timedelta(minutes=SMS_CODE_EXPIRE_MINUTES)
            VERIFICATION_CODES[phone] = {
                "code": code,
                "expire_time": expire_time
            }
            
            # 检查是否已成功存储
            logger.info(f"已将验证码存储到全局字典: {VERIFICATION_CODES.get(phone)}")
            
            # 3. 构建短信内容
            content = f'您的验证码是：{code}。请不要把验证码泄露给其他人。'
            values = {
                'account': self.account,
                'password': self.password,
                'mobile': phone,
                'content': content,
                'format': 'json',
            }
            
            # 4. 使用线程异步发送短信，避免阻塞API响应
            # 先返回成功响应，让用户等待短信
            threading.Thread(
                target=self._send_sms_request,
                args=(values, phone, code),
                daemon=True
            ).start()
            
            # 5. 立即返回成功结果，不等待短信API响应
            return {
                "success": True,
                "message": "验证码发送中，请稍候查收短信",
                "details": "验证码将在几秒钟内发送到您的手机"
            }
            
        except Exception as e:
            logger.error(f"发送验证码失败: {str(e)}")
            return {
                "success": False,
                "message": f"发送验证码失败: {str(e)}"
            }
    
    def _send_sms_request(self, values, phone, code):
        """
        实际发送短信的后台方法，在独立线程中执行
        """
        try:
            # 发送HTTP请求
            data = urllib.parse.urlencode(values).encode(encoding='UTF8')
            req = urllib.request.Request(self.sms_url, data)
            response = urllib.request.urlopen(req)
            res = response.read().decode("utf8")
            
            logger.info(f"短信API响应: {res}")
            logger.info(f"手机号 {phone} 的验证码 {code} 发送完成")
        except Exception as e:
            logger.error(f"后台发送短信失败: {str(e)}")
            # 即使发送失败，验证码仍然有效，用户可以手动输入（模拟环境中）
    
    async def verify_code(self, phone: str, code: str) -> bool:
        """
        验证手机验证码是否正确
        
        Args:
            phone: 手机号
            code: 验证码
            
        Returns:
            验证码是否正确
        """
        # 从全局字典获取存储的验证码信息
        stored_data = VERIFICATION_CODES.get(phone)
        
        # 验证前记录调试信息
        logger.info(f"验证手机号 {phone} 的验证码 {code}")
        logger.info(f"存储的验证码信息: {stored_data}")
        
        # 验证码不存在
        if not stored_data:
            logger.warning(f"手机号 {phone} 未发送验证码或验证码已被使用")
            return False
        
        # 验证码已过期
        if datetime.now() > stored_data["expire_time"]:
            logger.warning(f"手机号 {phone} 的验证码已过期")
            # 清除过期验证码
            del VERIFICATION_CODES[phone]
            return False
        
        # 验证码不匹配
        if stored_data["code"] != code:
            logger.warning(f"手机号 {phone} 的验证码不匹配，输入: {code}, 实际: {stored_data['code']}")
            return False
        
        # 验证通过后，删除验证码（一次性使用）
        del VERIFICATION_CODES[phone]
        logger.info(f"验证码验证成功，已从存储中删除")
        return True
    
    async def bind_phone_to_user(self, user_id: int, phone: str) -> bool:
        """
        将手机号绑定到用户
        
        Args:
            user_id: 用户ID
            phone: 手机号
            
        Returns:
            绑定是否成功
        """
        try:
            # 查询用户是否存在
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.error(f"用户ID {user_id} 不存在")
                return False
            
            # 更新用户手机号
            user.phone = phone
            self.db.commit()
            
            logger.info(f"用户ID {user_id} 成功绑定手机号 {phone}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"绑定手机号失败: {str(e)}")
            return False 