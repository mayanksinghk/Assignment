#ifndef NODE_H
#define NODE_H

#include "next_moves.h"
#include "cannon_list.h"


class Node{
    private:
      vector<vector<int> > board_config;
      vector<Node*> children;
      MOVE move;
      bool black = true;
      float eval;
      // Node parent;
      // bool is_root;
    public:
        void SetBoard(vector<vector<int> > temp);
        void SetChildren();
        void SetBlack(bool t);
        void SetMove(MOVE m);
        Node* newNode(vector<vector<int> > new_board, MOVE move, bool black );
        void SetEval(float t);

        // void SetParent(Node parent_node);

        bool GetBlack(){
          return black;
        }
        vector<vector<int> >GetBoard(){
          return board_config;
        }
        vector<Node*> GetChildren(){
          return children;
        }

        float GetEval(){
          return eval;
        }
        MOVE GetMove(){
          return move;
        }

};


#endif
