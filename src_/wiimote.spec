# Import necessary modules from PyInstaller
from PyInstaller import Analysis, EXE, BUNDLE

# Path to the libhidapi.dylib library (adjust this path based on where the library is located)
hidapi_lib_path = '/opt/homebrew/lib/libhidapi.dylib'  # Replace with your actual path

# Collect the application
block_cipher = None
a = Analysis(
    ['wiimote.py'],
    pathex=[],
    binaries=[(hidapi_lib_path, 'libhidapi.dylib')],  # Add libhidapi.dylib here
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

# Create the executable
exe = EXE(
    a,
    pathex=[],
    runtime_hooks=[],
    exclude_binaries=False,
    name='wiimote',
    debug=False,
    strip=False,
    upx=True,
    console=False,
)

# Bundle the executable into a macOS .app
app = BUNDLE(
    exe,
    name='WiimoteApp',
    icon=None,  # Optional: Specify the path to your .icns file if you have one
    bundle_identifier='com.yourcompany.wiimote',  # Optional
)