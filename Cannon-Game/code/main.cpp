#include "minimax.h"
#include "tree.h"
#include <cmath>
#include <time.h>
// #include <chrono>
int get_depth(int time_spent,int dur,int curr_depth=2){
  int t1=4,t2=1;
  if (dur>=t1){
    curr_depth--;
  }else if(dur<=t2){
    curr_depth++;
  }
  return curr_depth;
}
int main(int argc, char const *argv[]) {
  int player,n,m,tl,b_size;
  cin >> player;
  cin >> n;
  cin >> m;
  cin >> tl;
  if (n == 8 && m == 8){
    b_size=1;
  }else if (n == 10 && m == 8){
    b_size=2;
  }else{
    b_size=3;
  }

  char f,s;
  int a,b,c,d;
  bool my_turn,amBlack;
  Node curr_root;
  if (player == 1){
      my_turn = true; //my_color = black
      curr_root.SetBlack(true);
      amBlack=true;
  }else{
    my_turn = false; //my_color = white
    curr_root.SetBlack(false);
    amBlack=false;
  }

  vector<vector<int> >  board = initialise(b_size);
  long int time_spent = 0, dur = 0,depth=2; 
  int my_move=0;
  while (true){
    if (my_turn == false){
      char t[10];
      cin >> f;
      cin >> a;
      cin >> b;
      cin >> s;
      cin >> c;
      cin >> d;
      
      MOVE mv  = make_tuple(f,a,b,s,c,d);
      cerr<<"Move from computer: ";
      printerr_move(mv);
      cerr<<endl;
      board = Update_board(mv,board);
      my_turn = true;
    }else{
      time_t curr = time(0);      
      MOVE mv;
        if (my_move==0){
          if (amBlack){
          if (n==10 && m==10){
            mv = make_tuple('S',6,n-1,'M',7,n-2);
          }else{
            mv = make_tuple('S',4,n-1,'M',5,n-2);
          }
          }else{
          if (n==10 && m==10){
            mv = make_tuple('S',7,0,'M',8,1);
          }else{
            mv = make_tuple('S',5,0,'M',6,1);
          }            
          }
        }else if (my_move==1){
          if (amBlack){
          mv = make_tuple('S',2,n-1,'M',3,n-2);
          }else{
          mv = make_tuple('S',3,0,'M',2,1);
          }
        }else{
        if (m==10 && n==10 && my_move == 2){
          if (amBlack){
            mv = make_tuple('S',4,n-1,'M',4,n-4);
          }else{
            mv = make_tuple('S',5,0,'M',5,3);
          }
        }else{
        depth = get_depth(time_spent,dur,depth);        
        curr_root.SetBoard(board);
        create_tree(&curr_root,depth);
        tuple<int,MOVE> best_tuple = minimax(&curr_root,true,-1000,1000,amBlack);
        mv = get<1>(best_tuple);
        }
      }
      print_move(mv);
      cerr<<"Current Depth "<<depth<<endl;
      board = Update_board(mv,board);
      my_turn = false;
      
      time_t fin = time(0);
      dur = difftime(fin,curr);
      time_spent+=dur;
      my_move++;

    }
  }


  return 0;
}
