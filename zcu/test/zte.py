import unittest

from .context import zcu

class TestHeaderMethods(unittest.TestCase):

    ZXHN_H298N_config = 'resources/ZXHN_H298N.bin'
    ZXHN_H298N_signature = b'ZXHN H298N'

    ZXHN_H108N_V25_config = 'resources/ZXHN_H108N_V2.5.bin'
    ZXHN_H108N_V25_signature = b'ZXHN H108N V2.5'

    F600W_config = 'resources/F600W.bin'
    F600W_signature = b'F600W'

    # read_header
    def test_zxhn_h298n_read_header(self):
        with open(self.ZXHN_H298N_config, 'rb') as infile:
            header_length = zcu.zte.read_header(infile)
            self.assertEqual(128, header_length)
    def test_zxhn_h108n_v25_read_header(self):
        with open(self.ZXHN_H108N_V25_config, 'rb') as infile:
            header_length = zcu.zte.read_header(infile)
            self.assertEqual(128, header_length)
    def test_f600w_read_header(self):
        with open(self.F600W_config, 'rb') as infile:
            header_length = zcu.zte.read_header(infile)
            self.assertEqual(0, header_length)

    # read_signature
    def test_zxhn_h298n_read_signature(self):
        with open(self.ZXHN_H298N_config, 'rb') as infile:
            infile.seek(128)
            signature = zcu.zte.read_signature(infile)
            self.assertEqual(self.ZXHN_H298N_signature, signature)
    def test_zxhn_h108n_v25_read_signature(self):
        with open(self.ZXHN_H108N_V25_config, 'rb') as infile:
            infile.seek(128)
            signature = zcu.zte.read_signature(infile)
            self.assertEqual(self.ZXHN_H108N_V25_signature, signature)
    def test_f600w_read_signature(self):
        with open(self.F600W_config, 'rb') as infile:
            signature = zcu.zte.read_signature(infile)
            self.assertEqual(self.F600W_signature, signature)

    # read_payload_type
    def test_zxhn_h298n_read_payload_type(self):
        with open(self.ZXHN_H298N_config, 'rb') as infile:
            infile.seek(150)
            payload_type = zcu.zte.read_payload_type(infile)
            self.assertEqual(2, payload_type)
    def test_zxhn_h108n_v25_read_payload_type(self):
        with open(self.ZXHN_H108N_V25_config, 'rb') as infile:
            infile.seek(155)
            payload_type = zcu.zte.read_payload_type(infile)
            self.assertEqual(2, payload_type)
    def test_f600w_read_payload_type(self):
        with open(self.F600W_config, 'rb') as infile:
            infile.seek(17)
            payload_type = zcu.zte.read_payload_type(infile)
            self.assertEqual(0, payload_type)

    # add_header
    def test_add_header_type_0(self):
        payload = b'abcdefhi'
        signature = b'TEST'
        res = zcu.zte.add_header(payload, signature, 0)
        self.assertEqual(24, len(res))
        self.assertEqual(b'\x04\x03\x02\x01', res[:4])
        self.assertEqual(b'\x00\x00\x00\x00', res[4:8])
        self.assertEqual(b'\x00\x00\x00\x04', res[8:12])
        self.assertEqual(signature, res[12:16])
        self.assertEqual(payload, res[16:])
    def test_add_header_type_2(self):
        payload = b'abcdefhi'
        signature = b'TEST'
        res = zcu.zte.add_header(payload, signature, 2)
        self.assertEqual(b'\x99\x99\x99\x99\x44\x44\x44\x44\x55\x55\x55\x55\xaa\xaa\xaa\xaa',
                         res[:16])
        self.assertEqual(24, res[75])
        type_0_area = res[128:]
        self.assertEqual(b'\x04\x03\x02\x01', type_0_area[:4])
        self.assertEqual(b'\x00\x00\x00\x00', type_0_area[4:8])
        self.assertEqual(b'\x00\x00\x00\x04', type_0_area[8:12])
        self.assertEqual(signature, type_0_area[12:16])
        self.assertEqual(payload, type_0_area[16:])
