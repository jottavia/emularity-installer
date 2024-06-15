from utils import log

def create_html():
    log("Creating example_dosbox_wasm.html for Doom...")
    doom_html = """
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
    """
    with open("/var/www/html/emularity/doom.html", "w") as file:
        file.write(doom_html)

    log("Creating main menu HTML file...")
    index_html = """
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
    """
    with open("/var/www/html/emularity/index.html", "w") as file:
        file.write(index_html)
