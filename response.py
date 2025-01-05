from timed import timed

SSID_MARK = b"Device.WiFi.SSID."
SSID_MARK_LEN = len(SSID_MARK)


def find_ssid_mark(r: bytes, idx: int) -> int:
    i = r.find(SSID_MARK, idx)
    # self.logger.debug(r[i-4:i+20])
    while i > 3 and r[i-2:i] not in [b"\n\x13", b"\n\x14"]:
        i = r.find(b"Device.WiFi.SSID.", i + SSID_MARK_LEN)
    return i


def read_value(r: bytes, key: bytes, key_postfixes, start_idx: int, end_bytes: bytes, end_idx: int) -> str | None:
    for postfix in key_postfixes:
        i = r.find(key + postfix, start_idx, end_idx)
        if i >= 0:
            key_len = len(key) + len(postfix)
            j = r.find(end_bytes, i + key_len)
            if j >= 0 and j <= end_idx:
                value = r[i + key_len:j]
                return value.decode()
    return None


@timed
def read_wifi_networks(wifi_response: bytes):
    networks = {}
    response_len = len(wifi_response)
    idx1 = idx2 = 0
    while idx1 >= 0 and idx2 >= 0:
        idx1 = find_ssid_mark(wifi_response, idx1)
        # self.logger.debug(idx1)
        if idx1 >= 0:
            ref = wifi_response[idx1: wifi_response.find(b"\x12", idx1 + SSID_MARK_LEN)].decode().rstrip(".")
            # self.logger.debug(ref)
            idx2 = end_idx = find_ssid_mark(wifi_response, idx1 + SSID_MARK_LEN)
            if idx2 < 0:
                # self.logger.debug("idx2 LESS THAN 0")
                end_idx = response_len
            else:
                # self.logger.debug(r[idx1-10:idx2])
                pass

            ssid = read_value(wifi_response, b"\n\x04SSID", [b"\x12\n", b"\x12\x0f",
                              b"\x12\x0e", b"\x12\x07", b"\x12\t"], idx1 + SSID_MARK_LEN, b"\x12", end_idx)
            name = read_value(wifi_response, b"\n\x04Name", [b"\x12\x08", b"\x12\x07",
                              b"\x12\x0b", b"\x12\x10", b"\x12\x0e"], idx1 + SSID_MARK_LEN, b"\x12", end_idx)

            # self.logger.debug(ssid)
            # if ref.endswith(".1"):
            #     self.logger.debug(wifi_response[idx1-10:idx2])
            if ssid:
                networks[name] = {"ssid": ssid, "ref": ref}
                # self.logger.debug(r[idx1-10:idx2])
                # self.logger.debug("%s %s %s [%d:%d]" % (header, ssid, name, idx1, idx2))
            idx1 = idx2
    return networks
