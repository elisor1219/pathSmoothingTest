%% Give the path 
clc;clear;clf
hold on
grid on
title("Add at least 2 points")

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

%% Plot the path

clf;clc
[pointsCarmull,fakePointsCarmull] = carmull_faster(path, 60);

[pointsBSpline,fakePointsBSpline] = bSpline(path, 60);


% We could use an interpolation algorithm on the curve before using the
% b-spline to decreese the curvature, use the interpolation as a parameter
% to adjust the curvatuer.
% We could also do a dynamic interpolation, where we interpolate more when
% the angel is high.

%Plot the Carmull-Rom spline generated curve
subplot(2,1,1)
hold on
grid on
title("Testing a cubic spline (Carmull Rom spline)", 'FontSize',13)
plot(path(1,:), path(2,:), 'o-')
plot(pointsCarmull(1,:), pointsCarmull(2,:), 'LineWidth',3)
%Plot the fake points
line([fakePointsCarmull(1,1) path(1,1)], [fakePointsCarmull(2,1) path(2,1)], 'LineStyle', '--', 'Marker', 'o')
line([fakePointsCarmull(1,2) path(1,end)], [fakePointsCarmull(2,2) path(2,end)], 'LineStyle', '--', 'Marker', 'o')

saveas(gcf,"Carmull_spline_main.png")

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
