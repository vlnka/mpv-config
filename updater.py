import requests, os, subprocess, glob

repo_url = "https://api.github.com/repos/zhongfly/mpv-winbuild/releases/latest"
headers = {'Accept': 'application/vnd.github.v3+json'}
release = requests.get(repo_url, headers=headers).json()

for asset in release['assets']:
    if asset['name'].startswith('mpv-x86_64-v3-') and asset['name'].endswith('.7z'):
        file_url = asset['browser_download_url']
        break

new_version = file_url.split('/')[-1].replace('mpv-x86_64-v3-', '').replace('.7z', '')
current_version = open("ver.txt", "r").read().strip() if os.path.exists("ver.txt") else ""

if new_version != current_version:
    filename = f"mpv-x86_64-v3-{new_version}.7z"
    open(filename, "wb").write(requests.get(file_url, allow_redirects=True).content)
    subprocess.run(["7z", "x", "-aoa", filename])

for f in glob.glob("*.7z"):
    if (os.path.getmtime(f) - os.path.getctime(f)) // (24 * 3600) >= 7:
        os.unlink(f)

# Update the version file at the end
if new_version != current_version:
    open("ver.txt", "w").write(new_version)
