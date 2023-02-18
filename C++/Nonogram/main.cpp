#include <iostream>
#include "grid.hpp"

int main(){
    
    int dim;
    std::vector<int> n; //num gruppi
    std::vector<int> val; //val dei gruppi

    std::cout << "Inserire dimensione tabella:\n";
    std::cin >> dim;

    std::cout << "Inserire numero di gruppi (in c poi r):\n";
    for (int j = 0; j < 2*dim; ++j){
        int a;
        std::cin >> a;
        n.push_back(a);
    }

    std::cout << "Inserire valori dei gruppi (in c poi r):\n";
    for (int i = 0; i < 2*dim; ++i){
        for (int j = 0; j < n[i]; ++j){
            int a;
            std::cin >> a;
            val.push_back(a);
        }
    }
    std::cout << "\n";

    Griglia RIVALE = {dim, n, val};

    for (int i = 0; i < dim; ++i){
        for (int j = 0; j < dim; ++j){
            std::cout << "X";
        }
        std::cout << "\n";
    }

    // std::vector<int> righe{};
    // std::vector<int> colonne{};
    // int dim;
    
    // std::cin >> dim;

    // for (int i = 0; i < dim; ++i){
    //     for (int j = 0; j < dim; ++j){
    //         std::cout << "X";
    //     }

    //     std::cout << '\n';
    // }

    // for (int i = 0; i < dim; ++i){
    //     std::cout << "Numero gruppi colonna" << i+1 << ": ";
    //     int n; std::cin >> n;

    //     for (int j = 0; j < n; ++n){
    //         int val;
    //         std::cin >> val;
    //     }
    // }
}