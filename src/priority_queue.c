#include <stdlib.h>
#include "priority_queue.h"

PriorityQueue * create_pqueue() {
    PriorityQueue * queue = malloc(sizeof(PriorityQueue));
    queue->size = 0;
    queue->head = NULL;
    return queue;
}

void pqueue_insert(PriorityQueue * queue, void * data, int priority) {
    struct QueueNode *l, *n;
    struct QueueNode * new = malloc(sizeof(struct QueueNode));

    new->data = data;
    new->priority = priority;
    n = queue->head;

    // If it should be the first element just replace the head
    if ((queue->size == 0) || (new->priority > n->priority)) {
        queue->head = new;
        new->next = n;
        return;
    }

    do {
        l = n;
        n = n->next;
    } while ((n != NULL) && (new->priority <= n->priority));

    l->next = new;
    new->next = n;
    queue->size++;
}

void * pqueue_get(PriorityQueue * queue) {
    if (queue->size == 0) {
        exit(-1);
    }

    struct QueueNode * last_head = queue->head;
    void * out = last_head->data;
    
    queue->head = queue->head->next;
    free(last_head);
    return out;
}