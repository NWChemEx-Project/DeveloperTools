//NWChemEx Jenkins Commands for Argonne LCRC Site

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
// Note: The Gist credentials belong to a dummy account which was created just to generate the auth token. The key is separated so Github doesn't detect and revoke it.
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



def buildDependencies(String[] depends, cmakeCommand, credentialsID){

for (int i=0; i<depends.size(); i++){
    dir("${depends[i]}"){
        git credentialsId:"${credentialsID}",
        url:"https://github.com/NWChemEx-Project/${depends[i]}.git",
        branch: 'master'
        nwxJenkins.compileRepo("${depends[i]}", "True", cmakeCommand)
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
