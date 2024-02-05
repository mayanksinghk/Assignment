#ifndef MINIMAX_H
#define MINIMAX_H

#include "commonlib.h"
#include "node.h"

int Evaluation(int a, int b, int c, int d);
tuple<int,MOVE> minimax( Node* node, bool maximizingPlayer, int alpha, int beta,bool amBlack);

// Initial values of
// Aplha and Beta
const int MAX = 1000;
const int MIN = -1000;

#endif
