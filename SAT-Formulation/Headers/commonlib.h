#ifndef COMMON_H
#define COMMON_H
#include <iostream>
#include <tuple>
#include <vector>
#include <fstream>
#include <bits/stdc++.h>
using namespace std;

// int ClauseNo = 0;

int read(int &v1, int &v2, char *arg[]);
void convert(vector<vector<int>> &graph1, vector<vector<int>> &graph2, char *arg[]);

extern int si1, si2;
int Unique(vector<vector<int> > GraphE, vector<vector<int> > GraphP);
int Clauses(vector<vector<int> >GraphE, vector<vector<int> >GraphP);
void outwrite(string s, string s2);
#endif
