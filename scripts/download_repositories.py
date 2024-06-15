from utils import log, run_command

def download_repositories():
    log("Downloading and extracting Emularity repository...")
    run_command("cd /var/www/html && git clone https://github.com/db48x/emularity.git")

    log("Downloading Emularity dependencies...")
    run_command("cd /var/www/html/emularity && wget https://raw.githubusercontent.com/db48x/emularity/master/es6-promise.js -O es6-promise.js")
    run_command("cd /var/www/html/emularity && wget https://raw.githubusercontent.com/db48x/emularity/master/browserfs.min.js -O browserfs.min.js")
    run_command("cd /var/www/html/emularity && wget https://raw.githubusercontent.com/db48x/emularity/master/loader.js -O loader.js")

    log("Downloading pre-built DOSBox-WASM JavaScript files...")
    run_command("mkdir -p /var/www/html/emularity/emulators/dosbox-wasm")
    run_command("wget https://archive.org/download/emularity_engine_emdosbox/dosbox.js.gz -O /var/www/html/emularity/emulators/dosbox-wasm/dosbox.js.gz")
    run_command("wget https://archive.org/download/emularity_engine_emdosbox/dosbox.wasm.gz -O /var/www/html/emularity/emulators/dosbox-wasm/dosbox.wasm.gz")
    run_command("wget https://archive.org/download/emularity_engine_emdosbox/dosbox.html.mem.gz -O /var/www/html/emularity/emulators/dosbox-wasm/dosbox.html.mem.gz")

    log("Decompressing DOSBox-WASM JavaScript files...")
    run_command("gunzip /var/www/html/emularity/emulators/dosbox-wasm/dosbox.js.gz")
    run_command("gunzip /var/www/html/emularity/emulators/dosbox-wasm/dosbox.wasm.gz")
    run_command("gunzip /var/www/html/emularity/emulators/dosbox-wasm/dosbox.html.mem.gz")

    log("Downloading and decompressing Doom shareware...")
    run_command("mkdir -p /var/www/html/emularity/examples/doom")
    run_command("wget https://archive.org/download/doom1-sw1/doom-sw.zip -O /var/www/html/emularity/examples/doom/doom-sw.zip")
    run_command("unzip /var/www/html/emularity/examples/doom-sw.zip -d /var/www/html/emularity/examples/doom")
