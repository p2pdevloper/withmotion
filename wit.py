import asyncio
import bleak
import device_model
import time

# 扫描到的设备 Scanned devices
devices = []
# 蓝牙设备 BLEDevice
BLEDevice = None

last_update_time = 0


# 扫描蓝牙设备并过滤名称
# Scan Bluetooth devices and filter names
async def scan():
    global devices
    global BLEDevice
    find = []
    print("Searching for Bluetooth devices......")
    try:
        devices = await bleak.BleakScanner.discover(timeout=20.0)
        print("Search ended")
        for d in devices:
            if d.name is not None and "WT" in d.name:
                find.append(d)
                print(d)
        if len(find) == 0:
            print("No devices found in this search!")
        else:
            user_input = input(
                "Please enter the Mac address you want to connect to (e.g. DF:E9:1F:2C:BD:59)："
            )
            for d in devices:
                if d.address == user_input:
                    BLEDevice = d
                    break
    except Exception as ex:
        print("Bluetooth search failed to start")
        print(ex)


# 指定MAC地址搜索并连接设备
# Specify MAC address to search and connect devices
async def scanByMac(device_mac):
    global BLEDevice
    print("Searching for Bluetooth devices......")
    BLEDevice = await bleak.BleakScanner.find_device_by_address(device_mac, timeout=20)


# 数据更新时会调用此方法 This method will be called when data is updated
def updateData(DeviceModel):
    global last_update_time
    current_time = time.time()
    if current_time - last_update_time > 0.5:
        last_update_time = current_time

        data_display = f"""
        AccX: {DeviceModel.get("AccX")} | AccY: {DeviceModel.get("AccY")} | AccZ: {DeviceModel.get("AccZ")}
        AsX: {DeviceModel.get("AsX")} | AsY: {DeviceModel.get("AsY")} | AsZ: {DeviceModel.get("AsZ")}
        AngX: {DeviceModel.get("AngX")} | AngY: {DeviceModel.get("AngY")} | AngZ: {DeviceModel.get("AngZ")}
        HX: {DeviceModel.get("HX")} | HY: {DeviceModel.get("HY")} | HZ: {DeviceModel.get("HZ")}
        Q0: {DeviceModel.get("Q0")} | Q1: {DeviceModel.get("Q1")} | Q2: {DeviceModel.get("Q2")} | Q3: {DeviceModel.get("Q3")}
        """
        print("\033[H\033[J", end="")  # Clear the terminal
        print(data_display)


if __name__ == "__main__":
    # 方式一：广播搜索和连接蓝牙设备
    # Method 1:Broadcast search and connect Bluetooth devices
    asyncio.run(scan())

    # # 方式二：指定MAC地址搜索并连接设备
    # # Method 2: Specify MAC address to search and connect devices
    # asyncio.run(scanByMac("C6:46:21:41:0B:BD"))

    if BLEDevice is not None:
        # 创建设备 Create device
        device = device_model.DeviceModel("MyBle5.0", BLEDevice, updateData)
        # 开始连接设备 Start connecting devices
        asyncio.run(device.openDevice())
    else:
        print("This BLEDevice was not found!!")
