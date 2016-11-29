//========================================================================
// mtbmark-sort
//========================================================================

#include "common.h"
#include "mtbmark-sort.dat"

typedef struct {
  int* dest;  // pointer to dest array
  int* temp0;  // pointer to src0 array
  //int* src1;  // pointer to src1 array
  int  begin; // first element this core should process
  int  end;   // (one past) last element this core should process
} arg_t;
// '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Implement multicore sorting
// '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
__attribute__((noinline))
void merge(int* temp0, int h, int e, int k)
{
	int b[(k+1-h)*2];
	int i = h, j = e+1, k1 =0;
	while (i <= e && j <= k) {
        if (temp0[i] <= temp0[j])
            b[k1++] = temp0[i++];
        else
            b[k1++] = temp0[j++];
    }
    while (i <= e)
        b[k1++] = temp0[i++];
  
    while (j <= k)
        b[k1++] = temp0[j++];
  
    k1--;
    while (k1 >= 0) {
        temp0[h + k1] = b[k1];
        k1--;
    }
}
void mergeSort(int* temp0, int h, int k)
{
	if( h>=k ) return;

	int el = (h+k)/4;
	int e  = (h+k)/2;
	int er = 3*(h+k)/4;

	//mergeSort(b, h,  e);  // Sort temp0[h...e]
	//mergeSort(b, e+1,k);  // Sort temp0[e+1...k]
	merge(temp0, h,   el, e); // Merge the 2 segments
	merge(temp0, e+1, er, k); // Merge the other two segments
        merge(temp0, h,   e,  k); // Merge the whole segments
}

void mergeSort_cp(int* dest, int* temp0, int size)
{
  int l = 0;
  int r = size-1;
  mergeSort(temp0, l ,r );
  // Copy temp0 to dest array
  for(int i=0;i<size;i++) dest[i] = temp0[i];
}

int partition(int* temp0, int h, int k){
    int j;

    int i= h+1; j= k;
    while (i <= j) {
        if (temp0[i] < temp0[h]) i= i+1;
        else if (temp0[j] > temp0[h]) j= j-1;
        else {
            int t1= temp0[i]; temp0[i]= temp0[j]; temp0[j]= t1;
            i= i+1; j= j-1;
        }
    }
    int t= temp0[h]; temp0[h]= temp0[j]; temp0[j]= t;
    return j;
}
void quickSort(int* temp0, int l, int r)
{
    if (r-l+1 >= 2){
    int j = partition(temp0, l, r);
    quickSort(temp0, l, j-1);
    quickSort(temp0, j+1, r);}
}

void sort_mt(void* arg_vptr)
{
  // Cast void* to argument pointer.
  arg_t* arg_ptr = (arg_t*) arg_vptr;

  //Create local variables for each field of the argument structure.
  int* dest  = arg_ptr->dest;
  int* temp0 = arg_ptr->temp0;
  int  begin = arg_ptr->begin;
  int  end   = arg_ptr->end;

  int size = end-begin+1;  

  // Do the actual work.
  if(size>2) quickSort(dest, begin, end);

  //dummy copy temp0 into dest
  for(int i=0; i<size; i++) dest[i] = temp0[i];
}

void merge_mt(void* arg_vptr)
{
  // Cast void* to argument pointer
  arg_t* arg_ptr = (arg_t*) arg_vptr;

  // Create 
  int* dest = arg_ptr->dest;
  int* temp0 = arg_ptr->temp0;
  int  begin = arg_ptr->begin;
  int  end   = arg_ptr->end;
  
  int size = end-begin+1;
  if(size>2) mergeSort_cp( dest, temp0 , size); 

  for(int i=0;i<size;i++) dest[i]=temp0[i];

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

  // Initialize the bthread (bare thread)

  bthread_init();

  // Initialize dest array, which stores the final result.

  int dest[size];

  //--------------------------------------------------------------------
  // Start counting stats
  //--------------------------------------------------------------------

  test_stats_on();

  int block_size = size/4;

  int i = 0;

  // Because we need in-place sorting, we need to create a mutable temp
  // array.
  int temp0[size];

  for ( i = 0; i < size; i++ ) {
    temp0[i] = src[i];
  }

  arg_t arg0 = {dest, temp0, 0,              block_size};
  arg_t arg1 = {dest, temp0, block_size,   2*block_size};
  arg_t arg2 = {dest, temp0, 2*block_size, 3*block_size};
  arg_t arg3 = {dest, temp0, 3*block_size,         size};

  bthread_spawn( 1, &sort_mt, &arg1 );
  bthread_spawn( 2, &sort_mt, &arg2 );
  bthread_spawn( 3, &sort_mt, &arg3 );

  sort_mt( &arg0 );

  bthread_join(1);
  bthread_join(2);
  bthread_join(3);
//  mergeSort_cp( dest, &arg0, size);

  merge_mt(&arg0);

  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK:
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  //--------------------------------------------------------------------
  // Stop counting stats
  //--------------------------------------------------------------------

  test_stats_off();

  // verifies solution

  verify_results( dest, ref, size );

  return 0;
}
