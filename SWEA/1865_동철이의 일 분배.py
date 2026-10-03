"""
[SWEA 1865] 동철이의 일 분배
난이도: D4 | 유형: 백트래킹, 가지치기 | 풀이일: 2026-10-03

[문제 요약]
N명의 직원
N개의 할일

직원들의 번호가 1부터 N까지 매겨져 있고 
해야할 일에도 1부터N까지 매겨져 있음

주어진 일이 모두 성공할 확률의 최댓값 구하기


"""
N = 0
total_per = 0
def dfs(grid,visited, index, current_per):
   global total_per
   if current_per <= total_per:
      return
   if index == N:
      total_per = max(current_per, total_per)
      return
   
   for work in range(N):
      if visited[work] == True or grid[index][work] == 0:
         continue
      visited[work] = True
      dfs(grid, visited, index + 1, current_per * grid[index][work]/100)
      visited[work] = False


T = int(input())

for test_case in range(1, T + 1):
   total_per = 0
   N = int(input())
   grid = [list(map(int, input().split()))for _ in range(N)]
   visited = [False] * N

   dfs(grid, visited, 0, 100)
   print(f"#{test_case} {total_per:.6f}")

