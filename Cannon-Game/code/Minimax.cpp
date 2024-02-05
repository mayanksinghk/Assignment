#include "minimax.h"
#include "Evaluation.h"

int Evaluation(int a, int b, int c, int d){
    return a + b + c + d;
}


tuple<int,MOVE> minimax( Node *node, bool maximizingPlayer, int alpha, int beta,bool amBlack) {

  vector<Node*> list = (*node).GetChildren();

    if ((*node).GetChildren().size() == 0){

        vector<vector<int> > board = (*node).GetBoard();
        int typ;
        if(amBlack){
            typ = 1;
        }else{
            typ = -1;
        }
        float t = Eval(board, typ);
        (*node).SetEval(t);
        // cout<<t<<" "<<(*node).GetEval()<<endl;
        // print_move((*node).GetMove());
        tuple<int,MOVE> tmp = make_tuple(t,(*node).GetMove());
        return tmp;

    }

    if (maximizingPlayer) {
        int best = MIN;
        MOVE best_move;
        // Recur for all the child
        for (int i = 0; i < list.size(); i++) {

            tuple<int,MOVE> tup_val = minimax( (list[i]), false, alpha, beta,amBlack);
            int val = get<0>(tup_val);
            if (best<=val){
              best_move = (*(list[i])).GetMove();
            }
            best = max(best, val);

            alpha = max(alpha, best);
            // Alpha Beta Pruning
            if (beta <= alpha)
                break;
        }
        (*node).SetEval(best);
        // cout<<best<<" "<<(*node).GetEval()<<endl;
        tuple<int,MOVE> tmp_tup = make_tuple(best,best_move);
        return tmp_tup;
    }else{
        int best = MAX;
        MOVE best_move;

        // Recur for left and
        // right children
        for (int i = 0; i < list.size(); i++)
        {
            tuple<int,MOVE> tup_val = minimax( (list[i]),true, alpha, beta,amBlack);
            int val = get<0>(tup_val);

            if (best>=val){
              best_move = (*(list[i])).GetMove();
            }
            best = min(best, val);
            beta = min(beta, best);
            // Alpha Beta Pruning
            if (beta <= alpha)
                break;
        }
        (*node).SetEval(best);
        // cout<<best<<" "<<(*node).GetEval()<<endl;
        tuple<int,MOVE> tmp_tup = make_tuple(best,best_move);
        return tmp_tup;
    }
}
