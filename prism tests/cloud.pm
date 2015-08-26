// CLOUD SCENARIO

mdp

// === CONSTANTS ===
// grid dimension
const int k;
const int maxVM = 3;
const int maxTasks = 10;

// === INIT ===

//init 
//	rpos=1 & 
//	dpos=DIM/2 & 
//	choice=0 & 
//	token=true
//endinit

// === LABELS ===

//label "collision" = rpos=d1pos | rpos=d2pos;
//label "detect_left" = rpos=d1pos-1 | rpos=d2pos-1;
//label "detect_right" = rpos=d1pos+1 | rpos=d2pos+1;

// === REWARDS ===

//rewards
//	[] detect_left : 1;
//	[] detect_right : 1;
//	[] collision : 1;
//endrewards

// === FORMULAS ===

//formula detect_left = rpos=d1pos-1 | rpos=d2pos-1;

// === MODULES ===

// phisical machine
module PM
	VM : [0..maxVM] init 1;
	// may add or remove virtual machines
	[new]		VM < maxVM -> true;
	[remove]	VM > 1 -> true;
	[nothing]	true -> true;

endmodule

// === ENVIRONMENT ===

// fully probabilistic phisical machine module
module PPM
	VM : [0..maxVM] init 1; // stand still, left, right
	// can move at random left or right or stand still
	[] c1=0 -> 1/3 : (c1'=1) + 1/3 : (c1'=2) + 1/3 : (c1'=3);
	[s1] c1=1 -> (c1'=0);
	[l1] c1=2 -> (c1'=0);
	[r1] c1=3 -> (c1'=0);
endmodule

module d2=d1 [ c1=c2, b1=b2, s1=s2, l1=l2, r1=r2 ] endmodule

module queue
	tasks : [0..maxTasks] init 0;
	incoming : [0..5] init 0;
	losts : [0..5] init 0;
	completed : [0..maxTasks] init 0;
	phase : [0..2] init 0; // ready to sync the step action

	[] phase=0 ->
		1/6 : (incoming'=0) & (phase'=1) +
		1/6 : (incoming'=1) & (phase'=1) +
		1/6 : (incoming'=2) & (phase'=1) +
		1/6 : (incoming'=3) & (phase'=1) +
		1/6 : (incoming'=4) & (phase'=1) +
		1/6 : (incoming'=5) & (phase'=1);		

	[] phase=1 -> ...

	[] tasks<=maxTasks-5 -> 
		1/6 : (tasks'=0) +
		1/6 : (tasks'=tasks+1) & (losts'=0) +
		1/6 : (tasks'=tasks+2) & (losts'=0) +
		1/6 : (tasks'=tasks+3) & (losts'=0) +
		1/6 : (tasks'=tasks+4) & (losts'=0) +
		1/6 : (tasks'=tasks+5) & (losts'=0) ;
	[] tasks=maxTasks-4 -> 
		1/6 : (tasks'=0) +
		1/6 : (tasks'=tasks+1) & (losts'=0) +
		1/6 : (tasks'=tasks+2) & (losts'=0) +
		1/6 : (tasks'=tasks+3) & (losts'=0) +
		1/6 : (tasks'=tasks+4) & (losts'=0) +
		1/6 : (tasks'=tasks+4) & (losts'=1) ;
	[] tasks=maxTasks-3 -> 
		1/6 : (tasks'=0) +
		1/6 : (tasks'=tasks+1) & (losts'=0) +
		1/6 : (tasks'=tasks+2) & (losts'=0) +
		1/6 : (tasks'=tasks+3) & (losts'=0) +
		1/6 : (tasks'=tasks+3) & (losts'=1) +
		1/6 : (tasks'=tasks+3) & (losts'=2) ;
	[] tasks=maxTasks-2 -> 
		1/6 : (tasks'=0) +
		1/6 : (tasks'=tasks+1) & (losts'=0) +
		1/6 : (tasks'=tasks+2) & (losts'=0) +
		1/6 : (tasks'=tasks+2) & (losts'=1) +
		1/6 : (tasks'=tasks+2) & (losts'=2) +
		1/6 : (tasks'=tasks+2) & (losts'=3) ;
	[] tasks=maxTasks-1 -> 
		1/6 : (tasks'=0) +
		1/6 : (tasks'=tasks+1) & (losts'=0) +
		1/6 : (tasks'=tasks+1) & (losts'=1) +
		1/6 : (tasks'=tasks+1) & (losts'=2) +
		1/6 : (tasks'=tasks+1) & (losts'=3) +
		1/6 : (tasks'=tasks+1) & (losts'=4) ;
	[] tasks=maxTasks -> 
		1/6 : (losts'=0) +
		1/6 : (losts'=1) +
		1/6 : (losts'=2) +
		1/6 : (losts'=3) +
		1/6 : (losts'=4) +
		1/6 : (losts'=5) ;
endmodule
