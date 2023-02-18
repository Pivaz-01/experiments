#include "grid.hpp"

#include <vector>

using Grid = std::vector<Cell_status>;

Griglia::Griglia(int dim_, std::vector<int> n_, std::vector<int> val_):
    dim{dim_}, n{n_}, val{val_} {}

Griglia::Griglia() = default;

int Griglia::dim_(){return dim;}
std::vector<int> Griglia::n_(){return n;}
std::vector<int> Griglia::val_(){return val;}
int Griglia::N(){return dim*dim;}
Grid Griglia::cells_(){return cells;}