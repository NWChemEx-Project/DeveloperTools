Proposed Tensor API
===================

The purpose of this page is to describe the purposed tensor API.  None of the
class names are necessarily finalized and thus should be seen as descriptive
placeholders.  We assume that all classes and functions are namespace protected,
but omit said namespace for simplicity.

Contents
--------

1. [Declaring Tensors](#declaring-tensors)  
   a. [General Construction](#general-construction)  
   b. [Sparse Construction](#sparse-construction)  
2. [Accessing Tensor Data](#accessing-tensor-data)  
   a. [General Considerations](#general-considerations)  
   b. [Data Locality Considerations](#data-locality-considerations)  
3. [Basic Operations](#basic-operations)
4. [Template Concerns](#concerns-about-template-meta-programming)  

What is a Tensor?
-----------------

When designing an API it helps to model the API after the real world object it
is implementing.  The present section justifies, motivates the basics of our 
purposed Tensor API by appealing the definition of a tensor.  To that end let us
define a tensor.  Particularly in chemistry we like to think of tensors as 
multidimensional arrays of scalars.  However, this is a very limited view from 
the mathematical perspective.  From the latter's standpoint, one of the most 
general definitions of a tensor is that it is an element of a module over a 
ring.  If your abstract algebra is rusty, what this means is we have two sets
of objects, call them **M** and **R**.  **M** will turn out to be the set of all
possible tensors and **R** will be the set of all possible elements for those 
tensors.  From an API standpoint, this immediately implies that our tensor class
depends on the type of its elements, *i.e.* minimally the type of our tensor 
class should be:

```cpp
template<typename ElementType>
class Tensor;
``` 

We can use the fact that the elements of our tensor form a ring to motivate the 
C++ concept `ElementType` must satisfy.  To that end, we know that the members
of **R** are paired with two operations, typically termed "addition" and 
"multiplication", which must satisfy: 

- **R** and "addition":
  - **R** is closed under "addition"
  - "addition" is associative
  - one element of **R** is the addition identity element
  - "addition" is invertible
  - "addition" is commutative
- **R** and "multiplication":
  - **R** is closed under "multiplication"
  - "multiplication" is associative
  - one element of **R** is the multiplicative identity  
- "multiplication" distributes over "addition"

For our API purposes, what this means is that the elements must semantically 
behave as if they minimally have the following API:

```cpp
struct ElementType {

    //Implements "addition"
    ElementType operator+(const ElementType& rhs)const
    {
        //return *this + rhs
    }
    
    //Implements adding by the inverse of rhs
    ElementOfARing operator-(const ElementOfARing& rhs)const
    {
       //return (*this) + additive_inverse(rhs)
    }
    
    //Implements "multiplication"
    ElementOfARing operator*(const ElementOfARing& rhs)const
    {
        //return *this * rhs
    }
};
```

We say "semantically behave like" because plain old data types, such as `double`
do not formally have such an interface; however, the various operations are 
defined so that writing say `A = B + C` works if `A`, `B`, and `C` are all of
type `double`.  If we define our tensor right then any type satisfying this 
API can be used in our tensor without modification.  As we'll see this leads to
some pretty cool features for our Tensor class which allows its feature set to 
be easily extendable.

Returning to our mathematical definition we now focus on the "module" part. A 
module is very similar to a ring except that the multiplication occurs between
elements of **M** and **R** as opposed to between elements of the same set, 
hence our tensor class must minimally have the following API (assuming we 
want to support both right and left modules...):

```cpp
template<typename ElementType>
class Tensor {
public:
    //Add two tensors together
    Tensor<ElementType> operator+(const Tensor<ElementType>& rhs);
    
    //Add the additive inverse of rhs to this
    Tensor<ElementType> operator-(const Tensor<ElementType>& rhs);
    
    //Right multiply by an element
    Tensor<ElementType> operator*(const ElementType& rhs);
};

//Left multiply by an element
template<typename ElementType>
Tensor<ElementType> operator*(const ElementType& lhs,
                              const Tensor<ElementType>& rhs);
```

Interestingly we see that if we defined an operation:

```cpp
Tensor<ElementType> operator*(const Tensor<ElementType>& rhs);
``` 

then our tensor would additionally be a ring and could be used as an element of
itself (in turn giving us blocking for free).  Unfortunately how to do this is 
not unique, as we may choose multiplication to be the tensor product, 
element-wise multiplication, or contraction.  It turns out that it is possible 
to uniquely differentiate between all three of these products using index 
notation and we consider the distinction in more detail there.  Before 
concluding this section we point out that the API for the tensor elements is 
quite general and any functor defining addition, subtraction, and multiplication
can be used.


Declaring Tensors
-----------------

The first step to using a tensor is to declare it.  We assert that our tensor 
should have some minimal constructors to ensure compatibility with STL objects:

1. Default constructor `TensorType T;`
2. Copy constructor `TensorType T(const TensorType&);`
3. Move constructor `TensorType T(TensorType&&);`

Respectively these constructors make a null (order and size are unspecified) 
tensor which is default parallelized (likely to mean serial or threaded as 
those are the only two safe to assume), deep copy an existing tensor instance,
and take ownership of another tensor instance.  When appropriate we expect all 
constructors (and destructors) to adhere to RAII. For the above three 
constructors this largely applies to numbers two and three. For number two, the 
constructor is expected to allocate the memory into which the deep copy will 
go.  For number three this entails taking ownership of the other tensor's 
memory and thus being responsible for its deletion.

### General Construction

Arguably the next most important consideration is how to specify the structure 
of the tensor (its order, lengths of dimensions, lengths of blocks, *etc.*). 
Generally speaking this can be a complicated thing.  To that end we purpose 
the `Shape` class.

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

It's perhaps worth mentioning that blocking requests by the user are to be taken
as defining the user's preferred API to the tensor and may be implemented by
the backend via "views" (strided access to bigger blocks).

Take home messages:
- Number of arguments to `Shape` corresponds to order of tensor.  
- Blockings are given by lists of the lengths of each block
- Lists of `Shape` instances allow nesting blocks

Being the primary object providing parallelism to NWChemEx it is also important
to consider how the tensor will get its parallel resources.  To that end we
purpose an opaque class `ParallelRuntime` which will provide access to those
resources (think `MPI_Comm` except for more than MPI), the exact details of
which are to be hashed out later.  In light of this object's existence we 
purpose a fourth constructor:

4. Parallel constructor `TensorType T(ParallelRuntime)`

which is the same as the default constructor except that the user has set the
parallelization strategy.  We expect all further constructors to come in two
flavors, one which takes a `ParallelRuntime` instance (plus any additional
arguments) and one which only takes the additional arguments, thus assuming 
the default parallelization strategy.  

Using the `Shape` class to specify the dimensions of the tensor naturally leads
to constructors of the forms:
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

One drawback of this approach is that the type of the Tensor is a bit nasty and
changes with the number of block nestings.  A solution would be to take a page 
from the STL and define a function `make_tensor` such that:

```.cpp
//Makes tensor H from above (use auto to save the headache of determining type)
auto MyTensor = make_tensor<double>(RT,Shape({3,7},{2,8}));
```

where the type `double` specifies the most nested element type.

### Sparse Construction

The next consideration to be discussed is sparsity.  We're interested in 
exploiting three types of sparsity: 

- Block sparsity: Entire subtensors of our tensor are zero and need not be
  stored
- Element sparsity: a large number of elements of the tensor are zero and need
  not be stored
- Rank sparsity: the tensor, or a block of our tensor, can be decomposed into
  the product of lower order tensors in turn reducing the number of meaningful
  elements to store

We'll return to rank sparsity in a minute.  For now we focuse on element/block
sparsity.  Mathematically the block and element sparsity are identical (element 
sparsity is recovered from block sparsity by taking each element to be a block 
and block sparsity is recovered from element sparsity by treating groups of 
non-zero and zero elements as blocks).  Thus the distinction between element 
and block sparsity surmounts to what `T` in `Tensor<T>` is.  Assuming our 
tensor class is capable of nesting *i.e.* `Tensor<Tensor<T>>`, then we only 
need to worry about two scenarios: are we use dense machinery or sparse 
machinery behind the scenes? As it is likely to change the entirety of the 
class's internals and because for a given tensor it is likely to be known at
compile time we purpose that the block/element sparsity be encoded in the 
type leading to the extended type of the tensor class:

```.cpp
template<typename T, typename SparsityPolicy=DensePolicy> class Tensor;
```  

This does not change the above examples, but does identify that they correspond
to dense tensors.  If we want to repeat our constructor for sparse tensors the
results are:

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

We now return to the issue of rank sparsity.  In rank sparsity we decompose
some tensor `A` into the product of two or more lower order tensors, for 
concreteness assume our decomposition is `A=BC`.  This means we don't want to
store the elements of `A`, but rather those of `B` and `C`.  If we define a 
class `TimesOp<T,U>`, which will take the product of an instance of type `T` and
an instance of type `U`, then what we effectively have is that the type of 
`A` is `Tensor<TimesOp<Tensor<TypeOfB>,Tensor<TypeOfC>>`.  Hence as long as 
we are capable of using a `TimesOp` as the type of an element of a tensor we 
have rank sparsity covered.  As a slight technical aside in addition to the
memory reduction, one of the advantages of tensor decomposition is that it can
allow the canonical equations to be refactored.  Under this proposed solution
for rank sparsity the decomposed equations are hidden from the user and thus
taking advantage of the decomposition then falls to tensor class. 

We conclude our constructor section by comparing to the current TAMM API.

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

There are a couple of key differences (based on my understanding of TAMM):
- The purposed API relies on RAII for allocation/deallocation whereas TAMM makes
  it a separate function call
  - Most C++ libraries will assume RAII, not adhering to it will make it hard to
    interface
- TAMM stores tensor sizes as global variable (otherwise I have no idea how the
  tensors figure out their sizes)
  - Global variables and/or singletons are considered an anti-pattern in C++ for
    many reasons, not the least of which is they make parallelism far harder
- The purposed API supports arbitrary blocking, whereas TAMM assumes minimally
  spin and irrep blocking on top of using one of the recognized subspaces
  - Not all tensors in electronic structure theory have spin (*e.g.* electric 
    field of nuclei)
  - Not all tensors have spatial symmetry (*e.g.* inertia tensor)
  - Depending on the application there's more than just alpha/beta spin 
    (*e.g.* NMR)
  - Can have multiple MO spaces (*i.e.* would need V1,V2,...,O1,O2,...)
  - Can have multiple fitting spaces
  - Can have multiple AO spaces
  


Accessing Tensor Data
---------------------

Filling a tensor is arguably one of the hardest things given that the actual
tensor's data may not be in core memory on the current process's hardware, 
*i.e.* the actual tensor (or pieces of it) may live on a different node, on a
MIC, on a GPU, or even on disk.  Filling the tensor is a problem closely 
coupled to accessing elements of the tensor and we require a similar solution 
for that as well.  This section will address both setting and getting of tensor
elements.  First we address the general API and then we address how access can 
be done in a manner that is agnostic to data layout (row-major, column-major,
block-cyclic, as well as where it lives such as in core, on disk, on GPU, etc.).

### General Considerations

Regardless of where the data lives the user has the right to
request any particular element, slice, or block.  Requesting an element is most
naturally done via:

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
```

Given the recursive nature of the purposed tensor class this naturally extends
to blocked tensors.

```.cpp
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

If one makes the returned element writable (*i.e.* a reference) then setting an
element is as simple as:
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

Filling blocks is of the same complication.

```.cpp
BlkTensorD AVector;//Assumed blocked vector
AVector(1)(2)=5.8;//Sets element 2 of block 1 to 5.8

BlkTensorD AMatrix;//Assumed matrix blocked along rows and columns
AMatrix(2,3)(4,5)=6.7; //Sets element 4,5 of block 2,3 to 6.7
```

There are two other useful ways to access elements of a tensor: slicing and
chipping.  Slicing is similar to accessing a block; however, the block's 
boundaries don't need to line up with those of the tensor's shape.  Slices have 
the same order as the original tensor.  Chipping on the other hand is a 
generalization of grabbing a row or column of a matrix; the result is a 
tensor of order one less than the original tensor.  Although it is tempting to
say chipping can be treated as extracting a block where one or more of the 
dimensions have length 1, doing so in this manner does not account for the
reduced order.  It is possible to extract any arbitrary subtensor using a 
combination of chips and slices.

TODO: Chip/Slice APIs

### Data Locality Considerations

The above is all well and good, albeit a bit short sited in that it artificially
suggests that accessing any piece of data is just as easy as accessing any 
other piece.  This is in general not true.  Whether its because of which index
runs fast or because is literally located somewhere else, data access speeds
vary.  Our present solution is to provide the user an iterator which returns the
tensor indices which are local, and in the order they are stored in.

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

This is fine, but in general we can do one better by generalizing the above a
bit (as having access to the data locality information is useful `local_range()`
exists and the tensor can be filled this way, but this is not the preferred 
means of doing so).  Instead we can piggy-back off the fact that our tensor 
class's elements can be stored as a function:

```.cpp
TensorD AMatrix; //Assume it's allocated
auto MappedMatrix = AMatrix.apply_map(
    [](double,index_type idx)
    {
        return fxn_that_computes_value_given_index(idx);
    });

```

Basic Operations
----------------

We'll skip some of the more mundane operations and instead go to the operations
that are the basis for science.  To that end we note that index notation is a
natural way to express tensor operations and wish to utilize it in our API.

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
Thus we see that the Einstein summation convention is obeyed for any index
absent on the left side and appearing twice on the right side.  Hence we also
see the difference between element-wise multiplication and contraction amounts 
to whether or not the indices are present on the left side.  Index notation 
also allows us to easily express the tensor product:
```cpp
DenseTensorD A("i","j","k","l") = B("i","j")*C("k","l");
``` 
as well as the normal matrix trace:
```cpp
///Disclaimer: the left side needs tested to see if that works
DenseTensorD A() = B("i","i");
```
and more complicated traces:
```cpp
DenseTensorD A("i","j") = B("i","j","k","k"); 
```

Element sparse matricies work identically, at the API level, as their dense 
brethren.  Assuming the blockings are compatible, even block matrix
operations can be written in this form.


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

//Literal translation to proposed API
auto i1("a","i") = f1("a","i") + 0.5*t1("j","b")*v2("b","a","j","i");
double de = t1("i","a")*i1("a","i");
de += 0.25*t2("k","l","c","d")*v2("c","d","k","l");
```

Decompositions
--------------

As mentioned, the trick to rank sparsity lies in being able to decompose a 
tensor.  Minimally our tensor class will need to support the following list of 
decompositions:

- Eigen decomposition
- Singular value decomposition
- Choleskey
- Tensor train
- Density fitting (more general?)

Generally speaking all of these decompositions are of the form the 


Concerns About Template Meta-Programming
----------------------------------------

As proposed above the API makes heavy use of template meta-programming 
techniques.  The result is a series of nasty types for even simple operations.  
For example adding three tensors is easily expressed:
```cpp
auto D = A("i","j")+B("i","j")+C("i","j");
``` 
The resulting type of D would be:

```.cpp
AddOp<AddOp<LabeledTensor<Tensor<double>>,LabeledTensor<Tensor<double>>>, 
      LabeledTensor<Tensor<double>>>
```

You can imagine that these types get nasty fast for something like coupled 
cluster.  Note that you as the user never need to know about this type (you'll 
use auto to capture any intermediate) and the type will always be evaluated 
to something like `Tensor<double>`.  Where the existence of these types do 
matter is that the compiler needs to instantiate each one.  This causes the 
compile time to increase (as well as the binary size).  The stereotypical 
solution to combat template bloat is to externally instantiate the 
common instantiations so the compiler only needs to instantiate them once.  This
only helps if there's a lot of common templates.  Obviously the type of the SCF 
equations is going to be different then that of coupled cluster, they will 
however have common subexpressions like `LabeledTensor<Tensor<double>>`.  It is
not clear that external instantiation will solve the problem.

As a back-up one can make the result of each operation simply be `Operation<T>`,
even when they nest (`T` being the most nested element type).  This can be done 
something like (this is pseudo-code meant to show intent):

```cpp
Operation<T> operator+(Operation<T>& rhs)
{
    this->dag_.add_op(std::plus<Tensor<T>>(),rhs);
    return Operation<T>(std::move(this->queue_));
}
```

The idea is that `Operation` holds some queue (likely implemented as a 
directed acyclic graph).  When the operations are nesting, the current 
operation adds the operation (here symbolized by `std::plus<Tensor<T>>`, which 
will work if `operator+` is overloaded), and the contents of the rhs to the 
DAG and makes a new Operation containing the updated queue.  The result is we
only have two templated classes; however, some of the work that would have 
been done at compile-time is now done at run-time (we also loose some compiler 
optimizations of the resulting expression).

The cool thing about this proposal is it's largely internal, *i.e.* you still 
invoke the command like:
```cpp
TensorD D("i","j")=A("i","j")+B("i","j")+C("i","j");
```
and capturing intermediates still works:
```cpp
auto i1 = A("i","j")+B("i","j");
TensorD D = i1("i","j")+C("i","j");
```

Open Questions
--------------

- Order as template non-type parameter (?)
  - No conceivable scenario where order isn't known at compile time
  - Allows compile-time error checking
  - Facilitates some compile-time optimizations
  - Increases number of template types
- Non uniform blocking, *i.e.* jagged or ragged arrays (?)  
