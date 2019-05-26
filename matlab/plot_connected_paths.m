clear all

path_in = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/plots/plot_data/longest_connected_path/';
pathnames = dir([path_in '*.txt']);

connected_path_data = NaN(100,length(pathnames));

for i = 1:length(pathnames)
   loaddata = load([path_in pathnames(i).name]);
   connected_path_data(1:length(loaddata),i) = loaddata;
end