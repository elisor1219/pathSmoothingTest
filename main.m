%% Give the path 
clc;clear;clf
hold on
grid on
title("Add at least 2 points")

%TODO: Found a error when using the path
%path = [0, 1, 3, 6, 7; 0, 1, 2, -2, 3]*1/10;

axis([0 1 0 1])

%path = zeros(2,4);
i = 1;
%Get the control points
while true
    [xi, yi, but] = ginput(1);
    if ~isequal(but,1)
        break
    end
    path(:,i) = [xi; yi];
    if i == 1
        plot(path(1,1), path(2,1), 'o-')
    else
        line([path(1,i-1) path(1,i)], [path(2,i-1) path(2,i)])
        line([path(1,i-1) path(1,i)], [path(2,i-1) path(2,i)], 'Marker', 'o')
    end
    i = i + 1;
end
hold off

path = [0, 1, 3, 6, 7; 0, 1, 2, -2, 3];


%% Plot the path

%sizeOfPath = size(path,2);
%lessPath = zeros(2,floor(sizeOfPath/2));
%for i = 1:size(lessPath,2)
%    lessPath(:,i) = path(:,i*2)
%end

clf;clc
[pointsCatmull,fakePointsCatmull] = catmull_faster(path, 60);

[pointsBSpline,fakePointsBSpline] = bSpline(path, 60);


% We could use an interpolation algorithm on the curve before using the
% b-spline to decreese the curvature, use the interpolation as a parameter
% to adjust the curvatuer.
% We could also do a dynamic interpolation, where we interpolate more when
% the angel is high.

%Plot the Catmull-Rom spline generated curve
subplot(2,1,1)
hold on
grid on
title("Testing a cubic spline (Catmull Rom spline)", 'FontSize',13)
plot(path(1,:), path(2,:), 'o-')
plot(pointsCatmull(1,:), pointsCatmull(2,:), 'LineWidth',3)
%Plot the fake points
line([fakePointsCatmull(1,1) path(1,1)], [fakePointsCatmull(2,1) path(2,1)], 'LineStyle', '--', 'Marker', 'o')
line([fakePointsCatmull(1,2) path(1,end)], [fakePointsCatmull(2,2) path(2,end)], 'LineStyle', '--', 'Marker', 'o')

saveas(gcf,"Catmull_spline_main.png")

%Plot the B spline generated curve
subplot(2,1,2)
hold on
grid on
title("Testing a cubic spline (B-spline)", 'FontSize',13)
plot(path(1,:), path(2,:), 'o-')
plot(pointsBSpline(1,:), pointsBSpline(2,:), 'LineWidth',3)
%Plot the fake points
line([fakePointsBSpline(1,1) path(1,1)], [fakePointsBSpline(2,1) path(2,1)], 'LineStyle', '--', 'Marker', 'o')
line([fakePointsBSpline(1,2) path(1,end)], [fakePointsBSpline(2,2) path(2,end)], 'LineStyle', '--', 'Marker', 'o')

saveas(gcf,"B_spline_main.png")


%% Testing NURBS from a paper
clc;
%n = 4;
%P = zeros(n+1,2); % A set of n+1 contorl points 1 <= i <= n+1
P = [0,0; 1,1; 1,2; 2,2];
n = size(P,1) - 1;
w = [1 2 1 1]; % Weights w_i >= 0
m = 10;
%U = zeros(1,m+1); % A knot vector of m+1 knots, 0 = u_1 <= u_2 <= ... <= u_(m+1) = 1
%m = size(U,2);
U = linspace(0,1,m+1);
p = m - n - 1; %Degree p satisfying m = n + p + 1
if (p < 1)
    disp("WARNING: Degree of p is negative!")
end


u = 0.1; %Variable

% Initializing degree 0 B-spline basis functions
N = zeros(n+1, p);
for i = 1:(n+1)
    if (u >= U(i) && u < U(i+1))
        N(i,1) = 1;
    else
        N(i,1) = 0;
    end
end

% Recursiv definition of degree > 0 B-spline basis functions
for deg = 2:p
    for i = 1:(n)
        numerator = u - U(i);
        denumerator = U(i+deg) - U(i);
        if denumerator == 0
            left = 0;
        else
            left = numerator / denumerator;
        end

        numerator = U(i+deg+1) - u;
        denumerator = U(i+deg+1) - U(i+deg);
        if denumerator == 0
            right = 0;
        else
            right = numerator / denumerator;
        end
        
        N(i,deg) = left * N(i,deg-1) + right * N(i+1,deg-1);
    end
end

%Calculate the numerator
deg = 1; % Variable
if (deg > p)
    disp("WARNING: deg is larger then p")
end

numerator = 0;
for i = 1:n+1
    numerator = numerator + N(i,deg) .* w(i) * P(i,:);
end


denumerator = 0;
for i = 1:n+1
    denumerator = denumerator + N(i,deg) .* w(i);
end
C = numerator / denumerator

% Plot
%plot(P(:,1), P(:,2))
plot(N')

i = 5;
N = basisFuns(i, u, p, U);


%% Testing NURBS with the NURBS book
clc;





%u = 5/2;
%p = 3;

p = 2;
%U = [0,0,0,1,2,3,4,4,5,5,5];
u = 1;

U = [0 0 0 1 2 3 3 3];
m = size(U,2); %Number of knots - 1 
n = m - p - 1;

w = [1 4 1 1 1];
P = [0,0; 1,1; 3,2; 4,1; 5,-1];
Pw = ones(5, 3);
Pw(:,1:2) = P;
Pw = Pw.*w'; %Is wx, wy, w


basisFuns(i, u, p, U);
i = findSpan(n, p, u, U);

C = curvePoint(n, p, U, Pw, u,w )


%% Testing NURBS Curves, can prop remove
clc;

controlPoints = size(path,2);
pointsPerSection = 20;

pointsNURBS = zeros(pointsPerSection*controlPoints,2);

 

%First we calculate the B-spline basis functions as matix
degree = 2; %Minus 1
k = path(1,:); %Knots

u = linspace(0,1,size(pointsNURBS,1));
index = 1
u = 0.2

%for index = 1:size(pointsNURBS,1)
    B_basis = zeros(controlPoints, degree);

    
    f = @(u,i,n) (u - k(i))/(k(i+n) - k(i));
    
    g = @(u,i,n) 1 - f(u,i,n);
    
    for i = 1:controlPoints-3
        for n = 1:degree
            if n <= 1
                if u(index) >= k(i) && u(index) < k(i+1)
                    B_basis(i,n) = 1;
                else
                    B_basis(i,n) = 0;
                end
                continue
            end
            B_basis(i,n) = f(u(index),i,n) * B_basis(i,n-1) + g(u(index),i+1,n) * B_basis(i+1,n-1);
        end
    end
    
    weights = ones(controlPoints,1);
    
    numerator = sum(B_basis .* weights .* k',1);
    denumerator = sum(B_basis .* weights,1);
    C = numerator ./ denumerator;
    
    pointsNURBS(index,1) = C(2);

%end



B_basis
%pointsNURBS
clf;
plot(pointsNURBS)


