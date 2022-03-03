# 仓库功能(长度16字节)
# 122                     17 14 20 10
# 7A                      11 0E 14 0A 1D 10 09 0B
# 6A 7A 7B 7A 45 D1 F7 10 10 7A 7A 7A 7A 7A 7A 7A
# 6A 7A 7B 7A 45 D1 F7 10 13 7A 7A 7A 7A 7A 7A 7A
# 6A 7A 7B 7A 45 D1 F7 10 12 7A 7A 7A 7A 7A 7A 7A
# 6A 7A 7B 7A 45 D1 F7 10 15 7A 7A 7A 7A 7A 7A 7A
# 6A 7A 7B 7A 45 D1 F7 10 8A 7A 7A 7A 7A 7A 7A 7A
# 6A 7A 7B 7A 45 D1 F7 10 EE 7A 7A 7A 7A 7A 7A 7A
# 6A 7A 7B 7A 45 D1 F7 10 EE F1 7A 7A 7A 7A 7A 7A
# 6A 7A 7B 7A 45 D1 F7 10 EE F1 EB 7A 7A 7A 7A 7A
# 6A 7A 7B 7A 47 D1 F7 10 EE 7A 7A 7A 7A 7A 7A 7A
# 6A 7A 7B 7A 45 D1 F7 10 A7 B4 DE DB 7A 7A 7A 7A

# 聊天功能
# 报文长度                 聊天类型                  消息长度 消息体 接收人ID
# 7A                         7A 7A 7A 7A 7A 7A 7A    1C 1B 11 0E 14 0A 1D 10 09 0B 17 7A
# 67 7A 7B 7A BB D1 F7 10 10 7A 7A 7A 7A 7A 7A 7A 1B 2D 2A 20 3F 25 3B 2C 21 38 3A 26 7A
# 5F 7A 7B 7A BB D1 F7 10 14 7A 7A 7A 7A 7A 7A 7A 1B 2D 2A 20 3F 25 3B 2C 21 38 3A 26 7A 1C A4 42 BD 57 B9 FB 7A

# 弱攻击

# 6E 7A 7B 7A FF D4 F7 10 7A 4E 7A 7A 7A 7A 7A 7A 07 7A 7A 7A

import struct

OFFSETS = [0x11, 0x0E, 0x14, 0x0A, 0x1D, 0x10, 0x09, 0x0B]


def decrypt(data: str) -> str:
    print("加密数据: ", data)
    data = bytearray(bytes.fromhex(data))
    data = data.replace(b"\x7a", b"\x00")
    packet_lenth = data[0] ^ 0x7A
    print("报文长度: ", packet_lenth)

    if data[4] == 0x45:
        operate = "提款"
    elif data[4] == 0x47:
        operate = "存款"
    else:
        operate = "未知操作"
    ely_data = bytearray(data[-8:])
    for i in range(len(ely_data)):
        if ely_data[i] == 0x00:
            continue
        ely_data[i] = ely_data[i] ^ OFFSETS[i]
    value = struct.unpack("<Q", ely_data)[0]
    data[-8:] = ely_data
    print("解密数据: ", data.hex(" ").upper())
    print(f"动作: {operate}\n数值: {value}")


def encrypt(data: str) -> str:
    print("明文数据: ", data)
    data = bytearray(bytes.fromhex(data))
    data = data.replace(b"\x00", b"\x7a")
    ely_data = bytearray(data[-8:])
    for i in range(len(ely_data)):
        if ely_data[i] == 0x7A:
            continue
        ely_data[i] = ely_data[i] ^ OFFSETS[i]
    data[-8:] = ely_data
    data = data.hex(" ").upper()
    print("密文数据: ", data)


print("进行解密测试")
decrypt("6A 7A 7B 7A 45 D1 F7 10 A7 B4 DE DB 7A 7A 7A 7A")
print("进行加密测试")
encrypt("6A 00 7B 00 45 D1 F7 10 B6 BA CA D1 00 00 00 00")
