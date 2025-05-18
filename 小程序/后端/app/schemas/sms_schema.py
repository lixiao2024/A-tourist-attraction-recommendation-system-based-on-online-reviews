from pydantic import BaseModel, Field
from typing import Optional

# 发送验证码请求
class SendVerificationRequest(BaseModel):
    phone: str = Field(..., description="手机号", example="13812345678")
    
# 验证码响应
class VerificationResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="提示信息")
    details: Optional[str] = Field(None, description="详细信息")

# 验证验证码并绑定手机号请求
class VerifyCodeRequest(BaseModel):
    phone: str = Field(..., description="手机号", example="13812345678")
    code: str = Field(..., description="验证码", example="123456")

# 绑定手机号响应
class BindPhoneResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="提示信息") 