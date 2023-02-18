function[]=grafico()
clear all
close all
clc

%grafici
x=linspace(-2,2,50);
y=sin(x+1);
plot(x,y,'r--','Linewidth',2);

%etichette
xlabel('Asse X');
ylabel('Asse Y');

%titolo
title('Grafico funzione');

%assi
axis([-3 3 -3 3]);

%con box off tolgo il contorno del grafico

%legenda
legend('sin(x+1)');
end
