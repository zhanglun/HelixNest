class DomainException(Exception):
  """基础领域异常基类"""
  biz_code: str  # 业务错误码
  http_status: int  # 对应HTTP状态

  def __init__(
    self,
    message: str,
    biz_code: str,          # 变为必需参数
    http_status: int    # 变为必需参数
  ):
    super().__init__(message)
    self.biz_code = biz_code                 # 实例属性
    self.http_status = http_status   # 实例属性


class InvalidCredentialsError(DomainException):

  def __init__(self):
    super().__init__(
      message="无效的用户名或密码",
      biz_code = "AUTH_001",
      http_status = 401
    )

class UserNotActiveError(DomainException):

  def __init__(self, username: str):
    super().__init__(
      message=f"用户 {username} 尚未激活",
      biz_code = "AUTH_002",
      http_status = 403
    )
