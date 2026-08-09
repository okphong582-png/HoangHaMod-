// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "HoangHaMod",
    platforms: [
        .iOS(.v15)
    ],
    products: [
        .executable(name: "HoangHaMod", targets: ["HoangHaMod"])
    ],
    dependencies: [],
    targets: [
        .executableTarget(
            name: "HoangHaMod",
            dependencies: [],
            path: "Sources"
        )
    ]
)
