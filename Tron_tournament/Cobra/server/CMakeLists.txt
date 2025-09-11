
cmake_minimum_required(VERSION 3.16)
project(tron_battle LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Try Qt6 then Qt5
find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets Network)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets Network)

add_executable(tron_battle
    src/main.cpp
    src/AppConfig.cpp
    src/GameModel.cpp
    src/GameServer.cpp
    src/TickLoop.cpp
    src/MainWindow.cpp
    src/GameView.cpp
)

target_include_directories(tron_battle PRIVATE src)

target_link_libraries(tron_battle PRIVATE
    Qt${QT_VERSION_MAJOR}::Widgets
    Qt${QT_VERSION_MAJOR}::Network
)

if (WIN32)
    target_compile_definitions(tron_battle PRIVATE _WIN32_WINNT=0x0601)
endif()
