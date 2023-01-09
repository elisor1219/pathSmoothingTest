clc;clear;clf
hold on
grid on
title("Add 4|n points")

%We would like to hava the knot/joint points to be aligned or even mirrored
%Make it mirrired: We need to lock P_4! P_4 = 2*P_3-P_2
%Maybe we could make the "spline" C^inf to add more information at the end

%Could we use a hemite spline if we have the desired velocity at every
%point, but not the path?

%Look into cardinal spline!
%We estimate the velocity at the points using there neghibors and then
%Inserting that into the hemite spline. Also using a scale factor.

%Catmull-Rom Spline
%If we set the scale factor to 0.5 we get the Catmull-Rom Spline

%B-slpine
%Testi using a qubic C^2 contius spline (See 53:33)

%Look at 57:43 foor all splines

%Control points -> Splines -> Curves

%Think we need a Carmull-Rom!!!!

%See 1:01:42 for a table of splines
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

%path = [0 1 1.5 3 4 4 5 5  %x
%        0 1  0  1 2 3 2 2 ]; %y

%plot(path(1,:), path(2,:), 'o-')

% T-matrix * Charachteristic matrix * Point matrix
%Bezier spline
Bezier = @(t, P_0, P_1, P_2, P_3) [1 t t^2 t^3] * [1 0 0 0; -3 3 0 0; 3 -6 3 0; -1 3 -3 1] * [P_0; P_1; P_2; P_3];

%Carmull-Rom spline
Carmull = @(t, P_0, P_1, P_2, P_3) [1 t t^2 t^3] * (1/2.*[0 2 0 0; -1 0 1 0; 2 -5 4 -1; -1 3 -3 1]) * [P_0; P_1; P_2; P_3];

%Will go from 0 to 
u = 0;
hold off

%% Better way?
% Carmull-Rom spline
firstFakePoint = -(path(:,2) - path(:,1)) + path(:,1);
lastFakePoint = -(path(:,end-1) - path(:,end)) + path(:,end);
fakePoints = [firstFakePoint lastFakePoint];
extraPath = mod(size(path,2), 4);
if extraPath ~= 0
    error("Not implemented yet!")
end
numberOfSections = size(path,2)/4;

h = linspace(0,2);
onSection = floor(h) + 1;

i = 1;
onSection = floor(h(i)) + 1;

while onSection <= numberOfSections
    t = h(i) - floor(h(i))
    pointsCarmull(1,i) = Carmull(t, path(1,1), path(1,2), path(1,3), path(1,4));
    pointsCarmull(2,i) = Carmull(t, path(2,1), path(2,2), path(2,3), path(2,4));
    i = i+1;
    onSection = floor(h(i)) + 1;
end

hold on
title("Testing a cubic spline (Carmull-Rom)", 'FontSize',13)
plot(path(1,:), path(2,:), 'o-')
plot(pointsCarmull(1,:), pointsCarmull(2,:))
%Plot the fake points
line([fakePoints(1,1) path(1,1)], [fakePoints(2,1) path(2,1)], 'LineStyle', '--', 'Marker', 'o')
line([fakePoints(1,2) path(1,end)], [fakePoints(2,2) path(2,end)], 'LineStyle', '--', 'Marker', 'o')

%for i = 1:size(onSection,2)
%    
%end


%% Old way
t = 0;
times = 30;
h = 1/times;
sectionsOnPath = size(path,2)/4;

pointsBezier = zeros(2,(times+1)*sectionsOnPath);
pointsCarmull = zeros(2,times+1);
%For the carmull, mirror the second first and last point on the first and
%last point
firstFakePoint = -(path(:,2) - path(:,1)) + path(:,1);
lastFakePoint = -(path(:,end-1) - path(:,end)) + path(:,end);
fakePoints = [firstFakePoint lastFakePoint];
%For the bazier spline
%This part can be faster if we use h = [0, size(path,2)] instead of h = [0,1]
for j = 1:sectionsOnPath
    loop = times*(j-1)+1:(times+1)*2*(j-1);
    for i = loop
        pointsBezier(1,i) = Bezier(t, path(1,j+3*(j-1)), path(1,(j+1)+3*(j-1)), path(1,(j+2)+3*(j-1)), path(1,(j+3)+3*(j-1)));
        pointsBezier(2,i) = Bezier(t, path(2,j+3*(j-1)), path(2,(j+1)+3*(j-1)), path(2,(j+2)+3*(j-1)), path(2,(j+3)+3*(j-1)));
        t = t + h;
    end
    t = 0;
end

for i = 1:times+1
    pointsBezier(1,i) = Bezier(t, path(1,1), path(1,2), path(1,3), path(1,4));
    pointsBezier(2,i) = Bezier(t, path(2,1), path(2,2), path(2,3), path(2,4));

    pointsCarmull(1,i) = Carmull(t, path(1,1), path(1,2), path(1,3), path(1,4));
    pointsCarmull(2,i) = Carmull(t, path(2,1), path(2,2), path(2,3), path(2,4));
    t = t + h;
end
subplot(2,1,1) %Subplot 1 v-v-v-v-v-v-v-v-v-v-v
hold on
title("Testing a cubic spline (Bezier)", 'FontSize',13)
plot(path(1,:), path(2,:), 'o-')
plot(pointsBezier(1,:), pointsBezier(2,:))

subplot(2,1,2) %Subplot 2 v-v-v-v-v-v-v-v-v-v-v
hold on
title("Testing a cubic spline (Carmull-Rom)", 'FontSize',13)
plot(path(1,:), path(2,:), 'o-')
plot(pointsCarmull(1,:), pointsCarmull(2,:))
%Plot the fake points
line([fakePoints(1,1) path(1,1)], [fakePoints(2,1) path(2,1)], 'LineStyle', '--', 'Marker', 'o')
line([fakePoints(1,2) path(1,end)], [fakePoints(2,2) path(2,end)], 'LineStyle', '--', 'Marker', 'o')



hold off