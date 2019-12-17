from config import dir_for_monitoring, dir_for_copy, process_for_monitoring
import os
from dbdicom import session, Files
import shutil
import psutil
import logging
import logs


def check_process(prm_process_name):
    is_run = 0
    for proc in psutil.process_iter():
        if proc.name().strip().lower() == prm_process_name:
            is_run = 1
            break
    if is_run == 1:
        #logging.info(prm_process_name+' run')
        pass
    else:
        logging.error(prm_process_name+' not run')
    return is_run


def main():
    logging.warning('Импорт запущен')
    while True:
        try:
            if check_process(process_for_monitoring):
                for foldername, subfolders, files in os.walk(dir_for_monitoring):
                    for filename in files:
                        if filename.upper().endswith('.DCM'):
                            file_catalog = foldername.split('\\')[-1]
                            query = session.query(Files).filter(Files.file_catalog == file_catalog.strip()).filter(
                                Files.file_name == filename.strip())
                            if len(query.all()) == 0:
                                logging.warning(filename)
                                if not os.path.exists(os.path.join(dir_for_copy, file_catalog.strip())):
                                    os.makedirs(os.path.join(dir_for_copy, file_catalog.strip()))

                                file = Files()
                                file.file_name = filename.strip()
                                file.file_catalog = file_catalog.strip()
                                shutil.copy(os.path.join(dir_for_monitoring, file_catalog.strip(), filename.strip()),
                                            os.path.join(dir_for_copy, file_catalog.strip(), filename.strip()))
                                session.add(file)
                                session.commit()
                                logging.warning([file_catalog, filename, 'скопирован'])
                    #logging.warning('scan complete')
        except Exception as e:
            logging.error(e)

if __name__ == '__main__':
    logs.run('logmain.txt', 'logdebug.txt', 'logerror.txt')
    main()


