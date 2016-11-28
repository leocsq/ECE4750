//========================================================================
// ubmark-quicksort
//========================================================================

#include "common.h"
#include "ubmark-quicksort.dat"


//------------------------------------------------------------------------
// partition
//------------------------------------------------------------------------
int partition(int* src, int h, int k){
    // int j = 0;
    // int i = h+1;
    // j = k;
    // while(i <= j){
      // if(src[i] < src[h]) i=i+1;
      // else if(src[j]>src[h]) j=j-1;
      // else{
        // int temp = src[i];
        // src[i] = src[j];
        // src[j] = temp;
        // i = i+1;
        // j = j-1;
	    // }
    // }
    // int t = src[h];
    // src[h] = src[j];
    // src[j] = t;
    // return j;
  int j = h;
  int i = k;
  while(j>i){
    if(src[j+1]<=src[j]){
      int temp = src[j]; src[j]=src[j+1];src[j+1]=temp;
      j = j+1;
    }
    else{
      int temp = src[j+1]; src[j+1]=src[j];src[j]=temp;
      i = i-1;
      }
    }
    return j;
}
//------------------------------------------------------------------------
// sort 
//------------------------------------------------------------------------
void sort(int* src, int l, int r)
{
    int j = partition(src, l, r);
    sort(src, l, j-1);
    sort(src, j+1, r);
}
//------------------------------------------------------------------------
// quicksort-scalar
//------------------------------------------------------------------------
__attribute__ ((noinline))
void quicksort_scalar( int* dest, int* src, int size )
{

    int l = 0;
    int r = size-1;
    if (size>=2) {sort(src,l,r);}
    
    
    // implement quicksort algorithm here
    int i;

    // dummy copy src into dest
    for ( i = 0; i < size; i++ )
      dest[i] = src[i];

}

//------------------------------------------------------------------------
// verify_results
//------------------------------------------------------------------------

void verify_results( int dest[], int ref[], int size )
{
  int i;
  for ( i = 0; i < size; i++ ) {
    if ( !( dest[i] == ref[i] ) ) {
      test_fail( i, dest[i], ref[i] );
    }
  }
  test_pass();
}

//------------------------------------------------------------------------
// Test Harness
//------------------------------------------------------------------------

int main( int argc, char* argv[] )
{
  int dest[size];

  int i;
  for ( i = 0; i < size; i++ )
    dest[i] = 0;

  test_stats_on();
  quicksort_scalar( dest, src, size );
  test_stats_off();
  //printf("aaa");

  verify_results( dest, ref, size );
  return 0;
}

