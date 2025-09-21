using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization.Formatters;
using System.Text;
using System.Threading.Tasks;

namespace LeetCodeProblems.LeetcodeProblems
{
    public class ArrayProblems
    {
        public int[] TwoSum(int[] nums, int target)
        {
            Dictionary<int, int> map = new Dictionary<int, int>();
            for (int a = 0; a < nums.Length; a++)
            {
                map[nums[a]] = a;
            }
            for (int i = 0; i < nums.Length; i++)
            {
                int j = target - nums[i];
                if (map.ContainsKey(j) && map[j] != i)
                {
                    return new int[] { i, map[j] };
                }
            }
            return new int[] { };
        }

        public IList<IList<int>> ThreeSum(int[] nums)
        {
            Dictionary<string, int> addmap = new Dictionary<string, int>();
            IList<IList<int>> tempresult = new List<IList<int>>();
            IList<IList<int>> result = new List<IList<int>>();
            // Step 1: Store the sums of all pairs in a dictionary
            for (int i = 0; i < nums.Length - 2; i++)
            {
                addmap[$"{i}({nums[i]}), {i+1}({nums[i+1]})"] = nums[i] + nums[i+1];
                //for (int j = i + 1; j < nums.Length; j++)
                //{
                //    // Using index number in key names to avoid duplicates
                //    addmap[$"{i}({nums[i]}), {j}({nums[j]})"] = nums[i] + nums[j];
                //}
            }
            Console.WriteLine("addmap Dictionary:");
            foreach (var kvp in addmap)
            {
                Console.WriteLine($"{kvp.Key}: {kvp.Value}");
            }
            // Step 2: Find triplets that sum to zero by matching the complement from the dic to the array
            for (int a = 0; a < nums.Length; a++)
            {
                // Check if a is a complement for any pair sum in the dictionary
                int complement = -nums[a];
                var tripletPairs = addmap.Where(kvp => kvp.Value == complement).ToList();
                // Store all such pairs with nums[a] to form triplets in the tempresult list
                foreach(var pair in tripletPairs)
                { 
                    var indices = pair.Key.Split(',');
                    int i = int.Parse(indices[0].Split('(')[0]);
                    int j = int.Parse(indices[1].Split('(')[0]);
                    // Ensure we do not use the same index for a, i, or j
                    if (i != a && j != a && i != j)
                    {
                        var triplet = new List<int> { nums[a], nums[i], nums[j] };
                        triplet.Sort();
                        tempresult.Add(triplet);
                    }
                }
            }
            // Step 3: Remove duplicates from tempresult and store in result
            foreach (var triplet in tempresult)
                {
                string key = string.Join(",", triplet);
                if (!result.Any(r => string.Join(",", r) == key))
                {
                    result.Add(triplet);
                }
            }
            return result;
        }

        public int MaxProfit(int[] prices)
        {
            if (prices.Length < 2 || prices == null)
            {
                return 0;
            }

            int minprice = int.MaxValue;
            int profit = 0;
            foreach(int cp in prices)
            {
                minprice = Math.Min(minprice, cp);
                profit = Math.Max(profit, cp-minprice);
            }
            return profit;
        }

        public bool ContainsDuplicate(int[] nums)
        {
           if(nums.Any() && nums != null)
            {
                int distinctnumscount = nums.Distinct().Count();
                if (nums.Length != distinctnumscount)
                {
                    return true;
                }
            }
            return false;
        }

        public int[] ProductExcept(int[] nums)
            {
            int[] result = new int[nums.Length];
            if(nums.Any() && nums != null)
            {
                int suffix = 1, prefix = 1;
                for(int i = 0; i < nums.Length; i++)
                {
                    result[i] = prefix;
                    prefix *= nums[i];
                }
                for(int i = nums.Length - 1; i >= 0; i--)
                {
                    result[i] *= suffix;
                    suffix *= nums[i];
                }
            }
            return result;
        }

