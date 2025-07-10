import time
from machine import UART
import struct
import network
import umqtt.robust

# Função para calcular o CRC
def calculate_crc(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

# Configuração do UART
def setup_uart():
    return UART(2, baudrate=9600, tx=17, rx=16, parity=None, stop=2, bits=8, timeout=200)

# Criação do pacote de requisição Modbus
def create_modbus_request(slave_address, function_code, start_address, register_count):
    start_address_high = (start_address >> 8) & 0xFF
    start_address_low = start_address & 0xFF
    register_count_high = (register_count >> 8) & 0xFF
    register_count_low = register_count & 0xFF

    request = bytearray([
        slave_address,
        function_code,
        start_address_high,
        start_address_low,
        register_count_high,
        register_count_low
    ])

    crc = calculate_crc(request)
    request += bytearray([crc & 0xFF, (crc >> 8) & 0xFF])
    return request

# Processamento da resposta Modbus
def process_response(response):
    if not response:
        return None, "Nenhuma resposta recebida."

    data = response[:-2]  # Dados sem o CRC
    received_crc = struct.unpack('<H', response[-2:])[0]
    calculated_crc = calculate_crc(data)

    if received_crc != calculated_crc:
        return None, "Erro: CRC inválido."

    byte_count = response[2]  # Quantidade de bytes nos dados
    registers = [
        (response[i] << 8) | response[i + 1]  # Concatena os dois bytes para formar o valor do registrador
        for i in range(3, 3 + byte_count, 2)
    ]

    return registers, "CRC válido."

# Configuração da conexão Wi-Fi
def setup_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('MinhaRede', 'ygpa2508')
    print("Waiting for Wifi connection")
    while not sta_if.isconnected():
        time.sleep(1)
    print("Connected")
    print(sta_if.ifconfig())
    return sta_if

# Configuração do cliente MQTT
def setup_mqtt():
    mqtt_client = umqtt.robust.MQTTClient(
        "umqtt_client",
        server='192.168.43.202',
        port=1883,
        user='bipes',
        password='m8YLUr5uW3T'
    )
    mqtt_client.connect()
    print("MQTT Connected")
    return mqtt_client

# Função principal
def main():
    # Configurar UART e MQTT
    uart = setup_uart()
    setup_wifi()
    mqtt_client = setup_mqtt()

    # Parâmetros do Modbus
    slave_address = 0x01
    function_code = 0x03
    start_address =  0x4338 # Endereço inicial 0x4338
    register_count = 0x04  # Quantidade de registros

    request = create_modbus_request(slave_address, function_code, start_address, register_count)
    print("Enviando pacote Modbus:", request)

    while True:
        uart.write(request)  # Envia o pacote Modbus
        time.sleep(1)  # Aguarda resposta
        response = uart.read(16)  # Espera a resposta

        registers, message = process_response(response)
        print(message)

        if registers is not None:
            mqtt_client.publish("dados", str(registers), qos=1)
            print("Registros enviados:", registers)

        time.sleep(1)  # Intervalo entre requisições

if __name__ == "__main__":
    main()

