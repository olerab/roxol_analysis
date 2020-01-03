clear all;
close all;
clc;

% load data for permeability anisotropy based on FracPaQ

data_rand = load('90deg_final_k1k2_ratio_k1azim_FracPaQ_NEWORDER.txt');
data_semialigned = load('45deg_final_k1k2_ratio_k1azim_FracPaQ_NEWORDER.txt');
data_aligned = load('15deg_final_k1k2_ratio_k1azim_FracPaQ_NEWORDER.txt');

% note: order is unconfined, confined, comp 1%, comp 5%, comp 10%, comp 100%, ext 1%, ext 5%, ext 10%, ext 200%,

%% only extensional and confined
figure()
subplot(3,1,1)
yyaxis left
plot(data_rand(1,[2,7:10]),'.--')
xlim([1,5])
title('Initial Orientation \pm90^{\circ} (random)')
%xticklabels({'22.5', '60.75', '64.125', '66.825', '67.5', '68.175', '70.875', '74.25', '135'})
xlabel('stress anisotropy (%)')
ylabel('k_{1} / k_{2}')

yyaxis right
plot(data_rand(2,[2,7:10])-90,'.--')
ylabel('k1 azimuth')
ylim([-10,90])
% --------------------------
subplot(3,1,2)
yyaxis left
plot(data_semialigned(1,[2,7:10]),'.--')
xlim([1,5])
title('Initial Orientation \pm45^{\circ} (semi-aligned)')
%xticklabels({'22.5', '60.75', '64.125', '66.825', '67.5', '68.175', '70.875', '74.25', '135'})
xlabel('stress anisotropy (%)')
ylabel('k_{1} / k_{2}')

yyaxis right
plot(data_semialigned(2,[2,7:10])-90,'.--')
ylabel('k1 azimuth')
ylim([-10,90])

% ------------------
subplot(3,1,3)
yyaxis left
plot(data_aligned(1,[2,7:10]),'.--')
xlim([1,5])
title('Initial Orientation \pm15^{\circ} (aligned)') 
%xticklabels({'22.5', '60.75', '64.125', '66.825', '67.5', '68.175', '70.875', '74.25', '135'})
xlabel('stress anisotropy (%)')
ylabel('k_{1} / k_{2}')

yyaxis right
plot(data_aligned(2,[2,7:10])-90,'.--')
ylabel('k1 azimuth')
ylim([-10,90])
