#!/usr/bin/env python

import subprocess
import os
import sys


# clone from git


#ffmpeg_location='git://source.ffmpeg.org/ffmpeg.git'



#if (os.path.isdir('./ffmpeg')):
 #   print 'directory \'ffmpeg\' already exists!'
  #  sys.exit()
  #  pass

# clone to local directory
#subprocess.call('git clone ' + ffmpeg_location + ' ffmpeg', shell=True)



os.chdir('..')


class ArchDesc(object):
    def __init__(self, arch, aarch, cputype, SDK_ver, SDK_ver_min):
        self.arch = arch
        self.aarch = aarch
        self.cputype = cputype
        self.SDK_ver = SDK_ver
        self.SDK_ver_min = SDK_ver_min        
    pass



arch_list = []
arch_list.append(ArchDesc('armv7', 'armv7', 'generic', 'iphoneos', ' -miphoneos-version-min=7.0'))
arch_list.append(ArchDesc('arm64', 'aarch64', 'generic', 'iphoneos', ' -miphoneos-version-min=7.0'))
arch_list.append(ArchDesc('i386', 'i386', 'i386', 'iphonesimulator', ' -mios-simulator-version-min=7.0'))
arch_list.append(ArchDesc('x86_64', 'x86_64', 'x86_64', 'iphonesimulator', ' -mios-simulator-version-min=7.0'))



#mkdir -p ./${output_root}/${build_config}/yympeg.library/lib
#mkdir -p ./${output_root}/${build_config}/yympeg.library/include
# copy headers
#cp -a yympeg/include/*.h    ./${output_root}/${build_config}/yympeg.library/include



def get_xcrun_path(sdk, ver, opt2):
    full_cmd = 'xcrun --sdk ' + sdk + ver + ' ' + opt2
    path = subprocess.check_output(full_cmd, shell=True)
    return path





lipo_cmd = 'lipo -create '



for itr in (arch_list):

    #configure_cmd  = 'echo Configure for ' + itr.arch + ' build '
    
    print 'Configure for ' + itr.arch + ' build......'

    clang_path   = get_xcrun_path(itr.SDK_ver, '11.0', '-find clang')
    libtool_path = get_xcrun_path(itr.SDK_ver, '11.0', '-find libtool')
    sdk_path     = get_xcrun_path(itr.SDK_ver, '11.0', '--show-sdk-path')
    
    clang_path   = clang_path.rstrip()
    libtool_path = libtool_path.rstrip()
    sdk_path     = sdk_path.rstrip()
    
    configure_cmd  = './configure'
    configure_cmd += ' --cc=' + clang_path
    configure_cmd += ' --arch=' + itr.aarch
    configure_cmd += ' --cpu=' + itr.cputype
    configure_cmd += ' --sysroot=' + sdk_path
    configure_cmd += ' --target-os=darwin'
    configure_cmd += ' --prefix=compiled/' + itr.arch
    configure_cmd += ' --extra-cflags=\'-arch '  + itr.arch + itr.SDK_ver_min + '\''
    configure_cmd += ' --extra-ldflags=\'-arch ' + itr.arch + itr.SDK_ver_min + '\''
    configure_cmd += ' --enable-cross-compile --enable-pic '
    configure_cmd += ' --as=\'/usr/local/bin/gas-preprocessor.pl ' + clang_path + '\''
    configure_cmd += ' --disable-everything --disable-iconv --enable-decoder=h264 --enable-decoder=hevc --enable-asm '
    
    print configure_cmd + '\r\n\r\n'
    subprocess.call(configure_cmd, shell=True)
    subprocess.call('make clean', shell=True)
    subprocess.call('make', shell=True)
    subprocess.call('make install', shell=True)
    
    print 'begin build libyympeg.a for ' + itr.arch + '......'
    libtool_cmd  = libtool_path
    libtool_cmd += ' -static -arch_only ' + itr.arch
    libtool_cmd += ' -syslibroot ' + sdk_path
    libtool_cmd += ' -Lcompiled/' + itr.arch + '/lib -lavcodec -lavdevice -lavfilter -lavformat -lavutil -lswresample -lswscale '
    libtool_cmd += ' -o ./compiled/' + itr.arch + '/lib/libyympeg.a'
    
    print libtool_cmd + '\r\n\r\n\r\n\r\n'
    subprocess.call(libtool_cmd, shell=True)
    
    lipo_cmd += ' ./compiled/' + itr.arch + '/lib/libyympeg.a'

# the final lipo command
lipo_cmd += ' -output ./compiled/libyympeg.a'

print lipo_cmd
subprocess.call(lipo_cmd, shell=True)






