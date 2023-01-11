function [pointsCarmull,fakePoints] = carmull_faster(path,pointsPerSection)
%CARMULL_TWOFORLOOPS By using the Carmull-rom spline, compute the curve
%   Detailed explanation goes here

%Characteristic matrix
charMat = (1/2.*[0 2 0 0; -1 0 1 0; 2 -5 4 -1; -1 3 -3 1]);

%Carmull = @(t, P_0, P_1, P_2, P_3) [1 t t^2 t^3] * (1/2.*[0 2 0 0; -1 0 1 0; 2 -5 4 -1; -1 3 -3 1]) * [P_0; P_1; P_2; P_3];

firstFakePoint = -(path(:,2) - path(:,1)) + path(:,1);
lastFakePoint = -(path(:,end-1) - path(:,end)) + path(:,end);
fakePoints = [firstFakePoint lastFakePoint];

t = linspace(0,1,pointsPerSection)';
%T-matrix
tMat = [t.^0 t t.^2 t.^3];
pathAndFake = [firstFakePoint path lastFakePoint];
pointsCarmull = zeros(2, (size(path,2)-1)*size(t,2));
sectionSize = size(t,1);

%One problem right now is that the last point of a section is also the
%first point in the next section.
%This could effect the car in bad ways.
%One fix would be to skip on (j==1 || i>1), mostly temporary
%A better fix would be to do a linspace from 0, to #sections, this will
%ensure that all the points are diffrent.
%However, this method will not guarantee that the curve has a point exactly
%at a path-point.

for i = 1:size(pathAndFake,2)-3
    %Point Matrix
    pMat = [pathAndFake(:,i)'; pathAndFake(:,i+1)'; pathAndFake(:,i+2)'; pathAndFake(:,i+3)'];
    startWind = (sectionSize)*(i-1)+1;
    endWind = (sectionSize)*(i);
    pointsCarmull(:,startWind:endWind) = (tMat * charMat * pMat)';
end

end

