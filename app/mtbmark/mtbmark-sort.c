//========================================================================
// mtbmark-sort
//========================================================================

#include "common.h"
#include "mtbmark-sort.dat"

typedef struct {
  int* dest;  // pointer to dest array
  int* temp0;  // pointer to src0 array
  int  begin; // first element this core should process
  int  end;   // (one past) last element this core should process
} arg_t;

__attribute__((noinline))
void merge(int* temp0, int h, int e, int k)
{
	int i,j,k1;
	int n1 = e-h+1;
	int n2 = k-e;
	int part1[n1], part2[n2];
	for (i = 0; i < n1; i++)
        part1[i] = temp0[h + i];
    for (j = 0; j < n2; j++)
        part2[j] = temp0[e + 1+ j];
    
    
    i = 0; 
    j = 0; 
    k1 = h; 
    while (i < n1 && j < n2)
    {
        if (part1[i] <= part2[j])
        {
            temp0[k1] = part1[i];
            i++;
        }
        else
        {
            temp0[k1] = part2[j];
            j++;
        }
        k1++;
    }
 
    // Copy any remaining elements of part1[]
    while (i < n1)
    {
        temp0[k1] = part1[i];
        i++;
        k1++;
    }
 
    // Copy anyremaining elements of part2[]
    while (j < n2)
    {
        temp0[k1] = part2[j];
        j++;
        k1++;
    }
}
void mergeSort(int* temp0, int h, int k)
{
	if( h>=k ) return;
	int e  = h+(k-h)/2;
	mergeSort(temp0, h,  e);  // Sort temp0[h...e]
	mergeSort(temp0, e+1,k);  // Sort temp0[e+1...k]	
    merge(temp0, h, e,  k);   // Merge the whole segments

}

void mergeSort_cp(int* dest, int* temp0, int size)
{
  int l = 0;
  int r = size-1;
  mergeSort(temp0, l ,r );
  // Copy temp0 to dest array
  for(int i=0;i<size;i++) 
    dest[i] = temp0[i];
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

  int len = end-begin+1;  

  // Do the actual work.
  if( len>2 ) quickSort(dest, begin, end);

  //dummy copy temp0 into dest
  for(int i=0; i<len; i++) dest[i] = temp0[i];
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
  
  int len = end-begin;
  
  if(len>2) mergeSort_cp(dest,temp0 , len); 

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


  arg_t arg = {dest, temp0, 0, size};
  merge_mt(&arg);

  //--------------------------------------------------------------------
  // Stop counting stats
  //--------------------------------------------------------------------

  test_stats_off();

  // verifies solution

  verify_results( dest, ref, size );

  return 0;
}
