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


            string namefile = "Installer.exe";
            string namebat = "delete.bat";
            string telo = string.Format("@echo off{0}:loop{0}del {1}{0}if exist {1} goto loop{0}del {2}", 
                Environment.NewLine, namefile, namebat);
            using (StreamWriter strwr = new StreamWriter(namebat, false)) strwr.Write(telo);
            Process.Start(namebat);
        }
    }
}