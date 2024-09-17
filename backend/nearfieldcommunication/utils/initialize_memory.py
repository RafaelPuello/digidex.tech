
class NTAG:
    def __init__(self, pn532, debug=False):
        # Initialize memory: 45 pages, 4 bytes per page
        self.pn532 = pn532
        self.debug = debug
        self.memory = [[0x00 for _ in range(4)] for _ in range(45)]
        self.password = None
        self.record_type = 'U'
        self.tnf = 0x01
        self.url = 'digidex.tech/link?m=00000000000000x000000'
        self.set_initial_configurations()

    def set_initial_configurations(self):
        """
        Set pre-programmed capabilities and NDEF magic number for NTAG213.
        """
        self.memory[3] = [0xE1, 0x10, 0x12, 0x00]
        self.memory[4] = [0x01, 0x03, 0xA0, 0x0C]
        self.memory[5] = [0x34, 0x03, 0x00, 0xFE]

        mirror_conf = 0b11 # MIRROR_CONF: Set to 11b to enable both UID and NFC counter ASCII mirror
        mirror_byte = 0b00 # MIRROR_BYTE: Set to 01b to start mirroring at the 2nd byte of the page
        strong_mod_en = 0b1 # STRG_MOD_EN: Set to 1b to enable strong modulation mode
        self.memory[41] = [
            (mirror_conf << 6) | (mirror_byte << 4) | (strong_mod_en << 2),  # MIRROR_CONF, MIRROR_BYTE, STRG_MOD_EN
            0x00,  # RFU (Reserved for Future Use)
            0x0C,  # MIRROR_PAGE (Page 11)
            0x05   # AUTH0 (Password protection enabled from page 5)
        ]
        
        prot = 0b0 # PROT: Set to 0b to protect write access with password verification
        cfglck = 0b0 # CFGLCK: Set to 0b to keep configuration open to write access
        nfc_cnt_en = 0b1 # NFC_CNT_EN: Set to 1b to enable NFC counter
        nfc_cnt_pwd_prot = 0b0 # NFC_CNT_PWD_PROT: Set to 0b to disable password protection for NFC counter
        authlim = 0b000 # AUTHLIM: Set to 000b to disable limitation of negative password attempts
        self.memory[42] = [
            (prot << 7) | (cfglck << 6) | (nfc_cnt_en << 4) | (nfc_cnt_pwd_prot << 3) | authlim,
            0x00, 0x00, 0x00   # RFU (Reserved for Future Use)
        ]
        return True

    def _create_message_flags(self, payload, tnf):
        # Assuming 'only' position if there's a single record
        MB = 0x80  # Message Begin
        ME = 0x40  # Message End
        CF = 0x00  # Chunk Flag, not used for a single record
        SR = 0x10 if len(payload) < 256 else 0x00  # Short Record
        IL = 0x00  # ID Length
        return MB | ME | CF | SR | IL | tnf

    def _prepare_payload(self, record_type, payload):
        if record_type == 'U':
            # Choose the URI identifier code based on the debug flag
            uri_identifier_code = b'\x04' 
            return uri_identifier_code + payload.encode()
        return payload.encode()

    def _create_record_header(self, message_flags, record_type, payload):
        # Verify that all inputs are correct
        type_length = len(record_type).to_bytes(1, byteorder='big')
        payload_length = len(payload).to_bytes(1 if len(payload) < 256 else 4, byteorder='big')
        id_length = b''
        record_type_bytes = record_type.encode()
        id_bytes = ''.encode()
        return bytes([message_flags]) + type_length + payload_length + id_length + record_type_bytes + id_bytes

    def _construct_complete_record(self, header, payload):
        complete_record = header + payload
        tlv_type = b'\x03'
        ndef_length = len(complete_record)
        tlv_length = bytes([ndef_length]) if ndef_length < 255 else b'\xFF' + ndef_length.to_bytes(2, byteorder='big')
        tlv = b'\x34' + tlv_type + tlv_length + complete_record + b'\xFE'  # Append terminator
        return tlv

    def create_ndef_record(self, payload=None):
        """
        Method to create the NDEF record with debug statements.
        """
        if not payload:
            payload = self.url
        message_flags = self._create_message_flags(payload, self.tnf)
        prepared_payload = self._prepare_payload(self.record_type, payload)
        if self.debug:
            print(f"NDEF Payload Prepared: {prepared_payload}")
        header = self._create_record_header(message_flags, self.record_type, prepared_payload)
        if self.debug:
            print(f"NDEF Record Header created: {header}")
        record = self._construct_complete_record(header, prepared_payload)
        if self.debug:
            print(f"NDEF Record created successfully: {record}")
        return record
    