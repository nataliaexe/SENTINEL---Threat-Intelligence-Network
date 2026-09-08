import socket
import time

def test_ssh_honeypot():
    try:
        print("🔌 Conectando ao honeypot SSH...")
        s = socket.socket()
        s.connect(('localhost', 2222))
        s.settimeout(15)  # Timeout de 15 segundos
        print("✅ Conectado!")
        
        # Receber banner SSH
        time.sleep(1)
        banner = s.recv(1024)
        print(f"📝 Banner: {banner.decode().strip()}")
        
        # Aguardar prompt de login
        time.sleep(1)
        try:
            login_prompt = s.recv(1024)
            print(f"📝 Prompt: {login_prompt.decode().strip()}")
        except:
            print("📝 Prompt: (não recebido)")
        
        # Enviar username
        username = "root"
        print(f"👤 Enviando username: {username}")
        s.send(f"{username}\n".encode())
        
        # Aguardar prompt de senha
        time.sleep(2)
        try:
            pass_prompt = s.recv(1024)
            print(f"📝 Prompt senha: {pass_prompt.decode().strip()}")
        except:
            print("📝 Prompt senha: (não recebido)")
        
        # Enviar senha
        password = "123456"
        print(f"🔑 Enviando senha: {password}")
        s.send(f"{password}\n".encode())
        
        # Tentar receber resposta
        time.sleep(2)
        try:
            response = s.recv(1024)
            print(f"📝 Resposta: {response.decode().strip()}")
        except:
            print("📝 Resposta: (conexão fechada pelo honeypot)")
        
        s.close()
        print("✅ Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("ℹ️ Isso pode ser normal se o honeypot fechou a conexão")

if __name__ == "__main__":
    test_ssh_honeypot()
