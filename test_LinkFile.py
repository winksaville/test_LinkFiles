#!/usr/bin/python

# Copyright (C) 2015 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import subprocess

DBG = False
VDBG = False

rootLinks = {
  "Kbuild":".build/Kbuild",
  "Kconfig":".build/Kconfig",
  "Makefile":".build/Makefile",
  "mstr-configs":"apps/helloworld/master-configs",
  "newapp.sh":".build/newapp.sh",
  }

configsLinks = {
  "ia32_simulation_helloworld_defconfig":"../apps/helloworld/master-configs/ia32_simulation_helloworld_defconfig",
  }

libsLinks = {
  "libsel4":"../kernel/libsel4",
  }

srcsLinks = {
  "bootinfo.c":"../kernel/libsel4/src/bootinfo.c",
  "bootstrap.c":"../libs/libsel4utils/src/vspace/bootstrap.c",
  "client_server_vspace.c":"../libs/libsel4utils/src/vspace/client_server_vspace.c",
  "client_server_vspace.h":"../libs/libsel4utils/include/sel4utils/client_server_vspace.h",
  "elf.c":"../libs/libsel4utils/src/elf.c",
  "elf.h":"../libs/libsel4utils/include/sel4utils/elf.h",
  "helpers.h":"../libs/libsel4utils/src/helpers.h",
  "iommu_dma.c":"../libs/libsel4utils/src/iommu_dma.c",
  "iommu_dma.h":"../libs/libsel4utils/include/sel4utils/iommu_dma.h",
  "irq_server.c":"../libs/libsel4utils/src/irq_server/irq_server.c",
  "irq_server.h":"../libs/libsel4utils/include/sel4utils/irq_server.h",
  "mapping.c":"../libs/libsel4utils/src/mapping.c",
  "mapping.h":"../libs/libsel4utils/include/sel4utils/mapping.h",
  "page_dma.c":"../libs/libsel4utils/src/page_dma.c",
  "page_dma.h":"../libs/libsel4utils/include/sel4utils/page_dma.h",
  "process.c":"../libs/libsel4utils/src/process.c",
  "process.h":"../libs/libsel4utils/include/sel4utils/process.h",
  "profile.c":"../libs/libsel4utils/src/profile.c",
  "profile.h":"../libs/libsel4utils/include/sel4utils/profile.h",
  "sel4_debug.c":"../libs/libsel4utils/src/sel4_debug.c",
  "stack.c":"../libs/libsel4utils/src/stack.c",
  "util.h":"../libs/libsel4utils/include/sel4utils/util.h",
  "stack.h":"../libs/libsel4utils/include/sel4utils/stack.h",
  "vspace.h":"../libs/libsel4utils/include/sel4utils/vspace.h",
  "vspace.c":"../libs/libsel4utils/src/vspace/vspace.c",
  "thread.c":"../libs/libsel4utils/src/thread.c",
  "thread.h":"../libs/libsel4utils/include/sel4utils/thread.h",
  "vspace_internal.h":"../libs/libsel4utils/include/sel4utils/vspace_internal.h",
  "sel4_debug.h":"../libs/libsel4utils/include/sel4utils/sel4_debug.h",
  }

def displayDifferent(dic1, dic1Label, dic2, dic2Label):
  """Display what keys are missing from either dictionary"""
  setDic1 = set(dic1)
  setDic2 = set(dic2)
  intersection = setDic1.intersection(setDic2)

  for key in intersection:
    if dic1[key] != dic2[key]:
      print("  %s has \"%s\":\"%s\"" % (dic2Label, key, dic2[key]))
      print("    but in %s it was \"%s\":\"%s\"" % (dic1Label, key, dic1[key]))

def displayMissing(dic1, dic1Label, dic2, dic2Label):
  """Display what keys are missing from either dictionary"""
  setDic1 = set(dic1)
  setDic2 = set(dic2)
  dic1Diff = setDic1 - setDic2
  dic2Diff = setDic2 - setDic1

  for key in dic1Diff:
    print("  \"%s\":\"%s\", was missing from %s" % (key, dic1[key], dic2Label))

  for key in dic2Diff:
    print("  \"%s\":\"%s\", was missing from %s" % (key, dic2[key], dic1Label))

def check_dir(directory, expectedEntries):
  """Check if directory is correct"""
  lsoutput = subprocess.check_output(['ls', "-al", directory])
  lines = lsoutput.split("\n")
  foundEntries = {} 
  for line in lines:
    words = re.split(" +", line)
    if len(words) >= 11 and (words[0][0] == 'l'):
      foundEntries[words[8]] = words[10]
      if DBG: print("links[%s]=%s" % (words[8], foundEntries[words[8]]))


  result = cmp(expectedEntries, foundEntries)
  if result != 0 or DBG or VDBG:
    print("Errors in directory %s" % directory)
    if VDBG:
      print("expectedEntries len=%s" % len(expectedEntries))
      print("  key/values=%s" % expectedEntries)
      print("")
      print("foundEntries len=%s:" % len(foundEntries))
      print("  key/values=%s" % foundEntries)
      print("")
    displayMissing(expectedEntries, "expectedEntries", foundEntries, "foundEntries")
    displayDifferent(expectedEntries, "expectedEntries", foundEntries, "foundEntries")

  return result == 0

root="/Users/wink/prgs/repo/helloworld-test-linkfiles"

testList = (
  (root, rootLinks),
  (os.path.join(root, "configs"), configsLinks),
  (os.path.join(root, "libs"), libsLinks),
  (os.path.join(root, "srcs"), srcsLinks)
  )

errors = 0
for directory, expectedEntries in testList:
  result = check_dir(directory, expectedEntries)
  if not result:
    errors += 1

if errors == 0:
  print("Success")
else:
  print("%s errors" % errors)
