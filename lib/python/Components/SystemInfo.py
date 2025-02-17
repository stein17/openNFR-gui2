from enigma import eDVBResourceManager, Misc_Options
from boxbranding import getMachineProcModel, getBoxType, getMachineBuild, getBrandOEM, getDisplayType, getHaveRCA, getHaveDVI, getHaveYUV, getHaveSCART, getHaveAVJACK, getHaveSCARTYUV, getHaveHDMI, getMachineMtdKernel, getMachineMtdRoot
from os import path

from enigma import eDVBResourceManager, Misc_Options

from Tools.Directories import fileExists, fileCheck, fileHas, pathExists
from Tools.HardwareInfo import HardwareInfo

SystemInfo = { }

#FIXMEE...
def getNumVideoDecoders():
	idx = 0
	while fileExists("/dev/dvb/adapter0/video%d"% idx, 'f'):
		idx += 1
	return idx

SystemInfo["NumVideoDecoders"] = getNumVideoDecoders()
SystemInfo["PIPAvailable"] = SystemInfo["NumVideoDecoders"] > 1
SystemInfo["CanMeasureFrontendInputPower"] = eDVBResourceManager.getInstance().canMeasureFrontendInputPower()


def countFrontpanelLEDs():
	leds = 0
	if fileExists("/proc/stb/fp/led_set_pattern"):
		leds += 1

	while fileExists("/proc/stb/fp/led%d_pattern" % leds):
		leds += 1

	return leds

SystemInfo["12V_Output"] = Misc_Options.getInstance().detected_12V_output()
SystemInfo["ZapMode"] = fileCheck("/proc/stb/video/zapmode") or fileCheck("/proc/stb/video/zapping_mode")
SystemInfo["NumFrontpanelLEDs"] = countFrontpanelLEDs()
SystemInfo["FrontpanelDisplay"] = fileExists("/dev/dbox/oled0") or fileExists("/dev/dbox/lcd0")
SystemInfo["7segment"] = getDisplayType() in ('7segment')
SystemInfo["ConfigDisplay"] = SystemInfo["FrontpanelDisplay"] and getDisplayType() not in ('7segment')
SystemInfo["LCDSKINSetup"] = path.exists("/usr/share/enigma2/display") and getDisplayType() not in ('7segment')
SystemInfo["OledDisplay"] = fileExists("/dev/dbox/oled0") or getBoxType() in ('osminiplus')
SystemInfo["LcdDisplay"] = fileExists("/dev/dbox/lcd0") or getBoxType() in ('e4hdultra')
SystemInfo["FBLCDDisplay"] = fileCheck("/proc/stb/fb/sd_detach")
SystemInfo["VfdDisplay"] = getBoxType() not in ('anadol4k','dinobot4kl','dinobot4k','dinobot4kse', 'vuultimo', 'xpeedlx3', 'et10000', 'mutant2400', 'quadbox2400', 'atemionemesis') and fileExists("/dev/dbox/oled0")
SystemInfo["DeepstandbySupport"] = HardwareInfo().has_deepstandby()
SystemInfo["Fan"] = fileCheck("/proc/stb/fp/fan")
SystemInfo["FanPWM"] = SystemInfo["Fan"] and fileCheck("/proc/stb/fp/fan_pwm")
SystemInfo["StandbyPowerLed"] = fileExists("/proc/stb/power/standbyled")
SystemInfo["LEDButtons"] = getBoxType() == 'vuultimo'
SystemInfo["loadcidriver"] = getBoxType() == 'formuler1'
SystemInfo["loadci3driver"] = getBoxType() == 'formuler3'
SystemInfo["loadci4driver"] = getBoxType() == 'formuler4'
SystemInfo["WakeOnLAN"] = fileCheck("/proc/stb/power/wol") or fileCheck("/proc/stb/fp/wol")
if getBoxType() in ('gbquad', 'gbquadplus','gb800ueplus', 'gb800seplus', 'gbipbox'):
	SystemInfo["WOL"] = False
else:
	SystemInfo["WOL"] = fileCheck("/proc/stb/power/wol") or fileCheck("/proc/stb/fp/wol")
