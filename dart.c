// Labo3 Flechette
// Auteur: Nicolas Besson
 
#include <stdio.h>  // Includes stdio library to use printf function
#include <math.h>   // Includes math library for mathematical functions
 
// Defines  
    #define DIAMETER_ZONE_A_CM 2
    #define DIAMETER_ZONE_B_CM 10
    #define DIAMETER_ZONE_C_CM 20
 
    #define ZONE_A_PT 100
    #define ZONE_B_PT 25
    #define ZONE_C_PT 5
    #define ZONE_D_PT 0
 
/*
  Description:
  Main loop of the program
 
  Input:
  - argc = number of arguments
  - argv = values entered by the user
 
  Output:
  - returns 0 if everything went well
  - returns 1 if there are not enough arguments
  - returns 2 if an argument is not a valid number
*/
int main(int argc, char* argv[]) {
 
    double dart_in_x = 0;
    double dart_in_y = 0;
 
    double dart_distance = 0;
 
    int zone_a_pt = ZONE_A_PT;
    int zone_b_pt = ZONE_B_PT;
    int zone_c_pt = ZONE_C_PT;
    int zone_d_pt = ZONE_D_PT;
 
    int point_result = 0;
    
    // check if there are enough arguments
    if(argc <2)
    {
        return 1;
    }
    if(argc >= 2)
    {
        // check if -v argument
        if(argv[1][0] == '-' && argv[1][1] == 'v')
        {
            printf("Dart (c)2025 Besson Nicolas <nicolas.besson@heig-vd.ch>\n");
            printf("Version 1.0.0\n");
            return 0;
        }
        // Return error if only one argument is received
        if(argc == 2)
        {
            return 1;
        }
    }

    // read coordinates (x,y)
    if(argc >= 3)
    {
        if(sscanf(argv[1], "%lf", &dart_in_x)!=1)
        {
            return 2;
        }
        if(sscanf(argv[2], "%lf", &dart_in_y)!=1)
        {
            return 2;
        }
    }
    // read optional score A
    if (argc >= 4) {
 
        if(sscanf(argv[3], "%d", &zone_a_pt)!=1)
        {
            return 2;
        }  
    }
    // read optional score B
    if (argc >= 5) {
        if(sscanf(argv[4], "%d", &zone_b_pt)!=1)
        {
            return 2;
        }
    }
    // read optional score C
    if (argc >= 6) {
        if(sscanf(argv[5], "%d", &zone_c_pt)!=1)
        {
            return 2;
        }
    }
    // read optional score D
    if (argc >= 7) {
        if(sscanf(argv[6], "%d", &zone_d_pt)!=1)
        {
            return 2;
        }
    }
 
    // calculate distance from center
    dart_distance = sqrt((dart_in_x * dart_in_x) + (dart_in_y * dart_in_y));    
 
    // determine score zone
    if(dart_distance <= DIAMETER_ZONE_A_CM / 2) {
        point_result = zone_a_pt;
    } else if(dart_distance <= DIAMETER_ZONE_B_CM / 2) {
        point_result = zone_b_pt;
    } else if(dart_distance <= DIAMETER_ZONE_C_CM / 2) {
        point_result = zone_c_pt;
    } else {
        point_result = zone_d_pt;
    }
 
    // print result
    printf("%d\n",point_result);
 
    return 0;
}
