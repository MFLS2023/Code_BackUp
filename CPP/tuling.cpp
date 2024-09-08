#include<iostream>
using namespace std;

int main()
{
    double x;

    double pai = 3.14159;
    double square;
    while(cin>>x)
    {
        square = pai * x*x;
        printf("%.3f", square);
    }
    return 0;
}