# 聊天功能
# 报文长度                 聊天类型                  消息长度 消息体 接收人ID
# 7A                1C 1B 11 7A 7A 7A 7A 7A 7A 7A 17 1C 1B 11 0E 14 0A 1D 10 09 0B 17 7A
# 67 7A 7B 7A BB D1 F7 10 10 7A 7A 7A 7A 7A 7A 7A 1B 2D 2A 20 3F 25 3B 2C 21 38 3A 26 7A
# 5F 7A 7B 7A BB D1 F7 10 14 7A 7A 7A 7A 7A 7A 7A 1B 2D 2A 20 3F 25 3B 2C 21 38 3A 26 7A 1C A4 42 BD 57 B9 FB 7A
# 6C 7A 7B 7A BB D1 F7 10 10 7A 7A 7A 7A 7A 7A 7A 12 BB C1 B7 6C 7A

import struct

# 31 31 31 31 31 31 31 31 31 31 31
# 1C 1B 11 0E 14 0A 1D 10 09 0B 17
# 2D 2A 20 3F 25 3B 2C 21 38 3A 26

# KEYS = [0x1C, 0x1B, 0x11, 0x0E, 0x14, 0x0A, 0x1D, 0x10, 0x09, 0x0B, 0x17]
KEYS = [0x2D, 0x2A, 0x20, 0x3F, 0x25, 0x3B, 0x2C, 0x21, 0x38, 0x3A, 0x26]

"""
总结
1. 数据包头部的偏移值, 每天都会变化, 且有很强的规律, 在0x4B和0x7A之间切换, 通过进行与0x31进行XOR运算得到。
2. 数据包数据的密钥, 同样每天都会变化, 
"""


def decrypt(data: str, key) -> str:
    print("加密数据: ", data)
    data = bytearray(bytes.fromhex(data))
    # 解密头部信息
    header = data[:6]
    for i in range(len(header)):
        header[i] = header[i] ^ key
    # 解密正文信息
    content = data[6:]
    for i in range(len(content)):
        if content[i] == key:
            content[i] = content[i] ^ key
        else:
            content[i] = content[i] ^ KEYS[i % len(KEYS)]
    data = header + content
    print("解密数据: ", data.hex(" ").upper())
    # 解析明文数据
    packet_length = data[0]
    print("报文长度: ", packet_length)
    if data[8] == 1:
        channel = "一般"
    elif data[8] == 5:
        channel = "悄悄话"
    else:
        channel = "未知频道"
    message_length = data[16]
    print("消息长度: ", message_length)
    message = data[-message_length:].decode("big5")
    print(f"频道: {channel}\n喊话内容: {message}")


def chat(message: str, key, channel: int = 1):
    data = bytearray(bytes.fromhex("16 00 01 00 C1 AB EB 0B"))
    data.append(channel)
    data = data + bytes(7)
    message = message.encode("big5") + bytes(1)
    message_length = len(message)
    data.append(message_length)
    data = data + message
    data[0] = len(data)
    data = data.hex(" ").upper()
    print("待加密的数据: ", data)
    # 数据加密
    encrypted_data = encrypt(data, key)
    print("加密后的数据: ", encrypted_data)


def encrypt(data: str, key) -> str:
    data = bytearray(bytes.fromhex(data))
    # 加密头部信息
    header = data[:6]
    for i in range(len(header)):
        header[i] = header[i] ^ key
    # 加密正文信息
    content = data[6:]
    for i in range(len(content)):
        if content[i] == 0x00:
            content[i] = content[i] ^ key
        else:
            content[i] = content[i] ^ KEYS[i % len(KEYS)]
    data = header + content
    data = data.hex(" ").upper()
    return data


print("进行解密测试")
decrypt(
    "69 4B 4A 4B 8A E0 C6 21 21 4B 4B 4B 4B 4B 4B 4B 37 8A 74 86 68 89 8B 8A 54 FD 7A 8C E1 8B 70 98 E3 4B", key=0x4B
)
print("进行加密测试")
chat(message="吾名為守護者·希", key=0x4B)
# encrypt("6A 00 7B 00 45 D1 F7 10 B6 BA CA D1 00 00 00 00")
decrypt("5F 4B 4A 4B CE E5 C6 21 4B 7F 4B 4B 4B 4B 4B 4B 36 4B 4B 4B ", key=0x4B)

# 4B 4B 4B 4B 4B 4B 00 00 00 4B 4B 4B 4B 4B 4B 4B 00 2D 2A 20 3F 25 3B 2C 21 38 3A 26 2D 2A 20 3F 25 3B 2C 21 38 3A 26
# 64 4B 4A 4B 8A E0 C6 21 21 4B 4B 4B 4B 4B 4B 4B 38 1C 1B 11 0E 14 0A 1D 10 09 0B 17 1C 1B 11 0E 14 0A 1D 10 09 0B 17 1C 1B 11 0E 14 0A 1D 4B
