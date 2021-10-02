#include <stdio.h>
#include <stdlib.h>
#include "priority_queue.h"

PriorityQueue * create_pqueue() {
    PriorityQueue * queue = malloc(sizeof(PriorityQueue));
    queue->size = 0;
    queue->head = NULL;
    return queue;
}

struct QueueNode * create_pqueue_node(void * data, int priority) {
    struct QueueNode * node = malloc(sizeof(struct QueueNode));
    node->data = data;
    node->priority = priority;
    node->next = NULL;
    node->last = NULL;
    return node;
}

int delete_pqueue(PriorityQueue * pqueue) {
    delete_pqueue_node(pqueue->head);
    free(pqueue);
    return 0;
}

int delete_pqueue_node(struct QueueNode * node) {
    if (node->next != NULL) {
        delete_pqueue_node(node->next);
    }
    free(node);
    return 0;
}

void pqueue_append(PriorityQueue * queue, void * data, int priority) {
    struct QueueNode * n;
    struct QueueNode * new = create_pqueue_node(data, priority);

    if (queue->size == 0) {
        queue->head = new;
        queue->tail = new;
        queue->size++;
        return;
    }

    n = queue->head;
    while ((n != NULL) && (n->priority < new->priority)) {
        n = n->next;
    }

    if (n == queue->head) { 
        // head
        new->next = queue->head;
        queue->head->last = new;
        queue->head = new;
    }
    else if (n == NULL) {
        // tail
        new->last = queue->tail;
        queue->tail->next = new;
        queue->tail = new;
    }
    else {
        // middle
        new->next = n;
        new->last = n->last;
        new->next->last = new;
        new->last->next = new;
    }
    queue->size++;
}

void * pqueue_get_min(PriorityQueue * queue) {
    if (queue->size == 0) {
        printf("ERROR. The priority queue is empty. \n");
        exit(-1);
    }

    queue->size--;
    void * out = queue->head->data;
    struct QueueNode * del = queue->head;
    queue->head = queue->head->next;
    free(del);
    return out;    
}

void * pqueue_get_max(PriorityQueue * queue) {
    if (queue->size == 0) {
        printf("ERROR. The priority queue is empty. \n");
        exit(-1);
    }

    queue->size--;
    void * out = queue->tail->data;
    struct QueueNode * del = queue->tail;
    queue->tail = queue->tail->last;
    free(del);
    return out;    
}
