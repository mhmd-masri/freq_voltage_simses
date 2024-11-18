%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% OCV curve fitting parameter estimator
%  with this code the curve fitting parameters for OCV are estimated using global optimization tool-box
%  the SOC data is assumed to be in the first column and voltage in the second, if not suitable, modification
%  must be done
%  In order to achieve possibly better results, following can be done:
%  1. run program again
%  2. increase initial start points --> stpoints = RandomStartPointSet('NumStartPoints', 1000000);
%  
% 
% 
% yulong Zhao
% 22.05.2020
% 
% update 02.06.2020: stop condition added
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% define stop conditions
clear;
obj_limit = 0.005; % stop when fuction value goes below this limit
max_fcn   = 1e6; % maximal number of function evaluation


%% read CVS files
[file,path] = uigetfile('*.csv', 'Select csv file with ocv data'); % read file and get file path
filename = [path, file];
delimiterIn = ','; % set delimiter
headerlinesIn = 1; % line number of headers
xy_data = readmatrix(filename, 'NumHeaderLines', 1, 'Delimiter', ';', 'DecimalSeparator', ','); % read file into matrix
soc = xy_data(:, 1);
ocv = xy_data(:, 2);

%% define boundary conditions
global v0 v1
v0 = min(ocv); % minimal voltage at 0% SOC
v1 = max(ocv); % maximal voltage at 100% SOC

%% define estimation parameter
x_par = [2   , 3, 5;... 
         -5  , 0  , 5;...
         -5  , 0  , 5;...
         -5  , 0  , 5;...
         -5  , 0  , 5;...
         -1  , 0  , 1;...
         -500, 0  , 500;...
         -500, 0  , 500;...
         -500, 0  , 500;...
         -500, 0  , 500;...
         -10 , 0  , 10;...
         -10 , 0  , 10];
  
lb = x_par(:, 1); % lower bounds
x0 = x_par(:, 2); % initial values
ub = x_par(:, 3); % upper bounds

%% define objective function for optimization 
f_obj_OCV = @(x) sum(((x(1) + x(2)./(1+exp(x(7).*(soc-x(11)))) + x(3)./(1+exp(x(8).*(soc-x(12)))) + ...
    x(4)./(1+exp(x(9).*(soc-1))) + x(5)./(1+exp(x(10).*(soc))) + x(6).*soc - ocv)).^2);

%% define optimization problem
options = optimoptions(@fmincon, 'MaxFunctionEvaluations', max_fcn, 'PlotFcn', 'optimplotfval', ...
    'ObjectiveLimit', obj_limit);

[x_par,fval,exitflag,output,solutions] = fmincon(f_obj_OCV, x0, [], [], [], [], lb, ub, @nonlcon, options);
close all

%% validate optimization results
param = x_par;
k0 = param(1);
k1 = param(2);
k2 = param(3);
k3 = param(4);
k4 = param(5);
k5 = param(6);
a1 = param(7);
a2 = param(8);
a3 = param(9);
a4 = param(10);
b1 = param(11);
b2 = param(12);
ocv_fit = k0 + k1./(1+exp(a1.*(soc-b1))) + k2./(1+exp(a2.*(soc-b2))) + k3./(1+exp(a3.*(soc-1))) + k4./(1+exp(a4.*(soc))) + k5.*soc;

figure(1)
hold on
tiledlayout(2,1)
nexttile
plot(soc, ocv, '-*')
hold on
plot(soc, ocv_fit, '-o')
title('Open circuit voltage (OCV) curve fitting')
xlabel('SOC in p.u.');
ylabel('OCV in V');
legend('Measured', 'Fitted')
nexttile
plot(soc,(ocv-ocv_fit)*1000, 'Color', 'red')
title('Fitting error')
xlabel('SOC in p.u.');
ylabel('Error in mV');
legend('Measured - Fitted')

figure(2)
hold on
title('Fitting error')
xlabel('SOC [p.u.]')
ylabel('Relative error [%]')
semilogy(soc, abs(ocv - ocv_fit)./ocv*100, '-+')

%% define boundary conditions
function [c_ineq, c_eq] = nonlcon(x)
global v0 v1
c_ineq = [(x(1) + x(2)./(1+exp(x(7).*(1-x(11)))) + x(3)./(1+exp(x(8).*(1-x(12)))) + ...
    x(4)./(1+exp(x(9).*(1-1))) + x(5)./(1+exp(x(10).*(1))) + x(6).*1 - v1); ...
    -(x(1) + x(2)./(1+exp(x(7).*(1-x(11)))) + x(3)./(1+exp(x(8).*(1-x(12)))) + ...
    x(4)./(1+exp(x(9).*(1-1))) + x(5)./(1+exp(x(10).*(1))) + x(6).*1 - 0.995*v1); ...
    -(x(1) + x(2)./(1+exp(x(7).*(0-x(11)))) + x(3)./(1+exp(x(8).*(0-x(12)))) + ...
    x(4)./(1+exp(x(9).*(0-1))) + x(5)./(1+exp(x(10).*(0))) + x(6).*0 - v0); ...
    (x(1) + x(2)./(1+exp(x(7).*(0-x(11)))) + x(3)./(1+exp(x(8).*(0-x(12)))) + ...
    x(4)./(1+exp(x(9).*(0-1))) + x(5)./(1+exp(x(10).*(0))) + x(6).*0 - 1.005*v0)];  
c_eq = [];
end
