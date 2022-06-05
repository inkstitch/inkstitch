#!/bin/bash
# first part of codesiging which is importing to build keychain
echo $MACOS_CERTIFICATE | base64 --decode > certificate.p12
security create-keychain -p "$KEYCHAIN_PWD" build.keychain
security default-keychain -s build.keychain
security unlock-keychain -p "$KEYCHAIN_PWD" build.keychain
security import certificate.p12 -k build.keychain -P "$MACOS_CERTIFICATE_PWD" -T /usr/bin/codesign
security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k "$KEYCHAIN_PWD" build.keychain
# importing notary certificate
echo $INSTALLER_CERTIFICATE | base64 --decode > installer-certificate.p12
security import installer-certificate.p12 -k build.keychain -P "$INSTALLER_PWD" -T /usr/bin/pkgbuild
security set-key-partition-list -S apple-tool:,apple:,pkgbuild: -s -k "$KEYCHAIN_PWD" build.keychain
