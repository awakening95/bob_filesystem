i = 1 # GPT Partition Entry number
size = ['byte', "KB", "MB", "GB", "TB", "EB", "ZB"]
j = 0 # 사이즈 표시를 위한 변수

f = open("gpt_128.dd", "rb")
sector = f.seek(1024) # GPT Header

while True: # GPT GPT Partition Entry 탐색
    part_entry = f.read(128)  # Next GPT Partition Entry

    first_lba = part_entry[32:39]  # First LBA
    first_lba = int.from_bytes(first_lba, byteorder='little')  # int 형으로 변환

    if first_lba == 0: # lba 값이 0이면 더이상 파티션이 없으므로 while 문 탈출
        break

    last_lba = part_entry[40:47]  # Last LBA
    last_lba = int.from_bytes(last_lba, byteorder='little')  # int 형으로 변환

    part_size = (last_lba - first_lba + 1) * 512

    while part_size >= 1024: # 사이즈를 보기 편하게하기 위해 사용
        part_size = part_size / 1024
        j = j + 1

    print("Partition%d"%i, hex(first_lba * 512), "%.2f%s"%(part_size, size[j])) # PartitionN 시작위치 사이즈 출력

    i = i + 1
    j = 0 # 다음 part_size를 위해 초기화