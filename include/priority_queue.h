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

int delete_pqueue(PriorityQueue * pqueue);

int delete_pqueue_node(struct QueueNode * node);

void pqueue_append(PriorityQueue * queue, void * data, int priority);

void * pqueue_get_min(PriorityQueue * queue);

void * pqueue_get_max(PriorityQueue * queue);

#endif