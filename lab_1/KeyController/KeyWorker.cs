using System.Management;
using System.Security.Cryptography;
using System.Text;
using System.Diagnostics;
using System.Threading;

namespace KeyController
{
    public class KeyWorker
    {
        public const string keyPath = "../../../../key.txt";

        //серийный номер и SoftwareElementID BIOS
        static string getUniqueValue1()
        {
            string query = "SELECT * FROM Win32_BIOS";
            // Извлекает коллекцию управляющих объектов в соответствии с заданным запросом.
            // После создания экземпляр этого класса принимает в качестве исходных данных запрос WMI,
            // представленный объектом ObjectQuery
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(query); //windows only

            //При вызове метода Get() выполняет данный запрос в заданной области и возвращает
            //коллекцию управляющих объектов, которые удовлетворяют запросу
            foreach (ManagementObject info in searcher.Get())
            {

                return info["SerialNumber"].ToString() + info["SoftwareElementID"].ToString();
                /*
                 * https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-bios
                  Win32_BIOS:
                  uint16   BiosCharacteristics[];
                  string   BIOSVersion[];
                  string   BuildNumber;
                  string   Caption;
                  string   CodeSet;
                  string   CurrentLanguage;
                  string   Description;
                  uint8    EmbeddedControllerMajorVersion;
                  uint8    EmbeddedControllerMinorVersion;
                  !!!!string   IdentificationCode;  Manufacturer's identifier for this software element.
                  uint16   InstallableLanguages;
                  datetime InstallDate;
                  string   LanguageEdition;
                  String   ListOfLanguages[];
                  string   Manufacturer;
                  string   Name;
                  string   OtherTargetOS;
                  boolean  PrimaryBIOS;
                  datetime ReleaseDate;
                  !!!!!string   SerialNumber;  Assigned serial number of the software element.
                  string   SMBIOSBIOSVersion;
                  uint16   SMBIOSMajorVersion;
                  uint16   SMBIOSMinorVersion;
                  boolean  SMBIOSPresent;
                  !!!!!!!!!!string   SoftwareElementID; Identifier for this software element; designed to be used in conjunction with other keys to create a unique representation of this instance.
                  uint16   SoftwareElementState;
                  string   Status;
                  uint8    SystemBiosMajorVersion;
                  uint8    SystemBiosMinorVersion;
                  uint16   TargetOperatingSystem;
                  string   Version;
                };
                 */
            }

            return "";
        }

        static string getUniqueValue2()
        {
            string query = "SELECT * FROM Win32_Processor";
            // Извлекает коллекцию управляющих объектов в соответствии с заданным запросом.
            // После создания экземпляр этого класса принимает в качестве исходных данных запрос WMI,
            // представленный объектом ObjectQuery
            //{\\DESKTOP-TJ9D65N\root\cimv2:Win32_Processor.DeviceID="CPU0"}
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(query); //windows only

            //При вызове метода Get() выполняет данный запрос в заданной области и возвращает
            //коллекцию управляющих объектов, которые удовлетворяют запросу
            foreach (ManagementObject info in searcher.Get())
            {
                var tmp1 = info["UniqueId"]; //null
                return info["SerialNumber"].ToString() + info["Family"].ToString();
                /*
                 * https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-processor
{
  uint16   AddressWidth;
  uint16   Architecture;
  string   AssetTag;
  uint16   Availability;
  string   Caption;
  uint32   Characteristics;
  uint32   ConfigManagerErrorCode;
  boolean  ConfigManagerUserConfig;
  uint16   CpuStatus;
  string   CreationClassName;
  uint32   CurrentClockSpeed;
  uint16   CurrentVoltage;
  uint16   DataWidth;
  string   Description;
  string   DeviceID;
  boolean  ErrorCleared;
  string   ErrorDescription;
  uint32   ExtClock;
                            !!!!!! uint16   Family;    Processor family type.
  datetime InstallDate;
  uint32   L2CacheSize;
  uint32   L2CacheSpeed;
  uint32   L3CacheSize;
  uint32   L3CacheSpeed;
  uint32   LastErrorCode;
  uint16   Level;
  uint16   LoadPercentage;
  string   Manufacturer;
  uint32   MaxClockSpeed;
  string   Name;
  uint32   NumberOfCores;
  uint32   NumberOfEnabledCore;
  uint32   NumberOfLogicalProcessors;
  string   OtherFamilyDescription;
  string   PartNumber;
  string   PNPDeviceID;
  uint16   PowerManagementCapabilities[];
  boolean  PowerManagementSupported;
  string   ProcessorId;
  uint16   ProcessorType;
  uint16   Revision;
  string   Role;
  boolean  SecondLevelAddressTranslationExtensions;
                        !!!!!string   SerialNumber; The serial number of this processor This value is set by the manufacturer and normally not changeable.
  string   SocketDesignation;
  string   Status;
  uint16   StatusInfo;
  string   Stepping;
  string   SystemCreationClassName;
  string   SystemName;
  uint32   ThreadCount;
                            !!!! string   UniqueId;   Globally unique identifier for the processor. This identifier may only be unique within a processor family.
  uint16   UpgradeMethod;
  string   Version;
  boolean  VirtualizationFirmwareEnabled;
  boolean  VMMonitorModeExtensions;
  uint32   VoltageCaps;
};
                 */
            }

            return "";
        }

