#!/bin/bash

# Function to display messages
log() {
    echo "[$$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Step 1: Update the system
log "Updating the system..."
apt update && apt upgrade -y

# Step 2: Install required packages
log "Installing required packages..."
apt install -y apache2 git build-essential python3 python-is-python3 python3-pip unzip curl

# Step 3: Download and extract Emularity repository
log "Downloading and extracting Emularity repository..."
cd /var/www/html
git clone https://github.com/db48x/emularity.git

# Step 4: Download Emularity dependencies
log "Downloading Emularity dependencies..."
cd /var/www/html/emularity
wget https://raw.githubusercontent.com/db48x/emularity/master/es6-promise.js -O es6-promise.js
wget https://raw.githubusercontent.com/db48x/emularity/master/browserfs.min.js -O browserfs.min.js
wget https://raw.githubusercontent.com/db48x/emularity/master/loader.js -O loader.js

# Step 5: Download pre-built DOSBox-WASM JavaScript files
log "Downloading pre-built DOSBox-WASM JavaScript files..."
mkdir -p /var/www/html/emularity/emulators/dosbox-wasm
wget https://archive.org/download/emularity_engine_emdosbox/dosbox.js.gz -O /var/www/html/emularity/emulators/dosbox-wasm/dosbox.js.gz
wget https://archive.org/download/emularity_engine_emdosbox/dosbox.wasm.gz -O /var/www/html/emularity/emulators/dosbox-wasm/dosbox.wasm.gz
wget https://archive.org/download/emularity_engine_emdosbox/dosbox.html.mem.gz -O /var/www/html/emularity/emulators/dosbox-wasm/dosbox.html.mem.gz

# Step 6: Decompress DOSBox-WASM JavaScript files
log "Decompressing DOSBox-WASM JavaScript files..."
gunzip /var/www/html/emularity/emulators/dosbox-wasm/dosbox.js.gz
gunzip /var/www/html/emularity/emulators/dosbox-wasm/dosbox.wasm.gz
gunzip /var/www/html/emularity/emulators/dosbox-wasm/dosbox.html.mem.gz

# Step 7: Download and decompress Doom shareware
log "Downloading and decompressing Doom shareware..."
mkdir -p /var/www/html/emularity/examples/doom
wget https://archive.org/download/doom1-sw1/doom-sw.zip -O /var/www/html/emularity/examples/doom/doom-sw.zip
unzip /var/www/html/emularity/examples/doom-sw.zip -d /var/www/html/emularity/examples/doom

# Step 8: Set correct permissions
log "Setting correct permissions..."
chmod -R 755 /var/www/html/emularity
chown -R www-data:www-data /var/www/html/emularity

# Step 9: Configure Apache
log "Configuring Apache..."
cat <<EOF > /etc/apache2/sites-available/emularity.conf
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html/emularity
    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined

    <Directory /var/www/html/emularity>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
EOF

# Enable the new site and disable the default site
a2ensite emularity.conf
a2dissite 000-default.conf
systemctl reload apache2

# Step 10: Create example_dosbox_wasm.html for Doom
log "Creating example_dosbox_wasm.html for Doom..."
cat <<EOF > /var/www/html/emularity/doom.html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Doom</title>
</head>
<body>
    <canvas id="canvas" style="width: 50%; height: 50%; display: block; margin: 0 auto;"></canvas>
    <script type="text/javascript" src="browserfs.min.js"></script>
    <script type="text/javascript" src="es6-promise.js"></script>
    <script type="text/javascript" src="loader.js"></script>
    <script type="text/javascript">
        console.log("Initializing Emulator...");

        try {
            var canvas = document.getElementById("canvas");
            if (!canvas) {
                throw new Error("Canvas element not found.");
            }

            var emulator = new Emulator(canvas,
                                        null,
                                        new DosBoxLoader(DosBoxLoader.emulatorJS("emulators/dosbox-wasm/dosbox.js"),
                                                         DosBoxLoader.locateAdditionalEmulatorJS(locateAdditionalFiles),
                                                         DosBoxLoader.nativeResolution(640, 480),
                                                         DosBoxLoader.mountZip("c",
                                                                               DosBoxLoader.fetchFile("Game File",
                                                                                                      "examples/doom/doom-sw.zip")),
                                                         DosBoxLoader.startExe("DOOM.EXE")));

            console.log("Starting Emulator...");
            emulator.start({ waitAfterDownloading: true });
            console.log("Emulator Started.");
        } catch (error) {
            console.error("Error initializing emulator:", error);
        }

        function locateAdditionalFiles(filename) {
            console.log("Locating additional file: " + filename);
            if (filename === "dosbox.wasm" || filename === "dosbox.html.mem") {
                return "emulators/dosbox-wasm/" + filename;
            }
            return "emulators/dosbox-wasm/" + filename;
        }
    </script>
</body>
</html>
EOF

# Step 11: Create the main menu HTML file
log "Creating main menu HTML file..."
cat <<EOF > /var/www/html/emularity/index.html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Emularity Game Menu</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
        }
        h1 {
            color: #333;
        }
        .game-menu {
            list-style-type: none;
            padding: 0;
        }
        .game-menu li {
            margin: 10px 0;
        }
        .game-menu a {
            text-decoration: none;
            color: #007bff;
            font-size: 20px;
        }
    </style>
</head>
<body>
    <h1>Emularity Game Menu</h1>
    <ul class="game-menu">
        <li><a href="doom.html">Doom</a></li>
        <!-- Add more games here -->
    </ul>
</body>
</html>
EOF

log "index.html created at /var/www/html/emularity"

# Step 12: Verify Apache status
log "Verifying Apache status..."
systemctl status apache2

log "Setup complete. Open your browser and navigate to your server's IP address to check the setup."
