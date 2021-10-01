#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#include "huffman.h"
#include "bitarray.h"
#include "priority_queue.h"

#define IS_LEAF(p) (p->left == NULL || p->right == NULL)


struct TreeNode * create_huffman_tree(int table[]) {
    int freq;
    struct TreeNode * node;
    struct TreeNode * left;
    struct TreeNode * right;


    PriorityQueue * queue = create_pqueue();

    for (int i = 0; i < (1 << BYTESIZE); i++) {
        if (table[i] != 0) {
            node = create_tree_node(i, table[i]);
            pqueue_insert(queue, node, table[i]);
        }
    }

    while (queue->size > 1) {
        left   = pqueue_get_min(queue);
        right  = pqueue_get_min(queue);
        freq   = left->freq + right->freq;

        node = create_tree_node(BYTESIZE, freq);
        node->left = left;
        node->right = right;
        left->father = node;
        right->father = node;
        pqueue_insert(queue, node, freq);
    }

    return pqueue_get_min(queue);
}

struct TreeNode * create_tree_node(int data, int freq) {
    struct TreeNode * node = malloc(sizeof(struct TreeNode));
    node->data = data;
    node->freq = freq;
    node->left = NULL;// FHD = 1920 x 1080

    node->right = NULL;
    node->father = NULL;
    return node;
}

void print_tree(struct TreeNode * tree) {
    if (IS_LEAF(tree)) {
        printf("%c(%d) \n", tree->data, tree->freq);
    } else {
        printf("(%d) \n", tree->freq);
        print_tree(tree->left);
        print_tree(tree->right);
    }
}

struct TreeNode * tree_find(struct TreeNode * tree, int value) {
    /* note that when the priority is equal for every
     * content then it is a regular queue */
    struct TreeNode * node = tree;
    PriorityQueue * queue = create_pqueue();
    pqueue_insert(queue, node, 0);

    while (queue->size > 0) {
        node = pqueue_get_max(queue);

        if (node->data == value)
            break;
        
        if (!IS_LEAF(node)) {
            pqueue_insert(queue, node->left, 0);
            pqueue_insert(queue, node->right, 0);
        }
    }

    if (node->data != value) {
        printf("ERROR: Value [%c] not found on tree. \n", value);
        exit(-1);
    } else {
        return node;
    }
}

int tree_level(struct TreeNode * tree) {
    int level = 0;
    struct TreeNode * node = tree;
    while (node->father != NULL) {
        level++;
        node = node->father;
    }
    return level;
}

int * create_huffman_table(char data[], int size) {
    int * table = calloc(1 << BYTESIZE, sizeof(int));
    for (int i=0; i<size; i++) {
        table[(int) data[i]]++;
    }
    return table;
}

struct BitArray * huffman_encode(struct BitArray * array) {
    int i, j; 
    int * table;
    struct TreeNode * tree;
    struct TreeNode * node;
    struct BitArray * encoded;
    
    table = create_huffman_table(array->data, BITTOBYTE(array->size));
    tree  = create_huffman_tree(table);
    encoded = bitarray_create(array->max_size);

    /* compiler god, please dont let it be too slow
     * i cant think in a better aproach */
    for (i = 0; i < BITTOBYTE(array->size); i++) {
        node = tree_find(tree, array->data[i]);
        for (j = tree_level(node) - 1; j >= 0; j--) {
            bitarray_append_bit((node->father->right == node), encoded);
            node = node->father;
        }
    }   
    return encoded;
}

struct BitArray * huffman_decode(struct TreeNode * tree, struct BitArray * encoded) {
    int index = 0;
    struct TreeNode * node;
    struct BitArray * decoded = bitarray_create(BITTOBYTE(encoded->max_size));

    while (index < encoded->size) {
        node = tree;
        while (!IS_LEAF(node)) {
            node = bitarray_get_bit(index, encoded) ? node->right : node->left;
            index++;
        }
        bitarray_append_byte(node->data, decoded);
    }
    
    return decoded;
}