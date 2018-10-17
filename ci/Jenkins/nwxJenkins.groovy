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
    module load cmake
    git clone https://github.com/CMakePackagingProject/CMakePackagingProject
    cd CMakePackagingProject
    cmake -H. -Bbuild -DBUILD_TESTS=OFF \
                      -DCMAKE_INSTALL_PREFIX=${WORKSPACE}/install
    cmake --build build --target install
    """
}

def compileRepo(repoName){
    def installRoot="${WORKSPACE}/install"
    sh """
       set +x
	   source /etc/profile
	   module restore ${BUILD_TAG}
	   if [ -d build ]; then
	       rm -rf build
	   fi
       cmake -H. -Bbuild -DBUILD_TESTS=TRUE \
                         -DCMAKE_INSTALL_PREFIX=${installRoot}\
                         -DCMAKE_PREFIX_PATH=${installRoot} \
                         -DCMAKE_CXX_COMPILER=g++ \
                         -DCMAKE_C_COMPILER=gcc
       cmake --build build
       """
}


def formatCode(){
// Note: The Gist credentials belong to a dummy account which was created just to generate the auth token. The key is separated so Github doesn't detect and revoke it.
    sh """
    set +x
    source /etc/profile
    module load llvm
    wget https://raw.githubusercontent.com/NWChemEx-Project/DeveloperTools/master/ci/lint/clang-format.in -O .clang-format
    find . -type f -iname *.h -o -iname *.c -o -iname *.cpp -o -iname *.hpp | xargs clang-format -style=file -i -fallback-style=none
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

    stage('Get CMakePackagingProject') {
        getCPP()
    }

    def buildTypeList=buildModuleMatrix.keySet() as String[]
    for (int i=0; i<buildTypeList.size(); i++){
        def buildType = "${buildTypeList[i]}"

        stage("${buildType}: Export Module List"){
            def buildModules = "${buildModuleMatrix[buildType]}"
            exportModules(buildModules)
        }

        stage("${buildType}: Build Repo"){
            compileRepo(repoName)
        }

        stage("${buildType}: Test Repo"){
            testRepo()
        }

    }
}

return this
