How the Code is Structured
==========================

The point of this page is to provide context on various aspects of NWChemEx's
code structure.

Contents
--------
1. [Interactions With Users](#interactions-with-users)  
2. [NWChemEx SDK](#nwchemex-sdk)    
   a. [Calculation Runtime](#calculation-runtime)  
   b. ["The" Calculation](#the-calculation)  
   c. [Math Kernel](#math-kernel)  

Interactions With Users
----------------------- 

At the very top-level NWChemEx is targeted at four types of users:
 
1. Normal users
   - Goal: run "normal" computations 
   - Okay switching to new input syntax
2. Old users
   - Goal: run "normal" computations
   - Use old NWChem syntax
3. Power users
   - Run non-standard computations
   - Non-invasively extend functionality
4. Developers
   - Extend the functionality of NWChemEx
The following use case diagram is meant to provide more details pertaining to
the typical use cases one can expect.       

![](uml/top_level.png)

It is reasonable to anticipate that the main consumers of NWChemEx are going 
to be users who want to run "normal calculations".  For our purposes a normal
calculation is one of the following:

- Single-point energy computation
- Geometry optimization
- Thermochemistry calculation 
  - IR/Raman frequencies and intensities
  - ZPE, Enthalpy, Entropy, Free Energy
- Wavefunction property
  - Electrostatic potential
  - Charge analysis
  - Molecular orbitals
- Dynamics     

Ideally one would like to be able to perform all of these calculations on an 
arbitrary level of theory, even if that means finite difference computations 
for higher-order derivatives.  Being an NWChem product we especially want the
above to work and perform well in highly-parallel environments.  

Additionally we anticipate power users wanting
direct access to non-standard information (Fock matrix, integrals, the actual
gradient/Hessian, *etc.*), the ability to control every aspect of the 
computation, and the ability to extend a computation (say take a previously 
computed SCF computation and then use it to run an MP2 calculation).

Finally, we want NWChemEx to be a viable platform for further scientific 
discovery.  This has several aspects:
- Program flow is easily scriptable
- New features can be added with minimal influence on the rest of the code
- Rapid prototyping is facilitated by highly-tuned reusable components
- Adding features (or anything really) "Just Works"

NWChemEx SDK
------------

In order to meet the use cases laid out in the previous section we purpose 
the NWChemEx SDK (software development kit).  Summarily NWChemEx SDK is 
comprised of two major components:
- Scripting layer
  - Runtime aspect
    - User-friendly API to run basic quantum chemistry
  - SDK aspect
    - Rapid prototyping
    - Access to non-standard details
    - Integration into other packages supporting the scripting language
- C++ core: NWChemEx
  - Implementations of all functions
  - Self-contained runtime, *i.e.* scripting layer is optional
    - Running performance critical applications
    - Direct interface for other packages
    - Support alternative scripting layers
  - Broadly speaking arranged into:
    - Stuff normal users care about ("the" calculation)
    - Stuff to support "the" calculation

The relationships among these components are summarized in the following 
package diagram.

![](uml/program_structure.png)

The scripting layer is a detachable user-centric API consisting of:
- Parser
    - Maps old NWChem syntax to new syntax
- Basic API
  - Routines for performing common tasks 
    - *e.g.* energy, geometry optimization, thermochemistry
    - Minimal input (say XYZ, basis name, and level of theory)
    - Written in terms of Full API under the hood
- Full API: 
  - Script bindings for the C++ Core
  - Test new workflow in "input"
  - Add new feature in "input"
  - "Rewire" NWChemEx from the "input" for advanced calculations
  
In this summary input is in quotes because the traditional view of an input 
file is gone and instead replaced with a literal script that is then run 
through the interpreter of choice.   

Powering the scripting layer is the C++ core, the contents of which are:  
- Calculation Runtime
  - Environment calculation is run in
  - Contains hardware runtime
- Checkpointing
  - Facilitates chauffeuring data from calculation runtime to disk
- Math Kernels
  - Optimized, parallelized, math libraries and functions
- "The" Calculation
  - Parts of NWChemEx users care about 
  - Chemical System
    - Relevant details of the chemical system the calculation will be run on                
  - Levels of Theory
    - Physical models for describing a chemical system
  - Post processing methods
    - Processes results of levels of theory


These subpartitionings are somewhat theoretical/conceptual.  In practice the 
actual components will be finer-grained than this.  To this end the next 
three sub sections consider the use cases of the major components of the C++ 
core. 

### Calculation Runtime

As mentioned, the calculation runtime represents the environment that the 
calculation is currently running in.  It is thus the interface between the 
literal user of NWChemEx, the hardware, and the internals of NWChemEx.  The 
use cases are summarized below.

![](uml/runtime_use.png)

For conceptual clarity we have grouped the the full calculation runtime into 
three nested runtimes.  

- Calculation runtime
  - Calculation state
    - "Log" of inputs to commands as well as their outputs
    - Very similar to RTDB (I think)
    - Key quantities to checkpoint
  - Chemical runtime
    - Describes the physics/chemistry the calculation is being run under
        - Fundamental constants and unit conversions
        - Basis set libraries
        - Force field parameters
  - Computer runtime
    - I/O to disk
    - Output to standard streams (standard out, error, debug)
    - Parallel runtime
      - Fundamental access to inter- and intra-process parallelization
        - Inter-process likely MPI
        - Intra-process CPU: OpenMP (?)
        - Accelerators... (?)
      - Task Queue
        - Both inter-process and intra-process queues
        - Likely implemented by other library

### "The" Calculation

Together the level of theory, any post processing done on it, and the chemical 
system components represent what is typically thought of as a quantum chemistry
calculation. We anticipate the major research endeavors of developers to be 
directed at these three components.  The following diagram depicts the major 
use cases of these components

![](uml/chemical_use.png)   

- Chemical system
  - Molecules
    - Identities and fundamental properties of the molecules/atoms in the system
    - Used to compute other properties
  - Fields
    - Any sort of field the system is embedded in
    - Electromagnetic
    - PCM (?)
    - EFP (?)
  - Periodicity
    - Description of the space system lives in
- Level of theory
  - Energy derivatives
  - Wavefunction/density
    - MM: density is just Dirac delta functions at nuclei
- Post processing

### Math Kernel

Given that NWChemEx ultimately is a collection of mathematical theories it is
no surprise that math kernels will play a central role.  The primary 
mathematical needs we have are: 

![](uml/math_use.png)

Briefly these use cases can be summarized by:

- Tensors
  - Bread and butter of quantum chemistry
  - Implemented by TAMM
- Transforms
  - Fourier transform likely others
- Numerical calculus
  - Finite difference
  - Numerical integration
    - DFT grids here (?)
- Math constants
  - Not Euler's number or pi, but rather things like factorials
- Graphs
- Numerical solvers       

It will be essential to have implementations of these use cases that are 
efficient both in massively parallel environments, but also on commodity 
hardware. 

Program Flow
------------

Based on the previous sections a natural program-flow is given by:

![](uml/program_flow.png)

We foresee two entry points into a run (*i.e.* any use case designed at 
obtaining chemical results):

1. Simple API
   - Only accessible via scripting API
   - Automatically calls the routines shown in the Full API flow column
   - Responsible for reporting results to user
     - If checkpointed, can be restarted via Full API to get other results 
2. Full API
   - Executed as a script if in the scripting layer
   - Hard coded into a `main` function if only using C++ runtime
   - User is responsible for printing desired results
      
Regardless of which entry point is used program flow proceeds according to:
1. Runtime is started
   - `MPI_Init`, `omp_get_max_threads()`, *etc.*
2. An initial chemical system instance is created
   - This need not be just "XYZ" to molecule, can be entire algorithm
   - Will typically be a single class
     - Most "multi-system" calculations are approximations to a single system
       - Fragment based, QM/MM, embedding methods: target is supersystem
     - For geometry optimizations/PES scans starting geometry
     - System generation is considered part of the calculation and done there            
   - Multiple instances sometimes *e.g.* transition state searches
   - Application of basis handled here
     - Ghost functions would be applied as part of calculation
3. An initial wavefunction is created
   - Do we ever need more than 1 wavefunction initially?
     - Multi-reference is multi-determinant, not multi-wavefunction
     - Excited state methods generate multiple wavefunctions as output
       - Use as generator for dynamics
   - Formally, even MM has a wavefunction       
4. Next we load the initial chemical runtime state
   - If this is a restart it comes from the checkpoint file
   - Else start with an empty one
   - Valid, trivially restartable state is key to using Jupyter notebooks
5. Run requested computation
   - The loop allows for multiple jobs to be in an input file
     - Directly using runtime allows parallelization of jobs here, but...
   - Computation maps to "do a parameter scan" not "run bond length 1.24"       
     - Coarse-grained parallelism within these commands
6. If desired, save the chemical runtime's state (presumably to disk)      
7. Shut down the runtime
   - `MPI_Finalize`, *etc.*
8. If this was simple input, return a simple output
   - Full API can literally do anything, up to user to log what they wanted
   - Simple output: literally print and **return** requested data
     - Printing for the user avoids problem of user running 2 week coupled 
       cluster, trashing checkpoint, and forgetting to print result...
     - Returning the requested quantity avoids users having to parse outputs 
       - Direct return allows for direct usage
   - Traditional output is little more than debug logs, avoid it
     - Saw it somewhere in the Google drive notes and liked this sentiment   
                              
    
Throughout the above description take note of the forced uniformity, *i.e.* 
"one system", "one wavefunction", *etc.* This makes it easier to define common 
interfaces for disparate things like QM/MM and coupled-cluster and to 
automate as much as possible.  The overall design goal is to branch at the last
possible second.


