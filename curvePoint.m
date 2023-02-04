function C = curvePoint(n,p,U,Pw,u,w)
%basisFuns Compute point on ratinonal B-spline curve
%   Input: n,p,U,Pw,u
%   Output: C
%This is algorithm A4.1 from the book "The NURBS Book", 2nd Edition.
span = findSpan(n,p,u,U);
N = basisFuns(span,u,p,U);
Cw = 0;
for j = 0:p
    Cw = Cw + N(j+1)*Pw(span-p+j+1,1);
    disp("Cw = " + Cw)
end

C = Cw./w;

end

