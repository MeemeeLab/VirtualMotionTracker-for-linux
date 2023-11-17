from gi.repository import GLib, Gtk
from .osc_manager import OscManager
import openvr
import os
import threading
from pyrr import Quaternion, Matrix44, Vector3
from itertools import chain

@Gtk.Template(resource_path='/org/gpsnmeajp/vmt/vmt_manager/window.ui')
class VmtManagerGtkWindow(Gtk.Window):
    __gtype_name__ = 'VmtManagerGtkWindow'

    btn_reload_settings = Gtk.Template.Child()
    btn_device_reset = Gtk.Template.Child()
    btn_room_matrix_set = Gtk.Template.Child()
    btn_room_matrix_reset = Gtk.Template.Child()

    room_matrix_textbox_buffer = Gtk.Template.Child()
    vmt_0_textbox_buffer = Gtk.Template.Child()
    vmt_0_raw_vel_textbox_buffer = Gtk.Template.Child()

    vmt_0_device = -1

    ticking = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            self.setup_openvr()
        except Exception as e:
            print("General error:")
            print(e)
            alert = Gtk.AlertDialog(message='VMT Manager', detail='General error while setting up OpenVR: %s' % e.__str__())
            alert.choose(self, None, lambda _, __: GLib.idle_add(lambda: self.destroy()))
            return

        self.check_hmd_present()

        self.osc_manager = OscManager()

        self.btn_reload_settings.connect("clicked", self.on_btn_reload_settings)
        self.btn_device_reset.connect("clicked", self.on_btn_device_reset)
        self.btn_room_matrix_set.connect("clicked", self.on_btn_room_matrix_set)
        self.btn_room_matrix_reset.connect("clicked", self.on_btn_room_matrix_reset)

        self.connect("close-request", self.on_close)

        threading.Timer(0.1, self.tick).start()

    def get_connected_devices(self):
        devices = []

        for i in range(openvr.k_unMaxTrackedDeviceCount):
            if openvr.VRSystem().isTrackedDeviceConnected(i):
                devices.append(i)

        print(devices)
        return devices

    def get_device(self, serial):
        for device in range(openvr.k_unMaxTrackedDeviceCount):
            if openvr.VRSystem().getStringTrackedDeviceProperty(device, openvr.Prop_SerialNumber_String) == serial:
                return device

        return -1

    def setup_openvr(self):
        # "container" must be lower cased, I know, it's ugly...
        if "container" in os.environ and "XDG_CONFIG_HOME" in os.environ:
            print("Flatpak detected, using hacky method to patch OpenVR. Make sure to add a read permission on ~/.config for this flatpak.")
            del os.environ["XDG_CONFIG_HOME"]

        print("Using OpenVR runtime at '%s'" % openvr.getRuntimePath())

        try:
            openvr.init(openvr.VRApplication_Background)
        except Exception as e:
            # Map exception if possible
            if isinstance(e, openvr.error_code.InitError_Init_NoServerForBackgroundApp):
                raise Exception("Please start SteamVR")
            else:
                raise Exception("Unknown error: %s\nPlease refer to OpenVR documentation." % e.__class__.__name__)
        print("OpenVR Initialization complete")

        try:
            ret = openvr.VRSettings().getBool("driver_vmt", openvr.k_pch_Driver_Enable_Bool)
        except openvr.error_code.SettingsError_UnsetSettingHasNoDefault:
            print("SettingsError_UnsetSettingHasNoDefault while retrieving driver_vmt enabled flag")
            ret = None
        finally:
            if not ret or ret != 1:
                alert = Gtk.AlertDialog(message='OpenVR Setup', detail='Failed to setup driver: VirtualMotionTracker is not installed or enabled!\nDon\'t worry, please install SteamVR driver using install tab.')
                alert.show(self)
                return

        self.vmt_0_device = self.get_device("VMT_0")
        if self.vmt_0_device != -1:
            print("Found VMT_0 at index %d" % self.vmt_0_device)
        else:
            print("Could not find VMT_0")

    def check_hmd_present(self):
        if openvr.isHmdPresent() != 1:
            alert = Gtk.AlertDialog(message='VMT Manager', detail='HMD not detected, please configure SteamVR')
            alert.choose(self, None, lambda _, __: GLib.idle_add(lambda: self.destroy()))

    def update_matrix(self, arrarr):
        # makes [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]] to "0, 0, 0, 0\n0, 0, 0, 0\n0, 0, 0, 0"
        GLib.idle_add(lambda: self.room_matrix_textbox_buffer.set_text("\n".join(list(map(lambda arr: ", ".join(list(map(lambda val: str(val), arr))), arrarr)))))

    def update_vmt0_pose(self, pos, vel):
        GLib.idle_add(lambda: (
            self.vmt_0_textbox_buffer.set_text(", ".join(list(map(lambda v: str(v), pos)))),
            self.vmt_0_raw_vel_textbox_buffer.set_text(", ".join(list(map(lambda v: str(v), vel))))
        ))

    def tick(self):
        if not self.ticking:
            return False

        ret, m = openvr.VRChaperoneSetup().getWorkingStandingZeroPoseToRawTrackingPose()

        if ret:
            self.update_matrix(m)

        if self.vmt_0_device != -1:
            ret, vsync_sec, vsync_frame = openvr.VRSystem().getTimeSinceLastVsync()
            if ret:
                display_fps = openvr.VRSystem().getFloatTrackedDeviceProperty(openvr.k_unTrackedDeviceIndex_Hmd, openvr.Prop_DisplayFrequency_Float)
                photon = openvr.VRSystem().getFloatTrackedDeviceProperty(openvr.k_unTrackedDeviceIndex_Hmd, openvr.Prop_SecondsFromVsyncToPhotons_Float)
                frame_cycle = 1 / display_fps
                predicted_time = frame_cycle - vsync_sec + photon

                pose = openvr.VRSystem().getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseSeated, predicted_time, [])[self.vmt_0_device]
                m = list(chain.from_iterable(pose.mDeviceToAbsoluteTracking))

                matrix = Matrix44([
                    m[0], m[4], m[8], 0,
                    m[1], m[5], m[9], 0,
                    m[2], m[6], m[10], 0,
                    m[3], m[7], m[11], 1
                ])

                self.update_vmt0_pose(matrix.decompose()[2], list(pose.vVelocity.v))

        threading.Timer(0.1, self.tick).start()
        return True

    def on_btn_reload_settings(self, _):
        self.osc_manager.reload_settings()

        alert = Gtk.AlertDialog(message='Reload Settings', detail='Settings has been reloaded')
        alert.show(self)

    def on_btn_device_reset(self, _):
        self.osc_manager.reset_settings()

        alert = Gtk.AlertDialog(message='Device Reset', detail='Devices has been reset')
        alert.show(self)

    def on_btn_room_matrix_set(self, _):
        ret, m = openvr.VRChaperoneSetup().getWorkingStandingZeroPoseToRawTrackingPose()

        if not ret:
            alert = Gtk.AlertDialog(message='Room Matrix', detail='Failed to set room matrix: failed retrieving matrix')
            alert.show(self)
            return

        self.osc_manager.set_room_matrix(m)

    def on_btn_room_matrix_reset(self, _):
        self.osc_manager.set_room_matrix([0] * 12)

    def on_close(self, _):
        self.ticking = False
