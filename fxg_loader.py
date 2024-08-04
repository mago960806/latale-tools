import struct
from struct import calcsize

filename = "JUDGE_TARGET.FXG"

print(f"正在读取: {filename}")
stream = open(filename, "rb")

BINARY_CHECK = 415
FXG_HEADER_FORMAT = "255sifL"


description, binary, version, expansion = struct.unpack(FXG_HEADER_FORMAT, stream.read(calcsize(FXG_HEADER_FORMAT)))

if binary != BINARY_CHECK:
    raise ValueError("这不是一个 FXG 文件")


description = description.rstrip(b"\x00").decode("ascii")
print("FXG 文件读取成功")
print(
    f"文件头数据\n\t描述信息：{description}\n\t文件校验码：{binary}\n\t文件版本：{version:.2}\n\t额外信息：{expansion}"
)
fx_group_id = struct.unpack("i", stream.read(calcsize("i")))[0]

if fx_group_id <= 0:
    raise ValueError(f"FX Group ID 的值不合法: {fx_group_id}")

print(f"FX Group ID: {fx_group_id}")

fx_model_count = struct.unpack("i", stream.read(calcsize("i")))[0]

for _ in range(fx_model_count):
    fx_model_id = struct.unpack("i", stream.read(calcsize("i")))[0]
    print(f"FX Model ID: {fx_model_id}")
    unknown_data = stream.read(21)
    print(f"未知数据: {unknown_data.hex().upper()}")
