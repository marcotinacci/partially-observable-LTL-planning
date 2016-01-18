// ROBOT SCENARIO WITH OBSERVATIONS
// This scenario contains a robot moving in a simple shaped arena.
// The arena is a square DxD
mdp

// === CONSTANTS ===
const int D; // arena dimension
const int k; // steps number for formula
const int ix0 = 0;
const int iy0 = 0;
const int ix1 = floor(D/2);
const int iy1 = floor(D/2);
const int ix2 = D-1;
const int iy2 = D-1;
const int ix3 = 0;
const int iy3 = D-1;
const int ix4 = D-1;
const int iy4 = 0;

// === LABELS ===

label "collision" = see_h;
label "track" = see_something;
label "safe_track" = see_something & !see_h;

// === FORMULAS ===

formula see_h = (x0=x1 & y0=y1) | (x0=x2 & y0=y2) | (x0=x3 & y0=y3) | (x0=x4 & y0=y4);
formula see_n = (x0=x1 & y0=y1+1) | (x0=x2 & y0=y2+1) | (x0=x3 & y0=y3+1) | (x0=x4 & y0=y4+1);
formula see_e = (x0=x1+1 & y0=y1) | (x0=x2+1 & y0=y2) | (x0=x3+1 & y0=y3) | (x0=x4+1 & y0=y4);
formula see_w = (x0=x1 & y0=y1-1) | (x0=x2 & y0=y2-1) | (x0=x3 & y0=y3-1) | (x0=x4 & y0=y4-1);
formula see_s = (x0=x1-1 & y0=y1) | (x0=x2-1 & y0=y2) | (x0=x3-1 & y0=y3) | (x0=x4-1 & y0=y4);
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

	[obs_wsh] 	(see_h & !see_n & !see_e & see_w & see_s) -> true;
	[obs_esh] 	(see_h & !see_n & see_e & !see_w & see_s) -> true;
	[obs_ewh] 	(see_h & !see_n & see_e & see_w & !see_s) -> true;
	[obs_ews] 	(!see_h & !see_n & see_e & see_w & see_s) -> true;
	[obs_nsh] 	(see_h & see_n & !see_e & !see_w & see_s) -> true;
	[obs_nwh] 	(see_h & see_n & !see_e & see_w & !see_s) -> true;
	[obs_nws] 	(!see_h & see_n & !see_e & see_w & see_s) -> true;
	[obs_neh] 	(see_h & see_n & see_e & !see_w & !see_s) -> true;
	[obs_nes] 	(!see_h & see_n & see_e & !see_w & see_s) -> true;
	[obs_new] 	(!see_h & see_n & see_e & see_w & !see_s) -> true;

	[obs_news] 	(!see_h & see_n & see_e & see_w & see_s) -> true;
	[obs_ewsh] 	(see_h & !see_n & see_e & see_w & see_s) -> true;
	[obs_wshn] 	(see_h & see_n & !see_e & see_w & see_s) -> true;
	[obs_nesh] 	(see_h & see_n & see_e & !see_w & see_s) -> true;
	[obs_newh] 	(see_h & see_n & see_e & see_w & !see_s) -> true;

//	[obs_newsh] 	(see_h & see_n & see_e & see_w & see_s) -> true;

	// actions
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
module RR3=RR1 [ x1=x3, y1=y3, s1=s3, ix1=ix3, iy1=iy3 ] endmodule
module RR4=RR1 [ x1=x4, y1=y4, s1=s4, ix1=ix4, iy1=iy4 ] endmodule

// coordinating module
module Synchronizer
	// turns: robot, RR1, RR2, RR3, RR4
	turn : [0..4] init 0; 
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
	[obs_wsh]	(turn=0 & observation=true) -> (observation'=false);
	[obs_esh]	(turn=0 & observation=true) -> (observation'=false);
	[obs_ewh]	(turn=0 & observation=true) -> (observation'=false);
	[obs_ews]	(turn=0 & observation=true) -> (observation'=false);
	[obs_nsh]	(turn=0 & observation=true) -> (observation'=false);
	[obs_nwh]	(turn=0 & observation=true) -> (observation'=false);
	[obs_nws]	(turn=0 & observation=true) -> (observation'=false);
	[obs_neh]	(turn=0 & observation=true) -> (observation'=false);
	[obs_nes]	(turn=0 & observation=true) -> (observation'=false);
	[obs_new]	(turn=0 & observation=true) -> (observation'=false);
	[obs_news]	(turn=0 & observation=true) -> (observation'=false);
	[obs_ewsh]	(turn=0 & observation=true) -> (observation'=false);
	[obs_wshn]	(turn=0 & observation=true) -> (observation'=false);
	[obs_nesh]	(turn=0 & observation=true) -> (observation'=false);
	[obs_newh]	(turn=0 & observation=true) -> (observation'=false);
//	[obs_newsh]	(turn=0 & observation=true) -> (observation'=false);

	// [<action set>]
	[act_n]	(turn=0 & observation=false) -> (turn'=1) & (observation'=true);
	[act_e]	(turn=0 & observation=false) -> (turn'=1) & (observation'=true);
	[act_w]	(turn=0 & observation=false) -> (turn'=1) & (observation'=true);
	[act_s]	(turn=0 & observation=false) -> (turn'=1) & (observation'=true);
	[act_h] (turn=0 & observation=false) -> (turn'=1) & (observation'=true);

	// [<coordination set>]
	[s1]	turn=1 -> (turn'=2);
	[s2]	turn=2 -> (turn'=3);
	[s3]	turn=3 -> (turn'=4);
	[s4]	turn=4 -> (turn'=0);
	
endmodule
