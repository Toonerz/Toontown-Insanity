# Client
window-title Toontown
server-version sv0.0.0.1-dev
sync-video #f
want-dev #f
preload-avatars #t
texture-anisotropic-degree 16
icon-filename phase_3/models/gui/toontown.ico
audio-library-name p3fmod_audio
smooth-lag 0.4

# WASD Support
want-WASD-support #f
WASD-jump-key space
WASD-chat-key t

# Resources
vfs-mount resources/phase_3 /phase_3
vfs-mount resources/phase_3.5 /phase_3.5
vfs-mount resources/phase_4 /phase_4
vfs-mount resources/phase_5 /phase_5
vfs-mount resources/phase_5.5 /phase_5.5
vfs-mount resources/phase_6 /phase_6
vfs-mount resources/phase_7 /phase_7
vfs-mount resources/phase_8 /phase_8
vfs-mount resources/phase_9 /phase_9
vfs-mount resources/phase_10 /phase_10
vfs-mount resources/phase_11 /phase_11
vfs-mount resources/phase_12 /phase_12
vfs-mount resources/phase_13 /phase_13
vfs-mount resources/server /server
model-path resources
default-model-extension .bam

# Server
want-rpc-server #f
rpc-server-endpoint http://localhost:8080/
eventlog-host 127.0.0.1
want-cheesy-expirations #f

# DC Files
dc-file config/toon.dc
dc-file config/otp.dc

# Game features
want-pets #t
want-news-tab #f
want-news-page #t
want-accessories #t
want-parties #t
want-gardening #t
want-gifting #f
want-picnic-games #f
want-chinese-table #f
want-checkers-table #f
want-findfour-table #f
want-keep-alive #f
estate-day-night #t
want-instant-parties #t
show-total-population #t
want-toontorial #f
want-new-toonhall #t
want-old-fireworks #t
want-skip-button #t

# Chat
want-whitelist #f
want-blacklist-sequence #f
force-avatar-understandable #t
force-player-understandable #t

# Holidays/Event Manager
force-holiday-decorations 6
want-mega-invasions #f
mega-invasion-cog-type tm
