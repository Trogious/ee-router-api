class Message:
    SSID_REF_MARKER_2G = b"__SSID_REF_2G__"
    SSID_REF_MARKER_5G = b"__SSID_REF_5G__"
    # SSID_REF_MARKER_6G = b"__SSID_REF_6G__"
    WIFI_OFF = b'\n\x031.0\x12\x1dos::012345-:119746:2432000646\x1a\rusp-gui-admin:\xc0\x02\x12\xbd\x02\n(\n$09283ca2-3ba9-2c48-ecf6-3d7f1e13a74e\x10\x04\x12\x90\x02\n\x8d\x02"\x8a\x02\x08\x01\x12M\n<Device.WiFi.AccessPoint.[SSIDReference==' + SSID_REF_MARKER_2G + \
        b'].\x12\r\n\x06Enable\x12\x010\x18\x01\x12M\n<Device.WiFi.AccessPoint.[SSIDReference==' + SSID_REF_MARKER_5G + \
        b'].\x12\r\n\x06Enable\x12\x010\x18\x01\x123\n"Device.WiFi.SSID.[Name==guest_2G].\x12\r\n\x06Enable\x12\x010\x18\x01\x123\n"Device.WiFi.SSID.[Name==guest_5G].\x12\r\n\x06Enable\x12\x010\x18\x01'
    WIFI_ON = b'\n\x031.0\x12\x1dos::012345-:119746:2432000646\x1a\rusp-gui-admin:\xc0\x02\x12\xbd\x02\n(\n$df66e40b-ae5b-e8f1-0ec9-bec9dbeb604b\x10\x04\x12\x90\x02\n\x8d\x02"\x8a\x02\x08\x01\x12M\n<Device.WiFi.AccessPoint.[SSIDReference==' + SSID_REF_MARKER_2G + \
        b'].\x12\r\n\x06Enable\x12\x011\x18\x01\x12M\n<Device.WiFi.AccessPoint.[SSIDReference==' + SSID_REF_MARKER_5G + \
        b'].\x12\r\n\x06Enable\x12\x011\x18\x01\x123\n"Device.WiFi.SSID.[Name==guest_2G].\x12\r\n\x06Enable\x12\x011\x18\x01\x123\n"Device.WiFi.SSID.[Name==guest_5G].\x12\r\n\x06Enable\x12\x011\x18\x01'
    WIFI_QUERY = b'\n\x031.0\x12\x1dos::012345-:119746:2432000646\x1a\rusp-gui-admin:t\x12r\n(\n$c40a2910-752f-89a3-83a4-3ac59467c6a6\x10\x01\x12F\nD\nB\n\x0cDevice.WiFi.\n\x10Device.Ethernet.\n Device.X_BT-COM_NFC.Interface.1.'

    @staticmethod
    def get_wifi_off(ssid_ref_2G: str, ssid_ref_5G: str, ssid_ref_6G: str = None):
        if None in [ssid_ref_2G, ssid_ref_5G]:
            raise Exception("both 2G and 5G ssid refs are required")
        msg = Message.WIFI_OFF.replace(Message.SSID_REF_MARKER_2G, ssid_ref_2G.encode()
                                       ).replace(Message.SSID_REF_MARKER_5G, ssid_ref_5G.encode())
        # if ssid_ref_6G:
        #     # TODO: implement 6G support
        #     msg = msg.replace(Message.SSID_REF_MARKER_6G, ssid_ref_6G)
        return msg

    @staticmethod
    def get_wifi_on(ssid_ref_2G: str, ssid_ref_5G: str, ssid_ref_6G: str = None):
        if None in [ssid_ref_2G, ssid_ref_5G]:
            raise Exception("both 2G and 5G ssid refs are required")
        msg = Message.WIFI_ON.replace(Message.SSID_REF_MARKER_2G, ssid_ref_2G.encode()
                                      ).replace(Message.SSID_REF_MARKER_5G, ssid_ref_5G.encode())
        # if ssid_ref_6G:
        #     # TODO: implement 6G support
        #     msg = msg.replace(Message.SSID_REF_MARKER_6G, ssid_ref_6G)
        return msg
