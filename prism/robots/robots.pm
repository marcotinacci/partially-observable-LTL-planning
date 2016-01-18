// ROBOT SCENARIO
// This scenario contains a robot moving in a simple shaped arena.
// The arena is a square DxD
mdp

// === CONSTANTS ===
// grid dimension
const int D = 5;
const int k;
const int ix0 = 2;
const int iy0 = 1;
const int ix1 = 3;
const int iy1 = 3;

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

// fully nondeterministic robot module
module robot
	x0 : [0..D-1] init ix0;
	y0 : [0..D-1] init iy0;

	// can sense, move left, right or stand still
	[act_n]	true -> (x0'=max(x0-1,0));
	[act_e]	true -> (y0'=min(y0+1,D-1));
	[act_w]	true -> (y0'=max(y0-1,0));
	[act_s]	true -> (x0'=min(x0+1,D-1));
	[act_h] true -> true;
endmodule

// fully probabilistic robot module
// cant see walls or other robots
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

module RR2=RR1 [ x1=x2, y1=y2, s1=s2 ] endmodule

// arena environment module
module Serializator
	// turns: robot, RR1, RR2
	turn : [0..2] init 0; 
	
	[act_n]	turn=0 -> (turn'=1);
	[act_e]	turn=0 -> (turn'=1);
	[act_w]	turn=0 -> (turn'=1);
	[act_s]	turn=0 -> (turn'=1);
	[act_h]	turn=0 -> (turn'=1);

	[s1]	turn=1 -> (turn'=2);
	[s2]	turn=2 -> (turn'=0);

endmodule
