/* File: ga_player.i */
%module ga_player
%include cpointer.i


%{
#define SWIG_FILE_WITH_INIT
#include <stdlib.h>
#include <stdio.h>
#include "ga_player.h"
#include "client.h"
#include "sysdep.h"
#include "game.h"
extern int our_id;
extern char *address;
extern char *name;
//extern Game *the_game;
//extern PlayerP our_player;
extern char *l;
extern char buf[1000];
%}

/*pointer functions*/
%pointer_functions(Game, gamet);
void usage(char *pname,char *msg);
void get_inits(double c,double h,double m,double s);
void get_address(char *addr);
void ga_player_run(int ids,char *nm);
int despatch_line(char *line);
Game  *client_init(char *address);
int client_connect(Game *g, int id, char *name);

extern int our_id;
extern char *address;
extern char *name;
//extern Game *the_game;
//extern PlayerP our_player;
//extern char *l;
//extern char buf[1000];


