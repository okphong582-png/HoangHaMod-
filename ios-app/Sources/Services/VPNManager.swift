import Foundation
import UIKit

class VPNManager: ObservableObject {
    static let shared = VPNManager()
    
    @Published var isConnected: Bool = false
    @Published var serverAddress: String = ""
    @Published var isDownloadingProfile: Bool = false
    @Published var statusMessage: String = "Sẵn sàng kết nối"
    
    func downloadAndInstallVPNProfile(serverUrl: String, completion: @escaping (Bool) -> Void) {
        self.isDownloadingProfile = true
        self.statusMessage = "Đang kết nối Server PC HoangHa VIP..."
        
        guard let url = URL(string: "\(serverUrl)/api/register_device?hwid=\(getDeviceHWID())") else {
            self.isDownloadingProfile = false
            self.statusMessage = "URL Server PC không hợp lệ"
            completion(false)
            return
        }
        
        let task = URLSession.shared.dataTask(with: url) { [weak self] data, response, error in
            DispatchQueue.main.async {
                self?.isDownloadingProfile = false
                if let error = error {
                    self?.statusMessage = "Lỗi kết nối Server: \(error.localizedDescription)"
                    completion(false)
                    return
                }
                
                self?.isConnected = true
                self?.serverAddress = serverUrl
                self?.statusMessage = "Đã kết nối VPN & Đăng ký luồng PC thành công!"
                completion(true)
            }
        }
        task.resume()
    }
    
    func disconnectVPN() {
        self.isConnected = false
        self.statusMessage = "Đã ngắt kết nối VPN"
    }
    
    func getDeviceHWID() -> String {
        if let vendorId = UIDevice.current.identifierForVendor?.uuidString {
            return vendorId
        }
        return "IOS_DEVICE_" + UUID().uuidString.prefix(8)
    }
}
