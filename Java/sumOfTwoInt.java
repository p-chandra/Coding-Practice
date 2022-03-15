import java.util.*;

public class sumOfTwoInt {

	public static void main(String[] args) {
		
		int[] nums = {2,7,11,15,5,4};
		int target = 9;
		
		sumOfTwoInt m = new sumOfTwoInt();
		m.twoSum(nums,target);
		//System.out.print(Arrays.toString(m.twoSum(nums,target)));
	}


	public void twoSum(int[] nums, int target) {		
		HashMap<Integer, Integer> hm = new HashMap<>();
		for(int i=0; i<nums.length; i++){
			if (hm.containsKey(target - nums[i]))
				System.out.println(i + " " + hm.get(target-nums[i]));
			else
				hm.put(nums[i], i);
		}
	}
	//Brute Force
 	/*
	public void twoSum(int[] nums, int target) {		
		int[] ary = new int[2];
		for(int i = 0; i<=nums.length; i+=1) {
                        System.out.print("\n");
                        for(int j = nums.length-1; j>i; j--) {
                                System.out.println("i = " + i + " | j = " + j);
                                if(target == nums[i]+nums[j]){
					ary[0] = i;
					ary[1] = j;
				     	System.out.println("\n[" + i + "," + j + "]\n");
				}
			}
                }
	}
        */


}

