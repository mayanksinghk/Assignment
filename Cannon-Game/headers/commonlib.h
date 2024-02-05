#ifndef COMMON_H
#define COMMON_H
#include <iostream>
#include <tuple>
#include <algorithm>
#include <vector>

using namespace std;

struct coord{
  int x,y;
};


typedef tuple<coord,coord,coord> CANNON;
typedef tuple<char,int,int,char,int,int> MOVE;

bool contains(coord ele, vector<coord> list);
vector<coord> moves_filter(vector<coord> moves, vector<coord> soldier_list, int n = 8, int m = 8);
tuple<vector<coord>,vector<coord> > create_th_list(int b_size);


void print_board(vector<vector<int> >);
void print_cannon(vector<CANNON>);
void print_soldier(vector<coord>);
void print_move(MOVE m);
void printerr_move(MOVE m);

int AttackLine(vector<vector<int> > board, int type);
#endif
