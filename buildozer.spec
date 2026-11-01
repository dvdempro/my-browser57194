[app]
title = My Browser
package.name = mybrowser
package.domain = org.browser

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Обязательно: pyjnius и android для WebView и run_on_ui_thread
requirements = python3,kivy,pyjnius,android

orientation = portrait

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Отключаем лишние архитектуры для ускорения сборки (только 64-bit ARM)
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