SystemInfo["HDMICEC"] = (fileExists("/dev/hdmi_cec") or fileExists("/dev/misc/hdmi_cec0")) and fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/HdmiCEC/plugin.pyo")
SystemInfo["SABSetup"] = fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/SABnzbd/plugin.pyo")
SystemInfo["SeekStatePlay"] = False
SystemInfo["StatePlayPause"] = False
SystemInfo["StandbyState"] = False
SystemInfo["GraphicLCD"] = getBoxType() in ('vuultimo', 'xpeedlx3', 'et10000', 'mutant2400', 'quadbox2400', 'sezammarvel', 'atemionemesis', 'mbultra', 'beyonwizt4','osmio4kplus')
SystemInfo["Blindscan"] = fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/Blindscan/plugin.pyo")
SystemInfo["Satfinder"] = fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/Satfinder/plugin.pyo")
SystemInfo["HasExternalPIP"] = getMachineBuild() not in ('et9x00', 'et6x00', 'et5x00') and fileCheck("/proc/stb/vmpeg/1/external")
SystemInfo["hasPIPVisibleProc"] = fileCheck("/proc/stb/vmpeg/1/visible")
SystemInfo["VideoDestinationConfigurable"] = fileExists("/proc/stb/vmpeg/0/dst_left")
SystemInfo["GBWOL"] = fileExists("/usr/bin/gigablue_wol")
SystemInfo["LCDSKINSetup"] = path.exists("/usr/share/enigma2/display")
SystemInfo["VFD_scroll_repeats"] = fileCheck("/proc/stb/lcd/scroll_repeats")
SystemInfo["VFD_scroll_delay"] = fileCheck("/proc/stb/lcd/scroll_delay")
SystemInfo["VFD_initial_scroll_delay"] = fileCheck("/proc/stb/lcd/initial_scroll_delay")
SystemInfo["VFD_final_scroll_delay"] = fileCheck("/proc/stb/lcd/final_scroll_delay")
SystemInfo["CIHelper"] = fileExists("/usr/bin/cihelper")
SystemInfo["isGBIPBOX"] = fileExists("/usr/lib/enigma2/python/gbipbox.so")
SystemInfo["LCDMiniTV"] = fileExists("/proc/stb/lcd/mode")
SystemInfo["LCDMiniTV4k"] = fileExists("/proc/stb/lcd/live_enable") and getBoxType() in ('vusolo4k', 'e4hdultra')
SystemInfo["LCDMiniTVPiP"] = SystemInfo["LCDMiniTV"] and getBoxType() not in ('gb800ueplus','gbquad4k','gbue4k')
SystemInfo["LcdLiveTV"] = fileCheck("/proc/stb/fb/sd_detach") or fileCheck("/proc/stb/lcd/live_enable")
SystemInfo["LcdLiveTVPiP"] = fileCheck("/proc/stb/lcd/live_decoder")
SystemInfo["MiniTV"] = fileCheck("/proc/stb/fb/sd_detach") or fileCheck("/proc/stb/lcd/live_enable")
SystemInfo["FastChannelChange"] = False
SystemInfo["grautec"] = fileExists("/tmp/usbtft")
SystemInfo["3DMode"] = fileCheck("/proc/stb/fb/3dmode") or fileCheck("/proc/stb/fb/primary/3d")
SystemInfo["3DZNorm"] = fileCheck("/proc/stb/fb/znorm") or fileCheck("/proc/stb/fb/primary/zoffset")
SystemInfo["CanUse3DModeChoices"] = fileExists('/proc/stb/fb/3dmode_choices') and True or False
SystemInfo["need_dsw"] = getBoxType() not in ('osminiplus')
SystemInfo["HaveCISSL"] = fileCheck("/etc/ssl/certs/customer.pem") and fileCheck("/etc/ssl/certs/device.pem")
SystemInfo["HaveTouchSensor"] = getBoxType() in ('dm520', 'dm525', 'dm900')
SystemInfo["DefaultDisplayBrightness"] = getBoxType() == 'dm900' and 8 or 5
SystemInfo["HasRootSubdir"] = fileHas("/proc/cmdline", "rootsubdir=")
SystemInfo["RecoveryMode"] = SystemInfo["HasRootSubdir"] and getMachineBuild() not in ('vs1500','hd51','h7') or fileCheck("/proc/stb/fp/boot_mode")
SystemInfo["ForceLNBPowerChanged"] = fileCheck("/proc/stb/frontend/fbc/force_lnbon")
SystemInfo["ForceToneBurstChanged"] = fileCheck("/proc/stb/frontend/fbc/force_toneburst")
SystemInfo["USETunersetup"] = SystemInfo["ForceLNBPowerChanged"] or SystemInfo["ForceToneBurstChanged"]
SystemInfo["HDMIin"] = getMachineBuild() in ('inihdp', 'hd2400', 'et10000', 'dm7080', 'dm820', 'dm900', 'dm920', 'vuultimo4k', 'et13000', 'sf5008', 'vuuno4kse') or getBoxType() in ('spycat4k','spycat4kcombo','gbquad4k')
SystemInfo["canMultiBoot"] = getMachineBuild() in ('hd51','vs1500','h7','h9combo','hd60','hd61','multibox','8100s') and (1, 4, 'mmcblk0p') or getMachineBuild() in ('gb7252') and (3, 3, 'mmcblk0p') or getMachineBuild() in ('gbmv200','cc1','sf8008','ustym4kpro','beyonwizv2','viper4k') and fileCheck("/dev/sda") and (0, 3, 'sda') or getMachineBuild() in ('osmio4k','osmio4kplus','xc7439') and (1, 4, 'mmcblk1p')
SystemInfo["canMode12"] = getMachineBuild() in ('hd51','vs1500','h7') and ('brcm_cma=440M@328M brcm_cma=192M@768M', 'brcm_cma=520M@248M brcm_cma=200M@768M')
SystemInfo["HAScmdline"] = fileCheck("/boot/cmdline.txt")
SystemInfo["HasMMC"] = fileHas("/proc/cmdline", "root=/dev/mmcblk") or SystemInfo["canMultiBoot"] and fileHas("/proc/cmdline", "root=/dev/sda")
SystemInfo["HasSDmmc"] = SystemInfo["canMultiBoot"] and "sd" in SystemInfo["canMultiBoot"][2] and "mmcblk" in getMachineMtdRoot() 
SystemInfo["HasSDswap"] = getMachineBuild() in ("h9", "i55plus") and pathExists("/dev/mmcblk0p1")
SystemInfo["CanProc"] = SystemInfo["HasMMC"] and getBrandOEM() != "vuplus"
SystemInfo["canRecovery"] = getMachineBuild() in ('hd51','vs1500','h7','8100s') and ('disk.img', 'mmcblk0p1') or getMachineBuild() in ('xc7439','osmio4k','osmio4kplus') and ('emmc.img', 'mmcblk1p1') or getMachineBuild() in ('gbmv200','cc1','sf8008','ustym4kpro','beyonwizv2','viper4k') and ('usb_update.bin','none')
