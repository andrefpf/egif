#ifndef __HUFFMAN_H__
#define __HUFFMAN_H__


struct TreeNode {
    int data;
    int freq;
    struct TreeNode * left;
    struct TreeNode * right;
    struct TreeNode * father;
};


struct TreeNode * create_huffman_tree(int table[]);

struct TreeNode * create_tree_node(int data, int freq);

struct TreeNode * tree_find(struct TreeNode * tree, int value);

int delete_tree(struct TreeNode * tree);

int tree_level(struct TreeNode * tree);

int * create_huffman_table(char data[], int size);

struct BitArray * huffman_encode(struct BitArray * array);

struct BitArray * huffman_decode(struct TreeNode * tree, struct BitArray * encoded);

#endif