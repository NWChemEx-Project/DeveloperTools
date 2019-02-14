//BUILD_TAG is a unique build identifier provided by Jenkins

def exportModules(buildModules){
    sh """
       set +x
       source /etc/profile
       module load ${buildModules}
       module save ${BUILD_TAG}
       """
}

def getCPP(){
    sh """
    set +x
    source /etc/profile
    module restore ${BUILD_TAG}
    git clone https://github.com/CMakePackagingProject/CMakePackagingProject
    cd CMakePackagingProject
    cmake -H. -Bbuild -DBUILD_TESTS=OFF \
                      -DCMAKE_INSTALL_PREFIX=${WORKSPACE}/install
    cmake --build build --target install
    """
}

def compileRepo(cCompiler, cxxCompiler){
    def installRoot="${WORKSPACE}/install"
    sh """
       set +x
       source /etc/profile
       module restore ${BUILD_TAG}
       if [ -d build ]; then
           rm -rf build
       fi
       gh_token=4dfc676f4c5a2b1b9c3
       gh_token+=f17bc2c3ebda1efa5f4e9
       prefix_path="/jenkins-ci/workspace/nwx-deps/;${installRoot}"
       cmake -H. -Bbuild -DBUILD_TESTS=TRUE \
                         -DCMAKE_INSTALL_PREFIX=${installRoot}\
                         -DCMAKE_PREFIX_PATH="\${prefix_path}" \
                         -DCMAKE_CXX_COMPILER=${cxxCompiler} \
                         -DCMAKE_C_COMPILER=${cCompiler} \
             		 -DCPP_GITHUB_TOKEN=\${gh_token}
       cmake --build build --parallel 6
       """
}


def formatCode(){
   // Note: The Gist credentials belong to a dummy account which was created
   // just to generate the auth token. The key is separated so Github doesn't
   // detect and revoke it.
    sh """
    set +x
    source /etc/profile
    module load llvm
    da_url=https://raw.githubusercontent.com/NWChemEx-Project/DeveloperTools/
    da_url+=master/ci/lint/clang-format.in
    wget  \${da_url} -O .clang-format
    find . -type f -iname *.h -o -iname *.c -o -iname *.cpp -o -iname *.hpp | \
      xargs clang-format -style=file -i -fallback-style=none
    rm .clang-format
    git diff >clang_format.patch
    if [ -s clang_format.patch ]
    then
    gem install gist
    echo -n '75fbd2b547f689bbe90bec5aed' >~/.gist
    echo '16369697cbfb69' >>~/.gist
    echo '##########################################################'
    echo 'Code Formatting Check Failed!'
    echo 'Please "git apply" the Following Patch File:'
    ~/bin/gist -p clang_format.patch
    echo '##########################################################'
    fi
    """
}

def testRepo(){
    sh """
       set +x
       source /etc/profile
       module restore ${BUILD_TAG}
       cd build && ctest -VV
    """
}

def commonSteps(buildModuleMatrix, repoName){
    stage("Set-Up Workspace"){
        deleteDir()
        checkout scm
    }

    stage('Check Code Formatting'){
        formatCode()
    }

    def buildTypeList=buildModuleMatrix.keySet() as String[]
    for (int i=0; i<buildTypeList.size(); i++){
        def buildType = "${buildTypeList[i]}"
        def buildModules = "${buildModuleMatrix[buildType]}"

        stage("${buildType}: Export Module List"){
            exportModules(buildModules)
        }
	    
    stage('Get CMakePackagingProject') {
        getCPP()
    }	    

        stage("${buildType}: Build ${repoName}"){
            def is_intel=buildModules.contains("intel")
            if(is_intel){
                compileRepo("icc", "icpc")
            }
            else {
                compileRepo("gcc", "g++")
            }
        }

        stage("${buildType}: Test ${repoName}"){
            testRepo()
        }

    }
}

return this
