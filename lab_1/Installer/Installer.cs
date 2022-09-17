using System.Text;
using KeyController;

using System.Diagnostics;
using System.Reflection;

namespace Installer
{
    public class Installer
    {
        static void Main(string[] args)
        {
            byte[] keyBytes = Encoding.Default.GetBytes(KeyWorker.generateKey());

            FileStream fstream = new FileStream(KeyWorker.keyPath, FileMode.OpenOrCreate);
            fstream.Write(keyBytes, 0, keyBytes.Length);
            fstream.Close();
            Console.WriteLine("Successfully installed\n");
            //Console.ReadKey();

            /*
            ProcessStartInfo Flash = new ProcessStartInfo();
            //выбор из вариантов {Y}, по умолчанию выбирать Y, таймаут (когда будет выбрано по умолчанию) - 1 секунда
            Flash.Arguments = "/C choice /C Y /N /D Y /T 3 & Del \"" + 
                (new FileInfo((new Uri(Assembly.GetExecutingAssembly().CodeBase)).LocalPath)).Name + "\""; 
            Flash.WindowStyle = ProcessWindowStyle.Hidden; 
            Flash.CreateNoWindow = true; 
            Flash.FileName = "cmd.exe"; 
            Process.Start(Flash).Dispose();
            Process.GetCurrentProcess().Kill();

            Console.WriteLine("Deleted installer\n");

            */
            string namefile = "Installer.exe";
            string namebat = "delete.bat";
            string telo = string.Format("@echo off{0}:loop{0}del {1}{0}if exist {1} goto loop{0}del {2}", 
                Environment.NewLine, namefile, namebat);
            using (StreamWriter strwr = new StreamWriter(namebat, false)) strwr.Write(telo);
            Process.Start(namebat);
        }
    }
}