        static string getSystemNameAndVendor()
        {
            /*
             * Служебная программа командной строки WMI (WMIC) предоставляет интерфейс командной строки для Windows 
             * инструментария управления (WMI). 
            */
            Process.Start("cmd.exe", "/C " + "wmic csproduct get name > name.txt"); // имя системы
            Process.Start("cmd.exe", "/C " + "wmic csproduct get vendor > vendor.txt"); // производитель
            Thread.Sleep(3000);
            string res = File.ReadAllLines("name.txt")[1] + File.ReadAllLines("vendor.txt")[1];
            return res;

        }

        #region hashing

        /*
         * Хэш используется в качестве уникального значения фиксированного размера, 
         * представляющего большой объем данных. Хэши двух наборов данных должны совпадать только в том случае, 
         * если соответствующие данные совпадают. Небольшие изменения данных приводят к непредсказуемым изменениям в хэше.
         * Размер хэша для алгоритма SHA256 составляет 256 бит.
        */
        static string computeSHA256(string serialNum)
        {
            UnicodeEncoding ue = new UnicodeEncoding();
            SHA256 shHash = SHA256.Create();

            byte[] hashValue = shHash.ComputeHash(ue.GetBytes(serialNum));

            return Convert.ToBase64String(hashValue);
        }

        /*
         * HMACSHA1 — это тип хэш-алгоритма, созданного из хэш-функции SHA1 и используемого в качестве кода проверки 
         * подлинности сообщения на основе хэша или HMAC. Процесс HMAC смешивает секретный ключ с данными сообщения, 
         * хэширует результат с хэш-функцией, снова смешивает хэш-значение с секретным ключом, 
         * а затем применяет хэш-функцию во второй раз. Выходной хэш имеет длину 160 бит.
         */
        static string ComputeHmacsha1(string data, string key)
        {
            byte[] dataBytes = Encoding.Default.GetBytes(data);
            byte[] keyBytes = Encoding.Default.GetBytes(key);

            using (var hmac = new HMACSHA1(keyBytes))
            {
                return Convert.ToBase64String(hmac.ComputeHash(dataBytes));
            }
        }
#endregion

        public static string generateKey()
        {
            //string uniqueValue1 = getUniqueValue1();
            //return computeSHA256(uniqueValue1);

            string uniqueValue2 = getUniqueValue2();
            return computeSHA256(uniqueValue2);

            //string systemNameAndVendor = getSystemNameAndVendor();
            //return computeSHA256(systemNameAndVendor);

            //return ComputeHmacsha1(uniqueValue1, systemNameAndVendor);
        }

        public static bool compareKeys(string key)
        {
            string data = generateKey();
            return key.Equals(data);
        }
    }
}
