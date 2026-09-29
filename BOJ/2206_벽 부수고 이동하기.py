
"""
[BOJ 2206] 벽 부수고 이동하기
문제 링크: https://www.acmicpc.net/problem/2206
난이도: 골드 3 | 유형: BFS, 상태 추가 | 풀이일: 2026-09-29
[핵심 아이디어]
벽을 부쉈는지 안부쉈는지를 상태로 추가해 dist를 3차원배열로 관리
[시간복잡도]
O(N * M * 2) = 상태 수(N*M*2) x 방향 4
[막혔던 점/ 실수]
시작범위와 도착범위를 제대로 체크 안함

블럭을 부쉈을 때와 안 부쉈을 때로 나누어서 진행

3차원 배열로 관리

1. 입력 받기
    1-1. N, M 읽기
    1-2. 지도 읽기 
2. BFS 
    2-1. 출발지를 큐에저장 
    2-2. 큐 pop후 현재상태 확인
    2-3. 종료조건 작성 및  현재위치 범위확인
    2-4. 블럭이 있을 때 전진과 없을 때 전진
        2-4-1. 블럭이 있다면
            2-4-1-1. 아직 블럭이 안부서진 상태인가? 
                2-4-1-1-1. 맞다면 부수고 넘어감, 큐에 추가하고 거리 +1
            2-4-1-2 블럭을 한 번 부쉈다면 
                2-4-1-1-2. 넘어감 (그냥 전진과 같음)
        2-4-2. 일반 전진
            2-4-2-1. 큐에 추가하고 거리 +1


"""

from collections import deque

dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]


def input_test_case():
    # 1. 입력 받기
    # 1-1. N, M 읽기
    # 1-2. 지도 읽기 
    N,M = map(int, input().split())
    board = [list(map(int, input().strip())) for _ in range(N)]
    dist = [[[0, 0] for _ in range(M)] for _ in range(N)]
    return N,M,board,dist

def bfs(N,M,board,dist):
    q = deque()
    #  2-1. 출발지를 큐에저장 
    q.append((0,0,0))
    dist[0][0][0] = 1
    while q:
        # 2-2. 큐 pop후 현재상태 확인
        cur_r, cur_c, isBroken= q.popleft()
        # 2-3. 종료조건 작성 및  현재위치 범위확인
        if cur_r==N-1 and cur_c == M-1:
            return dist[cur_r][cur_c][isBroken]
        for d in range(4):
            nr = cur_r + dr[d]
            nc = cur_c + dc[d]
            #범위안에 없음 컷
            if not (0 <= nr < N) or not (0 <= nc < M):
                continue
            #2-4-1. 블럭이 있다면
            # 2-4-1-1. 아직 블럭이 안부서진 상태인가? 
            if (isBroken == 0) and (board[nr][nc] == 1):
                if dist[nr][nc][1] == 0:
                    # 2-4-1-1-1. 맞다면 부수고 넘어감, 큐에 추가하고 거리 +1
                    q.append((nr,nc,1))
                    dist[nr][nc][1] = dist[cur_r][cur_c][isBroken] +1
            # 2-4-1-2 블럭을 한 번 부쉈다면 or 벽이 아니라면
            if board[nr][nc] != 1 and (board[nr][nc]==0):
                if dist[nr][nc][isBroken] == 0:
                    # 2-4-2-1. 큐에 추가하고 거리 +1
                    dist[nr][nc][isBroken] = dist[cur_r][cur_c][isBroken] +1
                    q.append((nr,nc,isBroken))
                
    return -1

            
#MAIN
N,M,board,dist = input_test_case()
min_dist = bfs(N,M,board,dist)
print(min_dist)