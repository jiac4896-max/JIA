"""企业微信回调消息的验签与加解密 (AES-256-CBC, PKCS7 块长 32)。"""
import base64
import hashlib
import os
import struct

from Crypto.Cipher import AES


class WeComCryptoError(Exception):
    pass


class WeComCrypto:
    def __init__(self, token: str, encoding_aes_key: str, corp_id: str):
        self.token = token
        self.corp_id = corp_id
        self.key = base64.b64decode(encoding_aes_key + "=")
        if len(self.key) != 32:
            raise WeComCryptoError("EncodingAESKey 必须是 43 位")
        self.iv = self.key[:16]

    def signature(self, timestamp: str, nonce: str, encrypted: str) -> str:
        parts = sorted([self.token, timestamp, nonce, encrypted])
        return hashlib.sha1("".join(parts).encode()).hexdigest()

    def verify(self, signature: str, timestamp: str, nonce: str, encrypted: str) -> None:
        if self.signature(timestamp, nonce, encrypted) != signature:
            raise WeComCryptoError("签名校验失败")

    def decrypt(self, encrypted: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        plain = cipher.decrypt(base64.b64decode(encrypted))
        plain = plain[: -plain[-1]]  # 去 PKCS7 填充
        content = plain[16:]
        msg_len = struct.unpack(">I", content[:4])[0]
        msg = content[4 : 4 + msg_len]
        receive_id = content[4 + msg_len :].decode()
        if receive_id != self.corp_id:
            raise WeComCryptoError("CorpID 不匹配")
        return msg.decode()

    def encrypt(self, text: str) -> str:
        msg = text.encode()
        raw = os.urandom(16) + struct.pack(">I", len(msg)) + msg + self.corp_id.encode()
        pad = 32 - len(raw) % 32
        raw += bytes([pad]) * pad
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw)).decode()
