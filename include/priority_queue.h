#ifndef __PRIORITY_QUEUE_H__
#define __PRIORITY_QUEUE_H__

struct QueueNode {
    void * data;
    int priority;
    struct QueueNode * next;
};

typedef struct {
    int size;
    struct QueueNode * head;
} PriorityQueue;


PriorityQueue * create_pqueue();

void pqueue_insert(PriorityQueue * queue, void * data, int priority);

void * pqueue_get(PriorityQueue * queue);

#endif