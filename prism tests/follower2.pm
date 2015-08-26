// ROBOT SCENARIO
// This scenario contains a robot moving in a simple shaped arena.
// The arena is a line nx1

mdp

// === CONSTANTS ===
// grid dimension
const int DIM =5;
const int k;
// === INIT ===

//init 
//	rpos=1 & 
//	dpos=DIM/2 & 
//	choice=0 & 
//	token=true
//endinit

// === LABELS ===

label "collision" = rpos=d1pos | rpos=d2pos;
label "detect_left" = rpos=d1pos-1 | rpos=d2pos-1;
label "detect_right" = rpos=d1pos+1 | rpos=d2pos+1;

// === REWARDS ===

rewards
	[] detect_left : 1;
	[] detect_right : 1;
	[] collision : 1;
endrewards

// === FORMULAS ===

formula collision = rpos=d1pos | rpos=d2pos;
formula detect_left = rpos=d1pos-1 | rpos=d2pos-1;
formula detect_right = rpos=d1pos+1 | rpos=d2pos+1;

// === MODULES ===

// fully nondeterministic robot module
module robot
	// can move left, right or stand still
	[left]	!detect_left  -> true;
	[right]	!detect_right -> true;
	[stand]	true	      -> true;

endmodule

// fully probabilistic robot module
// cant see walls or other robots
module d1
	c1 : [0..3] init 0; // stand still, left, right
	// can move at random left or right or stand still
	[] c1=0 -> 1/3 : (c1'=1) + 1/3 : (c1'=2) + 1/3 : (c1'=3);
	[s1] c1=1 -> (c1'=0);
	[l1] c1=2 -> (c1'=0);
	[r1] c1=3 -> (c1'=0);
endmodule

module d2=d1 [ c1=c2, b1=b2, s1=s2, l1=l2, r1=r2 ] endmodule

// arena environment module
module arena

	rpos : [1..DIM] init 3; // robot position
	d1pos : [1..DIM] init 1; // drunk position
	d2pos : [1..DIM] init 5; // drunk position

	turn : [1..3] init 1; // turns: robot, d1, d2

	// robot actions
	[left] turn=1 & rpos > 1 -> (rpos'=rpos-1) & (turn'=2);
	[left] turn=1 & rpos = 1 -> (turn'=2);
	[right] turn=1 & rpos < DIM -> (rpos'=rpos+1) & (turn'=2);
	[right] turn=1 & rpos = DIM -> (turn'=2);
	[stand] turn=1 -> (turn'=2);

	// d1 actions
	[l1] turn=2 & d1pos > 1 -> (d1pos' = d1pos-1) & (turn'=3);
	[l1] turn=2 & d1pos = 1 -> (turn'=3);
	[r1] turn=2 & d1pos < DIM -> (d1pos' = d1pos+1) & (turn'=3);
	[r1] turn=2 & d1pos = DIM -> (turn'=3);
	[s1] turn=2 -> (turn'=3);

	// d2 actions
	[l2] turn=3 & d2pos > 1 -> (d2pos'=d2pos-1) & (turn'=1);
	[l2] turn=3 & d2pos = 1 -> (turn'=1);
	[r2] turn=3 & d2pos < DIM -> (d2pos' = d2pos+1) & (turn'=1);
	[r2] turn=3 & d2pos = DIM -> (turn'=1);
	[s2] turn=3 -> (turn'=1);

endmodule
