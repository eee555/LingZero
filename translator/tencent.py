# -*- coding: utf-8 -*-
# 腾讯文本翻译api封装
# 腾讯的图片翻译“图片翻译结果，翻译结果按识别的文本每一行独立翻译，后续会推出按段落划分并翻译的版本”，因此不能使用
# 控制台：https://console.cloud.tencent.com/tmt
# 每月一号刷新500万字符免费额度。超出后付费默认是关闭的。5次/秒。
import hashlib
import hmac
import json
import time
from datetime import datetime, timezone
from http.client import HTTPSConnection


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

class Trans():
    def __init__(self, config):
        self.config = config
    def translate(self, input_text: str, target = "zh") -> str:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        secret_id = self.config.get('DEFAULT', 'tencent_secret_id')
        secret_key = self.config.get('DEFAULT', 'tencent_secret_key')
        token = ""

        service = "tmt"
        host = "tmt.tencentcloudapi.com"
        region = self.config.get('DEFAULT', 'tencent_region')
        version = "2018-03-21"
        action = "TextTranslate"
        if target == "zh":
            payload = "{\"SourceText\":\"" + input_text +\
                "\",\"Source\":\"en\",\"Target\":\"zh\",\"ProjectId\":0,\"UntranslatedText\":\"\",\"TermRepoIDList\":[\"\"],\"SentRepoIDList\":[\"\"]}"
        elif target == "en":
            payload = "{\"SourceText\":\"" + input_text +\
                "\",\"Source\":\"zh\",\"Target\":\"en\",\"ProjectId\":0,\"UntranslatedText\":\"\",\"TermRepoIDList\":[\"\"],\"SentRepoIDList\":[\"\"]}"
        # params = json.loads(payload)
        # endpoint = "https://tmt.tencentcloudapi.com"
        algorithm = "TC3-HMAC-SHA256"
        timestamp = int(time.time())
        date = datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%d")

        # ************* 步骤 1：拼接规范请求串 *************
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        ct = "application/json; charset=utf-8"
        canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (ct, host, action.lower())
        signed_headers = "content-type;host;x-tc-action"
        hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        canonical_request = (http_request_method + "\n" +
                            canonical_uri + "\n" +
                            canonical_querystring + "\n" +
                            canonical_headers + "\n" +
                            signed_headers + "\n" +
                            hashed_request_payload)

        # ************* 步骤 2：拼接待签名字符串 *************
        credential_scope = date + "/" + service + "/" + "tc3_request"
        hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        string_to_sign = (algorithm + "\n" +
                        str(timestamp) + "\n" +
                        credential_scope + "\n" +
                        hashed_canonical_request)

        # ************* 步骤 3：计算签名 *************
        secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
        secret_service = sign(secret_date, service)
        secret_signing = sign(secret_service, "tc3_request")
        signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

        # ************* 步骤 4：拼接 Authorization *************
        authorization = (algorithm + " " +
                        "Credential=" + secret_id + "/" + credential_scope + ", " +
                        "SignedHeaders=" + signed_headers + ", " +
                        "Signature=" + signature)

        # ************* 步骤 5：构造并发起请求 *************
        headers = {
            "Authorization": authorization,
            "Content-Type": "application/json; charset=utf-8",
            "Host": host,
            "X-TC-Action": action,
            "X-TC-Timestamp": timestamp,
            "X-TC-Version": version
        }
        if region:
            headers["X-TC-Region"] = region
        if token:
            headers["X-TC-Token"] = token

        req = HTTPSConnection(host)
        try:
            req.request("POST", "/", headers=headers, body=payload.encode("utf-8"))
            resp = req.getresponse()
            res_str = resp.read()
            res_str = res_str.decode('utf-8')
            r = json.loads(res_str)
            return r["Response"]["TargetText"]
        except:
            return ""