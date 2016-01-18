// TIGER SCENARIO

mdp

// === CONSTANTS ===
// grid dimension
//const int DIM =10;

// === LABELS ===
//label "collision" = rpos=dpos;

// === FORMULAS ===
//formula detect_left = rpos=dpos-1 | rpos=1;

// === REWARDS ===
rewards
	[left] tpos=0 : 0;
	[right] tpos = 0: 0;
	[listen] true : 0;
	[left] tpos=1 : 10;
	[right] tpos=0 : 10;
endrewards

// === MODULES ===

// can go left, right or listen to the roar
module agent
	count_left : [0..5] init 0;
	count_right : [0..5] init 0;
	listening : bool init false;	

	[left] !listening -> (count_left'=0) & (count_right'=0);
	[right]	!listening -> (count_left'=0) & (count_right'=0);
	[listen] !listening -> (listening'=true);
	[hearleft] listening -> (listening'=false) & (count_left'=min(count_left+1,5));
	[hearright] listening -> (listening'=false) & (count_right'=min(count_right+1,5));
endmodule

module tiger

	tpos: [0..1]; // left, right
	roar: [0..2]; // not roaring, roar from left, roar from right

	[left] roar=0 -> 1/2 : (tpos'=0) + 1/2 : (tpos'=1);
	[right] roar=0 -> 1/2 : (tpos'=0) + 1/2 : (tpos'=1);
	[listen] roar=0 & tpos=0 -> 3/4 : (roar'=1) + 1/4 : (roar'=2);
	[listen] roar=0 & tpos=1 -> 1/4 : (roar'=1) + 3/4 : (roar'=2);
	[hearleft] roar=1 -> (roar'=0);
	[hearright] roar=2 -> (roar'=0); 

endmodule
