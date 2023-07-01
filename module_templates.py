PROJECT_NAME = 'PROJECT_NAME'  # react-native-orientation
MODULE_NAME = 'MODULE_NAME'  # Orientation
RTN_MODULE_NAME = 'RTN_MODULE_NAME'  # RTNOrientation
NATIVE_MODULE_NAME = 'NATIVE_MODULE_NAME'  # NativeOrientation
USERNAME = 'USERNAME'
EMAIL = 'EMAIL'
JAVA_PACKAGE_NAME = 'JAVA_PACKAGE_NAME'  # com.orientation
IOS_PLATFORM_VERSION = 'IOS_PLATFORM_VERSION'  # default to 13
MODULE_CLASS = 'MODULE_CLASS'  # OrientationModule.java
PACKAGE_CLASS = 'PACKAGE_CLASS'  # OrientationPackage.java

podspec_template = '''
require "json"

package = JSON.parse(File.read(File.join(__dir__, "package.json")))

Pod::Spec.new do |s|
  s.name            = "PROJECT_NAME"
  s.version         = package["version"]
  s.summary         = package["description"]
  s.description     = package["description"]
  s.homepage        = package["homepage"]
  s.license         = package["license"]
  s.platforms       = { :ios => "11.0" }
  s.author          = package["author"]
  s.source          = { :git => package["repository"], :tag => "#{s.version}" }

  s.source_files    = "ios/**/*.{h,m,mm,swift}"

  install_modules_dependencies(s)
end
'''


def buildPodspecFromTemplate(project_name):
    return podspec_template.replace(PROJECT_NAME, project_name, -1)


package_json_template = '''
{
    "name": "PROJECT_NAME",
    "version": "0.0.1",
    "description": "react-native",
    "react-native": "js/index",
    "source": "js/index",
    "files": [
        "js",
        "android",
        "ios",
        "PROJECT_NAME.podspec",
        "!android/build",
        "!ios/build",
        "!**/__tests__",
        "!**/__fixtures__",
        "!**/__mocks__"
    ],
    "keywords": [
        "react-native",
        "ios",
        "android"
    ],
    "repository": "https://github.com/USERNAME/PROJECT_NAME",
    "author": "USERNAME USERNAME@EMAIL (https://github.com/USERNAME)",
    "license": "MIT",
    "bugs": {
        "url": "https://github.com/USERNAME/PROJECT_NAME/issues"
    },
    "homepage": "https://github.com/USERNAME/PROJECT_NAME#readme",
    "devDependencies": {},
    "peerDependencies": {
        "react": "*",
        "react-native": "*"
    },
    "codegenConfig": {
        "name": "RTN_MODULE_NAMESpec",
        "type": "modules",
        "jsSrcsDir": "js",
        "android": {
            "javaPackageName": "JAVA_PACKAGE_NAME"
        }
    }
}
'''


def buildPackageJsonFromTemplate(project_name, user_name, email, rtn_module_name, java_package_name):
    t = package_json_template.replace(PROJECT_NAME, project_name, -1)
    t = t.replace(USERNAME, user_name, -1)
    t = t.replace(EMAIL, email, -1)
    t = t.replace(RTN_MODULE_NAME, rtn_module_name, -1)
    t = t.replace(JAVA_PACKAGE_NAME, java_package_name, -1)
    return t


js_module_template = '''
import type { TurboModule } from 'react-native/Libraries/TurboModule/RCTExport';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
    
}
export default TurboModuleRegistry.get<Spec>('RTN_MODULE_NAME') as Spec | null;
'''


def buildJsModuleFromTemplate(rtn_module_name):
    return js_module_template.replace(RTN_MODULE_NAME, rtn_module_name, -1)


ios_module_h_template = '''
#import <RTN_MODULE_NAMESpec/RTN_MODULE_NAMESpec.h>

NS_ASSUME_NONNULL_BEGIN

@interface RTN_MODULE_NAME : NSObject <NATIVE_MODULE_NAMESpec>

@end

NS_ASSUME_NONNULL_END
'''


def buildIosModuleHFromTemplate(rtn_module_name, native_module_name):
    t = ios_module_h_template.replace(RTN_MODULE_NAME, rtn_module_name, -1)
    t = t.replace(NATIVE_MODULE_NAME, native_module_name, -1)
    return t


