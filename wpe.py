# 4F 00 01 00 84 AE 8D 6A 00 2D EB 00 00 6B 00 61 5D 00 00 00 F4 00 00 00 00 44 00 00 00 53 14 5A 2B 00 A7 2D 37 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 4B 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

# 脱装备
# 第13字节为脱下的部位, 第20字节为装备栏格子号, 范围是1~240(0x01~0xF0)
# 6E 7A 7B 7A 83 D2 F7 10 17 7A 7A 7A 1C 11 7A 7A 7A 7A 7A 12
# 14 00 01 00 F9 A8 EB 0B 06 00 00 00 01 01 00 00 00 00 00 03
# 6E 7A 7B 7A 83 D2 F7 10 17 7A 7A 7A 19 11 7A 7A 7A 7A 7A 12
# 14 00 01 00 F9 A8 EB 0B 06 00 00 00 04 01 00 00 00 00 00 03

# 第13字节为装备栏格子号, 第20字节为穿上的部位, 部位01头, 04身体
# 穿装备
# 6E 7A 7B 7A 83 D2 F7 10 7A 7A 7A 7A 1E 11 7A 0D 7A 7A 7A 10
# 14 00 01 00 F9 A8 EB 0B 00 00 00 00 03 01 00 06 00 00 00 01
# 6E 7A 7B 7A 83 D2 F7 10 7A 7A 7A 7A 1E 11 7A 0D 7A 7A 7A 15
# 14 00 01 00 F9 A8 EB 0B 00 00 00 00 03 01 00 06 00 00 00 04
# 6E 7A 7B 7A 83 D2 F7 10 7A 7A 7A 7A 19 11 7A 0D 7A 7A 7A 10
# 14 00 01 00 F9 A8 EB 0B 00 00 00 00 04 01 00 06 00 00 00 01


# 無敵！！
# 27 00 01 00 1D A4 8D 6A E0 2B 00 00 66 00 63 41 6C 00 47 00 00 00 72 9A B9 77 00 A5 00 00 00 8C 90 81 00 E0 DF 36 5D 4F 00 01 00 84 AE 8D 6A 00 8C 90 81 00 E0 DF 36 5D 00 21 00 00 00 00 00 00 71 00 00 00 00 EB 84 2D 00 E7 4A 37 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00


# 15 00 01 00 7B A4 EB 0B 14 CC 10 00 00 00 00 00 FF FF FF FF 00
# 15 00 01 00 7B A4 EB 0B 14 CC 10 00 00 00 00 01 FF FF FF FF 00

# 13 00 01 00 7D A4 EB 0B 06 00 00 00 0F 52 4B 4C 00 00 00
# 13 00 01 00 7D A4 EB 0B 06 00 00 00 0F 52 4B 4C 00 00 00
KEYS = [0x1C, 0x1B, 0x11, 0x0E, 0x14, 0x0A, 0x1D, 0x10, 0x09, 0x0B, 0x17]


def decrypt(data: str) -> str:
    print("加密数据: ", data)
    data = bytearray(bytes.fromhex(data))
    # 解密头部信息
    header = data[:6]
    for i in range(len(header)):
        header[i] = header[i] ^ 0x7A
    # 解密正文信息
    content = data[6:]
    for i in range(len(content)):
        if content[i] == 0x7A:
            content[i] = content[i] ^ 0x7A
        else:
            content[i] = content[i] ^ KEYS[i % len(KEYS)]
    data = header + content
    print("解密数据: ", data.hex(" ").upper())


def encrypt(data: str) -> str:
    data = bytearray(bytes.fromhex(data))
    # 加密头部信息
    header = data[:6]
    for i in range(len(header)):
        header[i] = header[i] ^ 0x7A
    # 加密正文信息
    content = data[6:]
    for i in range(len(content)):
        if content[i] == 0x00:
            content[i] = content[i] ^ 0x7A
        else:
            content[i] = content[i] ^ KEYS[i % len(KEYS)]
    data = header + content
    data = data.hex(" ").upper()
    return data


decrypt("6E 7A 7B 7A 83 D2 F7 10 7A 7A 7A 7A 19 11 7A 0D 7A 7A 7A 10")
print(encrypt("14 00 01 00 F9 A8 EB 0B 06 00 00 00 01 01 00 00 00 00 00 04"))