Using Jenkins
=============

These are notes on how our Jenkins CI server works.  To that end I'll start by
noting the server itself is located at http://jenkins-ci.lcrc.anl.gov.  You'll
need an LCRC account to access it.  When you follow that link you'll be taken to
our group's dashboard.  On this dashboard you will see the projects Jenkins 
manages the testing for.  

Adding a New Repo to Jenkins
----------------------------

Configuring Jenkins occurs primarily when a new repo is added to a GitHub
organization.  Jenkins automatically scans the GitHub organization for new 
repos.  When a new repo is found Jenkins looks for a file called `Jenkinsfile`
in that repo.  This file describes the procedure Jenkins will use to test the
repo.  For most NWX repos the procedure is quite boilerplate and we have 
factored that boilerplate out into a script that lives in 
`DeveloperTools/ci/Jenkins/nwxJenkins.groovy`.  Your `Jenkinsfile` needs to 
construct a build matrix, load the aforementioned script, and forward the build
matrix to it.  The script will take care of the rest.  To accomplish this start
with a `Jenkinsfile` that looks like (the `Jenkinsfile.example` in this repo
already contains the following):

```groovy
def repoName="Your repo's name"
def buildModuleMatrix = [
    		   "GCC 7.1.0":("cmake gcc/7.1.0")
		  ]		  
node{
    def nwxJenkins
    stage('Import Jenkins Commands'){
        sh """
        da_url=https://raw.githubusercontent.com/NWChemEx-Project/
        da_url+=DeveloperTools/master/ci/Jenkins/nwxJenkins.groovy
        wget \${da_url} 
        """
        nwxJenkins=load("nwxJenkins.groovy")
    }
    nwxJenkins.commonSteps(buildModuleMatrix, repoName)
}
```

To add additional builds you simply add different sets of modules to the build
matrix.  For example, to also test GCC 7.3.0 you'd modify the matrix to be:

```groovy
def buildModuleMatrix = [
    		   "GCC 7.1":("cmake gcc/7.1.0"),
    		   "GCC 7.3":("cmake gcc/7.3.0")
		  ]
```		  
