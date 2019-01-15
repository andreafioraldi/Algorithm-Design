#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define AT(mat, x, y) (mat)[(x)*2 + (y)]
#define MIN(a, b) ((a) <= (b) ? (a) : (b))

#define HIRED 1
#define FREELANCE 0

struct Task
{
    int time;
    int cost;
};

int min_cost_aux(int last_worker_type, int t, int T, int s, int C, int S, int* c, int* matrix)
{
  if(t == T)
    return 0;
  
  if(AT(matrix, t+1, HIRED) == -1)
    AT(matrix, t+1, HIRED) = min_cost_aux(HIRED, t+1, T, s, C, S, c, matrix);
  if(AT(matrix, t+1, FREELANCE) == -1)
    AT(matrix, t+1, FREELANCE) = min_cost_aux(FREELANCE, t+1, T, s, C, S, c, matrix);
  
  int x,y;
  if(last_worker_type == HIRED) {
    x = s + AT(matrix, t+1, HIRED);
    y = S + c[t] + AT(matrix, t+1, FREELANCE);
  }
  else {
    x = C + s + AT(matrix, t+1, HIRED);
    y = c[t] + AT(matrix, t+1, FREELANCE);
  }
  
  return MIN(x, y);
}


int min_cost(int T, int s, int C, int S, struct Task* tasks, int task_num)
{
    int* matrix = calloc(sizeof(int), (2*T +2));
    memset(matrix, -1, sizeof(int)*2*T);
    
    int* c = calloc(sizeof(struct Task), T);
    int i, j;
    for(i = 0, j = 0; i < T; ++i) {
        while(j < task_num && tasks[j].time == i) {
            c[i] += tasks[j].cost;
            ++j;
        }
    }
    
    int r = min_cost_aux(FREELANCE, 0, T, s, C, S, c, matrix);
    
    free(matrix);
    free(c);
    return r;
}

int main()
{
    struct Task tasks[] = {{0,3},{0,2},{1,6},{4,1}};
    int sol = min_cost(5, 2, 2, 3, tasks, 4);
    
    printf("%d\n", sol); //10
    return 0;
}
