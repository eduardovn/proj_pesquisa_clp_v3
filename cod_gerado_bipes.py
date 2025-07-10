import time
import umqtt.robust
from machine import uart
import network

uart = None
result = None
registers = None
mqtt_client = None
start_address_high = None
bytearray2 = None
crc = None
quotient = None
bit = None
data = None
start_address_low = None
i = None
counter = None
k = None
register_count_high = None
size = None
a = None
slave_address = None
response = None
limite = None
start_address = None
register_count_low = None
b = None
function_code = None
abit = None
request = None
byte = None
bbit = None
register_count = None
low_byte = None
j = None
high_byte = None
lsb = None
received_crc = None
calculated_crc = None
byte_count = None
crc_low = None
crc_high = None
dados = None
fim = None
high = None
low = None
value = None

# Descreva esta função...
def main():
  global uart, result, registers, mqtt_client, start_address_high, bytearray2, crc, quotient, bit, data, start_address_low, i, counter, k, register_count_high, size, a, slave_address, response, limite, start_address, register_count_low, b, function_code, abit, request, byte, bbit, register_count, low_byte, j, high_byte, lsb, received_crc, calculated_crc, byte_count, crc_low, crc_high, dados, fim, high, low, value
  uart = setup_uart()
  setup_wifi()
  mqtt_client = setup_mqtt()
  slave_address = 1
  function_code = 3
  start_address = 17208
  register_count = 4
  request = create_modbus_request()
  while True:
    machine.UART.UART.write(request)
    time.sleep(1)
    response = uart.read(16)
    registers = process_response()
    if registers != None:
      mqtt_client.publish(dados, registers,qos=1)
    time.sleep(1)

# Descreva esta função...
def xor_bits():
  global uart, result, registers, mqtt_client, start_address_high, bytearray2, crc, quotient, bit, data, start_address_low, i, counter, k, register_count_high, size, a, slave_address, response, limite, start_address, register_count_low, b, function_code, abit, request, byte, bbit, register_count, low_byte, j, high_byte, lsb, received_crc, calculated_crc, byte_count, crc_low, crc_high, dados, fim, high, low, value
  result = 0
  bit = 1
  counter = 0
  while counter < 16:
    abit = a % (bit * 2) - a % bit
    bbit = b % (bit * 2) - b % bit
    if abit != 0 and bbit == 0 or abit == 0 and bbit != 0:
      result = result + bit
    bit = bit * 2
    counter = counter + 1
  return result

# Descreva esta função...
def process_response():
  global uart, result, registers, mqtt_client, start_address_high, bytearray2, crc, quotient, bit, data, start_address_low, i, counter, k, register_count_high, size, a, slave_address, response, limite, start_address, register_count_low, b, function_code, abit, request, byte, bbit, register_count, low_byte, j, high_byte, lsb, received_crc, calculated_crc, byte_count, crc_low, crc_high, dados, fim, high, low, value
  if response == None or len(response) == 0:
    return None
  data = not len(data)
  k = 0
  limite = len(response) - 2
  while k != limite:
    data = response[int(k)]
    k = k + 1
  response = len(response) - 2
  low_byte = response
  response = len(response) - 1
  high_byte = response
  received_crc = low_byte + high_byte * 256
  calculated_crc = calculate_crc()
  if received_crc != calculated_crc:
    return None
  byte_count = response[2]
  registers = not len(registers)
  i = 3
  fim = 3 + byte_count
  while i != fim:
    high = response[int(i)]
    low = response[int(i + 2)]
    value = high * (256 + low)
    registers.append(value)
    i = i + 2
  return registers

# Descreva esta função...
def setup_mqtt():
  global uart, result, registers, mqtt_client, start_address_high, bytearray2, crc, quotient, bit, data, start_address_low, i, counter, k, register_count_high, size, a, slave_address, response, limite, start_address, register_count_low, b, function_code, abit, request, byte, bbit, register_count, low_byte, j, high_byte, lsb, received_crc, calculated_crc, byte_count, crc_low, crc_high, dados, fim, high, low, value
  mqtt_buffer = ""; mqtt_client = umqtt.robust.MQTTClient("umqtt_client", server = '192.168.43.202', port = 1883, user = 'bipes', password = 'm8YLUr5uW3T'); mqtt_client.connect()
  return mqtt_client

