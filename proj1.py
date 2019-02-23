import sys
import socket
import json

# make run api_key=0864c16aa51949dedfaa85b41d7379fb city='Nove Mesto na Morave'
# https://docs.python.org/3/library/socket.html

host = 'api.openweathermap.org'
port = 80

######################################################################
###                  parsing command line argumets                 ###
######################################################################
if (len(sys.argv) != 3 and (len(sys.argv) != 4 or (sys.argv[3] != 'no' and sys.argv[3] != 'yes'))) or (sys.argv[1] == '' or sys.argv[2] == ''):
    sys.exit('error: wrong number/names of arguments\nexample: make run api_key=key city=\'Nove Mesto na Morave\'') 

api_key = sys.argv[1]
city = sys.argv[2].lower()
add_info = sys.argv[3]

######################################################################
###      connecting to api.openweather.org and sending request     ###
######################################################################

# create socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    sys.exit('error: creating socket')

# get IP address
try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    sys.exit('error: getting IP address')

# connect
s.connect((remote_ip, port))

# send request
request = 'GET /data/2.5/weather?q=' + city + '&APPID=' + api_key + '&units=metric HTTP/1.1\r\nHost: api.openweathermap.org\r\n\r\n'
try:
    s.sendall(request.encode())
except socket.error:
    sys.exit('error: request')

reply = s.recv(1024)


######################################################################
###                    parsing received data                       ###
######################################################################

# divide lines
delimiter = '\r\n'.encode()
lines = reply.split(delimiter)
#for line in lines:
#    print(line.decode())

# check response status code
cells = lines[0].decode().split(' ')
if int(cells[1]) == 404:
    print('404 (Not Found). The city name is wrong.')
elif int(cells[1]) == 401:
    print('401 (Unauthorized). The api key is wrong.')
elif int(cells[1]) >= 400 and int(cells[1]) < 427:
    print('Sorry, something went wrong. Client error (4xx)')
elif int(cells[1]) >= 500 and int(cells[1]) < 506:
    print('Sorry, something went wrong. Server error (5xx)')
elif int(cells[1]) == 200:
    s.shutdown(socket.SHUT_RDWR)
    ######################################################################
    ###                     extracting  data                           ###
    ######################################################################
    json_data = lines[len(lines)-1].decode()
    loaded_json = json.loads(json_data)
    print(loaded_json['name'])
    print(loaded_json['weather'][0]['description'])
    print('temp: ' + str(loaded_json['main']['temp']) + ' ' + u'\xb0' + 'C')
    print('humidity: ' + str(loaded_json['main']['humidity']) + ' %')
    print('pressure: ' + str(loaded_json['main']['pressure']) + ' hPa')
    print('wind speed: ' + str(loaded_json['wind']['speed']) + ' m/s')
    if 'deg' in(loaded_json['wind']):
        print('wind-deg: ' + str(loaded_json['wind']['deg']))
    else:
        print('wind-deg: -')
    if add_info == 'yes':
        print('visibility: ' + str(loaded_json['visibility']) + ' m')
        print('clouds: ' + str(loaded_json['clouds']['all']) + ' %')
        print('geo coords: [' + str(loaded_json['coord']['lat']) + ', ' + str(loaded_json['coord']['lon']) + ']')

else:
    print('Sorry, something went wrong. Other errors.')
s.close()

