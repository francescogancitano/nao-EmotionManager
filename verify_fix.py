
import mock
from faro import _make_request, set_color

def test_fix():
    with mock.patch('requests.get') as mocked_get:
        # Test set_color with integer
        print("Testing set_color('faro', 0x80190E)...")
        set_color("faro", 0x80190E)
        
        # We expect 4 calls to IP_ADDRESS_FARO (ch 7, 8, 9 for RGB) and 1 call to IP_ADDRESS_LED
        # ROSSO 0x80190E -> (128, 25, 14)
        
        print("Number of requests:", mocked_get.call_count)
        for i, call in enumerate(mocked_get.call_args_list):
            print("Call {}: {}".format(i, call[0][0]))

        # Check if the RGB values are correct in the calls
        expected_urls = [
            "http://192.168.178.40:8080/ch=7&val=128",
            "http://192.168.178.40:8080/ch=8&val=25",
            "http://192.168.178.40:8080/ch=9&val=14",
            "http://192.168.178.21/faro?action=color&hex=80190e"
        ]
        
        for i, expected_url in enumerate(expected_urls):
            actual_url = mocked_get.call_args_list[i][0][0]
            assert actual_url == expected_url, "Expected {}, got {}".format(expected_url, actual_url)
        
        print("Test passed!")

if __name__ == "__main__":
    test_fix()
