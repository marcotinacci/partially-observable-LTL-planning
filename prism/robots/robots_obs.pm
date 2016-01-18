// ROBOT SCENARIO WITH OBSERVATIONS
// This scenario contains a robot moving in a simple shaped arena.
// The arena is a square DxD
mdp

// === CONSTANTS ===
const int D; // arena dimension
const int k; // steps number for formula
const int ix0 = 0;
const int iy0 = 0;
const int ix1 = 1;
const int iy1 = 1;
const int ix2 = 2;
const int iy2 = 2;

// === LABELS ===

label "collision" = see_h;
label "track" = see_something;
label "safe_track" = see_something & !see_h;

// === FORMULAS ===

formula see_h = (x0=x1 & y0=y1) | (x0=x2 & y0=y2);
formula see_n = (x0=x1 & y0=y1+1) | (x0=x2 & y0=y2+1);
formula see_e = (x0=x1+1 & y0=y1) | (x0=x2+1 & y0=y2);
formula see_w = (x0=x1 & y0=y1-1) | (x0=x2 & y0=y2-1);
formula see_s = (x0=x1-1 & y0=y1) | (x0=x2-1 & y0=y2);
formula see_something = see_h | see_n | see_e | see_w | see_s;

// === MODULES ===

// robot module
module robot
	x0 : [0..D-1] init ix0;
	y0 : [0..D-1] init iy0;

	// at most 2 basic observation at once
	[obs_empty] 	(!see_h & !see_n & !see_e & !see_w & !see_s) -> true;
	[obs_n] 	(!see_h & see_n & !see_e & !see_w & !see_s) -> true;
	[obs_e] 	(!see_h & !see_n & see_e & !see_w & !see_s) -> true;
	[obs_w] 	(!see_h & !see_n & !see_e & see_w & !see_s) -> true;
	[obs_s] 	(!see_h & !see_n & !see_e & !see_w & see_s) -> true;
	[obs_h] 	(see_h & !see_n & !see_e & !see_w & !see_s) -> true;
	[obs_ne] 	(!see_h & see_n & see_e & !see_w & !see_s) -> true;
	[obs_nw] 	(!see_h & see_n & !see_e & see_w & !see_s) -> true;
	[obs_ns] 	(!see_h & see_n & !see_e & !see_w & see_s) -> true;
	[obs_nh] 	(see_h & see_n & !see_e & !see_w & !see_s) -> true;
	[obs_ew] 	(!see_h & !see_n & see_e & see_w & !see_s) -> true;
	[obs_es] 	(!see_h & !see_n & see_e & !see_w & see_s) -> true;
	[obs_eh] 	(see_h & !see_n & see_e & !see_w & !see_s) -> true;
	[obs_ws] 	(!see_h & !see_n & !see_e & see_w & see_s) -> true;
	[obs_wh] 	(see_h & !see_n & !see_e & see_w & !see_s) -> true;
	[obs_sh] 	(see_h & !see_n & !see_e & !see_w & see_s) -> true;

	[act_n]	true -> (x0'=max(x0-1,0));
	[act_e]	true -> (y0'=min(y0+1,D-1));
	[act_w]	true -> (y0'=max(y0-1,0));
	[act_s]	true -> (x0'=min(x0+1,D-1));
	[act_h] true -> true;
endmodule

// random robot module
module RR1
	x1 : [0..D-1] init ix1;
	y1 : [0..D-1] init iy1;

	// can sense, move left, right or stand still
	[s1]	true -> 
		1/5 : (x1'=max(x1-1,0)) +
		1/5 : (y1'=min(y1+1,D-1)) +
		1/5 : (y1'=max(y1-1,0)) +
		1/5 : (x1'=min(x1+1,D-1)) +
		1/5 : true;
endmodule

// random robot replica
module RR2=RR1 [ x1=x2, y1=y2, s1=s2, ix1=ix2, iy1=iy2 ] endmodule

// coordinating module
module Synchronizer
	// turns: robot, RR1, RR2
	turn : [0..2] init 0; 
	observation: bool init true;
	
	// [<observation set>]
	[obs_empty]	(turn=0 & observation=true) -> (observation'=false);
	[obs_n]		(turn=0 & observation=true) -> (observation'=false);
	[obs_e]		(turn=0 & observation=true) -> (observation'=false);
	[obs_w]		(turn=0 & observation=true) -> (observation'=false);
	[obs_s]		(turn=0 & observation=true) -> (observation'=false);
	[obs_h]		(turn=0 & observation=true) -> (observation'=false);
	[obs_ne]	(turn=0 & observation=true) -> (observation'=false);
	[obs_nw]	(turn=0 & observation=true) -> (observation'=false);
	[obs_ns]	(turn=0 & observation=true) -> (observation'=false);
	[obs_nh]	(turn=0 & observation=true) -> (observation'=false);
	[obs_ew]	(turn=0 & observation=true) -> (observation'=false);
	[obs_es]	(turn=0 & observation=true) -> (observation'=false);
	[obs_eh]	(turn=0 & observation=true) -> (observation'=false);
	[obs_ws]	(turn=0 & observation=true) -> (observation'=false);
	[obs_wh]	(turn=0 & observation=true) -> (observation'=false);
	[obs_sh]	(turn=0 & observation=true) -> (observation'=false);

	// [<action set>]
	[act_n]	(turn=0 & observation=false) -> (turn'=1) & (observation'=true);
	[act_e]	(turn=0 & observation=false) -> (turn'=1) & (observation'=true);
	[act_w]	(turn=0 & observation=false) -> (turn'=1) & (observation'=true);
	[act_s]	(turn=0 & observation=false) -> (turn'=1) & (observation'=true);
	[act_h] (turn=0 & observation=false) -> (turn'=1) & (observation'=true);

	// [<coordination set>]
	[s1]	turn=1 -> (turn'=2);
	[s2]	turn=2 -> (turn'=0);
	
endmodule
