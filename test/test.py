import unittest
import sys,time
sys.path.append("..")
from smms import *
from PIL import Image


class TestUploader(unittest.TestCase):

    def test_init(self):

        with self.assertRaisesRegex(AttributeError, "'Image' object has no attribute 'read'"):
            Uploader(Image.new("RGBA", (233, 233), (255, 255, 255)))
        with self.assertRaisesRegex(OSError, "cannot identify image file"):
            Uploader(r"D:\Project\VscodeProject\Python\smms\test\test_images\FakeImage.jpg")
        with self.assertRaisesRegex(ValueError, "img_fp has no legal meaning as a string!"):
            Uploader(r"1234567890")

        self.assertEqual(self.u1.img_name, "1")
        self.assertEqual(self.u1.img_format, "JPEG")
        self.assertEqual(self.u1.img_full_name, "1.jpg")

        self.assertEqual(self.u2.img_name, "2")
        self.assertEqual(self.u2.img_format, "PNG")
        self.assertEqual(self.u2.img_full_name, "2.png")

        self.assertEqual(self.u3.img_name, "3")
        self.assertEqual(self.u3.img_format, "GIF")
        self.assertEqual(self.u3.img_full_name, "3.gif")

        self.assertEqual(self.u4.img_name, "3e60b20604b6fdc7d081eb6a1ec72aa47c5a3964")
        self.assertEqual(self.u4.img_format, "JPEG")
        self.assertEqual(self.u4.img_full_name, "3e60b20604b6fdc7d081eb6a1ec72aa47c5a3964.jpg")

        self.assertEqual(self.u5.img_name, "782a4d10560280c10b2392be0355276a7dcea819")
        self.assertEqual(self.u5.img_format, "GIF")
        self.assertEqual(self.u5.img_full_name, "782a4d10560280c10b2392be0355276a7dcea819.gif")

        self.assertEqual(self.u6.img_name, "test_img_custom_name")
        self.assertEqual(self.u6.img_format, "JPEG")
        self.assertEqual(self.u6.img_full_name, "test_img_custom_name.jpg")

        self.assertEqual(self.u7.img_name, "2")
        self.assertEqual(self.u7.img_format, "PNG")
        self.assertEqual(self.u7.img_full_name, "2.png")

    def test_upload(self):
        result1 = self.u1.upload()
        result2 = self.u2.upload()
        result3 = self.u3.upload()
        result4 = self.u4.upload()
        result5 = self.u5.upload()
        result6 = self.u6.upload()
        result7 = self.u7.upload()

        print(result1)
        print(result2)
        print(result3)
        print(result4)
        print(result5)
        print(result6)
        print(result7)

        result1.delete()
        result2.delete()
        result3.delete()
        result4.delete()
        result5.delete()
        result6.delete()
        result7.delete()

    # 这个方法会分别在每调用一个测试方法的前被执行。
    def setUp(self):
        self.u1 = Uploader(r"D:\Project\VscodeProject\Python\smms\test\test_images\1.jpg")
        self.u2 = Uploader(r"D:\Project\VscodeProject\Python\smms\test\test_images\2.png")
        self.u3 = Uploader(r"D:\Project\VscodeProject\Python\smms\test\test_images\3.gif")
        self.u4 = Uploader(r"http://i1.hdslb.com/bfs/face/3e60b20604b6fdc7d081eb6a1ec72aa47c5a3964.jpg")
        self.u5 = Uploader(r"http://i2.hdslb.com/bfs/face/782a4d10560280c10b2392be0355276a7dcea819.gif")
        self.u6 = Uploader(r"D:\Project\VscodeProject\Python\smms\test\test_images\1.jpg", img_name="test_img_custom_name")
        self.u7 = Uploader(open(r"D:\Project\VscodeProject\Python\smms\test\test_images\2.png", "rb"))


class TestUploadResult(unittest.TestCase):
    def __init__(self, methodname='runTest'):
        super().__init__(methodname)
        self.u = Uploader(r"D:\Project\VscodeProject\Python\smms\test\test_images\1.jpg", img_name="test_img")
        self.ur = self.u.upload()
        print(self.ur)

    def test_img_size(self):
        self.assertEqual(self.ur.img_size, (420, 420))

    def test_img_name(self):
        self.assertEqual(self.ur.img_name, "test_img.jpg")

    def test_smms_url(self):
        self.assertRegex(self.ur.smms_url, "https://i.loli.net/.*")

    def test_ip(self):
        self.assertRegex(self.ur.ip, "171.*")

    def test_time(self):
        self.ur.upload_time
    
    def test_del(self):
        self.ur.delete()
        with self.assertRaises(FileAlreadyDeletedError):
            self.ur.delete()

if __name__ == '__main__':
    unittest.main()
