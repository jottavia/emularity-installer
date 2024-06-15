from scripts.install_packages import install_packages
from scripts.download_repositories import download_repositories
from scripts.configure_apache import configure_apache
from scripts.create_html import create_html

def main():
    install_packages()
    download_repositories()
    configure_apache()
    create_html()

if __name__ == "__main__":
    main()
