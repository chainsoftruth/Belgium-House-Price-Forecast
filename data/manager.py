class DataManager():

    @staticmethod
    def links_export(links: list[str]):
        """Exporting links to .txt"""
        with open("./data/links.txt", "w") as file:
            for link in links:
                file.write(f"{link}\n")
    
    @staticmethod
    def links_import() -> list[str]:
        """Importing links from .txt"""
        with open("./data/links.txt", "r") as file:
            lines = [line.strip() for line in file if line.strip()]
        return lines