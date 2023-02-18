
function [] = gravitazioneterra(ANNI)

%Simula moto Terra-Sole
%inizio
d_af = 152e9;
v_af = 29e3;

%dati fissi
G = 6.67e-11;
mS = 2e30;
mT = 6e24;

%dati iniziali 
pS = [0 0 0];
vS = [0 0 0];
pT = [d_af 0 0];
vT = [0 v_af 0];

%parametri 
t = 0; %%numero di giorni passati
dt = 1;
kMAX = 86400*365*ANNI;

%figura 1 che è in movimento 
for k=0:kMAX %%k sono i secondi passati
    k = k + 1;
    rTS = pT-pS;
    aT = -(G*mS)/(norm(rTS))^3.*rTS; %%da capire
    pT = pT + vT*dt + 0.5*aT*dt^2;
    vT = vT + aT*dt; 
    aS = -(G*mT)/(norm(rTS))^3.*rTS;
    pS = pS + vS*dt + 0.5*aS*dt^2;
    vS = vS + aS*dt;
    
    if mod(k,86400) == 0 %%mod è il resto, quindi ogni giorno
        t = t+1;
        plot(pT(1),pT(2),'.b','Markersize',20); %%coordinate, colore, grandezza punto
        plot(pS(1),pS(2),'.y','Markersize',60);
        grid on; %%assi di riferimento 
        hold on; %%traccia il grafico
        pause(0.0001); %%pausa tra un punto e l'altro 
        axis([-2e11 2e11 -2e11 2e11]); %%dimensione grafico
        KT(t) = 0.5*(mT*mS/(mT+mS))*(norm(vT))^2;
        UT(t) = -G*mS*mT/norm(rTS);
        ET(t) = KT(t) + UT(t);
        KS(t) = 0.5*(mT*mS/(mT+mS))*(norm(vS))^2;
        US(t) = -G*mT*mS/norm(rTS);
        ES(t) = KS(t) + US(t);
    end
end

%figura 2 che è un grafico
figure(2);

grid on;
plot(KT, '.b', 'LineWidth', 3); hold on;
plot(UT, '.r', 'LineWidth', 3); hold on;
plot(ET, '.g', 'LineWidth', 3); hold on;

figure(3);

grid on;
plot(KS, '.b', 'LineWidth', 3); hold on;
plot(US, '.r', 'LineWidth', 3); hold on;
plot(ES, '.g', 'LineWidth', 3); hold on;

figure(4);

grid on;
plot(KS+KT, '.b', 'LineWidth', 3); hold on;
plot(US+UT, '.r', 'LineWidth', 3); hold on;
plot(ES+ET, '.g', 'LineWidth', 3); hold on;

end