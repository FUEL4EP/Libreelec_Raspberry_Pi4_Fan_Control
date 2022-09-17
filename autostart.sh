

(python3 /storage/.config/fan_controller/fan_controller.py)&
(
 sleep 6s ;
 #echo "mq" | kodi-remote
 kodi-send --action="SetVolume(0)"
)
