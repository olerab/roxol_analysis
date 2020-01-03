clear all
close all

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


%figure()
%plot(connected_path_normalized(:,1:11))
%legend ('comp 100','comp 10','comp 1','comp 5','ext 10', 'ext 1', 'ext 200','ext 20','ext 5', 'iso', 'unconfined')

% figs for publication
figure()
plot(connected_path_normalized(:,26),'bo','MarkerFaceColor','b','linestyle','-','linewidth',1)
hold on
plot(connected_path_normalized(:,29),'r+','MarkerFaceColor','r','linestyle','-','linewidth',1)
plot(connected_path_normalized(:,30),'kd','MarkerFaceColor','k','linestyle','-','linewidth',1)
legend ('random, 10% extension', 'random, 5% extension','random, isotropic')
ylim([0,1])
xlabel('Simulation Step','FontSize',12)
ylabel('L_{con,max} / L_{tot}','FontSize',12)


figure()
plot(connected_path_normalized(:,26),'bo','MarkerFaceColor','b','linestyle','-','linewidth',1)
hold on
plot(connected_path_normalized(:,16),'yx','MarkerFaceColor','y','linestyle','-','linewidth',1)
plot(connected_path_normalized(:,5),'gv','MarkerFaceColor','g','linestyle','-','linewidth',1)
legend ('random, 10% extension', 'semialigned, 10% extension','aligned, 10% extension')
ylim([0,1])
xlabel('Simulation Step','FontSize',12)
ylabel('L_{con,max} / L_{tot}','FontSize',12)


% ----- fig for EarthFlows
figure()
plot(connected_path_normalized(:,[30, 26]),'linewidth',2)
legend ('67.5 MPa (isotropic)', '60.75 MPa (10% extension)')
ylim([0,1])
title('Connectivty Evolution')
xlabel('Simulation Step','FontWeight','bold')
ylabel('L_{con,max} / L_{tot}','FontWeight','bold')

% maximum connected pathways, per stress regime, ordered by increasing anisotropy
max_connected_path_15deg_comp = [nanmax(connected_path_normalized(:,3)), nanmax(connected_path_normalized(:,4)), nanmax(connected_path_normalized(:,2)), nanmax(connected_path_normalized(:,1))];
max_connected_path_15deg_ext = [nanmax(connected_path_normalized(:,6)), nanmax(connected_path_normalized(:,9)), nanmax(connected_path_normalized(:,5)), nanmax(connected_path_normalized(:,7))];
max_connected_path_15deg_conf = nanmax(connected_path_normalized(:,10));
max_connected_path_15deg_unconf = nanmax(connected_path_normalized(:,11));

max_connected_path_45deg_comp = [nanmax(connected_path_normalized(:,14)), nanmax(connected_path_normalized(:,15)), nanmax(connected_path_normalized(:,13)), nanmax(connected_path_normalized(:,12))];
max_connected_path_45deg_ext = [nanmax(connected_path_normalized(:,17)), nanmax(connected_path_normalized(:,19)), nanmax(connected_path_normalized(:,16)), nanmax(connected_path_normalized(:,18))];
max_connected_path_45deg_conf = nanmax(connected_path_normalized(:,20));
max_connected_path_45deg_unconf = nanmax(connected_path_normalized(:,21));

max_connected_path_90deg_comp = [nanmax(connected_path_normalized(:,24)), nanmax(connected_path_normalized(:,25)), nanmax(connected_path_normalized(:,23)), nanmax(connected_path_normalized(:,22))];
max_connected_path_90deg_ext = [nanmax(connected_path_normalized(:,27)), nanmax(connected_path_normalized(:,29)), nanmax(connected_path_normalized(:,26)), nanmax(connected_path_normalized(:,28))];
max_connected_path_90deg_conf = nanmax(connected_path_normalized(:,30));
max_connected_path_90deg_unconf = nanmax(connected_path_normalized(:,31));


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

%% ------ plot curves of final connectivity --------
figure()
subplot(3,1,1)
plot([fliplr(max_connected_path_90deg_ext),max_connected_path_90deg_conf,max_connected_path_90deg_comp],'.--')
xlim([1,9])
ylim([0.1,1])
title('Initial Orientation \pm90^{\circ} (random)')
xticklabels({'22.5', '60.75', '64.125', '66.825', '67.5', '68.175', '70.875', '74.25', '135'})
xlabel('Horizontal stress (MPa)')
ylabel('L_{con,max} / L_{tot}')

subplot(3,1,2)
plot([fliplr(max_connected_path_45deg_ext),max_connected_path_45deg_conf,max_connected_path_45deg_comp],'.--')
xlim([1,9])
ylim([0.1,1])
title('Initial Orientation \pm45^{\circ} (semi-aligned)')
xticklabels({'22.5', '60.75', '64.125', '66.825', '67.5', '68.175', '70.875', '74.25', '135'})
xlabel('Horizontal stress (MPa)')
ylabel('L_{con,max} / L_{tot}')

subplot(3,1,3)
plot([fliplr(max_connected_path_15deg_ext),max_connected_path_15deg_conf,max_connected_path_15deg_comp],'.--')
xlim([1,9])
ylim([0.1,1])
title('Initial Orientation \pm15^{\circ} (aligned)') 
xticklabels({'22.5', '60.75', '64.125', '66.825', '67.5', '68.175', '70.875', '74.25', '135'})
xlabel('Horizontal stress (MPa)')
ylabel('L_{con,max} / L_{tot}')

%% ------ plot curves of final connectivity only extensional and confined --------
figure()
subplot(3,1,1)
plot([fliplr(max_connected_path_90deg_ext),max_connected_path_90deg_conf],'.--')
xlim([1,5])
ylim([0.1,1])
title('Initial Orientation \pm90^{\circ} (random)')
%xticklabels({'22.5', '60.75', '64.125', '66.825', '67.5'})
xlabel('Horizontal stress (MPa)')
ylabel('L_{con,max} / L_{tot}')

subplot(3,1,2)
plot([fliplr(max_connected_path_45deg_ext),max_connected_path_45deg_conf],'.--')
xlim([1,5])
ylim([0.1,1])
title('Initial Orientation \pm45^{\circ} (semi-aligned)')
%xticklabels({'22.5', '60.75', '64.125', '66.825', '67.5'})
xlabel('Horizontal stress (MPa)')
ylabel('L_{con,max} / L_{tot}')

subplot(3,1,3)
plot([fliplr(max_connected_path_15deg_ext),max_connected_path_15deg_conf],'.--')
xlim([1,5])
ylim([0.1,1])
title('Initial Orientation \pm15^{\circ} (aligned)') 
%xticklabels({'22.5', '60.75', '64.125', '66.825', '67.5'})
xlabel('Horizontal stress (MPa)')
ylabel('L_{con,max} / L_{tot}')


