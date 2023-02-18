function[] = gravitazioneluna(MESI)

%dati
d_afL = 405.4e6;
v_afL = 960;
d_cmT = 4.6e6;

G = 6.67e-11;
mT = 6e24;
mL = 7e22;

%inizio
pT = [-d_cmT 0 0];
pL = [d_afL-d_cmT 0 0];
vT = [0 0 0]; 
vL = [0 v_afL 0];

%parametri
t = 0; 
dt = 1;
kMAX = 86400*28*MESI;

%figura 1 che è in movimento 
for k=0:kMAX 
    k = k+1;
    pCM = [(pT(1)*mT+pL(1)*mL)/(mT+mL) (pT(2)*mT+pL(2)*mL)/(mT+mL) 0];
    rLCM = pL;
    rTCM = pT;
    rLT = pL-pT; 
    aT = -(G*mL)/(norm(rLT))^3.*rLT; 
    pT = pT + vT*dt + 0.5*aT*dt^2;
    vT = vT + aT*dt;
    aL = -(G*mT)/(norm(rLT))^3.*rLT;
    pL = pL + vL*dt + 0.5*aL*dt^2;
    vL = vL + aL*dt; 
    
%     IL = mL * (norm(rLCM))^2;
%     IT = mT * (norm(rTCM))^2;
%     lL = IL * (2*pi/2332800);
%     lT = IT * (2*pi/2332800);

%     lT = mT*norm(rLT)^2 *2*pi/2332800;
%     lL = mL*norm(rLT)^2 *2*pi/2332800;

    lT=mT*norm(rLT)^2 *2*pi/2332800;
    lL=mL*norm(rLT)^2 *2*pi/2332800;
    
    if mod(k,86400) == 0 
        t = t+1;
        plot(pT(1),pT(2),'.b','Markersize',20); %%coordinate, colore, grandezza punto
        plot(pL(1),pL(2),'.g','Markersize',10); 
        plot(pCM(1),pCM(2),'.k','Markersize',10);
        grid on;  
        hold on; 
        pause(0.0001); %%attesa tra un punto e l'altro 
        axis([pCM(1)-800e6 pCM(1)+800e6 pCM(2)-800e6 pCM(2)+800e6]); %%dimensione grafico
        KT(t) = 0.5*(mT)*(norm(vT))^2;
        KL(t) = 0.5*(mT)*(norm(vL))^2;
        UT(t) = (-G*mL*mT/norm(rLT)) + ((lT^2)/(2*mT*norm(rLT)^2));
        UL(t) = (-G*mL*mT/norm(rLT)) + ((lL^2)/(2*mL*norm(rLT)^2));
        ET(t) = KT(t) + UT(t);
        EL(t) = KL(t) + UL(t);
    end
end

figure(2);

grid on;
plot(KT+KL, '.b', 'LineWidth', 3); hold on; 
plot(UT+UL, '.r', 'LineWidth', 3); hold on; 
plot(ET+EL, '.g', 'LineWidth', 3); hold on; 
legend('KT+KL','UT+UL','ET+EL');

figure(3);

grid on;
plot(KT, '.b', 'LineWidth', 3); hold on; 
plot(UT, '.r', 'LineWidth', 3); hold on; 
plot(ET, '.g', 'LineWidth', 3); hold on; 
legend('KT,','UT','ET');

figure(4);

grid on;
plot(KL, '.b', 'LineWidth', 3); hold on; 
plot(UL, '.r', 'LineWidth', 3); hold on; 
plot(EL, '.g', 'LineWidth', 3); hold on; 
legend('KL','UL','EL');

end