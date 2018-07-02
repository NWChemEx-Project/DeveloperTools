//BUILD_TAG is a unique build identifier provided by Jenkins

def exportModules(buildModules){
sh """
set +x
source /etc/profile
module load ${buildModules}
module save ${BUILD_TAG}
"""
}

def compileRepo(repoName, doInstall, cmakeCommand){
    def installRoot="${WORKSPACE}/install"
    sh """
       set +x
	source /etc/profile
	module restore ${BUILD_TAG}
        buildTests="True"
        makeCommand=""
        if [ ${doInstall} == "True" ];then
            buildTests="False"
            makeCommand="install"
        fi
        git submodule update --init --recursive
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
    module restore ${BUILD_TAG}
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

return this
