% k means on MNIST

% load a randomly selected subset of 7s and 9s from MNIST
load('MNIST_MEDIUM.mat','img','Cact');

accuracies = [];
% do 200 trials of k-means and compare accuracies
for i = [1:200],
    Cest = KMEANS(img,2); % random initialization
    m = ACCURACY(Cest,Cact,2);
    fprintf('trial %d:\taccuracy: %f\n', i, m);
    accuracies(i) = m;
end;

fp = fopen('hw8_1.txt', 'w');
fprintf(fp, '200 iterations of semi-supervised K-means performed\n');
fprintf(fp, 'max accuracy:\t%f%%\n', max(accuracies));
fprintf(fp, 'min accuracy:\t%f%%\n', min(accuracies));
fprintf(fp, 'mean:\t%f%%\n', mean(accuracies));
fclose(fp);