# Descreva esta função...
def create_modbus_request():
  global uart, result, registers, mqtt_client, start_address_high, bytearray2, crc, quotient, bit, data, start_address_low, i, counter, k, register_count_high, size, a, slave_address, response, limite, start_address, register_count_low, b, function_code, abit, request, byte, bbit, register_count, low_byte, j, high_byte, lsb, received_crc, calculated_crc, byte_count, crc_low, crc_high, dados, fim, high, low, value
  start_address_high = (start_address / 256) % 256
  start_address_low = start_address % 256
  register_count_high = (register_count / 256) % 256
  register_count_low = register_count % 256
  request = not len(request)
  request.append(start_address)
  request.append(function_code)
  request.append(start_address_high)
  request.append(start_address_low)
  request.append(register_count_high)
  request.append(register_count_low)
  crc = calculate_crc()
  crc_low = crc % 256
  crc_high = (crc / 256) % 256
  request.append(crc_low)
  request.append(crc_high)
  bytearray2 = request
  return bytearray2

# Descreva esta função...
def calculate_crc():
  global uart, result, registers, mqtt_client, start_address_high, bytearray2, crc, quotient, bit, data, start_address_low, i, counter, k, register_count_high, size, a, slave_address, response, limite, start_address, register_count_low, b, function_code, abit, request, byte, bbit, register_count, low_byte, j, high_byte, lsb, received_crc, calculated_crc, byte_count, crc_low, crc_high, dados, fim, high, low, value
  crc = 65535
  i = 0
  size = len(data)
  while i != size:
    byte = data[int(i)]
    crc = xor_bits()
    j = 0
    while j != 0:
      lsb = crc % 2
      crc = int_division()
      if lsb != 0:
        crc = xor_bits()
      j = j / 1
    i = i / 1
  return crc % 65536

# Descreva esta função...
def setup_uart():
  global uart, result, registers, mqtt_client, start_address_high, bytearray2, crc, quotient, bit, data, start_address_low, i, counter, k, register_count_high, size, a, slave_address, response, limite, start_address, register_count_low, b, function_code, abit, request, byte, bbit, register_count, low_byte, j, high_byte, lsb, received_crc, calculated_crc, byte_count, crc_low, crc_high, dados, fim, high, low, value
  uart = UART(1, 9600)
  uart.init(9600, bits=1, parity=None, stop=2)
  machine.Pin.Pin.value((17))
  machine.Pin.Pin.value((16))
  time.sleep_ms(200)
  return uart

# Descreva esta função...
def int_division():
  global uart, result, registers, mqtt_client, start_address_high, bytearray2, crc, quotient, bit, data, start_address_low, i, counter, k, register_count_high, size, a, slave_address, response, limite, start_address, register_count_low, b, function_code, abit, request, byte, bbit, register_count, low_byte, j, high_byte, lsb, received_crc, calculated_crc, byte_count, crc_low, crc_high, dados, fim, high, low, value
  quotient = 0
  while a >= b:
    a = a - b
    quotient = quotient + 1
  return quotient

# Descreva esta função...
def setup_wifi():
  global uart, result, registers, mqtt_client, start_address_high, bytearray2, crc, quotient, bit, data, start_address_low, i, counter, k, register_count_high, size, a, slave_address, response, limite, start_address, register_count_low, b, function_code, abit, request, byte, bbit, register_count, low_byte, j, high_byte, lsb, received_crc, calculated_crc, byte_count, crc_low, crc_high, dados, fim, high, low, value
  sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
  sta_if.scan()
  sta_if.connect('MinhaRede','ygpa2508')
  print("Waiting for Wifi connection")
  while not sta_if.isconnected(): time.sleep(1)
  print("Connected")
