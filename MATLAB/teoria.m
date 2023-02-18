close all
clear all
clc
%questi servono per far partire il programma da 0 e cancellare le azioni
%fatte prima

%creo vettore
v = [12 3 0];
%per avviare da terminare basta scrivere il nome del file

%creo l'output
disp(v);

%accedo ad un elemento di v
w = v(2);
disp(w);

u = [2 4 6];
disp(u);

%somma
somma = v + u;
disp(somma);

%prodotti scalari
a = u * w;
disp(a);

b = dot(u,v);
disp(b);

%prodotto di ogni singolo elemento per il corrispondente dei due vettori
c = v.*u;
disp(c);

%potenza di ogni elemento per il corrispondente
d = v.^u;
disp(d);

%cambiare un elemeno
u(3)=2;
disp(u);

%if 
if (v==u)
    fprintf("\nv uguale a u \n");
else
    fprintf("\nv diverso da u \n\n");
end
%gli altri operatori relazionali sono uguali a C, tranne != che è ~= 

%matrice 
m = [1 2 3; 4 5 6; 7 8 9];
disp(m);

%accedo a elementi di matrice 
e = m(2,3);
disp(e);
%seconda riga, terza colonna

%v trasposto 
v = v';
disp(v);

%m trasposta
m = m';
disp(m);

%carattere "jolly" per accedere a più elementi 
n = m(:,1);
disp(n);
%prende la prima colonna
n = m(1,:);
disp(n);
%prende prima riga
n = m(:);
disp(n);
%mi scrive i suoi elementi in colonna, prendendoli per colonne

%restringere la matrice (sottomatrice)
o = m(2:3, 1:2);
disp(o);
%dalla seconda alla terza riga e dal primo al secondo elemento

%creazione di matrice da vettori
a = [1 2 3];
b = [4 5 6];
c = [7 8 9];
m = [a; b; c];
disp(m);
%tratto i vettori come singoli elementi 

%allocazione dinamica matrice
m = [1 2; 3 4];
disp(m);
m(1,4)=9;
disp(m);
%aggiungo un elemento dove voglio, e lui mi regola la matrice

%matrice identità 
m = eye(3);
disp(m);
m = eye(2,4);
disp(m);

%matrice nulla
m = zeros(4);
disp(m);
m = zeros(2,4);
disp(m);
%utili per aggiungere elementi dopo

%matrici di 1
m = ones(4);
disp(m);
m = ones(2,4);
disp(m);

m = [1 2 3; 4 5 6];
n = [7 8 9; 10 11 12];

%somma (differenza uguale)
somma = m + n;
disp(somma);
differenza = m - n;
disp(differenza);

%prodotto (uguale per divisione)
prodotto = m.*n;
disp(prodotto);
%moltiplica ogni elemento per il corrispondente

%ciclo for
v=zeros(1, 10);
disp(v);
for i=1:length(v)
    v(1,i) = i;
end
disp(v);

%ciclo while
i = 1;
while i<=length(v)
    v(1,i)=i;
    i=i+1;
end
disp(v);

%funzione somma2
a = 2;
b = 3;
[somma, differenza, prodotto]=somma2(a,b); 
%si collega da solo alla funzione somma
disp(somma);
disp(differenza);
disp(prodotto);

%vedere tutte le cifre che voglio
format short %4 cifre
disp(pi);
format long %15 cifre
disp(pi);

%inf = infinito
i = inf;
disp(i);

%JOLLY ":"
%caso 1: me li scrive tutti in fila
x = 1:15;
disp(x);
%caso 2: da 1 a 30, separati di 2
x=1:2:30;
disp(x);

%linspace stampa tutti quelli in mezzo equidistanziati tra loro
format short
x = linspace(0,5);
disp(x);
%ora gli dico anche quanti
x=linspace(0,5,3); %me ne dà solo 3
disp(x);

%random: mi sputa numeri a caso tra 0 e 1
a=rand(5);
disp(a);
b=10*rand(5);
disp(b);

%size restituisce le dimensioni della matrice
a = rand(5);
b=size(a);
disp(b);

%switch mi analizza i casi che gli dico 
a=8;
b=0;
switch(a)
    case 2
        x=2;
    case {4,5,6} %prende più casi
        x=4;
    otherwise
        x=1;
end
disp(x);

%input: posso inserire anche matrici o vettori
a=input('Inserisci a: '); %per stringhe serve '...'
disp(a);

%confronto matrici
a=[2 3;4 5;6 7];
b=[2 4; 3 3; 6 8];
c=(a==b);%mi analizza ogni posizione se è uguale
disp(c);

%output: così mi mette le prime 5 cifre decimali di pi 
fprintf('%0.5f \n',pi);

%varargin , gestisce variabili non conosciute in input
%nargin   , gestisce il numero di variabili in input
%varargout, gestisce variabili non conosciute in output
%nargout  , gestisce il numero di varaibili in output