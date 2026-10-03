"""
[JUNGOL 1681] 해밀턴 순환회로
문제 링크: https://jungol.co.kr/problem/1681
난이도: - | 유형: 백트래킹, 가지치기 | 풀이일: 2026-10-03

[막혔던 점 / 실수]
- loc_visited = True 로 리스트 자체를 덮어씀 → loc_visited[loc]
- 출발점(회사)도 방문 처리하고 count=1부터 시작해야 함

[문제 요약]
해밀턴 순환회로
#1681
방문순서 정하기

배달해야하는 장소의 수 1 <= N <= 13

회사는 1번
단방향으로 가기위한 비용ㅇ임
gird [1][2] : 1->2로 가기위한 비용

이동할 수 없다면 비용을 0
모든 장소를 한 번씩 들러 물건을 배달하고 회사에 돌아오기 위한 최소 비용

장소와 장소기준으로 
끝까지 가서 돌아올때 조건 체크

횟수만큼 다 돌았는지 확인ㄴ


"""
# 들려야하는 장소의 수
N = int(input())
grid = [list(map(int, input().split()))for _ in range(N)]
min_weight = 1000
loc_visited = [False] * N

def find_min_path(cur, count, current_weight,loc_visited):
    global min_weight
    
    if current_weight >= min_weight:
            return
    
    if count == N:
        if grid[cur][0] ==0:
            return
        min_weight = min(min_weight, current_weight + grid[cur][0])
        return
    
    for loc in range(N):
        if loc == cur:
              continue
        if grid[cur][loc] ==0:
              continue
        if loc_visited[loc] == True:
             continue
        loc_visited[loc] = True
        find_min_path(loc, count+1, current_weight + grid[cur][loc],loc_visited)
        loc_visited[loc] = False 
    
#출발점도 이미 방문한 곳
# 그러니 방문처리하고 count+1
loc_visited[0] = True
find_min_path(0,1,0,loc_visited)
print(min_weight)