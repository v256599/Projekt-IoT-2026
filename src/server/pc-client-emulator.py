import socket
import json
import sys

def client():
    
    #Get info
    ip_adresa = input("Server IP:").strip()
    port = int(input("Port:").strip())
    token = input("Token:").strip()
    if ip_adresa and port and token:
        print(f"\n[*] Conn INFO: {ip_adresa}:{port}")
    else:
        print(f"\n[*] Ukončuji, chybné informace")
        exit();
    
    #Create Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5.0) #!!!Socket TIMEOUT
    

    while True:
        print("\n" + "="*40)
        # Get MSG to Send
        akce = input("Zprava (action):").strip()
          
        # Make json
        zprava_dict = {"action": akce, "token": token}
        zprava_json = json.dumps(zprava_dict)
        
        try:
            # Send
            print(f"\n[-->] SEND: {zprava_json}")
            client_socket.sendto(zprava_json.encode('utf-8'), (ip_adresa, port))
            
            # Wait to response
            data, server = client_socket.recvfrom(1024)
            
            odpoved = data.decode('utf-8')
            print(f"[<--] RECV: {odpoved}")
            
        except socket.timeout:
            print("[-] Chyba: Timeout")
        except ConnectionResetError:
            print("[-] Chyba: ConnReset")
        except Exception as e:
            print(f"[-] GenericError: {e}")


if __name__ == "__main__":
    try:
        client()
    except KeyboardInterrupt:
        print("\n======================KONEC====================")
        sys.exit(0)