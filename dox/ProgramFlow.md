Program Flow
============

The point of this section is to describe the flow of NWChemEx at various 
points during execution and at various levels of detail.  

Overall Flow
------------

Based on the layout of the packages within NWChemEx a natural flow for the 
program is:

![](uml/program_flow.png)

We foresee two entry points into a run (*i.e.* any use case designed at 
obtaining chemical results):

1. Basic API
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
   - Parallel-wise: `MPI_Init`, `omp_get_max_threads()`, *etc.*
   - Chemical-wise: Load selected basis set, atomic constants, *etc.*
   - Calculation-wise: Modules to be used, default options, *etc.*
2. An initial chemical system instance is created
   - This need not be just "XYZ" to molecule, can be entire algorithm
     - Algorithm examples: symmetrizing molecule, replicating, *etc.* 
   - System will be a single instance (typically)
     - Most "multi-system" calculations are approximations to a single system
       - Fragment based, QM/MM, embedding methods: target is supersystem
     - For geometry optimizations/PES scans starting geometry
     - System generation is considered part of the calculation and done there            
     - Multiple instances sometimes *e.g.* transition state searches
   - Application of basis handled here
     - Ghost functions would be applied as part of calculation
   - Wavefunction is part of chemical system
     - Do we ever need more than 1 wavefunction initially?
     - Multi-reference is multi-determinant, not multi-wavefunction
     - Excited state methods generate multiple wavefunctions as output
       - Use as generator for dynamics
     - Formally, even MM has a wavefunction       
3. Load the initial chemical state
   - If this is a restart it comes from the checkpoint file
   - Else start with an empty one
   - Valid, trivially restartable state is key to using Jupyter notebooks
5. Run requested computation
   - The loop allows for multiple jobs to be in an input file
     - Directly using runtime allows parallelization of jobs here, but...
   - Computation maps to "do a parameter scan" not "run bond length 1.24"       
     - Coarse-grained parallelism within these commands
6. If desired, save the calculation's state (presumably to disk)      
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

Running "The" Calculation
-------------------------

In this section we take a look at the process of running a calculation (or 
more generally speaking running a module).  There are two ways to run a module:

1. Via `run_and_log` member function of `CalculationState`
2. Directly calling `run` on the result of `get_module`

They differ in that the first option will automatically log the result (think
of it as the equivalent of the user running the module and then hitting save 
afterwards), whereas the second option will not save the result.  `run_and_log` 
is thus best thought of as a wrapper around scenario 2.  For this reason this is
the preferred mechanism for running a module; however, we ultimately leave the 
choice of how to call a submodule up to the writer of the module.  The following
sequence diagram shows the steps that occur within a `CalculationState` instance
when a user calls the `run_and_log` member function.

![](uml/run_and_log.png)

1. The `CalculationState` builds a new instance of the requested module
2. Arguments to `run_and_log` are forwarded to the module's `hash` function.
   - The hash is assumed unique for each unique input
     - In practice requires combining the hashes of
       1. The input arguments 
       2. Relevant options
       3. All submodules
       4. (possibly) the module info (*i.e.* version info)
3. A check is made to see if we already have the result
   - If it we don't, we compute and save it
4. The result is returned   

This mechanism keeps a dynamic record of a computation's state, using 
pre-cached data when available to speed up computation.  Furthermore, by 
pre-loading the cache with the answers, calls amount to little more than a 
pointer dereference (*i.e.* are basically free).  As written this call does 
not save the computation's state.  At least initially, the idea is that the 
user of `CalculationState` will save the contents manually.  The next step is
to make the `results` member an intelligent class that is capable of 
automatically saving itself to disk.  Long-term the intent is that this class
becomes more sophisticated by also gaining the ability to automatically free up
memory (*i.e.* via some yet to be derived mechanism it would know that 
certain results can be deleted; whereas other results cannot, but can be moved 
to disk).
