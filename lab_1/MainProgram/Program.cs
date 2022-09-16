using System;
using System.IO;
using KeyController;

namespace MainProgram
{
    class Program
    {
        static void Main(string[] args)
        {
            if (!File.Exists(KeyWorker.keyPath))
            {
                Console.WriteLine("ERROR: Run the installer first!");
            }
            else if (!KeyWorker.compareKeys(File.ReadAllText(KeyWorker.keyPath)))
            {
                Console.WriteLine("ERROR: Authentication failed!");
            }
            else
            {
                Console.WriteLine("Authentication was successful!");
            }

            Console.ReadKey();
        }
    }
}