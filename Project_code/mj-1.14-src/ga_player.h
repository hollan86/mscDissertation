#include "game.h"
#include "client.h"
#include "sysdep.h"
#include "tiles.h"

extern int our_id;
extern char *address;
extern char *name;
extern Game *the_game;
//=========================================================================



/* is this tile a doubling tile (or scoring pair) */
#define is_doubler(t) (is_dragon(t) || (is_wind(t) && \
 (suit_of(t) == our_player->wind || suit_of(t) == the_game->round)))

//Game *the_game;
//int our_id = 0;
extern PlayerP our_player;
extern seats our_seat;

char *password;

//static FILE *debugf;

/* New style strategy */
typedef struct {
  double chowness; /* how much do we like/dislike chows? 
		      From -1.0 (no chows) to +1.0 (no pungs) */
  double hiddenness; /* how much do we want to keep things concealed?
			From 0.0 (don't care) to 1.0 (absolutely no claims) */
  double majorness; /* are we trying to get all majors? 
		       From 0.0 (don't care) to 1.0 (discard all minors) */
  double suitness; /* are we trying to collect one suit? From 0.0 to 1.0 */
  TileSuit suit;   /* if so, which? */
} strategy;

/* values to try out */
typedef enum { chowness, hiddenness, majorness, suitness } stratparamtype;
//HERE

/* routine to parse a comma separated list of floats into
   the given strat param. Return num of comps, or -1 on error */


strategy curstrat;
/* These are names for computed strategy values. See the awful mess
   below... */
enum {pungbase,pairbase,chowbase,seqbase,sglbase,
      partpung,partchow,exposedpungpenalty,exposedchowpenalty,
      suitfactor, mjbonus, kongbonus,weight};

/* the value of a new strategy must exceed the current
   by this amount for it to be chosen */
 


/* Used to note availability of tiles */
int tilesleft[MaxTile];
/* track discards of player to right */
int rightdiscs[MaxTile]; /* disc_ser of last of each tile discarded */
int strategy_chosen;
int despatch_line(char *line);
void do_something(void);
void check_discard(PlayerP p,strategy *strat,int closed_kong);
Tile decide_discard(PlayerP p, double *score, strategy *newstrat);
void update_tilesleft(CMsgUnion *m);
void maybe_switch_strategy(strategy *strat);
double eval(Tile *tp, strategy *strat, double *stratpoints,int reclevel, int *ninc, int *npr, double *breadth);
double evalhand(PlayerP p, strategy *strat);
int chances_to_win(PlayerP p);
/* copy old tile array into new */
#define tcopy(new,old) memcpy((void *)new,(void *)old,(MAX_CONCEALED+1)*sizeof(Tile))
/* Convenience function */
#define send_packet(m) client_send_packet(the_game,(PMsgMsg *)m)

//=========================================================================
void usage(char *pname,char *msg);
void get_inits(double c,double h,double m,double s);
void get_address(char *addr);
void ga_player_run(int ids,char *nm);
int despatch_line(char *line);

//extern Game  *client_init(char *address);




