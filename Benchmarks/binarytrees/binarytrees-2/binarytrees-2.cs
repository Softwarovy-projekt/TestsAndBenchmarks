// The Computer Language Benchmarks Game
// https://benchmarksgame-team.pages.debian.net/benchmarksgame/
//
// based Jarkko Miettinen Java #2 and Anthony Lloyd C#
// contributed by Isaac Gouy

using System;

class BinaryTrees
{
    const int MinDepth = 4;
    const int NoTasks = 4;

    public static void Main(string[] args)
    {
        int maxDepth = 15;

        Console.WriteLine(string.Concat("stretch tree of depth ", maxDepth + 1,
            "\t check: ", (TreeNode.bottomUpTree(maxDepth + 1)).itemCheck()));

        var longLivedTree = TreeNode.bottomUpTree(maxDepth);

        var results = new string[(maxDepth - MinDepth) / 2 + 1];

        for (int i = 0; i < results.Length; i++)
        {
            int depth = i * 2 + MinDepth;
            int n = (1 << maxDepth - depth + MinDepth) / NoTasks;
            var check = 0;
            for (int t = 0; t < NoTasks; t++)
            {
                for (int j = n; j > 0; j--)
                    check += (TreeNode.bottomUpTree(depth)).itemCheck();
            }

            results[i] = string.Concat(n * NoTasks, "\t trees of depth ",
                depth, "\t check: ", check);
        }

        for (int i = 0; i < results.Length; i++)
            Console.WriteLine(results[i]);

        Console.WriteLine(string.Concat("long lived tree of depth ", maxDepth,
            "\t check: ", longLivedTree.itemCheck()));
    }

    private class TreeNode
    {
        readonly TreeNode left, right;

        internal static TreeNode bottomUpTree(int depth)
        {
            if (depth > 0)
            {
                return new TreeNode(
                    bottomUpTree(depth - 1),
                    bottomUpTree(depth - 1));
            }
            else
            {
                return new TreeNode(null, null);
            }
        }

        internal TreeNode(TreeNode left, TreeNode right)
        {
            this.left = left;
            this.right = right;
        }

        internal int itemCheck()
        {
            if (left == null) return 1;
            else return 1 + left.itemCheck() + right.itemCheck();
        }
    }
}
