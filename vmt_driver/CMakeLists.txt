cmake_minimum_required(VERSION 3.10)
project(vmtdriver VERSION 1.15.0 DESCRIPTION "vmtdriver")

set(CMAKE_CXX_STANDARD 14)

set(SOURCE_FILES
    ../json.hpp
    ../openvr-1.23.7/headers/openvr_driver.h
    ../oscpack_1_1_0/ip/IpEndpointName.h
    ../oscpack_1_1_0/ip/NetworkingUtils.h
    ../oscpack_1_1_0/ip/PacketListener.h
    ../oscpack_1_1_0/ip/TimerListener.h
    ../oscpack_1_1_0/ip/UdpSocket.h
    ../oscpack_1_1_0/osc/MessageMappingOscPacketListener.h
    ../oscpack_1_1_0/osc/OscException.h
    ../oscpack_1_1_0/osc/OscHostEndianness.h
    ../oscpack_1_1_0/osc/OscOutboundPacketStream.h
    ../oscpack_1_1_0/osc/OscPacketListener.h
    ../oscpack_1_1_0/osc/OscPrintReceivedElements.h
    ../oscpack_1_1_0/osc/OscReceivedElements.h
    ../oscpack_1_1_0/osc/OscTypes.h
    CommunicationManager.h
    Config.h
    DirectOSC.h
    framework.h
    dllmain.h
    Log.h
    ServerTrackedDeviceProvider.h
    TrackedDeviceServerDriver.h
    VRWatchdogProvider.h
    ../oscpack_1_1_0/ip/IpEndpointName.cpp
    ../oscpack_1_1_0/ip/posix/NetworkingUtils.cpp
    ../oscpack_1_1_0/ip/posix/UdpSocket.cpp
    ../oscpack_1_1_0/osc/OscOutboundPacketStream.cpp
    ../oscpack_1_1_0/osc/OscPrintReceivedElements.cpp
    ../oscpack_1_1_0/osc/OscReceivedElements.cpp
    ../oscpack_1_1_0/osc/OscTypes.cpp
    CommunicationManager.cpp
    Config.cpp
    DirectOSC.cpp
    dllmain.cpp
    Log.cpp
    ServerTrackedDeviceProvider.cpp
    TrackedDeviceServerDriver.cpp
    VRWatchdogProvider.cpp
)

include_directories(
    ..
    ../openvr-1.23.7/headers
    ../eigen-3.3.7
    ../oscpack_1_1_0
)

add_library(driver_vmt SHARED ${SOURCE_FILES})
