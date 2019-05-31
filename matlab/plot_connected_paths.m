clear all

path_in = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/plots/plot_data/longest_connected_path/';
pathnames = dir([path_in '*.txt']);

 all_paths_meters = NaN(100,length(pathnames));
connected_path_meters = NaN(100,length(pathnames));
connected_path_normalized = NaN(100,length(pathnames));

for i = 1:length(pathnames)
   loaddata = load([path_in pathnames(i).name]);
   loaddata(loaddata == 0) = NaN;
   all_paths_meters(1:length(loaddata),i) = loaddata(:,1);
   connected_path_meters(1:length(loaddata),i) = loaddata(:,2);
   connected_path_normalized(1:length(loaddata),i) = loaddata(:,3);
end

figure()
plot(connected_path_normalized(:,1:11))
legend ('comp 100','comp 10','comp 1','comp 5','ext 10', 'ext 1', 'ext 200','ext 20','ext 5', 'iso', 'unconfined')
%'
%
%figure()
%plot(connected_path_meters(:,1:10))
%hold on
%plot(all_paths_meters)

% crossplot
orient_list_comp = [ones(1, 4)*1, ones(1, 4)*2, ones(1, 4)*3];
aniso_list_comp = [6, 4, 2, 3, 6, 4, 2, 3, 6, 4, 2, 3];
data_comp = nanmax(connected_path_normalized(:,[1:4,12:15,22:25]));

orient_list_ext = [ones(1, 5)*1+0.1, ones(1, 4)*2+0.1, ones(1, 4)*3+0.1];
aniso_list_ext = [4, 2, 6, 5, 3, 4, 2, 6, 3, 4, 2, 6, 3];
data_ext = nanmax(connected_path_normalized(:,[5:9,16:19,26:29]));

orient_list_iso_unconf = [ones(1, 2)-[0.1, 0.2], ones(1, 2)*2-[0.1, 0.2], ones(1, 2)*3-[0.1, 0.2]];
aniso_list_iso_unconf = [1, 1, 1, 1, 1, 1];
data_iso_unconf = nanmax(connected_path_normalized(:,[10,11,20,21,30,31]));

figure()
scatter(aniso_list_comp,orient_list_comp,data_comp.*1000,data_comp,'filled')
hold on
scatter(aniso_list_ext,orient_list_ext,data_ext.*1000,data_ext,'filled')
scatter(aniso_list_iso_unconf,orient_list_iso_unconf,data_iso_unconf.*1000,data_iso_unconf,'filled')

