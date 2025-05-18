from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from datetime import datetime

from app.models.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services.sms_service import SMSService, VERIFICATION_CODES
from app.schemas.sms_schema import (
    SendVerificationRequest, 
    VerificationResponse, 
    VerifyCodeRequest, 
    BindPhoneResponse
)

# 设置日志
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.post("/phone/send-code", response_model=VerificationResponse)
async def send_verification_code(
    request: SendVerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    发送手机验证码
    
    Args:
        request: 包含手机号的请求对象
        db: 数据库会话
        current_user: 当前登录用户
        
    Returns:
        发送结果
    """
    try:
        logger.info(f"用户 {current_user.id} 请求发送验证码到手机 {request.phone}")
        
        # 检查手机号格式，简单验证
        if not request.phone or len(request.phone) != 11 or not request.phone.isdigit():
            logger.warning(f"手机号 {request.phone} 格式不正确")
            return {
                "success": False,
                "message": "手机号格式不正确"
            }
        
        # 创建短信服务
        sms_service = SMSService(db)
        
        # 发送验证码
        result = await sms_service.send_verification_code(request.phone)
        
        return result
    
    except Exception as e:
        logger.error(f"发送验证码时发生错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发送验证码失败: {str(e)}"
        )

@router.post("/phone/verify-and-bind", response_model=BindPhoneResponse)
async def verify_code_and_bind_phone(
    request: VerifyCodeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    验证验证码并绑定手机号
    
    Args:
        request: 包含手机号和验证码的请求对象
        db: 数据库会话
        current_user: 当前登录用户
        
    Returns:
        绑定结果
    """
    try:
        logger.info(f"用户 {current_user.id} 请求验证并绑定手机号 {request.phone}")
        logger.info(f"接收到的验证码: {request.code}, 类型: {type(request.code)}")
        
        # 输出全局验证码存储的当前状态
        logger.info(f"当前验证码存储状态: {VERIFICATION_CODES}")
        
        # 检查手机号格式
        if not request.phone or len(request.phone) != 11 or not request.phone.isdigit():
            logger.warning(f"手机号 {request.phone} 格式不正确")
            return {
                "success": False,
                "message": "手机号格式不正确"
            }
        
        # 检查验证码格式
        if not request.code or len(request.code) != 6 or not request.code.isdigit():
            logger.warning(f"验证码 {request.code} 格式不正确")
            return {
                "success": False,
                "message": "验证码格式不正确"
            }
        
        # 创建短信服务
        sms_service = SMSService(db)
        
        # 手动检查验证码 - 不直接使用verify_code以避免删除验证码
        stored_data = VERIFICATION_CODES.get(request.phone)
        logger.info(f"验证时找到的存储数据: {stored_data}")
        
        if not stored_data:
            logger.warning(f"手机号 {request.phone} 未发送验证码或验证码已被使用")
            return {
                "success": False,
                "message": "未找到有效的验证码，请重新获取验证码"
            }
        
        # 验证码已过期
        if datetime.now() > stored_data["expire_time"]:
            logger.warning(f"手机号 {request.phone} 的验证码已过期")
            # 清除过期验证码
            del VERIFICATION_CODES[request.phone]
            return {
                "success": False,
                "message": "验证码已过期，请重新获取"
            }
        
        # 验证码不匹配
        stored_code = stored_data["code"]
        logger.info(f"存储的验证码: '{stored_code}', 输入的验证码: '{request.code}'")
        
        if stored_code != request.code:
            logger.warning(f"验证码不匹配: 输入='{request.code}', 实际='{stored_code}'")
            return {
                "success": False,
                "message": f"验证码错误，请重新输入"
            }
            
        # 验证通过，删除验证码
        del VERIFICATION_CODES[request.phone]
        logger.info(f"验证码验证成功，已从存储中删除")
        
        # 绑定手机号
        bind_result = await sms_service.bind_phone_to_user(current_user.id, request.phone)
        
        if bind_result:
            return {
                "success": True,
                "message": "手机号绑定成功"
            }
        else:
            return {
                "success": False,
                "message": "手机号绑定失败，请稍后重试"
            }
        
    except Exception as e:
        logger.error(f"验证并绑定手机号时发生错误: {str(e)}")
        logger.exception(e)  # 打印完整堆栈跟踪
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"验证并绑定手机号失败: {str(e)}"
        ) 