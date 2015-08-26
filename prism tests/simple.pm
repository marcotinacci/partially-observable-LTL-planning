// ROBOT SCENARIO
// This scenario contains a robot moving in a simple shaped arena.
// The arena is a line nx1

mdp

// === CONSTANTS ===
// grid dimension
const int DIM =10;

// === INIT ===

//init 
//	rpos=1 & 
//	dpos=DIM/2 & 
//	choice=0 & 
//	token=true
//endinit

// === LABELS ===

label "collision" = rpos=dpos;
label "detect_left" = rpos=dpos-1 | rpos=1;
label "detect_right" = rpos=dpos+1 | rpos=DIM;

// === MODULES ===

formula detect_left = rpos=dpos-1 | rpos=1;
formula detect_right = rpos=dpos+1 | rpos=DIM;

// fully nondeterministic robot module
module robot
	// can move left, right or stand still
	[left]	!detect_left  -> true;
	[right]	!detect_right -> true;
	[stand]	true	      -> true;

endmodule

// fully probabilistic robot module
// cant see walls or other robots
module drunk
	choice : [0..3] init 0; // stand still, left, right
	// can move at random left or right or stand still
	[]	 choice=0 -> 1/3 : (choice'=1) + 1/3 : (choice'=2) + 1/3 : (choice'=3);
	[dstand] choice=1 -> (choice'=0);
	[dleft]	 choice=2 -> (choice'=0);
	[dright] choice=3 -> (choice'=0);
endmodule

// arena environment module
module arena

	token : bool init true; // turn variable
	rpos : [1..DIM] init 1; // robot position
	dpos : [1..DIM] init 3; // drunk position
	
	// robot actions
	[left] token & rpos > 1 -> (rpos'=rpos-1) & (token'=false);
	[left] token & rpos = 1 -> (token'=false);
	[right] token & rpos < DIM -> (rpos' = rpos+1) & (token'=false);
	[right] token & rpos = DIM -> (token'=false);
	[stand] token -> (token'=false);

	// drunk actions
	[dleft] !token & dpos > 1 -> (dpos' = dpos-1) & (token'=true);
	[dleft] !token & dpos = 1 -> (token'=true);
	[dright] !token & dpos < DIM -> (dpos' = dpos+1) & (token'=true);
	[dright] !token & dpos = DIM -> (token'=true);
	[dstand] !token -> (token'=true);

endmodule
