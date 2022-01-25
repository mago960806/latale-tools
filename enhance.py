import random

OPT_TARGET_VALUE = 80

OPT_MIN_VALUE = 18
OPT_MAX_VALUE = 61
OPT_MID_VALUE = 40

ENHANCE_OPT_TABLE = {
    0: {
        "min": 1,
        "max": 3,
    },
    1: {
        "min": 1,
        "max": 5,
    },
    2: {
        "min": 1,
        "max": 5,
    },
    3: {
        "min": 2,
        "max": 5,
    },
    4: {
        "min": 2,
        "max": 6,
    },
    5: {
        "min": 2,
        "max": 6,
    },
    6: {
        "min": 2,
        "max": 6,
    },
    7: {
        "min": 2,
        "max": 8,
    },
    8: {
        "min": 2,
        "max": 8,
    },
    9: {
        "min": 3,
        "max": 9,
    },
}


MAX_OPT_LEVEL = 10

values = []
for i in range(10000):
    current_opt_level = 0
    current_opt_value = 0
    while current_opt_level < MAX_OPT_LEVEL:
        opt_up_value = random.randint(ENHANCE_OPT_TABLE[current_opt_level]["min"], ENHANCE_OPT_TABLE[current_opt_level]["max"])
        current_opt_value += opt_up_value
        current_opt_level += 1
        print(f"Lv{current_opt_level} 物理最大伤害 +{current_opt_value}%")
    values.append(current_opt_value)
print(sum(values)/len(values))


def enhance():
    records = []
    current_value = OPT_MID_VALUE
    enchant_times = 0
    # print(f"Lv10 物理最大傷害 +{current_value}%")
    while current_value <= OPT_TARGET_VALUE:
        temp = current_value
        current_value -= random.randint(3, 6)
        # print(f"Lv9 物理最大傷害 +{current_value}%")
        current_value += random.randint(3, 9)
        # print(f"Lv10 物理最大傷害 +{current_value}%")
        enchant_times += 1
        # print(f"物理最大傷害 {current_value - temp}%")
        records.append(current_value - temp)

    print(f"鑲嵌結束，本次共需要 {enchant_times} 次")
    print(f"平均每次强化上升{sum(records) / enchant_times}")
    return enchant_times, sum(records) / enchant_times

count_total = 0
opt_total = 0
for i in range(100000):
    count, avg = enhance()
    count_total += count
    opt_total += avg

print(f"平均需要: {count_total/100000}")
print(f"平均每次上升: {opt_total/100000}")