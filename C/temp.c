#include<stdio.h>

int main()
{
    int x,sum=0;
    scanf("%d", &x);
    if(x<=1)
    {
        printf("0");
    }
    else
    {
        for (int i = 2; i < x;i++)
        {
            if(x%i==0)
            {
                printf("0");
                return 0;
            }
        }
        printf("1");
    }

    return 0;
}