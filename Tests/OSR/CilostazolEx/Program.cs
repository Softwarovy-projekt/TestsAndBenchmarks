using System;

class Program
{
    static void Main(string[] args)
    {
        int outputA = TestA();
        int result = TestB(outputA);
    }

    public static int TestA() {
        return 1;
    }

    public static int TestB(int a) {
        return a + TestA();
    }
}