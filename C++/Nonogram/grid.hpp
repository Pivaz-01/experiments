#ifndef grid_HPP
#define grid_HPP

#include <vector>

enum class Cell_status{X,O};

class Griglia{    
    private:
        using Grid = std::vector<Cell_status>;
        
        int dim;
        Grid cells; 

        std::vector<int> n; //numero gruppi c + r
        std::vector<int> val; //gruppi c + r
    public: 
        Griglia(int dim_, std::vector<int> n_, std::vector<int> val_);
        Griglia();

        int dim_();
        std::vector<int> n_();
        std::vector<int> val_();
        int N();
        Grid cells_();
};

#endif