import unittest

from .context import zcu

class TestEncryptionMethods(unittest.TestCase):

    ZXHN_H298N_config = 'resources/ZXHN_H298N.bin'
    ZXHN_H298N_key = b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0Wj'

    ZXHN_H108N_V25_config = 'resources/ZXHN_H108N_V2.5.bin'
    ZXHN_H108N_V25_key = b'GrWM2Hz&LTvz&f^5'

    def test_zxhn_h298n_decryption(self):
        with open(self.ZXHN_H298N_config, 'rb') as infile:
            infile.seek(210)
            res = zcu.encryption.decrypt(infile, self.ZXHN_H298N_key)
            self.assertEqual(18432, len(res.read()))

    def test_zxhn_h108n_v25_decryption(self):
        with open(self.ZXHN_H108N_V25_config, 'rb') as infile:
            infile.seek(215)
            res = zcu.encryption.decrypt(infile, self.ZXHN_H108N_V25_key)
            self.assertEqual(6528, len(res.read()))
