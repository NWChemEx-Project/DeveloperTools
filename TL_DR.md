Examples of how to specify shape of tensor:
```.cpp
//Declare a range for a vector with length 10
Shape r1(10);//Equivalent to r({10})

//Declare a range for a vector with length 10 divided into blocks of lengths
//2, 3, and 5
Shape r2({2,3,5});

//Declare a range for same vector where the blocks are further subdivided into
//blocks of lengths (1 and 1), (1 and 2), and (3 and 2) respectively
Shape r3({Shape({1,1}),Shape({1,2}),Shape({3,2})});
               
//Declare a range for a 10 by 10 matrix
Shape r4(10,10);//Equivalent to r({10},{10});

//Declare a range for a matrix blocked into blocks 2x2, 2x8, 8x2, and 8x8     
Shape r5({2,8},{2,8});

//Quarter the blocks of the previous range
Shape r6({Shape({1,1}),Shape({4,4})},{Shape({4,4}),Shape({1,1})});    

//Only block rows of 10 by 10 matrix
Shape r7({2,8},{10});

//Only subdivide rows into blocks
Shape r8({Shape({1,1}),Shape({4,4})},{10});        
```

Using `Shape` class constructors look like:
```.cpp
using TensorD=Tensor<double>;

//Default constructed
TensorD A;

//Copy constructed
TensorD B(A);

//Move constructed
TensorD C(std::move(B));

//Non-default parallel runtime
ParallelRuntime RT;
TensorD D(RT);

//A 10 element vector using RT
TensorD E(RT,Shape(10));

//A 10 by 10 element matrix using the default parallel strategy
TensorD F(Shape(10,10));

//A 2 by 3 by 4 tensor using RT
TensorD G(RT,Shape(2,3,4));

//A 10 by 10 matrix blocked into 3x2, 3x8, 7x2, and 7x8 blocks using RT
using BlkTensorD=Tensor<TensorD>>;
BlkTensorD H(RT,Shape({3,7},{2,8}));

//A scalar (unlikely to be used by user)
TensorD I(RT,Shape());
```
After chatting with Robert, this part will likely change with SparsePolicy moving out of the type, but for posterity.

```.cpp
using SparseTensorD=Tensor<double,SparsePolicy>;

//Default constructed
SparseTensorD A;

//Copy constructed
SparseTensorD B(A);

//Move constructed
SparseTensorD C(std::move(B));

//Non-default parallel runtime
ParallelRuntime RT;
SparseTensorD D(RT);

//A 10 element vector using RT
SparseTensorD E(RT,Shape(10));

//A 10 by 10 element matrix using the default parallel strategy
SparseTensorD F(Shape(10,10));

//A 2 by 3 by 4 tensor using RT
SparseTensorD G(RT,Shape(2,3,4));

//A 10 by 10 matrix blocked into 3x2, 3x8, 7x2, and 7x8 blocks using RT
using BlkSparseTensorD=Tensor<SparseTensorD>>;
BlkSparseTensorD H(RT,Shape({3,7},{2,8}));
```
The last example shows us how to declare a tensor which contains blocks 
exhibiting element sparsity.  To declare a block sparse version we'd instead do:

```.cpp
//Same tensor, but now assuming block sparsity and that non-zero blocks are 
//dense
using SparseBlkTensorD=Tensor<TensorD,SparsePolicy>;
SparseBlkTensorD I(RT,Shape({3,7},{2,8}));

//Same except now has block sparsity and element sparsity
using SparseBlkSparseTensorD=Tensor<SparseTensorD,SparsePolicy>;
SparseBlkSparseTensorD J(RT,Shape({3,7},{2,8}));
```

A direct comparison to TAMM's current API:

```.cpp
//Parallel setup

//TAMM
TCE::init(spins, spatials, sizes,noa,noab,nva,nvab,spin_restricted,
          irrep_f,irrep_v,irrep_t,irrep_x,irrep_y);

Tensor<T> T1{V | O, irrep, spin_restricted};
Tensor<T> T2{VV | OO, irrep, spin_restricted};
Tensor<T> F1{N | N, irrep, spin_restricted};
Tensor<T> V2{NN | NN, irrep, spin_restricted};

//mgr and distribution are made during parallel setup
Tensor<T>::allocate(&distribution, mgr, T1, T2, F1, V2);

//Proposed API
Shape virt({Shape(nv_a,nv_b),Shape(nirreps)});
Shape occ({Shape(no_a,no_b),Shape(nirreps)});
Shape mos({Shape(nmo_a,nmo_b),Shape(nirreps)});

BlkTensorD T1(RT,Shape(virt,occ));
BlkTensorD T2(RT,Shape(virt,virt,occ,occ));
BlkTensorD F1(RT,Shape(mos,mos));
BlkTensorD V2(RT,Shape(mos,mos,mos,mos));
```

