#NWChemEx Jenkins Commands for Argonne LCRC Site

def exportModules(buildModules){
sh """
set +x
source /etc/profile
module load ${buildModules}
module save nwx-buildModules
"""
}

def compileRepo(repoName, doInstall, cmakeCommand){
    def installRoot="${WORKSPACE}/install"
    sh """
       set +x
	source /etc/profile
	module restore nwx-buildModules
        buildTests="True"
        makeCommand=""
        if [ ${doInstall} == "True" ];then
            buildTests="False"
            makeCommand="install"
        fi
        cmake -H. -Bbuild -DBUILD_TESTS=\${buildTests} \
                          -DCMAKE_INSTALL_PREFIX=${installRoot}\
                          -DCMAKE_PREFIX_PATH=${installRoot}\
			  ${cmakeCommand}
        cd build && make \${makeCommand}
    """
}


def formatCode(){
// Note: The Gist credentials belong to a dummy account which was created just to generate the auth token
    sh """
    set +x
    source /etc/profile
    module restore nwx-buildModules
    wget https://raw.githubusercontent.com/NWChemEx-Project/DeveloperTools/master/ci/lint/clang-format.in -O .clang-format
    find . -type f -iname *.h -o -iname *.c -o -iname *.cpp -o -iname *.hpp | xargs clang-format -style=file -i -fallback-style=none
    rm .clang-format
    git diff >clang_format.patch
    if [ -s clang_format.patch ]
    then
    gem install gist
    echo '17f8954a565c9684397022a2b5a20bd0837a20e7' >~/.gist
    echo '##########################################################'
    echo 'Code Formatting Check Failed!'
    echo 'Please "git apply" the Following Patch File:'
    ~/bin/gist -p clang_format.patch
    echo '##########################################################'
    exit 1
    fi
    """
}



def buildDependencies(String[] depends, cmakeCommand, credentialsID){

for (int i=0; i<depends.size(); i++){
    dir("${depends[i]}"){
        git credentialsId:"${credentialsID}"
        url:"https://github.com/NWChemEx-Project/${depends[i]}.git",
        branch: 'master'
        compileRepo("${depends[i]}", "True", cmakeCommand, credentialsID)
        }
    }
}

def testRepo(){
    sh """
    set +x
    source /etc/profile
    module restore nwx-buildModules
    cd build && ctest
    """
}

return this