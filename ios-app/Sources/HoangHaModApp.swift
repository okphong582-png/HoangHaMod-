import SwiftUI

@main
struct HoangHaModApp: App {
    @State private var isLoggedIn: Bool = false
    @State private var userKey: String = ""
    @State private var remainingSeconds: Int = 86400 * 30
    @State private var pcServerUrl: String = "https://hoangha.loca.lt"
    
    var body: some Scene {
        WindowGroup {
            if isLoggedIn {
                MainDashboardView(
                    isLoggedIn: $isLoggedIn,
                    userKey: $userKey,
                    remainingSeconds: $remainingSeconds,
                    pcServerUrl: $pcServerUrl
                )
            } else {
                LoginView(
                    isLoggedIn: $isLoggedIn,
                    userKey: $userKey,
                    remainingSeconds: $remainingSeconds,
                    pcServerUrl: $pcServerUrl
                )
            }
        }
    }
}