ios_module_mm_template = '''
#import "RTN_MODULE_NAMESpec.h"
#import "RTN_MODULE_NAME.h"
#import <Foundation/Foundation.h>

@implementation RTN_MODULE_NAME

RCT_EXPORT_MODULE()

- (std::shared_ptr<facebook::react::TurboModule>)getTurboModule:
    (const facebook::react::ObjCTurboModule::InitParams &)params
{
    return std::make_shared<facebook::react::NATIVE_MODULE_NAMESpecJSI>(params);
}

@end
'''


def buildIosModuleMMFromTemplate(rtn_module_name, native_module_name):
    t = ios_module_mm_template.replace(RTN_MODULE_NAME, rtn_module_name, -1)
    t = t.replace(NATIVE_MODULE_NAME, native_module_name, -1)
    return t


#相对于java类，多了Kotlin的依赖
android_build_gradle_template = '''
buildscript {
  ext.safeExtGet = {prop, fallback ->
    rootProject.ext.has(prop) ? rootProject.ext.get(prop) : fallback
  }
  repositories {
    google()
    gradlePluginPortal()
  }
  dependencies {
    classpath("com.android.tools.build:gradle:7.3.1")
    classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:1.7.22")
  }
}

apply plugin: 'com.android.library'
apply plugin: 'com.facebook.react'
apply plugin: 'org.jetbrains.kotlin.android'

android {
  compileSdkVersion safeExtGet('compileSdkVersion', 33)
  namespace "JAVA_PACKAGE_NAME"
}

repositories {
  mavenCentral()
  google()
}

dependencies {
  implementation 'com.facebook.react:react-native'
}
'''


def buildAndroidBuildGradleFromTemplate(java_package_name):
    return android_build_gradle_template.replace(JAVA_PACKAGE_NAME, java_package_name, -1)


android_module_class_template = '''
package JAVA_PACKAGE_NAME

import com.facebook.react.bridge.Promise
import com.facebook.react.bridge.ReactApplicationContext
import JAVA_PACKAGE_NAME.NATIVE_MODULE_NAMESpec

class MODULE_CLASS(reactContext: ReactApplicationContext) : NATIVE_MODULE_NAMESpec(reactContext) {

  override fun getName() = NAME

  companion object {
    const val NAME = "RTN_MODULE_NAME"
  }
}
'''


def buildAndroidModuleClassFromTemplate(java_package_name, module_class, native_module_name, rtn_module_name):
    t = android_module_class_template.replace(JAVA_PACKAGE_NAME, java_package_name, -1)
    t = t.replace(MODULE_CLASS, module_class, -1)
    t = t.replace(NATIVE_MODULE_NAME, native_module_name, -1)
    t = t.replace(RTN_MODULE_NAME, rtn_module_name, -1)
    return t


android_module_package_template = '''
package JAVA_PACKAGE_NAME;

import com.facebook.react.TurboReactPackage
import com.facebook.react.bridge.NativeModule
import com.facebook.react.bridge.ReactApplicationContext
import com.facebook.react.module.model.ReactModuleInfo
import com.facebook.react.module.model.ReactModuleInfoProvider

class PACKAGE_CLASS : TurboReactPackage() {
 override fun getModule(name: String?, reactContext: ReactApplicationContext): NativeModule? =
   if (name == MODULE_CLASS.NAME) {
	MODULE_CLASS(reactContext)
   } else {
     null
   }

 override fun getReactModuleInfoProvider() = ReactModuleInfoProvider {
   mapOf(
	MODULE_CLASS.NAME to ReactModuleInfo(
	MODULE_CLASS.NAME,
	MODULE_CLASS.NAME,
       false, // canOverrideExistingModule
       false, // needsEagerInit
       true, // hasConstants
       false, // isCxxModule
       true // isTurboModule
     )
   )
 }
}
'''


def buildAndroidModulePackageFromTemplate(java_package_name, package_class, module_class):
    t = android_module_package_template.replace(JAVA_PACKAGE_NAME, java_package_name)
    t = t.replace(PACKAGE_CLASS, package_class)
    t = t.replace(MODULE_CLASS, module_class)
    return t
