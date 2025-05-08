#  download OpenSSL
	https://slproweb.com/products/Win32OpenSSL.html
	
# run below command to generate SSL.
	openssl req -x509 -nodes -days 9125 -newkey rsa:2048 -keyout ./nginx_ssl.key -out ./nginx_ssl.crt
	
# refer snap.png for configs.