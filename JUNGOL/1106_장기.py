"""
[JUNGOL 1106] 장기
문제 링크: https://jungol.co.kr/problem/1106
난이도: - | 유형: BFS | 풀이일: 2026-10-03

[핵심 아이디어]
말(나이트 이동 8방향)로 졸까지 가는 최소 이동 횟수 → BFS

[막혔던 점 / 실수]
- q.append(r, c, d)처럼 튜플로 안 묶음
- 방문 체크, 범위 체크 누락 / return 위치가 while 안에 있었음
"""

from collections import deque

N,M = map(int, input().split())
# R, C : 말이 있는 행열
# S, K : 졸이 있는 행열 
R, C, S, K = map(int, input().split())



dr = [-2, -2, -1, -1, 1, 1, 2, 2]  # 세로 이동 (Row)
dc = [-1, 1, -2, 2, -2, 2, -1, 1]  # 가로 이동 (Column)
def bfs(R, C, S, K):
    visited = [[False] * (M + 1) for _ in range(N + 1)]
    visited[R][C] = True
    q = deque([(R, C, 0)])
    while q:
        r, c, dist = q.popleft()
        if r == S and c == K:
            return dist
        for d in range(8):
            nr, nc = r + dr[d], c + dc[d]
            if 1 <= nr <= N and 1 <= nc <= M and not visited[nr][nc]:
                visited[nr][nc] = True
                q.append((nr, nc, dist + 1))
    return -1   # 도달 불가: 문제에서 요구하는 출력값으로 바꾸세요

print(bfs(R,C,S,K))

    