load('.\data\B0005.mat')
cycles=B0005.cycle;
k=0;
for i=cycles
    if (i.type=="discharge")
        lastT=0;  
        voltageM= i.data.Voltage_measured;
        currentM=i.data.Current_measured;
        t=i.data.Time;
        voltageC= i.data.Voltage_load;
        currentC= i.data.Current_load;
        save(['Voltage_Measure',int2str(k),'.txt'],'voltageM','-ascii','-double');
        save(['Current_Measure',int2str(k),'.txt'],'currentM','-ascii','-double');
        save(['Voltage_Load',int2str(k),'.txt'],'voltageC','-ascii','-double');
        save(['Current_Load',int2str(k),'.txt'],'currentC','-ascii','-double');
        save(['Time',int2str(k),'.txt'],'t','-ascii','-double');
        k=k+1;
    end
end