function mid = findSpan(n,p,u,U)
%findSpan Determine the knot span index
% Input: n,p,u,U
% Output: The knot span index
%This is algorithm A2.1 from the book "The NURBS Book", 2nd Edition.

%Special case
if (u == U(n+1))
    mid = n;
    return
end

%Do binary search
low = p;
high = n+1;
mid = floor((low + high)/2);
while (u < U(mid) || u >= U(mid+1))
    if (u < U(mid))
        high = mid;
    else
        low = mid;
    end
    mid = floor((low + high)/2);
end

end
