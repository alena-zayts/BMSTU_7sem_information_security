# BMSTU_7sem_information_security
7th sem BMSTU, Information security

(6 лаб)

Брянская (шарп)
https://github.com/Bryanskaya/InformationSecurity 

Иванов (го)

Неклепаева (питон)
https://github.com/AnaNek/Information_security 

Пума (шарп)
https://github.com/Winterpuma/bmstu_security/tree/master 


https://github.com/Kulikov17/BMSTU-Information-Security 


## ЛР1. Реализовать программу (установщик + ПО), привязав её к конкретной машине, используя уникальные параметры компьютера.

Есть две программы: программа-установщик(installer) и основная программа(main). При запуске основной программы без предварительного запуска установщика будет выведена ошибка, т.к. произойдет несовпадение уникального значения, привязанного к железу, полученного в основной программе и прочитанного из файла(key.txt), при запуске установщика перед основной программой в файл key.txt ключ(в данном случае серийный номер и семейство процессора) записывается в этот файл.

