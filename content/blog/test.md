---
title: "Lorem Ipsum"
author: "yayoi_mizuha"
images: ["img/eye-catch/test.png"]
textonimage: "test"
date: 2020-05-26T02:42:38+09:00
draft: false
description: "test post"
categories: ["test"]
tags: ["test"]
---

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.


###### 6
##### 5
#### 4
### 3
## 2
# 1
0

[this code is from here](https://github.com/ROCmSoftwarePlatform/tensorflow-upstream/blob/develop-upstream/configure.py)
```

# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""configure script to get build parameters from user."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import errno
import os
import platform
import re
import subprocess
import sys

# pylint: disable=g-import-not-at-top
try:
  from shutil import which
except ImportError:
  from distutils.spawn import find_executable as which
# pylint: enable=g-import-not-at-top

_DEFAULT_CUDA_VERSION = '10'
_DEFAULT_CUDNN_VERSION = '7'
_DEFAULT_TENSORRT_VERSION = '6'
_DEFAULT_CUDA_COMPUTE_CAPABILITIES = '3.5,7.0'

_TF_OPENCL_VERSION = '1.2'
_DEFAULT_COMPUTECPP_TOOLKIT_PATH = '/usr/local/computecpp'
_DEFAULT_TRISYCL_INCLUDE_DIR = '/usr/local/triSYCL/include'
_SUPPORTED_ANDROID_NDK_VERSIONS = [10, 11, 12, 13, 14, 15, 16, 17, 18]

_DEFAULT_PROMPT_ASK_ATTEMPTS = 10

_TF_BAZELRC_FILENAME = '.tf_configure.bazelrc'
_TF_WORKSPACE_ROOT = ''
_TF_BAZELRC = ''
_TF_CURRENT_BAZEL_VERSION = None
_TF_MIN_BAZEL_VERSION = '2.0.0'
_TF_MAX_BAZEL_VERSION = '3.99.0'

NCCL_LIB_PATHS = [
    'lib64/', 'lib/powerpc64le-linux-gnu/', 'lib/x86_64-linux-gnu/', ''
]

# List of files to configure when building Bazel on Apple platforms.
APPLE_BAZEL_FILES = [
    'tensorflow/lite/experimental/ios/BUILD',
    'tensorflow/lite/experimental/objc/BUILD',
    'tensorflow/lite/experimental/swift/BUILD',
    'tensorflow/lite/tools/benchmark/experimental/ios/BUILD'
]

# List of files to move when building for iOS.
IOS_FILES = [
    'tensorflow/lite/experimental/objc/TensorFlowLiteObjC.podspec',
    'tensorflow/lite/experimental/swift/TensorFlowLiteSwift.podspec',
]



```