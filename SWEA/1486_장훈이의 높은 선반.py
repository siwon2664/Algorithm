"""
[SWEA 1486] 장훈이의 높은 선반
난이도: D4 | 유형: 백트래킹, 부분집합 | 풀이일: 2026-10-03

[문제 요약]
높이가 B인 선반
N명의 점원들이 B의 높이에 있는 물건을 사용해야함
탑은 점원 1명 이상으로 이루어짐
점원이 1명 이면 높이는 점원의 키
2명이면 2명키의 합

높이가 B 이상이면서 최소높이 찾기
"""
N = 0
B = 0
T = int(input())
total_height = 0
# index : 사람 수 
# total height : 현재까지 더한 값
def dfs(index, current_height):
    #끝까지 왔으면
    global total_height
    if index == N:
        if current_height >= B:
            total_height = min(current_height, total_height)
        return
    # 지금까지 더한 값이 더 크면 끝내기
    if current_height >= total_height:
        return

    #현재 값을 더한 경우
   
    dfs(index+1, current_height + height_array[index])

    # 현재값을 안 더한 경우
    dfs(index+1, current_height)

    return -1


for test_case in range(1, T + 1):
    N,B = map(int, input().split())
    height_array = list(map(int, input().split()))
    S = sum(height_array)
    total_height = S
    dfs(0,0)
    #여기서부터 로직
    print(f"#{test_case} {total_height - B}")