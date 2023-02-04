function N = basisFuns(i,u,p,U)
%basisFuns Compute the nonvanishing basis functions
% Input: i,u,p,U
% Output: N
%This is algorithm A2.2 from the book "The NURBS Book", 2nd Edition.

N = ones(1,p);
left = zeros(1,p);
right = zeros(1,p);

for j = 2:p
    temp = i+1-j;
    disp("i+1-j = " + temp)
    left(j) = u - U(i+1-j+1);
    temp = i+j;
    disp("i+j = " + (i+j))
    right(j) = U(i+j)-u;
    saved = 0;
    for r = 0:j-1
        temp = N(r+1) / (right(r+1) + left(j-r));
        N(r+1) = saved + right(r+1)*temp;
        saved = left(j-r)*temp;
    end
    N(j+1) = saved;
end

end