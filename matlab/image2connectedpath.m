
% ------------------------------- image2connectedpath.m ----------------
% Author: Ole Rabbel, 2019, ole.rabbel@geo.uio.no. 
% No guarantee of 100% correct functionality!
%
% This script reads a .png image, binarizes it, and extracts the largest
% connected area (both in pixels and meters. This script was written in the
% context of fracture network simulations, and is used to extract the
% longest connected fracture path from the b/w image of each simulation
% step

clear all;
close all;

% specify path names
path_in = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/plots/15deg_aligned/extensional/10perc/animations/simple_network/';
pathnames = dir([path_in 'FN_*.png']);
path_out = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/plots/plot_data/longest_connected_path/';
filename_out = [path_out '15deg_aligned_extensional_20perc.txt'];

savefile = 0; %1 if result data should be written to a ASCII file


pixels = 1166; % length of image
domainsize = 0.5; % in meters
pxl_per_meter = 1166/0.5; % conversion factor

startidx = 1; %index of first filename within pathnames structure
longest_con_fracpath = NaN(length(pathnames)-startidx,1);
all_fracs = NaN(length(pathnames)-startidx,1);

% loop through all png images
for i = startidx:length(pathnames)
    filename = [path_in pathnames(i).name];
    image = imread(filename);

    %cut image
    image = image(:,315:1515);
    % turn image into binary and plot result
    BW = im2bw(image,0.5);
    BW = imcomplement(BW);
    
    BW_longest = BW;
    % find connected components
    CC = bwconncomp(BW);
    numPixels = cellfun(@numel,CC.PixelIdxList);
    [longest_con_fracpath(i-startidx+1),idx] = max(numPixels);
    all_fracs(i-startidx+1) = sum(numPixels(:));
    BW_longest(CC.PixelIdxList{idx}) = 0;
    
end

figure()
imshow(BW)

figure()
imshow(BW_longest)
% convert longest connected fracture path form pixels to meters
longest_con_fracpath_meters = longest_con_fracpath./pxl_per_meter;
all_fracs_meters = all_fracs./pxl_per_meter;
longest_con_fracpath_meters_normbytotal = longest_con_fracpath_meters./all_fracs_meters;
% plot for QC
figure()
plot(longest_con_fracpath_meters)
hold on
plot(all_fracs_meters)

figure()
plot(longest_con_fracpath_meters./all_fracs_meters)

% save to file
if savefile == 1
    dlmwrite(filename_out,[all_fracs_meters, longest_con_fracpath_meters, longest_con_fracpath_meters_normbytotal])
end




