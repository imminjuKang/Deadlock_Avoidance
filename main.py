# input.txt에 있는 내용 읽어오기
def read_file(file):
    with open(file, 'r') as f:
        # 줄 단위로 읽어오기
        lines = [list(map(int, line.split())) for line in f.readlines()]

    n = lines[0][0] # 프로세스 개수
    m = lines[0][1] # resource type 개수
    total = lines[1] # type 별 리소스 개수
    max_claim = lines[2 : 2+n] # 최대 사용 자원
    allocation = lines[2+n : 2+2*n]
    need = [[0]*m for _ in range(n)]
    available = []

    for i in range(n):
        for j in range(m):
            need[i][j] = max_claim[i][j] - allocation[i][j]

    for j in range(m):
        temp = 0
        for i in range(n):
            temp += allocation[i][j]

        available.append(total[j] - temp)

    return n, m, total, max_claim, allocation, need, available

# 입력 오류 판단
def validation(n, m, total, max_claim, allocation):
    # 자원 할당은 total을 넘을 수 없음
    for j in range(m):
        sum = 0
        for i in range(n):
            sum += allocation[i][j]
        if total[j] < sum:
            print("총 자원 개수를 초과하여 프로세스에 할당할 수는 없습니다.")
            return False

    # 각 프로세스의 max_claim은 total 개수 넘을 수 없음
    for i in range(n):
        for j in range(m):
            if max_claim[i][j] > total[j]:
                print("존재하는 자원의 개수를 초과할 수 없습니다.")
                return False
    
    return True


# safety 체크
def is_safe(n, m, allocation, need, available):
    safe_sequence = []
    unit = available[:] 
    finish = [False] * n 

    while len(safe_sequence) < n:
        next = False
 
        for i in range(n):
            if not finish[i]:
                possible = True
                for j in range(m):
                    if need[i][j] > unit[j]:
                        possible = False
                        break
                # 모든 need가 unit보다 작아서 자원줄 수 있으면 일단 자원 주고 실행
                if possible:  
                    for j in range(m):
                        unit[j] += allocation[i][j] # 자원 회수
                    finish[i] = True
                    safe_sequence.append(i)
                    next = True 
                    break # 한 프로세스가 끝나면 break로 for문 종료
        # 실행할 수 있는 프로세스 없으면 deadlock
        if not next:
            return []
        
    # while문 다 돌면 safe
    return safe_sequence


def main():
    n, m , total, max_claim, allocation, need, available = read_file("input.txt")
    safe_sequence = is_safe(n, m, allocation, need, available)
    valid = validation(n, m, total, max_claim, allocation)

    if not valid:
        print("프로그램을 종료합니다.")
        return

    if safe_sequence:
        print("Safe State입니다.")
        print("Safe sequence: ", end = "")
        for i in range(n):
            if (i != n-1):
                print(f"P{safe_sequence[i] + 1} -> ", end = "")
            else:
                print(f"P{safe_sequence[i] + 1}")
    else:
        print("Unsafe State입니다.")


if __name__ == "__main__":
    main()
