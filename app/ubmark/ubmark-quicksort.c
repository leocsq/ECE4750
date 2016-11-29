//========================================================================
// ubmark-quicksort
//========================================================================

#include "common.h"
#include "ubmark-quicksort.dat"

__attribute__((noinline))
//------------------------------------------------------------------------
// partition
//------------------------------------------------------------------------
int partition(int* src, int h, int k){
  int j;
  int i = h+1;
  j = k;
  while (i <= j) {
    if (src[i] < src[h]) i= i+1;
    else if (src[j] > src[h]) j= j-1;
    else {// {b[j] < x < b[i]}
      int t1= src[i]; src[i]= src[j]; src[j]= t1;
      i= i+1; j= j-1;
      }
  }
  int temp = src[h]; src[h] = src[j]; src[j] =temp;
  return j;
}
//------------------------------------------------------------------------
// sort 
//------------------------------------------------------------------------
void sort(int* src, int l, int r)
{
    if(r-l+1 < 2) return;
    int j = partition(src, l, r);
    sort(src, l, j-1);
    sort(src, j+1, r);
}
//------------------------------------------------------------------------
// quicksort-scalar
//------------------------------------------------------------------------
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

