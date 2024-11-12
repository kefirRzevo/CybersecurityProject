cmake_minimum_required(VERSION 3.12)
project(Cybersecurity)

include(ExternalProject)
ExternalProject_Add(
  mp4parser
  
  GIT_REPOSITORY https://github.com/DigiDNA/ISOBMFF.git
  GIT_TAG main

  CONFIGURE_COMMAND ""
  UPDATE_COMMAND ""
  PATCH_COMMAND ""
  TEST_COMMAND ""
  INSTALL_COMMAD ""

  BUILD_IN_SOURCE True
) # Если не либа не компилируется, в мэйкфале ставим компилятор gcc и убераем флаги -stdlib и -lc++
