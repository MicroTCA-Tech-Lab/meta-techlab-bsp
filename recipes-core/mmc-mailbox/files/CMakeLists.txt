cmake_minimum_required(VERSION 3.0)

project(mmc-mailbox VERSION 1.0.0)

include(GNUInstallDirs)

add_library(mmcmb SHARED mmcmb.c)
set_target_properties(mmcmb PROPERTIES PUBLIC_HEADER "mmcmb/mmcmb.h;mmcmb/fpga_mailbox_layout.h")
set_target_properties(mmcmb PROPERTIES VERSION ${PROJECT_VERSION})

# Invoke cmake with -DMAILBOX_FILE=/sys/bus/i2c/devices/5-002a/eeprom to adapt mailbox file path to the platform
if(MAILBOX_FILE)
    message(STATUS "Set mailbox file to ${MAILBOX_FILE}")
    target_compile_definitions(mmcmb PRIVATE MB_DEVICE_FILE="${MAILBOX_FILE}")
else()
    message(FATAL_ERROR "Define mailbox file path, such as -DMAILBOX_FILE=/sys/bus/i2c/devices/5-002a/eeprom")
endif()

install(TARGETS mmcmb
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/mmcmb
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})

add_executable(mmcinfo mmcinfo.c)
target_link_libraries(mmcinfo mmcmb)
install(TARGETS mmcinfo DESTINATION ${CMAKE_INSTALL_BINDIR})

add_executable(mmcctrld mmcctrld.c)
target_link_libraries(mmcctrld mmcmb)
install(TARGETS mmcctrld DESTINATION ${CMAKE_INSTALL_SBINDIR})
