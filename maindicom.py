from config import dir_for_monitoring
import os, sqlite3
from dbdicom import session, Files


def main():
    for foldername, subfolders, files in os.walk(dir_for_monitoring):
        for filename in files:
            if filename.upper().endswith('.DCM'):
                file_catalog = foldername.split('\\')[-1]
                print(file_catalog, filename)
                query = session.query(Files).filter(Files.file_catalog == file_catalog.strip()).filter(Files.file_name == filename.strip())
                if len(query.all()) == 0:
                    file = Files()
                    file.file_name = filename.strip()
                    file.file_catalog = file_catalog.strip()
                    session.add(file)
                    session.commit()


if __name__ == '__main__':
    main()


