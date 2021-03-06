import shutil
import os
import glob
import re
import xml.dom.minidom as md

import wget
from bs4 import BeautifulSoup

ROOT_FOLDER = os.getcwd()
ROOT_TEMP_DIR = f'{ROOT_FOLDER}/TEMP'
ROOT_ARCHIVE = "distr.zip"
ROOT_ARCHIVE_PATH = f'{ROOT_FOLDER}/{ROOT_ARCHIVE}'
ASSEMBLY_TEMP_DIR = f'{ROOT_TEMP_DIR}/ASSEMBLY_TEMP'
version = ""


def modify_castor_module():
    os.chdir(ASSEMBLY_TEMP_DIR)
    module_base_name = f'castor-{version}'
    module_full_name = f'{module_base_name}.jar'
    module_unpack_dir = f'{ASSEMBLY_TEMP_DIR}/castor'
    shutil.unpack_archive(module_full_name,
                          extract_dir=module_unpack_dir,
                          format='zip')
    castor_xml_file = f'{module_unpack_dir}/META-INF/beans.xml'

    xml_doc = md.parse(castor_xml_file)
    interceptors_node = xml_doc.getElementsByTagName("interceptors")[0]
    alternatives_node = xml_doc.createElement("alternatives")
    alternatives_class_node = xml_doc.createElement("class")
    alternatives_class_node.appendChild(xml_doc.createTextNode("com.maykor.sms.NoopSmsSender"))
    alternatives_node.appendChild(alternatives_class_node)
    interceptors_node.parentNode.insertBefore(alternatives_node, interceptors_node)

    bs = BeautifulSoup(xml_doc.toxml(), 'xml')
    with open(castor_xml_file, "w+") as file:
        file.write(str(bs.prettify()))

    shutil.make_archive(module_base_name, format="zip", root_dir=module_unpack_dir)
    shutil.rmtree(module_unpack_dir)
    os.remove(module_full_name)
    os.rename(f'{module_base_name}.zip', module_full_name)


def modify_procyon_module():
    os.chdir(ASSEMBLY_TEMP_DIR)
    module_base_name = f'procyon-{version}'
    module_full_name = f'{module_base_name}.jar'
    module_unpack_dir = f'{ASSEMBLY_TEMP_DIR}/procyon'
    shutil.unpack_archive(module_full_name,
                          extract_dir=module_unpack_dir,
                          format='zip')
    castor_xml_file = f'{module_unpack_dir}/META-INF/beans.xml'

    xml_doc = md.parse(castor_xml_file)
    beans_node = xml_doc.getElementsByTagName("beans")[0]
    alternatives_node = xml_doc.createElement("alternatives")

    alternatives_class_node = xml_doc.createElement("class")
    alternatives_class_node.appendChild(xml_doc.createTextNode("com.maykor.ipc.request.processor"
                                                               ".NoopAssignTestsProcessor"))
    alternatives_node.appendChild(alternatives_class_node)

    alternatives_class_node = xml_doc.createElement("class")
    alternatives_class_node.appendChild(xml_doc.createTextNode("com.maykor.ipc.request.processor"
                                                               ".NoopGetTestResultsProcessor"))
    alternatives_node.appendChild(alternatives_class_node)

    alternatives_class_node = xml_doc.createElement("class")
    alternatives_class_node.appendChild(xml_doc.createTextNode("com.maykor.ipc.request.processor"
                                                               ".NoopAssignMoreTestsRequestProcessor"))
    alternatives_node.appendChild(alternatives_class_node)

    beans_node.appendChild(alternatives_node)

    bs = BeautifulSoup(xml_doc.toxml(), 'xml')
    with open(castor_xml_file, "w+") as file:
        file.write(str(bs.prettify()))

    shutil.make_archive(module_base_name, format="zip", root_dir=module_unpack_dir)
    shutil.rmtree(module_unpack_dir)
    os.remove(module_full_name)
    os.rename(f'{module_base_name}.zip', module_full_name)


