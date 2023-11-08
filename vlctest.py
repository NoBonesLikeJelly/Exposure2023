import vlc

# Create a VLC instance
instance = vlc.Instance()

# Create a media player
player = instance.media_player_new()

# Load a video file
video_file = "/mnt/usbdrive0/In_Her_Steps.mov"
media = instance.media_new(video_file)
player.set_media(media)

# Set the options you need (e.g., no-repeat, fullscreen)
player.set_fullscreen(True)
#player.set_repeat(False)

# Play the video
player.play()

# You can interact with the player as needed (e.g., pause, stop, volume control)
player.pause()
# player.stop()
# player.set_volume(50)  # Set the volume to 50%

# Wait for user interaction or perform other actions
# For example, you can set up a loop to monitor user input and control the player based on it.
while True:
    user_input = input("Enter a command (play, pause, stop, exit): ")
    
    if user_input == "play":
        player.play()
    elif user_input == "pause":
        player.pause()
    elif user_input == "stop":
        player.stop()
    elif user_input == "exit":
        break

# Release the player and instance when done
player.release()
instance.release()