        public int[] solution(int[] numbers)
        {
            int[] result = Array.Empty<int>();
            for (int i = 1; i < numbers.Length - 1; i++)
            {
                if (((numbers[i - 1] < numbers[i]) && (numbers[i] > numbers[i + 1])) ||
                (numbers[i - 1] > numbers[i]) && (numbers[i] < numbers[i + 1]))
                {
                    result.Append(1);
                }
                else
                {
                    result.Append(0);
                }
            }
            return result;
        }

        public int unitdiffheights(int[] nums)
        {
            int ops = 0;
            Array.Sort(nums);
            for(int i = 0; i < nums.Length - 1; i++)
            {
                int diff = nums[i + 1] - nums[i];
                if (diff == 1)
                {
                    ops += 0;
                }
                else
                {
                    ops = ops + (diff - 1);
                }
            }
            return ops;
        }

        public string Multiply(string num1, string num2)
        {
            int res = 0;
            string result = "";
            res = Convert.ToInt32(num1) * Convert.ToInt32(num2);
            result = Convert.ToString(res);
            return result;
        }

        public int MaxSubArray(int[] nums)
        {
            if (nums == null || nums.Length == 0) return 0;
            if(nums.Length == 1)
            {
                return nums[0];
            }
            else
            {
                int left = 0, right = (nums.Length - 1);

                int CompAndMergeArr(int[] arr, int left, int right, int unusedmax)
                {
                    if (left == right) return arr[left];
                    int middle = left + (right - left) / 2;
                    
                    int leftMax = CompAndMergeArr(arr, left, middle, unusedmax);
                    int rightMax = CompAndMergeArr(arr, middle + 1, right, unusedmax);

                    int leftSum = int.MinValue;
                    int sum = 0;
                    for(int i = middle; i >= left; i--)
                    {
                        sum += arr[i];
                        if(sum > leftSum) leftSum = sum;
                    }

                    int rightSum = int.MinValue;
                    sum = 0;
                    for(int j = middle + 1; j <= right; j++)
                    {
                        sum+= arr[j];
                        if(sum > rightSum) rightSum = sum;
                    }

                    int crossMax = leftSum + rightSum;

                    return Math.Max(Math.Max(leftMax, rightMax), crossMax);
                }

                // Calling the CompareAndMergeArr Function
                int res = CompAndMergeArr(nums, left, right, int.MinValue);
                return res;
            }
        }

        // Q. Fins the MaxProduct Sub Array
        public int MaxProduct(int[] nums)
        {
            if (nums == null || nums.Length == 0) return 0;
            if (nums.Length == 1)
            {
                return nums[0];
            }
            else
            {
                int maxprod = int.MinValue, prefix = 1, suffix = 1;
                for (int i = 0; i < nums.Length; i++)
                {
                    if (prefix == 0) prefix = 1;
                    if (suffix == 0) suffix = 1;
                    prefix = prefix * nums[i];
                    suffix = suffix * nums[nums.Length - i - 1];
                    maxprod = Math.Max(maxprod, Math.Max(prefix, suffix));
                }
                return maxprod;
            }
        }

        // Q. Find the Kth Largest Element in the Array
        public int FindKthlargest(int[] arr, int k)
        {
            int result = 0;
            LinkedListProblems.HeapSortArr(arr);
            int index = arr.Length - 1;
            int target = index - (k + 1);
            result = arr[target];
            return result;
        }
        // Q. Sliding Window Maximum
        public int[] MaxSlidingWindow(int[] nums, int k)
        {
            // Brute Force Approach
            List<int> maxarr = new();
            for (int i = 0; i < nums.Length - k +1; i++)
            {
                int max = int.MinValue;
                int range = k - 1;
                Console.WriteLine($"Round: {i}");
                while (range >= 0 && (i+range < nums.Length))
                {
                    Console.WriteLine($"Checking for: {nums[i+range]}");
                    range--;
                }
            }

            // Max Heap Approach
            LinkedListProblems.BuildHeap(nums, nums.Length);
            LinkedListProblems.PrintHeap(nums, nums.Length);
            return maxarr.ToArray();
        }
    }
}
