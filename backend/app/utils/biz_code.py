from enum import IntEnum

class BizCode(IntEnum):
  # 成功类 (20000+)
  SUCCESS = 20000
  PARTIAL_SUCCESS = 20001  # 部分成功

  # 客户端错误 (40000+)
  PARAM_MISSING = 40001
  INVALID_TOKEN = 40002

  # 服务端错误 (50000+)
  DB_CONN_FAIL = 50001

  # 第三方错误 (60000+)
  PAYMENT_TIMEOUT = 60001

  @classmethod
  def get_message(cls, code):
    messages = {
      BizCode.SUCCESS: "操作成功",
      BizCode.PARTIAL_SUCCESS: "部分数据处理失败",
      BizCode.PARAM_MISSING: "缺少必要请求参数",
      BizCode.INVALID_TOKEN: "身份验证失败",
      BizCode.DB_CONN_FAIL: "数据库连接异常",
      BizCode.PAYMENT_TIMEOUT: "第三方服务响应超时"
    }

    return messages.get(code, "未知状态")
