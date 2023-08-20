/* The Computer Language Benchmarks Game
             https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
             
             started with Java #2 program (Krause/Whipkey/Bennet/AhnTran/Enotus/Stalcup)
             adapted for C# by Jan de Vaan
          */

using System;

public class MandelBrot
{
    private static int n = 16000;
    private static int[][] data;
    private static int lineCount = -1;

    private static double[] Crb;
    private static double[] Cib;

    static int getByte(int x, int y)
    {
        int res = 0;
        for (int i = 0; i < 8; i += 2)
        {
            double Zr1 = Crb[x + i];
            double Zi1 = Cib[y];

            double Zr2 = Crb[x + i + 1];
            double Zi2 = Cib[y];

            int b = 0;
            int j = 49;
            do
            {
                double nZr1 = Zr1 * Zr1 - Zi1 * Zi1 + Crb[x + i];
                double nZi1 = Zr1 * Zi1 + Zr1 * Zi1 + Cib[y];
                Zr1 = nZr1;
                Zi1 = nZi1;

                double nZr2 = Zr2 * Zr2 - Zi2 * Zi2 + Crb[x + i + 1];
                double nZi2 = Zr2 * Zi2 + Zr2 * Zi2 + Cib[y];
                Zr2 = nZr2;
                Zi2 = nZi2;

                if (Zr1 * Zr1 + Zi1 * Zi1 > 4)
                {
                    b |= 2;
                    if (b == 3) break;
                }

                if (Zr2 * Zr2 + Zi2 * Zi2 > 4)
                {
                    b |= 1;
                    if (b == 3) break;
                }
            } while (--j > 0);

            res = (res << 2) + b;
        }

        return res ^ -1;
    }

    public static void Main(String[] args)
    {
        if (args.Length > 0) n = Int32.Parse(args[0]);

        int lineLen = (n - 1) / 8 + 1;
        data = new int[n][];

        Crb = new double[n + 7];
        Cib = new double[n + 7];

        double invN = 2.0 / n;
        for (int i = 0; i < n; i++)
        {
            Cib[i] = i * invN - 1.0;
            Crb[i] = i * invN - 1.5;
        }

        for (int i = 0; i < 8; i++)
        {
            int y;
            while ((y = ++lineCount) < n)
            {
                var buffer = new int[lineLen];
                for (int x = 0; x < lineLen; x++)
                {
                    buffer[x] = (byte) getByte(x * 8, y);
                }

                data[y] = buffer;
            }
        }

        Console.WriteLine("P4\n" + n + " " + n);
        for (int y = 0; y < n; y++)
        for (int i = 0; i < lineLen; i++)
            Console.Write(data[y][i]);
    }
}
