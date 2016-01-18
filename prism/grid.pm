mdp

const int D = 50;
const int x0;
const int y0;

module agent
	x : [1..D] init x0;
	y : [1..D] init y0;
	
	// actions
	[act_n]	true -> (x'=max(x-1,1));
	[act_e]	true -> (y'=min(y+1,D));
	[act_w]	true -> (y'=max(y-1,1));
	[act_s]	true -> (x'=min(x+1,D));

endmodule