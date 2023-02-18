function[] = esperimento(MESI)

%dati che so
G = 6.67e11;
mA = 2e30;
mB = 2e30;
mC = 5e24;
dAB = 150e9;

%impostazione avvio
pA = [-75e9 0];
vA = [0 0];
pB = [75e9 0];
vB = [0 0];
pC = [0 -150e9];
vC = [0 0];

%parametri
t=0;
dt=1;
iMAX = MESI*28*24*60*60;

for i=0:iMAX
    i = i+1;
    rCA = pA-pC;
    rCB = pB-pC;  
    aC = (-G*(mA)/(norm(rCA))^3.*rCA) -G*(mB)/(norm(rCB))^3.*rCB;
    pC = pC + vC*dt + 0.5*aC*dt^2;
    vC = vC + aC*dt;
    if mod(i,60*60*24)==0
        t=t+1;
        plot(pA, '.k','Markersize',50);
        plot(pB, '.k','Markersize',50);
        plot(pC, '.r','Markersize',30);
        grid on;
        hold on;
        pause(0.001);
        axis ([-300e9 300e9 -300e9 300e9]);
    end
end
end