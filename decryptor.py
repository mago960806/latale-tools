# KEYS = [0x1C, 0x1B, 0x11, 0x0E, 0x14, 0x0A, 0x1D, 0x10, 0x09, 0x0B, 0x17]
# KEYS = [0x2D, 0x2A, 0x20, 0x3F, 0x25, 0x3B, 0x2C, 0x21, 0x38, 0x3A, 0x26]

KEYS = [0x66, 0x61, 0x6B, 0x74, 0x6E, 0x70, 0x67, 0x6A, 0x73, 0x71, 0x6D]

# 3D 28 29 28 53 8C A5 42 66 D8 5D 28 28 28 28 28 BA B1 B6 BC 28
# 0x28

# 04 28 29 28 E9 83 A5 42 42 28 28 28 28 28 28 28 5E 7F 78 72 6D 77 69 7E 73 6A 68 74 7F 78 72 6D 77 69 7E 73 6A 68 74 7F 78 72 6D 28
#                                                    66 61 6b 74 6e 70 67 6a 73 71 6d 66 61 6b 74 6e 70 67 6a 73 71 6d 66 61 6b 74 6e 70
# 2d 00 01 00 c1 ab 8d 6a 6a 00 00 00 00 00 00 00 71 57 50 5a 45 5f 41 56 5b 42 40 5c 57 50 5a 45 5f 41 56 5b 42 40 5c 57 50 5a 45 5f 00


def decrypt(data: str, key) -> str:
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
    return data


if __name__ == "__main__":
    print("彩虹島物語封包解密工具")
    try:
        while True:
            encrypted_data = input("[input]:   ")
            try:
                decrypted_data = decrypt(encrypted_data, key=0x00)
            except ValueError:
                continue
            else:
                print("[output]: ", decrypted_data.hex(" ").upper())
    except KeyboardInterrupt:
        print("感謝使用")
