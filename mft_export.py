from latale_extractor.utils import read_int32, read_string

MFT_DESCRIPTION_LENGTH = 256


with open("MONSTER.MFT", "rb") as f:
    description = read_string(f, MFT_DESCRIPTION_LENGTH, encoding="big5")
    print(f"文件头描述信息: {description}")
    unknown_data = f.read(12)
    print(f"未知数据: {unknown_data.hex(' ').upper()}")
    total = read_int32(f)
    print(f"总共数据: {total} 条")
    for i in range(total):
        length = read_int32(f)
        content = read_string(f, length, encoding="big5")
        print(f"第 {i + 1} 条: {content}")