Beginning of musings on how to specify arbitrary index symmetries

```cpp
Symmetry sym;
//Establishes that elements 0,0 and 1,1 are equivalent
//Lambda syntax: 
//   input: index of input element, value of input element, index of element to 
//          generate 
//   return: The generated element
sym.add_symmetry({{0,0},{1,1}},
    [](IndexType& idx_in, ElementType& e_in, IndexType& idx_out){return e_in;});

//Convenience function for above
sym.are_equal({0,0},{1,1});

//Theoretically how one could make a 3x3 matrix symmetric with said API
Symmetry sym;
sym.are_equal({0,1},{1,0});
sym.are_equal({0,2},{2,0});
sym.are_equal({1,2},{2,1}); 
```

A better approach for full index symmetry:

```cpp
Symmetry sym;
//Establishes that element (i,j) equals element (j,i)
sym.add_idx_set({0,1});

//Establishes that element (i,j,k) equals element (i,k,j)
sym.add_idx_set({1,2});

//Establishes (i,j,k)==(i,k,j)==(j,i,k)==(j,k,i)==(k,i,j)==(k,j,i)
sym.add_idx_set({0,1,2});
``` 
How do we get Tensor Data?

```.cpp
TensorD AScalar;//Assume filled scalar
TensorD AVector;//Assume filled vector
TensorD AMatrix;//Assume filled matrix
TensorD ATensor;//Assume order 3 tensor

//Accessing element 5 of the vector
double a_5 = AVector(5);

//Accessing element 3,4
double a_34 = AMatrix(3,4);

//Accessing element 1,2,3 of the tensor
double a_123 = ATensor(1,2,3);


//Accessing scalar
double a = AScalar; //Scalars are implicitly convertible to an element type
double b = AScalar(); //Or via the same API as higher order tensors

//Single element access in TAMM
Tensor<T> A;//Assume initialized and order 3 tensor 
Block<T> blk = A.get(0); //(Must be blocked so assume 1 block)
T* buf = blk.buf();
T e_321 = buf[3*nrows*ncols + 2*ncols + 1]; //assuming row-major... 

BlkTensorD AVector;//Assume  filled and blocked
BlkTensorD AMatrix;//Assume filled and blocked along rows only
BlkTensorD AMatrix2;//Assume filled and blocked along rows and columns

//Returns block 1
TensorD blk_1 = AVector(1);

//Returns element 2 of block 1
double a_1_1 = AVector(1)(2);
//double a_1_1 = AVector(1,2);//Possible if rank is in type

//Returns block 3
TensorD blk_3 = AMatrix(3);

//Element 2,1 of block 3
double a_3_21 = AMatrix(3)(2,1);
//double a_3_21 = AMatrix(3,2,1);//Possible if rank is in type

//Returns block 5,9
TensorD blk_59 - AMatrix2(5,9);

//Returns element 3,1 of block 5,9
double a_59_31 = AMatrix2(5,9)(3,1);
//double a_59_31 = AMatrix2(5,9,3,1);//Possible if rank is in type

//TAMM
Tensor<T> A;//Assume initialized and matrix 
Block<T> blk = A.get(5,9);
T* buf = blk.buf();
T e_31 = buf[3*ncols + 1]; //assuming row-major... 
```
The element access can continue *ad infintum*, say for a blocked blocked tensor:

```.cpp
using BlkBlkTensorD=Tensor<BlkTensorD>;
BlkBlkTensorD A;//Assume initialized and matrix like at each blocking

//Get element 3,2 of subblock 4,5 of block 9,8
double a = A(9,8)(4,5)(3,2);

//TAMM
Tensor<T> B;//Assume initialized matrix
Block<T> blk = B.get(9*nblkcol*nsubrow*nsubcol+4,8*nsubrow*nsubcol+5);
T* buf = blk.buf();
T e_32 = buf[3*ncols + 2];//assuming row-major 
```
How does one write to a tensor?

```.cpp
TensorD AVector;//Assume a vector
AVector(3)=4.5;//Element 3 is now 4.5

TensorD AMatrix;//Assume a matrix
AMatrix(3,4)=5.6;//Element 3,4 is now 5.6

TensorD ATensor;//Assume an order 3 tensor
ATensor(3,4,5)=6.7;//Element 3,4,5 is now 6.7

TensorD AScalar;//Assume it's a scalar
AScalar=3.2;//Scalar assignment overloaded for element type
AScalar()=3.2;//Generalization of other API

//TAMM for a matrix
Tensor<T> A;
Block<T> blk = A.alloc(0);//Assume one block
T* buf = blk.buf();
blk[3*ncols+4]=5.6;
A.put(0,blk);
```

How does one set a block?

```.cpp
BlkTensorD AVector;//Assumed blocked vector
AVector(1)(2)=5.8;//Sets element 2 of block 1 to 5.8

BlkTensorD AMatrix;//Assumed matrix blocked along rows and columns
AMatrix(2,3)(4,5)=6.7; //Sets element 4,5 of block 2,3 to 6.7
```

