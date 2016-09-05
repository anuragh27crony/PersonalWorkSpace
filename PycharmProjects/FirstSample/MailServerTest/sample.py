from __future__ import with_statement
import time
import os

from sikuli.Sikuli import *
import java.lang.System
from config.settings import Settings
from org.sikuli.natives import Vision

# Reducing scale
Vision.setParameter("MinTargetSize", 24.0)

ThisScript = os.path.abspath(__file__)
Anchor = os.sep + "Testing" + os.sep
AnchorPath = ThisScript[:ThisScript.rfind(Anchor) + len(Anchor)]
settings = Settings({"scripts_location_path": AnchorPath, "AnchorPath": AnchorPath})

if '2008' in java.lang.System.getProperty('os.name'):
    addImagePath(settings["ScreenshotDir_Windows2008"])
elif '2012' in java.lang.System.getProperty('os.name'):
    addImagePath(settings["ScreenshotDir_Windows2012"])
else:
    # Use Windows2012 screenshots as default
    addImagePath(settings["ScreenshotDir_Windows2012"])


class PCDetector(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        # Constants (add later self.SCORETHRESHOLD = 0.99)
        self.total_channels = settings["NumberOfChannels"]
        self.region_offset = 66
        self.resize_offset = 50
        self.application = None
        self.processing_offset = 86
        self.wm_offset = self.processing_offset + (0 * 28)
        self.vfp_offset = self.processing_offset + (1 * 28)
        self.rt_vfp_offset = self.processing_offset + (2 * 28)
        self.afp_offset = self.processing_offset + (3 * 28)
        self.rt_afp_offset = self.processing_offset + (4 * 28)
        self.cc_offset = self.processing_offset + (5 * 28)
        self.rt_cc_offset = self.processing_offset + (6 * 28)
        self.thumb_offset = self.processing_offset + (7 * 28)

    def set_Configuration_Type(self, configType):
        if configType == "UDP":
            self.total_channels = settings["NumberOfUDPChannels"]
        else:
            self.total_channels = settings["NumberOfChannels"]

        print("Number of %s Channels = %s" % (configType, self.total_channels))

    def stop_channel(self, channel):
        self.confirm_error(channel)
        try:
            channel.find("status_busy.png")
            print("status is busy")
            stop_button = channel.find("channel_stop.png")
            click(stop_button)
            if self.is_warning_displayed():
                yes_button = find("dialog_yes_button.png")
                click(yes_button)
        except:
            print("status is not busy")

    def start_channel(self, channel):
        try:
            channel.find("status_stopped.png")
            print("status is stopped")
            start_button = channel.find("channel_start.png")
            click(start_button)
            if self.is_warning_displayed():
                yes_button = find("dialog_yes_button.png")
                click(yes_button)
        except:
            print("status is not stopped")

    def stop_all_channels(self):
        try:
            stop_button = find("stop_all_button_enabled.png")
            click(stop_button)
            if self.is_warning_displayed():
                yes_button = find("dialog_yes_button.png")
                click(yes_button)
        except:
            print("stop button not found")

    def start_all_channels(self):
        try:
            start_button = find("start_all_button_enabled.png")
            click(start_button)
            if self.is_warning_displayed():
                yes_button = find("dialog_yes_button.png")
                click(yes_button)
        except:
            print("start button not found")

    def channel_stopped(self, channel):
        is_channel_stopped = False
        try:
            channel.find("status_stopped.png")
            is_channel_stopped = True
        except:
            print("status is not stopped")
            self.confirm_error(channel)  # Try to confirm an error when it is active
        finally:
            return is_channel_stopped

    def channel_busy(self, channel):
        is_channel_busy = False
        try:
            channel.find("status_busy.png")
            is_channel_busy = True
        except:
            print("status is not busy")
            self.confirm_error(channel)  # Try to confirm an error when it is active
        finally:
            return is_channel_busy

    def all_channels_stopped(self):
        are_all_channels_stopped = True
        for channel in range(1, self.total_channels + 1):
            region = self.channel_Region(channel)
            if not self.channel_stopped(region):
                # ignore streaming errors (defect D-08055) by checking the channel state once more
                if not self.channel_stopped(region):
                    print("channel %s is not stopped" % str(channel))
                    are_all_channels_stopped = False
                    break
        return are_all_channels_stopped

    def all_channels_busy(self):
        are_all_channels_busy = True
        for channel in range(1, self.total_channels + 1):
            region = self.channel_Region(channel)
            if not self.channel_busy(region):
                print("channel %s is not busy" % str(channel))
                are_all_channels_busy = False
                break
        return are_all_channels_busy

    def confirm_error(self, channel):

        try:
            redScore = channel.find("error_ok_red.png").getScore()
        except:
            redScore = 0

        try:
            yellowScore = channel.find("error_ok_yellow.png").getScore()
        except:
            yellowScore = 0
        print("Score: red_ok_button =%s and yellow_ok_button =%s" % (redScore, yellowScore))

        if redScore > yellowScore:
            okScreenshot = "error_ok_red.png"
        elif redScore < yellowScore:
            okScreenshot = "error_ok_yellow.png"
        else:
            return

        try:
            ok_button = channel.find(okScreenshot)
            print("error is active")
            click(ok_button)
        except:
            print("No error active")

    def confirm_all_errors(self):
        for channel in range(1, self.total_channels + 1):
            region = self.channel_Region(channel)
            self.confirm_error(region)

    def __find_quality(self):
        quality_reg = find("quality_header.png")
        return quality_reg

    def _wm_region(self, channel):
        quality_reg = self.__find_quality()
        wm_region = Region(quality_reg.x + self.wm_offset, channel.y, 30, 57)
        return wm_region

    def _vfp_file_region(self, channel):
        quality_reg = self.__find_quality()
        vfp_reg = Region(quality_reg.x + self.vfp_offset, channel.y, 30, 57)
        return vfp_reg

    def _vfp_stream_region(self, channel):
        quality_reg = self.__find_quality()
        rt_vfp_reg = Region(quality_reg.x + self.rt_vfp_offset, channel.y, 30, 57)
        return rt_vfp_reg

    def _afp_file_region(self, channel):
        quality_reg = self.__find_quality()
        afp_reg = Region(quality_reg.x + self.afp_offset, channel.y, 30, 57)
        return afp_reg

    def _afp_stream_region(self, channel):
        quality_reg = self.__find_quality()
        rt_afp_reg = Region(quality_reg.x + self.rt_afp_offset, channel.y, 30, 57)
        return rt_afp_reg

    def _cc_file_region(self, channel):
        quality_reg = self.__find_quality()
        cc_reg = Region(quality_reg.x + self.cc_offset, channel.y, 30, 57)
        return cc_reg

    def _cc_stream_region(self, channel):
        quality_reg = self.__find_quality()
        rt_cc_reg = Region(quality_reg.x + self.rt_cc_offset, channel.y, 30, 57)
        return rt_cc_reg

    def _thumb_region(self, channel):
        quality_reg = self.__find_quality()
        thumb_reg = Region(quality_reg.x + self.thumb_offset, channel.y, 30, 57)
        return thumb_reg

    def watermarking_state(self, channel):
        wm_reg = self._wm_region(channel)
        return self._feature_state(wm_reg, "watermarking_disabled.png", "watermarking_enabled.png")

    def vfp_ceco_state(self, channel):
        vfp_reg = self._vfp_file_region(channel)
        return self._feature_state(vfp_reg, "fingerprint_file_writing_disabled.png",
                                   "fingerprint_file_writing_enabled.png")

    def vfp_streaming_state(self, channel):
        rt_vfp_reg = self._vfp_stream_region(channel)
        return self._feature_state(rt_vfp_reg, "vfp_streaming_disabled.png", "vfp_streaming_enabled.png")

    def afp_ceco_state(self, channel):
        afp_reg = self._afp_file_region(channel)
        return self._feature_state(afp_reg, "afp_disabled.png", "afp_enabled.png")

    def afp_streaming_state(self, channel):
        rt_afp_reg = self._afp_stream_region(channel)
        return self._feature_state(rt_afp_reg, "afp_streaming_disabled.png", "afp_streaming_enabled.png")

    def thumbnail_capturing_state(self, channel):
        thumb_reg = self._thumb_region(channel)
        return self._feature_state(thumb_reg, "thumbnail_capturing_disabled.png", "thumbnail_capturing_enabled.png")

    def closed_captioning_state(self, channel):
        cc_reg = self._cc_file_region(channel)
        return self._feature_state(cc_reg, "closed_captioning_disabled.png", "closed_captioning_enabled.png")

    def cc_streaming_state(self, channel):
        rt_cc_reg = self._cc_stream_region(channel)
        return self._feature_state(rt_cc_reg, "cc_streaming_disabled.png", "cc_streaming_enabled.png")

    def _feature_state(self, region, disabledRef, enabledRef):

        final_feature_state = "Inconclusive"
        try:
            disabledScore = region.find(disabledRef).getScore()
        except:
            disabledScore = 0

        try:
            enabledScore = region.find(enabledRef).getScore()
        except:
            enabledScore = 0
        print("Scores: enabled_score=%s and disabled_score=%s " % (enabledScore, disabledScore))

        if disabledScore > enabledScore:
            final_feature_state = "Disabled"
        elif disabledScore < enabledScore:
            final_feature_state = "Enabled"

        return final_feature_state

    def enable_watermarking(self, channel):
        wm_reg = self._wm_region(channel)
        self._toggle_feature_state(wm_reg, "watermarking_disabled.png")

    def disable_watermarking(self, channel):
        wm_reg = self._wm_region(channel)
        self._toggle_feature_state(wm_reg, "watermarking_enabled.png")

    def enable_vfp_ceco(self, channel):
        vfp_reg = self._vfp_file_region(channel)
        self._toggle_feature_state(vfp_reg, "fingerprint_file_writing_disabled.png")

    def disable_vfp_ceco(self, channel):
        vfp_reg = self._vfp_file_region(channel)
        self._toggle_feature_state(vfp_reg, "fingerprint_file_writing_enabled.png")

    def enable_vfp_streaming(self, channel):
        rt_vfp_reg = self._vfp_stream_region(channel)
        self._toggle_feature_state(rt_vfp_reg, "vfp_streaming_disabled.png")

    def disable_vfp_streaming(self, channel):
        rt_vfp_reg = self._vfp_stream_region(channel)
        self._toggle_feature_state(rt_vfp_reg, "vfp_streaming_enabled.png")

    def enable_afp_ceco(self, channel):
        afp_reg = self._afp_file_region(channel)
        self._toggle_feature_state(afp_reg, "afp_disabled.png")

    def disable_afp_ceco(self, channel):
        afp_reg = self._afp_file_region(channel)
        self._toggle_feature_state(afp_reg, "afp_enabled.png")

    def enable_afp_streaming(self, channel):
        rt_afp_reg = self._afp_stream_region(channel)
        self._toggle_feature_state(rt_afp_reg, "afp_streaming_disabled.png")

    def disable_afp_streaming(self, channel):
        rt_afp_reg = self._afp_stream_region(channel)
        self._toggle_feature_state(rt_afp_reg, "afp_streaming_enabled.png")

    def enable_closed_captioning(self, channel):
        cc_reg = self._cc_file_region(channel)
        self._toggle_feature_state(cc_reg, "closed_captioning_disabled.png")

    def disable_closed_captioning(self, channel):
        cc_reg = self._cc_file_region(channel)
        self._toggle_feature_state(cc_reg, "closed_captioning_enabled.png")

    def enable_cc_streaming(self, channel):
        rt_cc_reg = self._cc_stream_region(channel)
        self._toggle_feature_state(rt_cc_reg, "cc_streaming_disabled.png")

    def disable_cc_streaming(self, channel):
        rt_cc_reg = self._cc_stream_region(channel)
        self._toggle_feature_state(rt_cc_reg, "cc_streaming_enabled.png")

    def enable_thumbnail_capturing(self, channel):
        thumb_reg = self._thumb_region(channel)
        self._toggle_feature_state(thumb_reg, "thumbnail_capturing_disabled.png")

    def disable_thumbnail_capturing(self, channel):
        thumb_reg = self._thumb_region(channel)
        self._toggle_feature_state(thumb_reg, "thumbnail_capturing_enabled.png")

    def _toggle_feature_state(self, channel, featureRef):
        try:
            wm = channel.find(featureRef)
            click(wm)
            if self.is_warning_displayed():
                yes_button = find("dialog_yes_button.png")
                click(yes_button)
            else:
                print("Warning dialog could not be found")
        except:
            print("Button could not be found")

    def open_preview_window(self, channel):
        try:
            refLocation = find("preview.png")
            previewLocation = Location(refLocation.x, channel.y + (self.region_offset / 2))
            click(previewLocation)
        except:
            print("preview window could not be opened")

    def preview_window_is_opened(self):
        is_preview_open = False
        try:
            find("preview_header.png")
            is_preview_open = True
        finally:
            return is_preview_open

    def close_preview_window(self):
        try:
            header = find("preview_header.png")
            region = Region(header.x, header.y - 5, 600, 30)
            # region.highlight(2) # uncomment only while debugging
            region.click("window_close_button.png")
        except Exception as e:
            print("Closing the preview window failed", e)

    def start_application(self):
        self.application = App.open(settings["PCDetectorApplication"])
        time.sleep(30)
        self.close_license_warning()

    def resize_application_window(self):
        self.close_license_warning()
        resized = False
        #        while not resized:
        while self.vertical_scrollbar_visible():
            print("resizing window")
            try:
                logo = find("civolution_logo.png")
                if logo.x > self.resize_offset and logo.y > self.resize_offset:
                    drag_point = Location(logo.x, logo.y)
                    drop_point = Location(logo.x - self.resize_offset, logo.y - self.resize_offset)
                    dragDrop(drag_point, drop_point)
                # resized = True
                else:
                    drag_point = Location(logo.x + self.resize_offset, logo.y + 10)
                    drop_point = Location(logo.x + (2 * self.resize_offset), logo.y + 10 + self.resize_offset)
                    dragDrop(drag_point, drop_point)

            except Exception as e:
                print("resize failed!!", e)
                break

    def vertical_scrollbar_visible(self):
        time.sleep(0.5)
        try:
            find("vertical_scrollbar.png")
            print("vertical_scrollbar found")
        except FindFailed as e:
            print("vertical_scrollbar not found")
        return

    def maximize_application_window(self):
        try:
            header = find("teletrax_cvbs-svid_detector.png")
            click(header)
            region = Region(header.x, header.y - 5, 1, 30).right()
            # region.highlight(2) # uncomment only while debugging
            region.click("window_maximize_button.png")
        except Exception as  e:
            print("Maximizing the application window failed", e)

    def exit_application(self, text):
        try:
            logo = find("civolution_logo.png")
            region = Region(logo.x, logo.y, 300, 100)
            file_menu = region.find("file_menu.png")
            region.click(file_menu)
            exit_menu_item = find("exit.png")
            click(exit_menu_item)
        except Exception as e:
            print(e)
        self.click_button_in_warning(text)

    def close_license_warning(self):
        try:
            find("lock.png")
            find("warning_message.png")
            click("ok_button.png")
        except:
            print("License warning not found, no need to make it disappear")

    def close_application_window(self, text):
        try:
            header = find("teletrax_cvbs-svid_detector.png")
            click(header)
            region = Region(header.x, header.y - 5, 1, 30).right()
            region.click("window_close_button.png")
        except:
            print("Closing the application window failed")
        self.click_button_in_warning(text)

    def is_warning_displayed(self):
        is_warning_displayed = False
        try:
            find("dialog_title_warning.png")
            print("Dialog warning found")
            is_warning_displayed = True
        finally:
            return is_warning_displayed

    def click_button_in_warning(self, text):
        if text == "yes":
            button_screenshot = "dialog_yes_button.png"
        else:
            button_screenshot = "dialog_no_button.png"

        try:
            find("dialog_title_warning.png")
            dialogButton = find(button_screenshot)
            click(dialogButton)
        except FindFailed:
            print("Failed to find dialog title or dialog button")
        except Exception as  e:
            print("Failed to click button in warning dialog", e)

    def set_ceco_length_and_stop_application(self, length):
        restart_required = False
        self.open_preferences()
        if self.preferences_is_displayed():
            try:
                if self.get_current_ceco_length() != int(length):
                    fpSettings = find("fingerprint_settings.png")
                    region = Region(fpSettings.x, fpSettings.y - 10, 400, 50)
                    inputField = region.find("fingerprint_input_field.png")
                    region.type(inputField, Key.BACKSPACE + Key.BACKSPACE + str(length))
                else:
                    print("No need to update the ceco length")
                okButton = find("dialog_ok_button_round_edge.png")
                click(okButton)
                if self.is_warning_displayed():
                    okButton = find("dialog_ok_button_sharp_edge.png")
                    click(okButton)
                    restart_required = True

            except:
                print("Failed to update ceco length")

        return restart_required

    def get_current_ceco_length(self):
        ceco_time_length = 0
        try:
            score_2mins = find("ceco_length_2.png").getScore()
        except:
            score_2mins = 0

        try:
            score_15mins = find("ceco_length_15.png").getScore()
        except:
            score_15mins = 0
        print("Scores 15_min_ceco=%s and 2_min_ceco=%s " % (score_15mins, score_2mins))

        if score_2mins > score_15mins:
            ceco_time_length = 2
        elif score_2mins < score_15mins:
            ceco_time_length = 15

        return ceco_time_length

    def disable_audio_input_and_stop_application(self):
        audio_input_checkbox = "enable_audio_input_checkbox_enabled.png"
        self._toggle_audio_input_and_stop_application(audio_input_checkbox)

    def enable_audio_input_and_stop_application(self):
        audio_input_checkbox = "enable_audio_input_checkbox_disabled.png"
        self._toggle_audio_input_and_stop_application(audio_input_checkbox)

    def _toggle_audio_input_and_stop_application(self, audio_input_checkbox):
        self.open_preferences()
        if self.preferences_is_displayed():
            try:
                audioInputCheckbox = find(audio_input_checkbox)
                click(audioInputCheckbox)
                okButton = find("dialog_ok_button_round_edge.png")
                click(okButton)
                if self.is_warning_displayed():
                    okButton = find("dialog_ok_button_sharp_edge.png")
                    click(okButton)
            except Exception as e:
                print("Failed to toggle Audio Input Checkbox", e)

    def open_preferences(self):
        type("p", KEY_ALT)

    def preferences_is_displayed(self):
        is_preferences_displayed = False
        try:
            find("dialog_title_preferences.png")
            print("Dialog preferences found")
            is_preferences_displayed = True
        except Exception as e:
            print(e)
        finally:
            return is_preferences_displayed

    def _find_signal(self):
        signal_header = find("signal_header.png")
        return signal_header

    def channel_Region(self, channel):
        signal_reg = self._find_signal()  # signal is the name of the most left column
        start_stop = find("start_stop.png")  # Start/Stop is the name of the most right column
        region = Region(signal_reg.x, signal_reg.y + 23 + (int(channel) - 1) * self.region_offset, start_stop.x + 30,
                        63)
        # region.highlight(2) # uncomment only during debugging
        return region

    def runTest(self):

        processing = find("processing.png")
        print("location of processing = ", processing)

        offset = 65
        channels = []
        for id in range(1, 9):
            channels.append(Region(processing.x, processing.y + 23 + (int(id - 1)) * offset, 971, 57))

        for channel in channels:
            self.stop_channel(channel)

        for channel in channels:
            self.start_channel(channel)


if __name__ == "__main__":
    pcdetector = PCDetector()
    pcdetector.runTest()
