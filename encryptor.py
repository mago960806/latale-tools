# KEYS = [0x1C, 0x1B, 0x11, 0x0E, 0x14, 0x0A, 0x1D, 0x10, 0x09, 0x0B, 0x17]
KEYS = [0x2D, 0x2A, 0x20, 0x3F, 0x25, 0x3B, 0x2C, 0x21, 0x38, 0x3A, 0x26]


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
    return data


if __name__ == "__main__":
    print("彩虹島物語封包解密工具")
    try:
        while True:
            decrypted_data = input("[input]:   ")
            try:
                encrypted_data = encrypt(encrypted_data, key=0x4B)
            except ValueError:
                continue
            else:
                print("[output]: ", encrypted_data.hex(" ").upper())
    except KeyboardInterrupt:
        print("感謝使用")
