[app]
title = My Browser
package.name = mybrowser
package.domain = org.browser
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,android,pyjnius
orientation = portrait
android.minapi = 14
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
