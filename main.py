# replace tasks
import os

import module_templates as mdt
import utils


# two major part: project name & module name
# eg:
# project name => react-native-turbo-module
# module name => Module
# rtn module name [base on module name] => RTNModule
# native module name[base on module name] => NativeModule


def parseJavaPackage(package_name):
    return package_name.split('.')


# /Users/_sseon/data/python/scripts/new_arch/./main.py[或 main.py]
current_script_path: str = __file__


def generatePackageJson():
    content = mdt.buildPackageJsonFromTemplate(project_name, user_name, email, rtn_module_name, java_package_name)
    with open(package_json, 'w+') as f:
        f.write(content.removeprefix('\n'))


def generatePodspec():
    content = mdt.buildPodspecFromTemplate(project_name)
    with open(podspec, 'w+') as f:
        f.write(content.removeprefix('\n'))


def generateJsModule():
    content = mdt.buildJsModuleFromTemplate(rtn_module_name)
    with open(js_native_module, 'w+') as f:
        f.write(content.removeprefix('\n'))


def generateIosH():
    content = mdt.buildIosModuleHFromTemplate(rtn_module_name, native_module_name)
    with open(ios_module_h, 'w+') as f:
        f.write(content.removeprefix('\n'))


def generateIosMM():
    content = mdt.buildIosModuleMMFromTemplate(rtn_module_name, native_module_name)
    with open(ios_module_mm, 'w+') as f:
        f.write(content.removeprefix('\n'))


def generateAndroidBuildGradle():
    content = mdt.buildAndroidBuildGradleFromTemplate(java_package_name)
    with open(an_build_gradle, 'w+') as f:
        f.write(content.removeprefix('\n'))


def generateAndroidModuleClass():
    content = mdt.buildAndroidModuleClassFromTemplate(java_package_name, module_class, native_module_name, rtn_module_name)
    with open(an_module_class, 'w+') as f:
        f.write(content.removeprefix('\n'))


def generateAndroidPackageClass():
    content = mdt.buildAndroidModulePackageFromTemplate(java_package_name, package_class, module_class)
    with open(an_package_class, 'w+') as f:
        f.write(content.removeprefix('\n'))


if __name__ == '__main__':

    global java_package_name
    global project_name
    global module_name
    global user_name
    global email
    global gen_module_path

    args = utils.parseArgs()

    # --java-package
    # --name (project name)
    # --module (module name: Orientation )
    # --user
    # --email

    p_java_package = utils.getArgParam(args, 'java-package')
    p_name = utils.getArgParam(args, 'name')
    p_module = utils.getArgParam(args, 'module')
    p_user = utils.getArgParam(args, 'user')
    p_email = utils.getArgParam(args, 'email')
    if p_java_package == '':
        utils.error("android package-name [--java-package] cannot leave empty!")
        exit(-1)
    if p_name == '':
        utils.error("project name [--name] cannot leave empty!")
        exit(-1)
    if p_module == '':
        utils.error("module name [--module] cannot leave empty!")
        exit(-1)
    if p_user == '':
        user_name = 'USER_NAME'
    else:
        user_name = p_user
    if p_email == '':
        email = 'USER_EMAIL_DOMAIN'
    else:
        email = p_email

    java_package_name = p_java_package
    project_name = p_name
    module_name = p_module

    rtn_module_name = 'RTN' + module_name
    native_module_name = 'Native' + module_name
    ios_platform_version = '13'
    module_class = module_name + 'Module'
    package_class = module_name + 'Package'

    gen_module_path = os.path.join(os.getcwd(), project_name)
    # gen_module_path = os.path.join(current_script_path.removesuffix('main.py'), 'build', project_name)

    package_json = os.path.join(gen_module_path, 'package.json')
    podspec = os.path.join(gen_module_path, project_name + '.podspec')
    __js_src = os.path.join(gen_module_path, 'js')
    js_native_module = os.path.join(__js_src, native_module_name + '.ts')
    __ios_src = os.path.join(gen_module_path, 'ios')
    ios_module_h = os.path.join(gen_module_path, 'ios', rtn_module_name + '.h')
    ios_module_mm = os.path.join(gen_module_path, 'ios', rtn_module_name + '.mm')
    __an_src = os.path.join(gen_module_path, 'android', 'src')
    an_build_gradle = os.path.join(gen_module_path, 'android', 'build.gradle')
    __an_package = os.path.join(__an_src, 'main/java', java_package_name.replace('.', '/', -1))
    an_module_class = os.path.join(__an_package, module_class + '.kt')
    an_package_class = os.path.join(__an_package, package_class + '.kt')

    if not os.path.exists(gen_module_path):
        os.makedirs(gen_module_path, 0o777)
    if not os.path.exists(__an_src):
        os.makedirs(__an_src, 0o777)
    if not os.path.exists(__an_package):
        os.makedirs(__an_package, 0o777)
    if not os.path.exists(__ios_src):
        os.makedirs(__ios_src, 0o777)
    if not os.path.exists(__js_src):
        os.makedirs(__js_src, 0o777)

    generatePackageJson()
    generateJsModule()
    generatePodspec()
    generateIosH()
    generateIosMM()
    generateAndroidBuildGradle()
    generateAndroidModuleClass()
    generateAndroidPackageClass()

    utils.info("🎉 " + project_name + " is generated, you can find it at location: " + gen_module_path)
