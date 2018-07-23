i = 1 # MBR Partition Entry number
size = ['byte', "KB", "MB", "GB", "TB", "EB", "ZB"]
j = 0 # 사이즈 단위 표시를 위한 변수

f = open("mbr_128.dd", "rb")
f.seek(446) # Boot Code
mbr = f.read(16)  # Partition Table Entry 1

for x in range(0, 3): # Partition Table Entry 탐색
    start_lba = mbr[8:12]
    start_lba = int.from_bytes(start_lba, byteorder='little') * 512 # int 형으로 변환, 실제 각 Partition Table LBA 시작 주소

    part_size = mbr[12:16]
    part_size = int.from_bytes(part_size, byteorder='little') * 512 # int 형으로 변환, 실제 각 Partition Table LBA 크기

    while part_size >= 1024: # 사이즈 단위 표시를 위해 사용
        part_size = part_size / 1024
        j = j + 1

    print("Partition%d" %i, hex(start_lba), "%.2f%s" %(part_size, size[j]))  # Partition N 시작위치 사이즈 출력

    i = i + 1 # Partition Table Entry i
    j = 0  # 사이즈 단위 표시를 위한 변수 초기화

    mbr = f.read(16)  # Next partition Table Entry

start_lba = mbr[8:12]
start_lba = int.from_bytes(start_lba, byteorder='little') * 512 # int 형으로 변환, 실제 각 Partition Table LBA 시작 주소

part_size = mbr[12:16]
part_size = int.from_bytes(part_size, byteorder='little') * 512  # int 형으로 변환, 실제 각 Partition Table LBA 크기

if start_lba != 0 and part_size != 0: # Partition Table Entry 4가 비어있지 않을 때
    f.seek(2, 1)
    f.seek(start_lba - 512, 1)
    f.seek(446, 1)
    ebr = f.read(32)

    ebr_first_part_start = ebr[8:12]
    ebr_first_part_start = int.from_bytes(ebr_first_part_start, byteorder='little') * 512  # int 형으로 변환, 실제 첫 번째 ebr Partition LBA 시작 주소

    ebr_first_part_size = ebr[12:16]
    ebr_first_part_size = int.from_bytes(ebr_first_part_size, byteorder='little')  * 512 # int 형으로 변환, 실제 첫 번째 ebr Partition LBA 크기

    ebr_second_part_start = ebr[24:28]
    ebr_second_part_start = int.from_bytes(ebr_second_part_start, byteorder='little') * 512 # int 형으로 변환, 실제 두 번째 ebr Partition Table LBA 시작 주소

    ebr_second_part_size = ebr[28:32]
    ebr_second_part_size = int.from_bytes(ebr_second_part_size, byteorder='little') * 512 # int 형으로 변환, 실제 두 번째 ebr Partition Table LBA 시작 주소

    unit = ebr_first_part_size

    while unit >= 1024: # 사이즈 단위 표시를 위해 사용
        unit = unit / 1024
        j = j + 1

    print("Partition%d" %i, hex(start_lba + ebr_first_part_start), "%.2f%s" %(unit, size[j]))  # Partition N 시작위치 사이즈 출력

    i = i + 1
    j = 0  # 사이즈 단위 표시를 위한 변수 초기화

    f.seek(34, 1) # 섹터 끝으로 이동

    f.seek(ebr_second_part_size - 512, 1) # 다음 ebr Partition Table LBA 시작 주소로 이동
    f.seek(446, 1)
    ebr = f.read(32)

    while ebr_second_part_start != 0 and ebr_second_part_size != 0: # 다음 ebr Partition Table LBA가 있을 경우 실행
        ebr_first_part_start = ebr[8:12]
        ebr_first_part_start = int.from_bytes(ebr_first_part_start, byteorder='little') * 512 # int 형으로 변환, 실제 각 첫 번째 ebr Partition LBA 시작 주소

        ebr_first_part_size = ebr[12:16]
        ebr_first_part_size = int.from_bytes(ebr_first_part_size, byteorder='little') * 512 # int 형으로 변환, 실제 각 첫 번째 ebr Partition LBA 크기

        unit = ebr_first_part_size

        while unit >= 1024:  # 사이즈 단위 표시를 위해 사용
            unit = unit / 1024
            j = j + 1

        print("Partition%d" %i, hex(start_lba + ebr_first_part_start + ebr_second_part_start), "%.2f%s" %(unit, size[j]))  # Partition N 시작위치 사이즈 출력

        ebr_second_part_start = ebr[24:28]
        ebr_second_part_start = int.from_bytes(ebr_second_part_start, byteorder='little') * 512 # int 형으로 변환, 실제 두 번째 ebr Partition Table LBA 시작 주소

        ebr_second_part_size = ebr[28:32]
        ebr_second_part_size = int.from_bytes(ebr_second_part_size, byteorder='little') * 512  # int 형으로 변환, 실제 두 번째 ebr Partition Table LBA 시작 주소

        i = i + 1
        j = 0  # 사이즈 단위 표시를 위한 변수 초기화

        f.seek(34, 1) # 섹터 끝으로 이동

        f.seek(ebr_first_part_start + ebr_first_part_size - 512, 1) # 다음 ebr Partition Table LBA 시작 주소로 이동
        f.seek(446, 1)
        ebr = f.read(32)