Need to be able to do this in a manner that respects data locality:

```.cpp
TensorD AMatrix;//Assume this a row-major matrix all elements are local

//idx starts at (0,0) and then proceeds to (0,1), (0,2), ..., (1,0), ...
for(auto idx : AMatrix.local_range())//type would be std::vector-like
{   
    AMatrix(idx)=fxn_that_computes_value_given_index(idx);
}

TensorD AnotherMatrix;//Assume this one's column major

//idx starts at (0,0) and then proceeds to (1,0), (2,0), ..., (0,1), ...
for(auto idx : AnotherMatrix.local_range())
{
    AnotherMatrix(idx) = fxn_that_computes_value_given_index(idx);
}

TensorD YetAnotherMatrix;//Assume this one's row-major with period 2

//idx starts at (0,0) then goes to (0,2), (0,4), ..., (1, (ncols+1)%2), ...
for(auto idx : YetAnotherMatrix.local_range())
{
    YetAnotherMatrix(idx) = fxn_that_computes_value_given_index(idx);
}
```
Could also assign elements by giving tensor a function (really useful for integral direct)

```.cpp
TensorD AMatrix; //Assume it's allocated
auto MappedMatrix = AMatrix.apply_map(
    [](double,index_type idx)
    {
        return fxn_that_computes_value_given_index(idx);
    });

```

Function syntax allows for somewhat arbitrary operations (albeit they're likely to be inefficient)
```.cpp
TensorD LHSTensor;//Assume allocated
TensorD RHSTensor;//Assume allocated
auto Result=LHSTensor.apply_map([=](double lhs_elem, index_type idx)
    { return elem + RHSTensor(idx);});
```  

To add two tensors this looks like:
```.cpp
DenseTensorD A("i","j") = B("i","j")+C("i","j");
```
If we wanted to define `A` to `B` plus `C` transpose:
```cpp
DenseTensorD A("idx 1","idx 2") = B("idx 1","idx 2") + C("idx 2", "idx 1");
```
this example also illustrates that the indices can be arbitrary length strings.
Subtraction is done analogous to addition (except with a minus sign).  To scale
by a constant:
```cpp
DenseTensorD A("i","j") = 3.4*B("i","j");
```
To transpose:
```cpp
DenseTensorD A("j","i") = B("i","j");
```
Where things really get fun is multiplication.  Element-wise multiplication is
done via:
```cpp
DenseTensorD A("i","j") = B("i","j")*C("i","j");
```
Normal matrix multiplication:
```cpp
DenseTensorD A("i","j") = B("i","k")*C("k","j");
```
`A` equals `B` times `C` transpose:
```cpp
DenseTensorD A("i","j") = B("i","k")*C("j","k");
```
Tensor product
```cpp
DenseTensorD A("i","j","k","l") = B("i","j")*C("k","l");
``` 
as well as the normal matrix trace:
```cpp
DenseTensorD A() = B("i","i");

//Overloaded for scalar
double A = B("i","i");
```
and more complicated traces:
```cpp
DenseTensorD A("i","j") = B("i","j","k","k"); 
```
Comparision to TAMM's API

```cpp
//TAMM
  sch.alloc(i1)
      .io(f1, v2, t1, t2)
      .output(de)
          (i1(h6, p5) = f1(h6, p5))
          (i1(h6, p5) += 0.5 * t1(p3, h4) * v2(h4, h6, p3, p5))
          (de() = 0)
          (de() += t1(p5, h6) * i1(h6, p5))
          (de() += 0.25 * t2(p1, p2, h3, h4) * v2(h3, h4, p1, p2))
      .dealloc(i1);

//Literal translation to proposed API (not sure spin is right...)
auto i1("s","t")("a","i") = f1("s","t")("a","i") + 
         0.5*t1("u","v")("j","b")*v2("v","s","u","t")("b","a","j","i");
double de = t1("t","s")("i","a")*i1("s","t")("a","i");
de += 0.25*t2("s","u","t","v")("a","b","i","j")*
           v2("t","v","s","u")("i","j","a","b");
```

How do we do decompositions?

```cpp
TensorD A;//Assume square matrix and filled

//I=QDQ^-1
EigenDecomposition<Tensor<T>> evs(I);

//Get Q
TensorD Q = evs.Q();

//Get diagonal
TensorD D = evs.D();

//Get Q^-1
TensorD Qinv = evs.Q_inv();
```

Possible to use decompositions as part of tensor expressions:

```cpp
TensorD A;
EigenDecomposition<TensorD> evs(A);

//Some equation "C=AB" where we use "evs" instead
TensorD C("i","k")=evs("i","j")*B("j","k");

//The backend actually sees: C=(QDQ^-1)B and optimizes that expression
```
