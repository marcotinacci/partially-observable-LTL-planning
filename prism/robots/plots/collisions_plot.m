%=========================================
%Generated by PRISM Chart Package
%=========================================

x0 = [0.0 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0 10.0 11.0 12.0 13.0 14.0 15.0 16.0 17.0 18.0 19.0 20.0 ];
y0 = [1.0 1.0 1.0 0.8 0.8 0.8 0.6 0.47999999999999987 0.4416 0.4416 0.1247999999999998 0.09983999999999993 0.08345599999999986 0.08345599999999986 0.008575999999999917 0.006860799999999667 0.005918719999999933 0.005918719999999933 0.0015871999999996778 0.0012697599999997866 0.0011165695999997283 ];
x1 = [1.0 5.0 9.0 13.0 17.0 ];
y1 = [1.0 0.8 0.4416 0.08345599999999986 0.005918719999999933 ];

figure1 = figure('Color', [1 1 1], 'PaperPosition',[0.6345 6.345 20.3 15.23],'PaperSize',[20.98 29.68]);

axes1 = axes('Parent', figure1, 'FontSize', 16);
xlabel(axes1, 'k');
ylabel(axes1, 'Minimum probability');
box(axes1, 'on');
hold(axes1, 'all');

title(axes1,[])
plot0 = plot(x0, y0, 'o-', 'Parent', axes1, 'LineWidth', 2);
plot1 = plot(x1, y1, 's-', 'Parent', axes1, 'LineWidth', 2);
legend1 = legend(axes1,{'collisions', 'collisions (1)'},'Location', 'EastOutside');
