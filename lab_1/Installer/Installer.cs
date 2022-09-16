using System.Text;
using KeyController;

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
            Console.ReadKey();
        }
    }
}