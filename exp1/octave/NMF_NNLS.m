function [w,h,alpha,c] = NMF_NNLS(Va, vel, wini, hini, aini, lambda, mus, niter)
%NMF_NNLS A joint audio-motion model

%parameters
F = size(Va,1);
N = size(Va,2);
K = size(wini,2);
vc = size(aini,2);
%initial values
w = wini;
h = hini;
alpha = aini;

%normalize w and rescale h and alpha
wn = sqrt(sum(w.^2));
w = bsxfun(@rdivide,w,wn);
h = bsxfun(@times, h,wn');
alpha = bsxfun(@rdivide,alpha,wn');

flr = 1e-9;
c = []; %[cost_compute(Va, vel,w,h,alpha,lambda,mus)];

v = max(w*h,flr);

for i = 1:niter
    
    %update H
    dh = (w'*ones(F,N)) + lambda * (alpha*alpha'*h);
    dh = max(dh,flr);
    nh = (w'*(Va./v)) + lambda*(alpha*vel');
    h = h.*(nh./dh);
 
    v = max(w*h,flr);
    
    %update W
    w = update_w(w, h, Va, v, true(K,1), flr);
    w = bsxfun(@rdivide, w, sqrt(sum(w.^2)));
    
    v = max(w*h,flr);
    
    %update alpha
    alpha = alpha.*(lambda*(h*vel)./(lambda*(h*h'*alpha)+ (mus*ones(K,vc))));
    
    c = [c cost_compute(Va, vel,w,h,alpha,lambda,mus)];
end

end

function [cost] = cost_compute(Va, vel,w,h,alpha,lambda, mus)
cost = sum(sum((Va.* log(Va./(w*h))) - Va +(w*h))) + ((lambda/2)*(sum(sum((vel - (h'*alpha)).^2)))) + (mus*sum(alpha(:)));
end

function w = update_w(w, h, Va, v, w_ind, flr)
dpw = bsxfun(@plus,sum(h(w_ind, :), 2)', ...
                    bsxfun(@times, ...
                    sum((Va ./ v) * h(w_ind, :)' .* w(:, w_ind)), w(:, w_ind)));
dpw = max(dpw, flr);
dmw = Va ./ v * h(w_ind, :)' ...
                    + bsxfun(@times, ...
                    sum(bsxfun(@times, sum(h(w_ind, :),2)', w(:, w_ind))), w(:, w_ind));
w(:, w_ind) = w(:,w_ind) .* dmw ./ dpw;
end
