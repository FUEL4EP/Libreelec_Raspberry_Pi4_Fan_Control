(
 sleep 10s ;
python3 /storage/.config/fan_controller/fan_controller_LE13.py
)&
(
 sleep 20s ;
 bash /storage/.config/update_script/my_update.bsh
)&
(
 sleep 8s ;
 kodi-send --action="SetVolume(0)"
)&
