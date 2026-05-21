
from faro import hex_to_rgb, _make_request

def test_hex_to_rgb_failure():
    # Test with string that set_color produces
    action = "color&hex=80190E"
    try:
        colore = hex_to_rgb(action)
        print("colore:", colore)
    except Exception as e:
        print("hex_to_rgb failed as expected for action '{}': {}".format(action, e))

    # Test with the loop logic in faro.py
    colore = (128, 25, 14) # ROSSO 0x80190E -> (128, 25, 14)
    ch = 7
    try:
        for i in colore:
            print("Trying to access colore[{}]".format(i))
            val = colore[i]
            print("val:", val)
    except Exception as e:
        print("Loop failed as expected: {}".format(e))

if __name__ == "__main__":
    test_hex_to_rgb_failure()
