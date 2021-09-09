#ifndef __PRIORITY_QUEUE_H__
#define __PRIORITY_QUEUE_H__

struct QueueNode {
    void * data;
    int priority;
    struct QueueNode * next;
    struct QueueNode * last;
};

typedef struct {
    int size;
    struct QueueNode * head;
    struct QueueNode * tail;
} PriorityQueue;


PriorityQueue * create_pqueue();

struct QueueNode * create_pqueue_node();

void pqueue_insert(PriorityQueue * queue, void * data, int priority);

void * pqueue_get_min(PriorityQueue * queue);

void * pqueue_get_max(PriorityQueue * queue);

#endif