def modify_rigel_module():
    os.chdir(ASSEMBLY_TEMP_DIR)
    module_base_name = f'rigel-{version}'
    module_full_name = f'{module_base_name}.war'
    module_unpack_dir = f'{ASSEMBLY_TEMP_DIR}/rigel'
    shutil.unpack_archive(module_full_name,
                          extract_dir=module_unpack_dir,
                          format='zip')
    castor_xml_file = f'{module_unpack_dir}/WEB-INF/beans.xml'
    xml_doc = md.parse(castor_xml_file)
    interceptors_node = xml_doc.getElementsByTagName("interceptors")[0]
    alternatives_node = xml_doc.createElement("alternatives")
    alternatives_class_node = xml_doc.createElement("class")
    alternatives_class_node.appendChild(xml_doc.createTextNode("com.maykor.sms.NoopSmsSender"))
    alternatives_node.appendChild(alternatives_class_node)
    interceptors_node.parentNode.insertBefore(alternatives_node, interceptors_node)
    bs = BeautifulSoup(xml_doc.toxml(), 'xml')
    with open(castor_xml_file, "w+") as file:
        file.write(str(bs.prettify()))
    shutil.make_archive(module_base_name, format="zip", root_dir=module_unpack_dir)
    shutil.rmtree(module_unpack_dir)
    os.remove(module_full_name)
    os.rename(f'{module_base_name}.zip', module_full_name)


def extract_t2_assembly():
    print('Образ скачан и модифицируется... ')
    if os.path.exists(ROOT_TEMP_DIR):
        shutil.rmtree(ROOT_TEMP_DIR)
    os.mkdir(ROOT_TEMP_DIR)
    shutil.unpack_archive(ROOT_ARCHIVE, extract_dir=ROOT_TEMP_DIR, format='zip')
    os.chdir(f'{ROOT_TEMP_DIR}/distr')
    main_archive_name = os.path.basename(glob.glob('./*.tar.gz')[0])

    shutil.unpack_archive(main_archive_name,
                          extract_dir=ROOT_TEMP_DIR,
                          format='gztar')
    os.chdir(ROOT_TEMP_DIR)
    global version
    with open('version.txt', 'r') as version_file:
        version = version_file.read().strip()
    print(f'Определена версия образа: {version}')
    shutil.rmtree('./distr')
    main_module_base_name = f't2-{version}'
    main_module_full_name = f'{main_module_base_name}.ear'
    shutil.unpack_archive(main_module_full_name,
                          extract_dir=ASSEMBLY_TEMP_DIR,
                          format='zip')
    print("-- Модифицируется модуль castor")
    modify_castor_module()
    print("-- Модифицируется модуль rigel")
    modify_rigel_module()
    print("-- Модифицируется модуль procyon")
    modify_procyon_module()
    os.chdir(ROOT_TEMP_DIR)
    shutil.make_archive(main_module_base_name, format="zip", root_dir=ASSEMBLY_TEMP_DIR)
    os.rename(f'{main_module_base_name}.zip', f'{ROOT_FOLDER}/{main_module_full_name}')
    os.chdir(ROOT_FOLDER)
    shutil.rmtree(ROOT_TEMP_DIR)
    os.remove(ROOT_ARCHIVE_PATH)
    print(f'Образ модифицирован и сохранен {ROOT_FOLDER}/{main_module_full_name}')


if __name__ == "__main__":
    print('Начато скачивание файла сборки...')
    if os.path.exists(ROOT_TEMP_DIR):
        shutil.rmtree(ROOT_TEMP_DIR)
    download_section = os.getenv('T2_VERSION', 'lastBuild')
    download_url = f'http://172.19.21.138/jenkins/job/T2/{download_section}/artifact/distr/*zip*/distr.zip'
    wget.download(download_url, ROOT_ARCHIVE_PATH)
    extract_t2_assembly()
