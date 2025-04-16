# sd_manager.py
import board
import adafruit_sdcard
import storage
import busio
import os
import digitalio

_mounted = False  # Internal state
_spi = None
_cs = None
_sdcard = None


def is_sd_mounted():
    return not "placeholder.txt" in os.listdir("/sd")

def can_access_sd():
    try:
        os.listdir("/sd")
        return True
    except OSError:
        return False

def init_sd(change_dir=True):
    global _mounted,_spi,_cs

    if is_sd_mounted():
        if change_dir:
            os.chdir("/sd")
        _mounted = True
        return True

    SD_CS = board.D5
    SD_TX = board.D7
    SD_RX = board.D4
    SD_CLK = board.D6

    _spi = busio.SPI(SD_CLK, SD_TX, SD_RX)
    _cs = digitalio.DigitalInOut(SD_CS)

    try:
        sdcard = adafruit_sdcard.SDCard(_spi, _cs)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")
        if change_dir:
            os.chdir("/sd")
        _mounted = True
        print("SD card mounted")
        return True
    except OSError as e:
        print("SD init failed:", e)
        try:
            if _spi.try_lock():
                _spi.deinit()
        except Exception:
            pass
        try:
            _cs.deinit()
        except Exception:
            pass
        _mounted = False
        return False

def unmount_sd():
    global _mounted
    if is_sd_mounted():
        try:
            storage.umount("/sd")
            cleanup()
            print("SD unmounted")
        except Exception as e:
            print("Unmount error:", e)
    _mounted = False

def is_mounted():
    return _mounted
        
               
def cleanup():
    global _spi, _cs
    try:
        if _spi.try_lock():
            _spi.deinit()  # Clean up SPI so it can be reused
    except Exception as cleanup_err:
        print("SPI cleanup failed:", cleanup_err)
        
# Clean up CS pin (D5)
    try:
        _cs.deinit()
    except Exception as cs_cleanup_err:
        print("CS pin cleanup failed:", cs_cleanup_err)