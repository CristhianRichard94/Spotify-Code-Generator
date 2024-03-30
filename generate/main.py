import requests
import os
import re

while True:
  spotify_code = ""
  input_url = ""
  while not input_url:
    try:
      print("Paste your Spotify song code below:")
      input_url = input()
      spotify_code = "spotify%3Atrack%3A" + input_url
      download_url = f"https://spotifycodes.com/downloadCode.php?uri=svg%2F000000%2Fwhite%2F640%2F{spotify_code}"
    except:
      print("Invalid code")
      continue

  # Download Spotify Code
  try:
    print("Downloading the Spotify Code...")
    response = requests.get(download_url)
    content = response.content.decode("utf-8")
    # Remove background for OpenSCAD
    content = content.replace('<rect x="0" y="0" width="400" height="100" fill="#000000"/>', "")

    # Save SVG file
    save_path = os.path.join(os.getcwd(), "generate", "OpenSCAD", "code.svg")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Create directory if needed
    with open(save_path, "w") as f:
      f.write(content)

    # Keychain option
    key_choice = ""
    while key_choice not in ("y", "n"):
      print("\nDo you want your Model to have a Keychain ring? [y/n]")
      key_choice = input().lower()

    # Output filename
    name_choice = ""
    print("\nGive your output file a name. [ENTER] for \"code.stl\":")
    name_input = input()
    name_input = name_input or ""  # Use empty string if no input
    name_choice = name_input
    if not name_choice.endswith(".stl"):
      name_choice += ".stl"

    # OpenSCAD conversion command
    code_path = os.path.join(os.getcwd(), "generate", "OpenSCAD", "CodeConverter.scad")
    scad = os.path.join(os.getcwd(), "generate", "OpenSCAD", "openscad.exe")
    keychain_param = "true " if key_choice == "y" else "false "
    command = f"{scad} -o {name_choice} -D keychain={keychain_param} {code_path}"
    print("Converting with OpenSCAD... (This may take a few seconds)")
    os.system(command)

    print("\nSuccess! File saved in program directory as \"" + name_choice + "\"")
  except Exception as e:
    print(f"Unexpected Error: {e}, restarting...")

