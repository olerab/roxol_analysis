clear all;
close all;
clc;

% load data for permeability anisotropy based on FracPaQ

data_rand = load('90deg_final_k1k2_ratio_k1azim_FracPaQ.txt');
data_semialigned = load('45deg_final_k1k2_ratio_k1azim_FracPaQ.txt');
data_aligned = load('15deg_final_k1k2_ratio_k1azim_FracPaQ.txt');

figure()
subplot(3,1,1)
plot(data_rand(1,:),'.--')
xlim([1,9])
title('Initial Orientation \pm90^{\circ} (random)')
xticklabels({'22.5', '60.75', '64.125', '66.825', '67.5', '68.175', '70.875', '74.25', '135'})
xlabel('Horizontal stress (MPa)')
ylabel('Permeability anisotropy (k_{1} / k_{2})')

subplot(3,1,2)
plot(data_semialigned(1,:),'.--')
xlim([1,9])
title('Initial Orientation \pm45^{\circ} (semi-aligned)')
xticklabels({'22.5', '60.75', '64.125', '66.825', '67.5', '68.175', '70.875', '74.25', '135'})
xlabel('Horizontal stress (MPa)')
ylabel('Permeability anisotropy (k_{1} / k_{2})')

subplot(3,1,3)
plot(data_aligned(1,:),'.--')
xlim([1,9])
title('Initial Orientation \pm15^{\circ} (aligned)') 
xticklabels({'22.5', '60.75', '64.125', '66.825', '67.5', '68.175', '70.875', '74.25', '135'})
xlabel('Horizontal stress (MPa)')
ylabel('Permeability anisotropy (k_{1} / k_{2})')