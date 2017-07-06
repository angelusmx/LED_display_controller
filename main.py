import serial
import time
import threading
import random

master_counter = 0
random_decimal = 0


def calculate_checksum(prefix, message, start_position):

    # required to start the XOR iteration
    zero_value = 0x00

    if message == "None":
        input_string = prefix

    else:
        # put the string to be evaluated together
        input_string = prefix + message

    # iterate through the string
    for i in range(start_position, len(input_string)):

        character = input_string[i]
        print character

        # for the first character
        if i < 1:
            # transform the unicode character to hex (int is the data type)
            hex_char = ord(character)
            xor_crc = hex_char ^ zero_value

        else:
            hex_char = ord(character)
            xor_crc = hex_char ^ xor_crc

    return xor_crc

# ++++++++++++++++++++++++ End of function ++++++++++++++++++++++


def send_serial_data(input_message, close_command):
    # Start the counter for the loop
    count = 0

    # Open the serial port
    ser = serial.Serial(
        port='COM2',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        write_timeout=None,
        timeout=1)

    while count < len(input_message):

        # check that the port is open and ready
        if ser.isOpen():
            print(ser.name + ' is now open...')

            print('current character is... ' + input_message[count])
            # print('current counter value = '), count

            # Write one character to the Buffer of COM2
            ser.write(input_message[count])

            # update the counter
            count += 1

    # After the last character was sent close the port
    time.sleep(0.1)

    # TODO: Implement the step wise streaming of the date to the display when ACK received. Read makes Tx much slower
    # serial_input = ser.readline()
    # print serial_input

    if close_command:
        print "Closing the serial port"
        ser.close()

    else:
        print "Port will not be closed"

# ++++++++++++++++++++++++ End of function ++++++++++++++++++++++


# ************** The main function *******************
def main(coma_value):

    # Structure of the Configuration message
    config_prefix = "<ID01>"
    config_crc_prefix = "<BE>"
    config_suffix = "<E>"
    config_message = "None"

    # Structure of the string is : string_prefix + crc_prefix + the_message + crc_string + string_suffix
    string_prefix = "<ID01>"
    crc_prefix = "<L1><PA><FA><MA><WC><FK>"
    the_message = "1." + str(coma_value) + " Rack/min"
    string_suffix = "<E>"

    # Structure of the closing message
    closing_prefix = "<ID01>"
    closing_crc_prefix = "<BF>"
    closing_suffix = "<E>"
    closing_message = "None"

    # ---------------- The configuration message ------------------------ #
    # initialize the variable
    start_character = 0

    # calculate the crc for the configuration message
    config_crc_string = calculate_checksum(config_crc_prefix, config_message, start_character)

    # convert the configuration crc to hex and format to string
    config_crc_string = "{0:#0{1}x}".format(config_crc_string, 4)
    config_crc_string = config_crc_string[2:]
    config_crc_string = config_crc_string.upper()

    # Assemble the complete configuration string
    config_transmission = config_prefix + config_crc_prefix + config_crc_string + config_suffix

    # Send the configuration message to the display panel
    send_serial_data(config_transmission, True)

    print "here"

    # ---------------- The transmission message ------------------------ #
    # initialize the variable
    start_character = 0

    # calculate the crc for the display message
    crc_string = calculate_checksum(crc_prefix, the_message, start_character)

    # convert the display message string to hex and format to string
    crc_string = "{0:#0{1}x}".format(crc_string, 4)
    crc_string = crc_string[2:]
    crc_string = crc_string.upper()

    # Put together the whole string with the CRC check
    string_transmission = string_prefix + crc_prefix + the_message + crc_string + string_suffix

    # Send the configuration message to the display panel
    send_serial_data(string_transmission, True)

    # ---------------- The closing message ------------------------ #
    # initialize the variable
    start_character = 0

    # calculate the crc for the display message
    closing_crc_string = calculate_checksum(closing_crc_prefix, closing_message, start_character)

    # convert the display message string to hex and format to string
    closing_crc_string = "{0:#0{1}x}".format(closing_crc_string, 4)
    closing_crc_string = closing_crc_string[2:]
    closing_crc_string = closing_crc_string.upper()

    # Put together the whole string with the CRC check
    closing_string = closing_prefix + closing_crc_prefix + closing_crc_string + closing_suffix

    # ****test *****
    # put the whole string together

    # Send the configuration message to the display panel
    send_serial_data(closing_string, True)

    # ++++++++++++++++++++++++ End of function ++++++++++++++++++++++


def calculate_performance():

    threading.Timer(10.0, calculate_performance).start()
    global random_decimal
    random_decimal = random.randrange(0, 99, 2)   # Even integer from 0 to 100

    # call the main function
    main(random_decimal)

# Start the timer thread
calculate_performance()

