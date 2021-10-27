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
            pqueue_append(queue, node, table[i]);
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
        pqueue_append(queue, node, freq);
    }

    return pqueue_get_min(queue);
}

struct TreeNode * create_tree_node(int data, int freq) {
    struct TreeNode * tree = malloc(sizeof(struct TreeNode));
    tree->data = data;
    tree->freq = freq;
    tree->left = NULL;
    tree->right = NULL;
    tree->father = NULL;
    return tree;
}

int delete_tree(struct TreeNode * tree) {
    if (tree->left != NULL) {
        delete_tree(tree->left);
    }

    if (tree->right != NULL) {
        delete_tree(tree->right);
    }

    free(tree);

    return 0;
}

void print_tree(struct TreeNode * tree) {
    if (IS_LEAF(tree)) {
        printf("%c(%d) \n", tree->data, tree->freq);
    } 
    else {
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
    pqueue_append(queue, node, 0);

    while (queue->size > 0) {
        node = pqueue_get_max(queue);

        if (node->data == value)
            break;
        
        if (!IS_LEAF(node)) {
            pqueue_append(queue, node->left, 0);
            pqueue_append(queue, node->right, 0);
        }
    }

    if (node->data != value) {
        printf("ERROR: Value [%d] not found on tree. \n", value);
        exit(-1);
    } 
    else {
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

int * create_huffman_table(byte_t data[], int size) {
    byte_t index;
    int * table = calloc(256, sizeof(int));

    for (int i = 0; i < size; i++) {
        index = data[i];
        table[index]++;
    }
    return table;
}

struct BitArray * huffman_encode(int table[], struct BitArray * decoded) {
    int i, j;
    int size;
    int tmp[255];
    struct TreeNode * tree;
    struct TreeNode * node;
    struct BitArray * encoded;
    
    tree  = create_huffman_tree(table);
    encoded = create_bitarray(decoded->max_size);

    // compiler god, please dont let it be too slow
    for (i = 0; i < bitarray_size_bytes(decoded); i++) {
        node = tree_find(tree, decoded->data[i]);

        // find path from node to root
        for (size = 0; node->father != NULL; size++) {
            tmp[size] = (node->father->right == node);
            node = node->father;
        }

        // append path from root to node
        for (j = (size - 1); j >= 0; j--) {
            bitarray_append_bit(tmp[j], encoded);
        }
    }   

    return encoded;
}

struct BitArray * huffman_decode(int table[], struct BitArray * encoded) {
    int index;
    struct TreeNode * tree;
    struct TreeNode * node;
    struct BitArray * decoded;
    
    tree  = create_huffman_tree(table);
    decoded = create_bitarray(encoded->max_size);

    index = 0;

    while (index < bitarray_size_bits(encoded)) {
        node = tree;

        while (!IS_LEAF(node)) {
            if (bitarray_get_bit(index, encoded)) {
                node = node->right;
            } 
            else {
                node = node->left;
            }
            index++;
        }

        // check array boundaries
        if (index < bitarray_size_bits(encoded)) {
            bitarray_append_byte((byte_t) node->data, decoded);
        }

    }

    return decoded;
}