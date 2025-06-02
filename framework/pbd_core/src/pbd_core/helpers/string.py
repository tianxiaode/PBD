import re


class StringHelper:
    @classmethod
    def camel_to_snake(self,name: str) -> str:
        """
        将驼峰式命名字符串转换为蛇形命名
        
        参数：
            camel_case_str (str): 驼峰格式字符串，如"CamelCaseString"
            
        返回：
            str: 蛇形格式字符串，如"camel_case_string"
            
        功能特点：
            1. 处理连续大写字母（如"HTTPRequest" -> "http_request"）
            2. 保留原始下划线和前缀
            3. 正确处理数字与字母的组合
            4. 首字母大写自动转小写
        """
        if not name:
            return ""
            
        # 处理大写字母后接小写字母的情况（如 HttpRequest → Http_Request）
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
        # 处理小写字母或数字后接大写字母的情况（如 user2API → user2_API）
        s2 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1)
        result = s2.lower()
        result = re.sub(r'_{2,}', '_', result)
        return result

    @classmethod
    def safe_truncate_utf8(self,text: str, max_bytes: int) -> str:
        """
        安全截断UTF-8字符串，确保不超过指定字节数且不截断多字节字符
        
        参数:
            text: 要截断的字符串
            max_bytes: 最大允许字节数
            
        返回:
            截断后的字符串
        """
        if not text:
            return text
            
        encoded = text.encode('utf-8')
        if len(encoded) <= max_bytes:
            return text
            
        # 找到最后一个完整的UTF-8字符边界
        truncated = encoded[:max_bytes]
        # 尝试解码，忽略不完整的末尾字符
        return truncated.decode('utf-8', errors='ignore').rstrip()

    @classmethod
    def is_empty(self,s:str)->bool:
        """
        判断字符串是否为空
        """
        return s is None or len(s) == 0